---
name: skill-evo
description: >
  交互式锻造项目专属 Claude Code skills，内置自我进化能力。
  扫描项目 → 规划 → 问答 → 生成。可反复执行，越用越好。
  触发词：初始化 skills、init skills、skill-evo、锻造 skill、
  优化 skill、进化 skill、审查 skill、skill review。
version: 5.0.0
source: claude-skill-evo
license: MIT
author: Atompilot
---

# Claude Skill Evo — 锻造会进化的项目 Skill

```
/skill-evo                     # 扫描项目，初始化或优化
/skill-evo 补充 API 规范        # 带提示词，重点优化指定方向
/skill-evo review              # 审查 SKILL.md 质量
/skill-evo review {prefix}-dev # 审查指定 skill
```

**ARGUMENTS**: $ARGUMENTS

---

## 核心理念

### Skill 编写的判断框架

把 Claude 理解为一个很聪明、学习能力很强的大学生。Skill 要提供的是**靠实践和时间堆积才能掌握的业务经验**，其余靠 Claude 的基础能力、搜索和自学就能解决。

区分三种内容：

| 类型 | 定义 | 写入 Skill 吗 |
|------|------|--------------|
| **经验** | 靠实践积累的业务知识（架构决策、踩坑记录、领域判断标准） | ✅ 必须写 |
| **约定** | Claude 能做但每次可能做法不同，需要显式固定以保证一致性（格式规范、安全边界、命名惯例） | ✅ 必须写 |
| **共识** | Claude 每次都会一样做的事（怎么扫描项目、怎么提问、怎么格式化输出） | ❌ 不写 |

**判断标准**：
- 经验 → 「去掉后 Claude 会做错吗？」会 → 写
- 约定 → 「去掉后 Claude 每次做法一致吗？」不一致 → 写
- 共识 → 「去掉后 Claude 还会这么做吗？」会 → 不写

### 进化是核心，脚手架是副产品

skill-evo 的核心价值不是生成文件，而是**让 skill 活着**。skill 通过日常工作被动进化——每次对话都是进化的机会，不依赖显式命令。

每个生成的 Skill 必须内置自我进化协议（详见 [reference/evolution-protocol.md](reference/evolution-protocol.md)）：

- **被动感知**：用户纠正、失败→修复、显式指令"记住这个"、内容过期 → 提议更新
- **绝不擅自修改**：展示变更预览，用户确认后才写入
- **体积守护**：每个 SKILL.md ≤ 15KB，超过先压缩
- **版本追踪**：每次写入 version patch +1

### Skill vs Command

| | Skill | Command |
|-|-------|---------|
| 触发 | 关键词自动触发 | 显式 `/command` 调用 |
| 进化 | 内置自我进化协议 | 无（轻量，用户手动维护） |
| 适合 | 持续性行为模式 | 一次性过程执行 |

---

## 约定（保证跨 session 一致性）

### 文件格式

**Skill**（`.claude/skills/{prefix}-{name}/SKILL.md`）：
```yaml
---
name: {prefix}-{name}
description: >
  一句话描述。触发词：xxx、yyy。
version: 1.0.0
---
```

**Command**（`.claude/commands/{prefix}-{name}.md`）：
```yaml
---
name: {prefix}-{name}
description: 一句话描述
---
```

### 安全边界

- **不修改** `~/.claude.json`、`~/.claude/settings.json` 等全局配置
- `.gitignore` **只追加不覆盖**，先读取现有内容再 append
- 写入文件前必须先 Read 确认目标路径
- **尊重用户已有 skill**：除非用户明确指示，只为现有 skill 补充自我进化协议，不改动其他内容。用户自己积累的 skill 内容是宝贵资产，不得擅自修改或覆盖

### 完成报告格式

每次生成/更新完成后输出：

```
✅ {skill-name} v{version} — {动作}（created/updated/skipped）
...
📊 共 N 个 skill，M 个 command
```

---

## 运行模式

根据 $ARGUMENTS 和 `.claude/` 目录状态，进入不同模式：

### 模式判断

| 条件 | 模式 | 行为 |
|------|------|------|
| $ARGUMENTS 含 `review`/`审查` | **审查模式** | 独立路径：并行审查现有 skill 质量，不走生成流程 |
| 无 `.claude/` 目录 | **首次初始化** | 完整流程：感知 → 规划 → 问答 → 生成全套 |
| 有 CLAUDE.md 无 skills | **补充模式** | 读取已有 CLAUDE.md 作为上下文，只生成 skills |
| 有 CLAUDE.md 和 skills | **优化模式** | 读取现有 skill 体系，找缺失/过期/可改进项 |

### 优化模式的关键约束

这是踩坑经验——**绝不全量覆盖已有 skill**：

- 用户可能已经手动编辑了 skill 内容，全量覆盖会丢失这些自定义
- 只用 Edit 精确修改需要变化的章节，保留用户已有内容
- 对照模板库找出**缺失的 skill**（模板库有但项目没有）和**过期内容**（`<!-- STALE: -->` 标记）
- 每次更新递增 version patch，记录到 evolution.log

---

## 执行流程

### 感知项目

信息源优先级：**$ARGUMENTS > README > 目录结构 > Git 信息**

从这些信息中理解项目，推断 prefix，向用户展示感知结果并确认。只问无法从项目中推断出的信息。

### 规划 skill 体系

从模板库中选择适合的 skill/command 组合。**根据项目特性裁剪**——不是所有模板都适合所有项目：

- 纯 Skill/文档项目不需要 dev 和 debug
- 项目的核心产品本身是 skill 时，需要创建模板库之外的自定义 skill
- 向用户展示方案，让用户增减

### 构建

SubAgent 并行生成。每个 SubAgent 通过 Read 读取 `${CLAUDE_PLUGIN_ROOT}/templates/` 下的模板文件，结合项目上下文替换占位符。

Skill 类型还需 Read [reference/evolution-protocol.md](reference/evolution-protocol.md)，注入到末尾。

### 进化系统基础设施（首次初始化时）

生成 skill 文件之外，还需初始化进化系统：

```
.claude/evolution/
├── raw/                    # hook 捕获的原始数据（.gitignore）
├── hooks/                  # capture.sh 等 hook 脚本
├── session-meta.json       # 会话元数据（.gitignore）
└── evolution-digest.md     # 进化摘要
```

将 `evolution/capture.sh` 和 `evolution/digest.py`（位于本插件的 `evolution/` 目录下）的逻辑适配到目标项目。在 `.gitignore` 中排除 `raw/`、`session-meta.json` 等临时文件。

---

## 模板库

SubAgent 通过 Read 读取对应模板，结合项目上下文生成实际文件。

**Skills**（`.claude/skills/`，注入 [进化协议](reference/evolution-protocol.md)）：

| 模板 | 用途 |
|------|------|
| [skill-dev.md](templates/skill-dev.md) | 本地开发环境 |
| [skill-debug.md](templates/skill-debug.md) | 深度调试 + 经验沉淀 |
| [skill-meta.md](templates/skill-meta.md) | 元技能（管理所有 skill） |
| [skill-digest.md](templates/skill-digest.md) | 知识沉淀 |
| [skill-todo.md](templates/skill-todo.md) | 项目待办 |

**Commands**（`.claude/commands/`，无进化协议）：

| 模板 | 用途 |
|------|------|
| [command-commit.md](templates/command-commit.md) | Git 提交 |
| [command-review.md](templates/command-review.md) | 代码审查 |
| [command-research.md](templates/command-research.md) | 技术调研 |

**其他**：[claude-md.md](templates/claude-md.md)（项目 CLAUDE.md）、[knowledge-index.md](templates/knowledge-index.md)（知识库索引）
