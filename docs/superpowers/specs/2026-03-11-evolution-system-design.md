# Evolution System Design — SkillForge v3.0

**Date**: 2026-03-11
**Status**: Approved
**Author**: Atompilot + Claude

## Summary

Upgrade SkillForge's Self-Evolution Protocol from a passive, in-session-only system to an active, cross-session evolution engine powered by Claude Code hooks. Skills gain persistent memory across sessions through a three-layer architecture: Capture → Digest → Evolve.

## Problem

Current Self-Evolution Protocol has three fundamental flaws:

| Flaw | Impact |
|------|--------|
| **No cross-session memory** | Claude forgets corrections from previous sessions; same mistakes recur |
| **Passive detection only** | Relies on Claude "noticing" signals during conversation; high miss rate |
| **No incremental learning** | No checkpoint system; every analysis starts from zero |

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Scope | SkillForge built-in + standalone install | Maximizes adoption |
| Analysis engine | Hybrid: shell preprocessing + Claude deep analysis | Balances cost and intelligence |
| Data privacy | Capture full prompts, local storage, 30-day auto-cleanup | Semantic analysis needs original text; privacy controlled by local-only + TTL |
| PostToolUse scope | Selective: Edit/Write/Bash (full) + Read (path only) | 80% noise reduction vs full capture |

## Architecture

```
Layer 1: Capture (async hooks, zero latency)
┌────────────────────────────────────────────────┐
│ UserPromptSubmit → raw/prompts-{sid}.jsonl     │
│ PostToolUse      → raw/tools-{sid}.jsonl       │
│   (Edit|Write|Bash: full, Read: path only)     │
│ Stop             → raw/responses-{sid}.jsonl   │
│ SessionEnd       → triggers Layer 2            │
│ SessionStart     → conditionally triggers L3   │
└────────────────────────────────────────────────┘
                         ▼
Layer 2: Digest (SessionEnd, shell/python script)
┌────────────────────────────────────────────────┐
│ 1. Read raw/ data for current session          │
│ 2. Extract correction signals (regex)          │
│ 3. Extract explicit instructions (regex)       │
│ 4. Compute tool usage patterns (counters)      │
│ 5. Detect failed commands                      │
│ 6. Append to pending-signals.jsonl             │
│ 7. Update session-meta.json                    │
│ 8. Cleanup raw/ files older than 30 days       │
└────────────────────────────────────────────────┘
                         ▼
Layer 3: Evolve (SessionStart conditional, Claude)
┌────────────────────────────────────────────────┐
│ Trigger conditions (any one):                  │
│   - pending_signal_count >= 5                  │
│   - sessions since last analysis >= 3          │
│   - user runs /{prefix}-evolve                 │
│                                                │
│ Claude reads:                                  │
│   1. evolution-digest.md (checkpoint)          │
│   2. pending-signals.jsonl (new signals)       │
│   3. Current skill files                       │
│                                                │
│ Claude produces:                               │
│   - Evolution proposals (user confirms)        │
│   - Updated evolution-digest.md                │
│   - Updated skills (version bump)              │
│   - Cleared consumed signals                   │
└────────────────────────────────────────────────┘
```

## Directory Structure

```
.claude/
├── evolution/                          # Evolution data root (.gitignore raw/)
│   ├── raw/                            # Layer 1: raw captured data (NOT in git)
│   │   ├── prompts-{session_id}.jsonl
│   │   ├── tools-{session_id}.jsonl
│   │   └── responses-{session_id}.jsonl
│   ├── pending-signals.jsonl           # Layer 2: preprocessed signals (NOT in git)
│   ├── evolution-digest.md             # Layer 3: incremental summary checkpoint (in git)
│   ├── session-meta.json               # Session counter + timing (NOT in git)
│   └── hooks/                          # Hook scripts (in git)
│       ├── capture.sh                  # Unified hook entry point
│       └── digest.py                   # SessionEnd preprocessor
├── settings.json                       # Hook registrations (merged, not overwritten)
└── skills/
    ├── {prefix}-evolve/SKILL.md        # Manual evolution trigger
    ├── {prefix}-digest/SKILL.md        # View evolution status
    └── {prefix}-skill/
        └── evolution.log               # Version change log (in git)
```

## Layer 1: Capture (capture.sh)

Unified entry point for all hook events. All hooks run async with 5s timeout (except SessionEnd: 30s).

### Hook Registration

```json
{
  "hooks": {
    "SessionStart": [{"hooks": [{"type": "command", "command": "bash .claude/evolution/hooks/capture.sh", "timeout": 10}]}],
    "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "bash .claude/evolution/hooks/capture.sh", "timeout": 5}]}],
    "PostToolUse": [{"matcher": "Edit|Write|Bash|Read", "hooks": [{"type": "command", "command": "bash .claude/evolution/hooks/capture.sh", "timeout": 5}]}],
    "Stop": [{"hooks": [{"type": "command", "command": "bash .claude/evolution/hooks/capture.sh", "timeout": 5}]}],
    "SessionEnd": [{"hooks": [{"type": "command", "command": "bash .claude/evolution/hooks/capture.sh", "timeout": 30}]}]
  }
}
```

### Capture Rules

| Event | Captured Fields | Truncation |
|-------|----------------|------------|
| UserPromptSubmit | Full prompt text | None (need full text for semantic analysis) |
| PostToolUse (Edit/Write) | file_path + input preview | input: 200 chars |
| PostToolUse (Bash) | command + result preview | input: 200 chars, result: 300 chars |
| PostToolUse (Read) | file_path only | No result captured |
| Stop | response preview | 500 chars |

### SessionStart: Conditional Trigger

```bash
# Check trigger conditions
if pending_signal_count >= 5 OR sessions_since_last_analysis >= 3:
    # Output to stdout → injected into Claude's context
    echo "<evolution-trigger>..."
fi
# Always increment session counter
```

## Layer 2: Digest (digest.py)

### Signal Extraction Rules

#### Correction Detection

```python
CORRECTION_PATTERNS = [
    r'不对|不要这样|不是这样|应该是|错了|改成|别用|不应该|用错了',
    r'wrong|not like that|should be|don\'t use|instead of|fix this',
    r'重新|再来|不行|换一种',
]
```

Each correction signal includes `prev_prompt` (context window) for Claude to understand what was being corrected.

#### Instruction Detection

```python
INSTRUCTION_PATTERNS = [
    r'记住|以后都|以后要|always|remember|从现在开始',
    r'写入.*skill|更新.*skill|加到.*规范',
]
```

#### Pattern Detection

- Hot files: same file edited ≥3 times in one session
- Frequent commands: same command used ≥3 times in one session
- Failed commands: Bash results containing error indicators

### pending-signals.jsonl Format

```jsonl
{"type":"correction","session_id":"abc","ts":"...","prompt":"不对，应该用 const","prev_prompt":"帮我声明一个变量"}
{"type":"instruction","session_id":"abc","ts":"...","prompt":"以后 commit message 都用英文"}
{"type":"pattern","subtype":"hot_file","session_id":"abc","file":"src/routes/api.ts","edit_count":5}
{"type":"pattern","subtype":"frequent_cmd","session_id":"abc","command":"pnpm test","count":8}
{"type":"failure","session_id":"abc","command":"pnpm build","error_preview":"Type error..."}
```

### Cleanup

- Raw files older than 30 days: deleted
- Consumed signals: cleared after Claude analysis

## Layer 3: Evolve (Claude)

### Trigger Conditions

```python
should_evolve = (
    pending_signal_count >= 5
    or (total_sessions - last_digest_session) >= 3
    or user_explicitly_triggered  # /{prefix}-evolve
)
```

### Execution Strategy

| Scenario | Behavior |
|----------|----------|
| User's first message is a task | Complete task first, then propose evolution |
| User's first message is casual | Can start evolution analysis immediately |
| User runs `/{prefix}-evolve` | Execute immediately, this is the primary intent |

### Quality Control

| Rule | Description |
|------|-------------|
| Evidence threshold | Single correction → propose directly; patterns need ≥2 occurrences |
| No duplicates | Check against digest's Confirmed Patterns; skip already-applied rules |
| Conflict detection | New rule contradicts existing skill → show conflict, let user choose |
| Deferral | Insufficient evidence → mark as "deferred", accumulate for later |

### evolution-digest.md Format

```markdown
# Evolution Digest — {prefix} Skills

## Last Updated: 2026-03-10 (Session #47)

## Confirmed Patterns
- [S#12] API errors must include request_id → written to api skill v1.0.3
- [S#23] All DB queries use .returning() → written to db skill v1.0.2

## Pending Proposals
- [S#45] Error boundary added manually 3 times → propose for frontend skill

## Correction History
- [S#8] var → const/let (written to skill)
- [S#15] throw Error → AppError class (written to skill)

## Tool Usage Patterns
- Most edited: src/routes/api.ts (23x), src/db/schema.ts (18x)
- Most used commands: pnpm dev (45x), pnpm test (38x)
- Skill trigger frequency: bugfix 34%, dev 28%, api 22%, commit 16%

## Evolution Log
- [S#12] api v1.0.0 → v1.0.3: added request_id rule
- [S#23] db v1.0.0 → v1.0.2: added .returning() rule
```

## New Skills: evolve & digest

### {prefix}-evolve

Manual trigger for evolution analysis. Reads digest + pending signals, compares against current skills, generates proposals with user confirmation.

### {prefix}-digest

Read-only view of evolution status. Shows digest content + session stats + pending signal count.

## Integration with SkillForge

### Phase 4 additions

1. Create `.claude/evolution/` directory structure
2. Write `capture.sh` and `digest.py`
3. **Merge** hook config into `.claude/settings.json` (never overwrite existing hooks)
4. Append `raw/` and `pending-signals.jsonl` to `.gitignore`
5. Initialize `session-meta.json` and empty `evolution-digest.md`
6. Generate `{prefix}-evolve` and `{prefix}-digest` skills

### Standalone Installation

```bash
curl -fsSL https://raw.githubusercontent.com/atompilot/skillforge/main/evolution/install.sh | bash
```

## Changes to Self-Evolution Protocol Template

Add "Evolution System Integration" section to the protocol injected into every skill:

- When `<evolution-trigger>` is received: don't interrupt user's task, analyze at appropriate moment
- Auto-Learn remains for real-time in-session proposals; evolution system handles cross-session accumulation
- Manual triggers: `/{prefix}-evolve` and `/{prefix}-digest`

## Git Policy

| File | In git? | Reason |
|------|---------|--------|
| `evolution/hooks/*` | Yes | Shared team config |
| `evolution/evolution-digest.md` | Yes | Shared evolution knowledge |
| `evolution/raw/*` | No | Contains prompt text |
| `evolution/pending-signals.jsonl` | No | Temporary data |
| `evolution/session-meta.json` | No | Personal session data |
| `skills/*/evolution.log` | Yes | Version history, no sensitive data |
