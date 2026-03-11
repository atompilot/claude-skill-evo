<p align="center">
  <h1 align="center">SkillForge</h1>
  <p align="center">
    <strong>Your Claude Code skills rot. SkillForge makes them evolve.</strong>
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
/skillforge
```

> **No config files. No templates to fill. No YAML to write.**
> SkillForge scans your codebase, asks smart questions, and forges skills that actually match how you work.

---

## Why SkillForge?

| Without SkillForge | With SkillForge |
|---|---|
| Manually write CLAUDE.md and skills from scratch | Auto-generated from project scanning + guided Q&A |
| Skills go stale as your project evolves | Skills **detect their own staleness** and propose fixes |
| Copy-paste generic templates | Every path, command, and convention is **your project's real data** |
| One-time setup, then forgotten | Run `/skillforge` again anytime — it only gets better |
| "I forgot to update the skill" | Skills **learn from your corrections** in real-time |

## Quick Start

```bash
# Install (one time)
claude plugin marketplace add atompilot/skillforge
claude plugin install skillforge@skillforge

# Use (as many times as you want)
/skillforge                              # Full scan → initialize or optimize
/skillforge add API conventions          # Focus on a specific area
/skillforge update dev based on README   # Improve using specific references
```

## How It Works

Every `/skillforge` run starts by detecting your project state:

```
┌─────────────────────────────────────────────────────────────┐
│  /skillforge                                                │
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

SkillForge scans your project and pre-fills answers before asking:

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

**This is what makes SkillForge different from every other scaffolding tool.**

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

SkillForge includes a **hook-based evolution system** that captures interaction data across sessions:

```
Session 1: You correct Claude → hook captures it
Session 2: You correct again  → hook captures it
Session 3: You start working  → Claude reads accumulated signals
                               → "I noticed you corrected X twice. Write to skill?"
```

**How it works:**

| Layer | When | What |
|-------|------|------|
| **Capture** | Every session (async hooks) | Records prompts, tool usage, commands |
| **Digest** | Session end (shell script) | Extracts corrections, patterns, failures |
| **Evolve** | Next session start (Claude) | Reads digest checkpoint + new signals → proposes updates |

**Key innovation: incremental digest checkpoint.** Claude never re-reads all historical data. It reads a summary of what it already knows (`evolution-digest.md`) plus only new signals — so analysis gets faster, not slower, as your project grows.

```bash
# Manual triggers
/{prefix}-evolve    # Run evolution analysis now
/{prefix}-digest    # View evolution status
```

**Standalone installation** (for projects with existing skills):

```bash
curl -fsSL https://raw.githubusercontent.com/atompilot/skillforge/main/evolution/install.sh | bash
```

## Guided Q&A

SkillForge doesn't interrogate you — it guides you:

- Every question comes with **options, examples, and recommendations**
- Answers are **pre-filled from project scanning** when possible
- **"Not sure"** is always valid (sensible defaults are used)
- Skipped questions can be filled in on the **next `/skillforge` run**
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

**Other stacks work too** — SkillForge asks more targeted questions to compensate.

## Installation

```bash
# Plugin marketplace (recommended)
claude plugin marketplace add atompilot/skillforge
claude plugin install skillforge@skillforge

# Or copy manually
cp -r skills/skillforge ~/.claude/skills/
```

## Design Principles

| Principle | What it means |
|-----------|--------------|
| **Run repeatedly, improve incrementally** | Every `/skillforge` makes your skills better |
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

### 你的 Claude Code Skills 在腐烂。SkillForge 让它们进化。

一条命令，为你的项目锻造一整套量身定制的 skill 体系——而且每个 skill **都会自我学习、检测过期、主动提议更新**。

```bash
/skillforge
```

> **不需要写配置文件。不需要填模板。不需要手写 YAML。**
> SkillForge 扫描你的代码库，问几个聪明的问题，然后锻造出真正匹配你工作方式的 skills。

### 为什么选 SkillForge？

| 没有 SkillForge | 有 SkillForge |
|---|---|
| 手动从零写 CLAUDE.md 和 skills | 扫描项目 + 引导式问答，自动生成 |
| 项目迭代后 skills 就过时了 | Skills **自己检测过期内容**并提议修复 |
| 复制粘贴通用模板 | 每个路径、命令、规范都是**你项目的真实数据** |
| 一次性配置，之后再也不管 | 随时再跑 `/skillforge`——只会越来越好 |
| "忘了更新 skill 了" | Skills **从你的纠正中实时学习** |

### 核心特性

**自我进化协议** —— 每个生成的 skill 内置三大进化机制：

1. **Auto-Learn（主动学习）**：检测你的纠正、重复模式、显式指令，提议写入 skill
2. **Stale Detection（过期检测）**：发现失效路径、失败命令、API 变更、规范冲突
3. **Session Review（会话回顾）**：长会话结束前主动盘点可沉淀的新知识
4. **Cross-Session Evolution（跨会话进化）**：通过 hooks 捕获交互数据，跨会话积累分析，增量摘要永不从零开始

**所有更新都需要你确认，skills 绝不擅自修改。**

### 跨会话进化系统

会话内的进化靠 Claude 实时感知，但上次会话的纠正怎么办？

SkillForge 内置 hook 系统，**自动捕获你的交互数据**（纠正、指令、操作模式），跨会话积累分析：

```
会话 1: 你纠正了 Claude → hook 自动捕获
会话 2: 你又纠正了一次  → hook 自动捕获
会话 3: 你开始工作      → Claude 读取积累的信号
                        → "我发现你纠正过 X 两次，要写入 skill 吗？"
```

核心创新：**增量摘要 checkpoint**。Claude 不会每次重读所有历史数据，而是读取上次的总结 + 新增信号——分析速度越来越快，而不是越来越慢。

```bash
/{prefix}-evolve    # 手动触发进化分析
/{prefix}-digest    # 查看进化状态
```

### 引导式问答

SkillForge 不是审问你——而是引导你：

- 每个问题都有**选项、示例、推荐**
- 能从项目扫描中推断的答案会**预填好**
- **"不确定"** 永远是合法答案（会用合理默认值）
- 跳过的问题可以在**下次 `/skillforge`** 时补充

### 支持的技术栈

TypeScript/JavaScript、Python、Go、Rust、Swift、Java/Kotlin、Ruby —— 自动检测框架和数据库。

其他技术栈也能用——SkillForge 会多问几个问题来补偿。

### 安装

```bash
# Plugin 市场（推荐）
claude plugin marketplace add atompilot/skillforge
claude plugin install skillforge@skillforge

# 或手动复制
cp -r skills/skillforge ~/.claude/skills/
```
