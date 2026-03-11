<p align="center">
  <h1 align="center">Claude Skill Evo</h1>
  <p align="center">
    <strong>Claude Code skills go stale. Claude Skill Evo makes them evolve.</strong>
  </p>
  <p align="center">
    <a href="#installation">Install</a> &middot;
    <a href="#quick-start">Quick Start</a> &middot;
    <a href="#how-it-works">How It Works</a> &middot;
    <a href="#self-evolution-protocol">Self-Evolution</a> &middot;
    <a href="README.zh.md">中文文档</a>
  </p>
  <p align="center">
    <img src="https://img.shields.io/github/stars/atompilot/claude-skill-evo?style=flat-square" alt="GitHub stars">
    <img src="https://img.shields.io/github/license/atompilot/claude-skill-evo?style=flat-square" alt="License">
    <img src="https://img.shields.io/badge/Claude%20Code-Plugin-blue?style=flat-square" alt="Claude Code Plugin">
  </p>
</p>

---

**For Claude Code users** who want their skill system to grow with their project — not decay into obsolete instructions.

One command. Your entire project gets a tailored skill system — and every skill **learns, detects staleness, and proposes its own updates**.

```bash
/skill-evo
```

> **No config files. No templates to fill. No YAML to write.**
> Claude Skill Evo scans your codebase, asks smart questions, and forges skills that actually match how you work.

---

## Why Claude Skill Evo?

| Without Claude Skill Evo | With Claude Skill Evo |
|---|---|
| Manually write CLAUDE.md and skills from scratch | Auto-generated from project scanning + guided Q&A |
| Skills go stale as your project evolves | Skills **detect their own staleness** and propose fixes |
| Copy-paste generic templates | Every path, command, and convention is **your project's real data** |
| One-time setup, then forgotten | Run `/skill-evo` again anytime — it only gets better |
| "I forgot to update the skill" | Skills **learn from your corrections** in real-time |

## Quick Start

```bash
# Install (one time)
claude plugin marketplace add atompilot/claude-skill-evo
claude plugin install claude-skill-evo@claude-skill-evo

# Use (as many times as you want)
/skill-evo                              # Full scan → initialize or optimize
/skill-evo add API conventions          # Focus on a specific area
/skill-evo update dev based on README   # Improve using specific references
```

## How It Works

Every `/skill-evo` run starts by detecting your project state:

```
┌─────────────────────────────────────────────────────────────┐
│  /skill-evo                                                │
│                                                             │
│  Phase 0: State Detection                                   │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │ No .claude│  │ Has CLAUDE.md│  │ Has CLAUDE.md + skills│  │
│  │ directory │  │ but no skills│  │                       │  │
│  └────┬─────┘  └──────┬───────┘  └───────────┬───────────┘  │
│       ▼               ▼                      ▼              │
│  Initialize      Supplement              Optimize           │
│  (full setup)   (add skills)       (scan & improve)         │
│                                                             │
│  Phase 1: Project Scan (auto-detect everything)             │
│  Phase 2: Skill Planning (propose what to create/update)    │
│  Phase 3: Guided Q&A (smart questions with defaults)        │
│  Phase 4: Generate / Update (surgical edits, never nuke)    │
│  Phase 5: Verify & Report                                   │
└─────────────────────────────────────────────────────────────┘
```

### First Run — Initialize

Claude Skill Evo scans your project and pre-fills answers before asking:

```
I scanned your project and found:

📁 Type: TypeScript monorepo
🛠️ Framework: Next.js + tRPC
📦 Package manager: pnpm
🐳 Docker: Yes (docker-compose.yml)
📛 Suggested prefix: myapp (from package.json)

Confirm and fill in what I couldn't detect...
```

### Subsequent Runs — Optimize

Compares your project's current state against existing skills:

```
📊 Skill System Health Report

Existing skills:
  ✅ myapp-dev      v1.0.2  — healthy
  ⚠️ myapp-debug    v1.0.1  — 1 stale reference found
  ✅ myapp-review   v1.0.0  — healthy

Improvement opportunities:
  1. 🆕 Detected Vitest but no test skill → create one?
  2. 🔄 README has new commands not in dev skill → update?

Which ones? (1,2 / all / skip)
```

## What Gets Generated

```
.claude/
├── CLAUDE.md                          # Project-level Claude instructions
├── knowledge/                         # Project knowledge base
│   ├── decisions/                     # Architecture decisions
│   ├── research/                      # Tech research notes
│   ├── pitfalls/                      # Known pitfalls & lessons learned
│   ├── conventions/                   # Project conventions
│   └── references/                    # External references
└── skills/
    ├── {prefix}-skill/SKILL.md        # Meta-skill + evolution engine
    ├── {prefix}-dev/SKILL.md          # Local dev commands & environment
    ├── {prefix}-commit/SKILL.md       # Git commit conventions
    ├── {prefix}-debug/SKILL.md        # Bug fix workflow + experience DB
    ├── {prefix}-digest/SKILL.md       # Knowledge capture
    ├── {prefix}-review/SKILL.md       # Multi-agent code review
    └── {prefix}-research/SKILL.md     # Tech evaluation + source analysis
```

`{prefix}` is auto-detected from your project (package.json, go.mod, Cargo.toml, etc.) — you just confirm.

All 7 skills are generated by default. The meta-skill (`{prefix}-skill`) includes a built-in evolution engine — run `/{prefix}-skill evolve` to trigger a full skill health scan.

## Self-Evolution Protocol

**This is what makes Claude Skill Evo different from every other scaffolding tool.**

Every generated skill is a living document with three built-in evolution mechanisms:

### 1. Auto-Learn

Skills listen for learning signals during normal use:

| Signal | Example | What happens |
|--------|---------|-------------|
| User correction | "Don't use `var`, use `const`" | Proposes adding the rule to the skill |
| Repeated pattern | Same file structure used 3 times | Proposes as a convention |
| Explicit instruction | "Remember: always use UTC" | Proposes writing to skill |
| Toolchain change | New dependency added | Proposes updating related skill |

### 2. Stale Detection

Skills detect when their own content goes out of date:

| Signal | Example |
|--------|---------|
| Dead paths | `src/utils/` referenced but directory renamed to `src/lib/` |
| Failed commands | `pnpm test` changed to `pnpm vitest` |
| API changes | Framework method deprecated in new version |
| Norm conflicts | Skill says "use tabs" but codebase uses spaces |

### 3. Session Review

At the end of long sessions, skills proactively ask:

```
📝 Session Review — I noticed things worth capturing:

1. [New pattern] AppError class adopted across all handlers → write to myapp-skill?
2. [Bug fix] OAuth token refresh race condition → write to myapp-debug/records/?

Write all? Or confirm one by one?
```

**All updates require your confirmation.** Skills propose, you decide.

### 4. Cross-Session Evolution (Hooks)

The three mechanisms above work **within** a single session. But what about corrections you made last week? Patterns that emerge over months?

Claude Skill Evo includes a **three-layer incremental digest chain** that captures interaction data across sessions and gets smarter over time — without ever re-reading all historical data.

```
┌─────────────────────────────────────────────────────────────────┐
│                  Three-Layer Evolution Architecture              │
│                                                                 │
│  Layer 1: CAPTURE (async, every session)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ SessionStart  │  │UserPrompt    │  │ PostToolUse            │ │
│  │ (count+trigger│  │Submit        │  │ (Edit/Write/Bash/Read) │ │
│  │  conditions)  │  │(full prompt) │  │ selective capture      │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬─────────────┘ │
│         │                 │                      │               │
│         ▼                 ▼                      ▼               │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │           raw/prompts-{sid}.jsonl + tools-{sid}.jsonl    │     │
│  └────────────────────────┬────────────────────────────────┘     │
│                           │                                      │
│  Layer 2: DIGEST (SessionEnd, Python)                            │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Extract signals from raw data:                          │     │
│  │  • corrections  ("不对", "should be", "wrong")           │     │
│  │  • instructions ("记住", "always", "never")              │     │
│  │  • patterns     (hot files ≥3 edits, frequent cmds)      │     │
│  │  • failures     (exit code ≠ 0, command not found)       │     │
│  └────────────────────────┬────────────────────────────────┘     │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              pending-signals.jsonl (append-only)          │     │
│  └────────────────────────┬────────────────────────────────┘     │
│                           │                                      │
│  Layer 3: EVOLVE (next SessionStart, Claude)                     │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Trigger conditions:                                      │     │
│  │    pending signals ≥ 5  OR  sessions since last ≥ 3       │     │
│  │                                                           │     │
│  │  Claude reads:                                            │     │
│  │    evolution-digest.md  (checkpoint of all past analysis) │     │
│  │  + pending-signals.jsonl (only new signals)               │     │
│  │  + .claude/skills/      (current skill content)           │     │
│  │                                                           │     │
│  │  → Proposes updates → User confirms → Skills evolve       │     │
│  │  → Updates digest checkpoint (never grows unbounded)      │     │
│  └─────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

#### How each layer works

**Layer 1 — Capture** runs as async Claude Code hooks with zero latency impact. It selectively records:

| Hook Event | What's Captured | Why |
|------------|----------------|-----|
| `UserPromptSubmit` | Full prompt text | Detect corrections and explicit instructions |
| `PostToolUse` (Edit/Write) | File path + input preview | Track hot files (edited ≥3 times) |
| `PostToolUse` (Bash) | Command + result preview | Track frequent commands, detect failures |
| `PostToolUse` (Read) | File path only | Understand what you reference |
| `Stop` | Response preview (500 chars) | Correlate responses with prompts |

Glob, Grep, and Agent calls are **intentionally skipped** — they're exploratory noise. This selective approach reduces captured data by ~80%.

**Layer 2 — Digest** runs automatically at `SessionEnd`. A Python script scans the raw captured data and extracts structured **evolution signals** using regex pattern matching (supports both Chinese and English). Signals are appended to `pending-signals.jsonl`. Raw files older than 30 days are auto-cleaned.

**Layer 3 — Evolve** triggers conditionally at the next `SessionStart`:
- Only when `pending_signal_count ≥ 5` **or** `sessions_since_last_analysis ≥ 3` (with at least 1 pending signal)
- Claude reads the **digest checkpoint** (`evolution-digest.md`) — a summary of everything already analyzed — plus only the **new pending signals**
- Compares against current skill content and proposes targeted updates
- After analysis, updates the checkpoint and clears pending signals

**Key innovation: the digest checkpoint means Claude never re-reads history.** Analysis stays fast regardless of how many months you've been using it.

#### Data directory structure

```
.claude/evolution/
├── hooks/
│   ├── capture.sh              # Unified hook entry point
│   └── digest.py               # Signal extraction engine
├── raw/                        # Per-session capture (auto-cleaned after 30 days)
│   ├── prompts-{session}.jsonl
│   ├── tools-{session}.jsonl
│   └── responses-{session}.jsonl
├── pending-signals.jsonl       # Accumulated signals awaiting analysis
├── evolution-digest.md         # Checkpoint — summary of all past analysis
└── session-meta.json           # Session counter + trigger state
```

All data stays **local** (never uploaded). Add `raw/` and `pending-signals.jsonl` to `.gitignore` — only `evolution-digest.md` is worth committing as team knowledge.

```bash
# Manual triggers
/{prefix}-skill 进化    # Run evolution analysis now
/{prefix}-digest        # Capture knowledge
```

**Standalone installation** (for projects with existing skills):

```bash
curl -fsSL https://raw.githubusercontent.com/atompilot/claude-skill-evo/main/evolution/install.sh | bash
```

## Guided Q&A

Claude Skill Evo doesn't interrogate you — it guides you:

- Every question comes with **options, examples, and recommendations**
- Answers are **pre-filled from project scanning** when possible
- **"Not sure"** is always valid (sensible defaults are used)
- Skipped questions can be filled in on the **next `/skill-evo` run**
- Questions **help you discover what you actually need**, not just collect data

## Supported Tech Stacks

Auto-detection works for all major stacks:

| Language | Frameworks | Databases |
|----------|-----------|-----------|
| TypeScript/JavaScript | Next.js, React, Vue, Svelte, Hono, Express, tRPC | PostgreSQL, MySQL, MongoDB, SQLite |
| Python | Django, Flask, FastAPI | PostgreSQL, MySQL, SQLite |
| Go | Gin, Echo, Fiber, GoFrame | PostgreSQL, MySQL |
| Rust | Axum, Actix | PostgreSQL |
| Swift | SwiftUI, UIKit | CoreData, SwiftData, GRDB |
| Java/Kotlin | Spring Boot | PostgreSQL, MySQL |
| Ruby | Rails | PostgreSQL, MySQL, SQLite |

**Other stacks work too** — Claude Skill Evo asks more targeted questions to compensate.

## Installation

```bash
# Plugin marketplace (recommended)
claude plugin marketplace add atompilot/claude-skill-evo
claude plugin install claude-skill-evo@claude-skill-evo

# Or copy manually
cp -r skills/claude-skill-evo ~/.claude/skills/
```

## Design Principles

| Principle | What it means |
|-----------|--------------|
| **Run repeatedly, improve incrementally** | Every `/skill-evo` makes your skills better |
| **Detect more, ask less** | Scan the project before asking questions |
| **Guide, don't interrogate** | Options with explanations, not blank fields |
| **Concrete over generic** | Real paths, real commands, real framework names |
| **Start minimal, evolve naturally** | v1.0.0 skills are lean — they grow through use |
| **Never overwrite** | Optimize mode edits surgically, never replaces wholesale |
| **Skills that learn** | Every skill detects, proposes, and evolves with confirmation |

## License

MIT
