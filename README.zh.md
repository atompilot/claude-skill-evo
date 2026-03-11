<p align="center">
  <h1 align="center">Claude Skill Evo</h1>
  <p align="center">
    <strong>你的 Claude Code Skills 在腐烂。Claude Skill Evo 让它们进化。</strong>
  </p>
  <p align="center">
    <a href="#安装">安装</a> &middot;
    <a href="#快速开始">快速开始</a> &middot;
    <a href="#工作原理">工作原理</a> &middot;
    <a href="#自我进化协议">自我进化</a> &middot;
    <a href="README.md">English</a>
  </p>
  <p align="center">
    <img src="https://img.shields.io/github/stars/atompilot/claude-skill-evo?style=flat-square" alt="GitHub stars">
    <img src="https://img.shields.io/github/license/atompilot/claude-skill-evo?style=flat-square" alt="License">
    <img src="https://img.shields.io/badge/Claude%20Code-Plugin-blue?style=flat-square" alt="Claude Code Plugin">
  </p>
</p>

---

**适合 Claude Code 用户**——如果你希望 skill 体系随项目一起成长，而不是随时间腐烂成过期指令。

一条命令，为你的项目锻造一整套量身定制的 skill 体系——而且每个 skill **都会自我学习、检测过期、主动提议更新**。

```bash
/skill-evo
```

> **不需要写配置文件。不需要填模板。不需要手写 YAML。**
> Claude Skill Evo 扫描你的代码库，问几个聪明的问题，然后锻造出真正匹配你工作方式的 skills。

---

## 为什么选 Claude Skill Evo？

| 没有 Claude Skill Evo | 有 Claude Skill Evo |
|---|---|
| 手动从零写 CLAUDE.md 和 skills | 扫描项目 + 引导式问答，自动生成 |
| 项目迭代后 skills 就过时了 | Skills **自己检测过期内容**并提议修复 |
| 复制粘贴通用模板 | 每个路径、命令、规范都是**你项目的真实数据** |
| 一次性配置，之后再也不管 | 随时再跑 `/skill-evo`——只会越来越好 |
| "忘了更新 skill 了" | Skills **从你的纠正中实时学习** |

## 快速开始

```bash
# 安装（一次即可）
claude plugin marketplace add atompilot/claude-skill-evo
claude plugin install claude-skill-evo@claude-skill-evo

# 使用（随时可跑）
/skill-evo                              # 完整扫描 → 初始化或优化
/skill-evo add API conventions          # 聚焦某个特定领域
/skill-evo update dev based on README   # 使用特定参考优化 skill
```

## 工作原理

每次 `/skill-evo` 都从检测项目状态开始：

```
┌─────────────────────────────────────────────────────────┐
│  /skill-evo                                             │
│                                                         │
│  Phase 0: 状态检测                                       │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │ 没有     │  │ 有 CLAUDE.md │  │ 有 CLAUDE.md + skills│ │
│  │ .claude/ │  │ 但没有 skills│  │                     │ │
│  └────┬─────┘  └──────┬───────┘  └──────────┬──────────┘ │
│       ▼               ▼                     ▼            │
│   初始化          补充 skills             优化            │
│  （完整建立）     （新增 skills）     （扫描并改进）        │
│                                                         │
│  Phase 1: 项目扫描（自动检测一切）                        │
│  Phase 2: Skill 规划（提议创建或更新什么）                 │
│  Phase 3: 引导式问答（智能问题 + 默认值）                  │
│  Phase 4: 生成/更新（精准编辑，绝不整体替换）              │
│  Phase 5: 验证并报告                                     │
└─────────────────────────────────────────────────────────┘
```

### 首次运行——初始化

Claude Skill Evo 在提问前先扫描项目并预填答案：

```
I scanned your project and found:

📁 Type: TypeScript monorepo
🛠️ Framework: Next.js + tRPC
📦 Package manager: pnpm
🐳 Docker: Yes (docker-compose.yml)
📛 Suggested prefix: myapp (from package.json)

Confirm and fill in what I couldn't detect...
```

### 后续运行——优化

将项目当前状态与已有 skills 进行对比：

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

## 生成的文件结构

```
.claude/
├── CLAUDE.md                          # 项目级 Claude 指令
├── knowledge/                         # 项目知识库
│   ├── decisions/                     # 架构决策
│   ├── research/                      # 技术调研笔记
│   ├── pitfalls/                      # 已知坑点与教训
│   ├── conventions/                   # 项目约定
│   └── references/                    # 外部参考资料
└── skills/
    ├── {prefix}-skill/SKILL.md        # 元 skill + 进化引擎
    ├── {prefix}-dev/SKILL.md          # 本地开发命令与环境
    ├── {prefix}-commit/SKILL.md       # Git 提交规范
    ├── {prefix}-debug/SKILL.md        # Bug 修复工作流 + 经验库
    ├── {prefix}-digest/SKILL.md       # 知识沉淀
    ├── {prefix}-review/SKILL.md       # 多 Agent 代码审查
    └── {prefix}-research/SKILL.md     # 技术调研 + 来源分析
```

`{prefix}` 从你的项目自动检测（package.json、go.mod、Cargo.toml 等）——你只需确认。

默认生成全部 7 个 skill。元 skill（`{prefix}-skill`）内置进化引擎——运行 `/{prefix}-skill evolve` 即可触发完整 skill 健康扫描。

## 自我进化协议

**这就是 Claude Skill Evo 与所有其他脚手架工具的本质区别。**

每个生成的 skill 都是一份活文档，内置三大进化机制：

### 1. Auto-Learn（主动学习）

Skills 在日常使用中监听学习信号：

| 信号 | 示例 | 发生什么 |
|------|------|---------|
| 用户纠正 | "不要用 `var`，用 `const`" | 提议将规则写入 skill |
| 重复模式 | 同一文件结构使用 3 次 | 提议作为规范固化 |
| 显式指令 | "记住：始终用 UTC" | 提议写入 skill |
| 工具链变更 | 新增依赖 | 提议更新相关 skill |

### 2. Stale Detection（过期检测）

Skills 检测自身内容何时过期：

| 信号 | 示例 |
|------|------|
| 失效路径 | `src/utils/` 被引用，但目录已改名为 `src/lib/` |
| 命令失败 | `pnpm test` 已改为 `pnpm vitest` |
| API 变更 | 框架方法在新版本中被废弃 |
| 规范冲突 | Skill 说"用 Tab"，但代码库用空格 |

### 3. Session Review（会话回顾）

长会话结束前，skills 主动盘点：

```
📝 Session Review — I noticed things worth capturing:

1. [New pattern] AppError class adopted across all handlers → write to myapp-skill?
2. [Bug fix] OAuth token refresh race condition → write to myapp-debug/records/?

Write all? Or confirm one by one?
```

**所有更新都需要你确认。** Skills 提议，你决定。

### 4. 跨会话进化（Hooks）

上面三个机制在**单次会话内**生效。但上周的纠正怎么办？跨月积累的模式怎么沉淀？

Claude Skill Evo 内置**三层增量摘要链**，通过 hooks 跨会话捕获交互数据，持续变聪明——且**永远不从零开始**。

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
│   • 纠正信号（"不对"、"应该是"、"wrong"、"should be"）    │
│   • 指令信号（"记住"、"以后都"、"always"、"never"）       │
│   • 模式信号（同一文件编辑 ≥3 次、同一命令执行 ≥3 次）    │
│   • 失败信号（exit code ≠ 0、command not found）          │
│                        │                                 │
│                        ▼                                 │
│        pending-signals.jsonl（追加写入，只增不覆盖）       │
│                        │                                 │
│  第 3 层：EVOLVE（下次 SessionStart 时条件触发）           │
│                        ▼                                 │
│   触发条件：待分析信号 ≥ 5 或 距上次分析 ≥ 3 个会话        │
│                                                         │
│   Claude 读取：                                          │
│     evolution-digest.md  ← 已分析内容的 checkpoint       │
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
| `PostToolUse`（Edit/Write） | 文件路径 + 输入预览 | 追踪热点文件（编辑 ≥3 次） |
| `PostToolUse`（Bash） | 命令 + 结果预览 | 追踪高频命令、检测失败 |
| `PostToolUse`（Read） | 仅文件路径 | 了解你在参考什么 |

Glob、Grep、Agent 调用**故意跳过**——它们是探索性噪音，选择性捕获减少约 80% 数据量。

**第 2 层 — Digest**：`SessionEnd` 时自动运行 Python 脚本，用正则匹配（支持中英文）从原始数据中提取结构化信号，追加到 `pending-signals.jsonl`。超过 30 天的原始数据自动清理。

**第 3 层 — Evolve**：下次 `SessionStart` 时条件触发。Claude 读取 **digest checkpoint**（已分析过所有内容的总结）+ **仅新增的待分析信号**，对比当前 skill 内容后提议更新。分析完成后更新 checkpoint 并清空待分析信号。

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
/{prefix}-skill 进化    # 手动触发进化分析
/{prefix}-digest        # 沉淀知识
```

**独立安装**（适用于已有 skills 的项目）：

```bash
curl -fsSL https://raw.githubusercontent.com/atompilot/claude-skill-evo/main/evolution/install.sh | bash
```

## 引导式问答

Claude Skill Evo 不是审问你——而是引导你：

- 每个问题都有**选项、示例、推荐**
- 能从项目扫描中推断的答案会**预填好**
- **"不确定"** 永远是合法答案（会用合理默认值）
- 跳过的问题可以在**下次 `/skill-evo`** 时补充
- 问题帮你**发现你真正需要什么**，而不只是收集数据

## 支持的技术栈

主流技术栈均支持自动检测：

| 语言 | 框架 | 数据库 |
|------|------|--------|
| TypeScript/JavaScript | Next.js、React、Vue、Svelte、Hono、Express、tRPC | PostgreSQL、MySQL、MongoDB、SQLite |
| Python | Django、Flask、FastAPI | PostgreSQL、MySQL、SQLite |
| Go | Gin、Echo、Fiber、GoFrame | PostgreSQL、MySQL |
| Rust | Axum、Actix | PostgreSQL |
| Swift | SwiftUI、UIKit | CoreData、SwiftData、GRDB |
| Java/Kotlin | Spring Boot | PostgreSQL、MySQL |
| Ruby | Rails | PostgreSQL、MySQL、SQLite |

**其他技术栈也能用**——Claude Skill Evo 会多问几个问题来补偿。

## 安装

```bash
# Plugin 市场（推荐）
claude plugin marketplace add atompilot/claude-skill-evo
claude plugin install claude-skill-evo@claude-skill-evo

# 或手动复制
cp -r skills/claude-skill-evo ~/.claude/skills/
```

## 设计原则

| 原则 | 含义 |
|------|------|
| **反复运行，持续改进** | 每次 `/skill-evo` 都让 skills 更好 |
| **多检测，少提问** | 先扫描项目，再提问 |
| **引导，不审问** | 带选项和解释的问题，而非空白填写 |
| **具体胜过通用** | 真实路径、真实命令、真实框架名 |
| **从精简开始，自然进化** | v1.0.0 的 skills 轻量——通过使用成长 |
| **绝不覆盖** | 优化模式精准编辑，绝不整体替换 |
| **会学习的 skills** | 每个 skill 都能检测、提议、并在你确认后进化 |

## License

MIT
