<p align="center">
  <h1 align="center">Claude Skill Evo</h1>
  <p align="center">
    <strong>Your Claude Code skills rot. Claude Skill Evo makes them evolve.</strong>
  </p>
  <p align="center">
    <a href="#installation">Install</a> &middot;
    <a href="#quick-start">Quick Start</a> &middot;
    <a href="#how-it-works">How It Works</a> &middot;
    <a href="#self-evolution-protocol">Self-Evolution</a> &middot;
    <a href="#中文说明">中文</a>
  </p>
</p>

---

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
  ⚠️ myapp-bugfix   v1.0.1  — 1 stale reference found
  ✅ myapp-api      v1.0.0  — healthy

Improvement opportunities:
  1. 🆕 Detected Vitest but no test skill → create one?
  2. 🔄 README has new commands not in dev skill → update?
  3. 📝 docker-compose.yml found but no cloud skill → create one?

Which ones? (1,2 / all / skip)
```

## What Gets Generated

```
.claude/
├── CLAUDE.md                          # Project-level Claude instructions
└── skills/
    ├── {prefix}-skill/SKILL.md        # Meta-skill + evolution engine
    ├── {prefix}-dev/SKILL.md          # Local dev commands & environment
    ├── {prefix}-commit/SKILL.md       # Git commit conventions
    ├── {prefix}-bugfix/SKILL.md       # Bug fix workflow + experience DB
    │   └── records/                   # Bug fix records (grows over time)
    ├── {prefix}-api/SKILL.md          # API conventions
    ├── {prefix}-frontend/SKILL.md     # Frontend component standards
    ├── {prefix}-mobile/SKILL.md       # Mobile app patterns
    ├── {prefix}-db/SKILL.md           # Database schema & migration
    ├── {prefix}-cloud/SKILL.md        # Deployment & infrastructure
    ├── {prefix}-test/SKILL.md         # Testing strategy & commands
    ├── {prefix}-review/SKILL.md       # Multi-agent code review
    ├── {prefix}-research/SKILL.md     # Tech evaluation workflow
    ├── {prefix}-ref/SKILL.md          # Reference code analysis
    ├── {prefix}-experiment/SKILL.md   # Experiment tracking (AI/ML)
    ├── {prefix}-admin/SKILL.md        # Admin panel conventions
    └── {prefix}-migration/SKILL.md    # Migration workflow
```

`{prefix}` is auto-detected from your project (package.json, go.mod, Cargo.toml, etc.) — you just confirm.

Only applicable skills are created. A Python CLI tool won't get a `frontend` skill. A static site won't get a `db` skill.

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

1. [New pattern] API errors now use AppError class → write to myapp-api?
2. [Bug fix] OAuth token refresh race condition → write to myapp-bugfix/records/?

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
/{prefix}-evolve    # Run evolution analysis now
/{prefix}-digest    # View evolution status
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

---

<a id="中文说明"></a>

## 中文说明

### 你的 Claude Code Skills 在腐烂。Claude Skill Evo 让它们进化。

一条命令，为你的项目锻造一整套量身定制的 skill 体系——而且每个 skill **都会自我学习、检测过期、主动提议更新**。

```bash
/skill-evo
```

> **不需要写配置文件。不需要填模板。不需要手写 YAML。**
> Claude Skill Evo 扫描你的代码库，问几个聪明的问题，然后锻造出真正匹配你工作方式的 skills。

### 为什么选 Claude Skill Evo？

| 没有 Claude Skill Evo | 有 Claude Skill Evo |
|---|---|
| 手动从零写 CLAUDE.md 和 skills | 扫描项目 + 引导式问答，自动生成 |
| 项目迭代后 skills 就过时了 | Skills **自己检测过期内容**并提议修复 |
| 复制粘贴通用模板 | 每个路径、命令、规范都是**你项目的真实数据** |
| 一次性配置，之后再也不管 | 随时再跑 `/skill-evo`——只会越来越好 |
| "忘了更新 skill 了" | Skills **从你的纠正中实时学习** |

### 核心特性

**自我进化协议** —— 每个生成的 skill 内置三大进化机制：

1. **Auto-Learn（主动学习）**：检测你的纠正、重复模式、显式指令，提议写入 skill
2. **Stale Detection（过期检测）**：发现失效路径、失败命令、API 变更、规范冲突
3. **Session Review（会话回顾）**：长会话结束前主动盘点可沉淀的新知识
4. **Cross-Session Evolution（跨会话进化）**：通过 hooks 捕获交互数据，跨会话积累分析，增量摘要永不从零开始

**所有更新都需要你确认，skills 绝不擅自修改。**

### 跨会话进化系统（三层增量摘要链）

会话内的进化靠 Claude 实时感知，但上次会话的纠正怎么办？跨月份积累的模式怎么沉淀？

Claude Skill Evo 内置**三层增量摘要链**（Capture → Digest → Evolve），通过 Claude Code hooks 自动捕获交互数据，跨会话积累分析——而且**永远不会从零开始**。

```
┌─────────────────────────────────────────────────────────┐
│              三层增量摘要链架构                            │
│                                                         │
│  第 1 层：CAPTURE（异步 hooks，每次会话实时运行）          │
│  ┌────────────┐ ┌────────────┐ ┌──────────────────────┐ │
│  │SessionStart│ │UserPrompt  │ │PostToolUse           │ │
│  │计数+触发   │ │Submit      │ │仅 Edit/Write/Bash/   │ │
│  │条件检查    │ │完整 prompt │ │Read，跳过探索性操作   │ │
│  └─────┬──────┘ └─────┬──────┘ └──────────┬───────────┘ │
│        └───────────────┼──────────────────┘              │
│                        ▼                                 │
│        raw/prompts-{sid}.jsonl + tools-{sid}.jsonl        │
│                        │                                 │
│  第 2 层：DIGEST（SessionEnd 时自动运行 Python 脚本）      │
│                        ▼                                 │
│   提取 4 类进化信号：                                     │
│   • 纠正信号 ("不对"、"应该是"、"wrong"、"should be")     │
│   • 指令信号 ("记住"、"以后都"、"always"、"never")        │
│   • 模式信号 (同一文件编辑 ≥3 次、同一命令执行 ≥3 次)     │
│   • 失败信号 (exit code ≠ 0、command not found)           │
│                        │                                 │
│                        ▼                                 │
│        pending-signals.jsonl（追加写入，只增不覆盖）       │
│                        │                                 │
│  第 3 层：EVOLVE（下次 SessionStart 时条件触发）           │
│                        ▼                                 │
│   触发条件：待分析信号 ≥ 5 或 距上次分析 ≥ 3 个会话        │
│                                                         │
│   Claude 读取：                                          │
│     evolution-digest.md  ← 上次分析的总结 checkpoint      │
│   + pending-signals.jsonl ← 仅新增信号                   │
│   + .claude/skills/       ← 当前 skill 内容              │
│                                                         │
│   → 提议更新 → 你确认 → Skills 进化                      │
│   → 更新 digest checkpoint（永不无限增长）                │
└─────────────────────────────────────────────────────────┘
```

#### 各层详解

**第 1 层 — Capture**：以零延迟异步 hooks 运行，选择性捕获关键数据：

| Hook 事件 | 捕获内容 | 目的 |
|-----------|---------|------|
| `UserPromptSubmit` | 完整 prompt | 检测纠正和显式指令 |
| `PostToolUse`（Edit/Write） | 文件路径 + 输入预览 | 追踪热点文件 |
| `PostToolUse`（Bash） | 命令 + 结果预览 | 追踪高频命令、检测失败 |
| `PostToolUse`（Read） | 仅文件路径 | 了解你在参考什么 |

Glob、Grep、Agent 调用**故意跳过**——它们是探索性噪音，选择性捕获减少约 80% 数据量。

**第 2 层 — Digest**：`SessionEnd` 时自动运行 Python 脚本，用正则匹配（支持中英文）从原始数据中提取结构化信号，追加到 `pending-signals.jsonl`。超过 30 天的原始数据自动清理。

**第 3 层 — Evolve**：下次 `SessionStart` 时条件触发。Claude 读取 **digest checkpoint**（已分析过的所有内容的总结）+ **仅新增的待分析信号**，对比当前 skill 内容后提议更新。分析完成后更新 checkpoint 并清空待分析信号。

**核心创新：digest checkpoint 意味着 Claude 永远不用重读历史。** 无论用了多少个月，分析速度始终恒定。

#### 数据目录结构

```
.claude/evolution/
├── hooks/
│   ├── capture.sh              # 统一 hook 入口
│   └── digest.py               # 信号提取引擎
├── raw/                        # 按会话存储（30 天自动清理）
│   ├── prompts-{session}.jsonl
│   ├── tools-{session}.jsonl
│   └── responses-{session}.jsonl
├── pending-signals.jsonl       # 待分析信号（追加写入）
├── evolution-digest.md         # Checkpoint——所有历史分析的总结
└── session-meta.json           # 会话计数器 + 触发状态
```

所有数据**仅存储在本地**（永不上传）。`raw/` 和 `pending-signals.jsonl` 加入 `.gitignore`——只有 `evolution-digest.md` 值得提交，作为团队知识沉淀。

```bash
/{prefix}-evolve    # 手动触发进化分析
/{prefix}-digest    # 查看进化状态
```

**独立安装**（适用于已有 skills 的项目）：

```bash
curl -fsSL https://raw.githubusercontent.com/atompilot/claude-skill-evo/main/evolution/install.sh | bash
```

### 引导式问答

Claude Skill Evo 不是审问你——而是引导你：

- 每个问题都有**选项、示例、推荐**
- 能从项目扫描中推断的答案会**预填好**
- **"不确定"** 永远是合法答案（会用合理默认值）
- 跳过的问题可以在**下次 `/skill-evo`** 时补充

### 支持的技术栈

TypeScript/JavaScript、Python、Go、Rust、Swift、Java/Kotlin、Ruby —— 自动检测框架和数据库。

其他技术栈也能用——Claude Skill Evo 会多问几个问题来补偿。

### 安装

```bash
# Plugin 市场（推荐）
claude plugin marketplace add atompilot/claude-skill-evo
claude plugin install claude-skill-evo@claude-skill-evo

# 或手动复制
cp -r skills/claude-skill-evo ~/.claude/skills/
```
