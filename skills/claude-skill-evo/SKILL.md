---
name: skill-evo
description: >
  交互式锻造项目专属 Claude Code skills，内置自我进化能力。
  扫描项目 → 规划 → 问答 → 生成。可反复执行，越用越好。
  触发词：初始化 skills、init skills、skill-evo、锻造 skill、
  优化 skill、进化 skill、审查 skill、skill review。
version: 5.1.0
source: claude-skill-evo
license: MIT
author: Atompilot
---

# Claude Skill Evo — 锻造会进化的项目 Skill

```
/skill-evo                     # 扫描项目，初始化或优化
/skill-evo 补充 API 规范        # 带提示词，重点优化指定方向
/skill-evo review              # 审查 SKILL.md 质量
/skill-evo review {prefix}-debug # 审查指定 skill
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
| $ARGUMENTS 含 `review`/`审查` | **审查模式** | 独立路径：并行 4 Agent 审查现有 skill 质量（结构、内容、一致性、安全），不走生成流程。详见下方「审查模式」 |
| 无 `.claude/` 目录 | **首次初始化** | 完整流程：感知 → 规划 → 问答 → 生成全套 |
| 有 CLAUDE.md 无 skills | **补充模式** | 读取已有 CLAUDE.md 作为上下文，只生成 skills |
| 有 CLAUDE.md 和 skills | **优化模式** | 读取现有 skill 体系，找缺失/过期/可改进项 |

> **CLAUDE.md 位置检测**：检查 `./CLAUDE.md` 和 `./.claude/CLAUDE.md`，以实际存在的为准。部分项目将 CLAUDE.md 放在根目录而非 `.claude/` 目录下。

### 优化模式的关键约束

这是踩坑经验——**绝不全量覆盖已有 skill**：

- 用户可能已经手动编辑了 skill 内容，全量覆盖会丢失这些自定义
- 只用 Edit 精确修改需要变化的章节，保留用户已有内容
- 对照模板库找出**缺失的 skill**（模板库有但项目没有）和**过期内容**（`<!-- STALE: -->` 标记）
- 每次更新递增 version patch，记录到 evolution.log

### 优化模式的内容健康检查

除了文件存在性检查，还需做内容交叉验证：

- 对每个 skill 中引用的文件路径，用 Glob/Grep 确认路径在项目中实际存在
- 对比 CLAUDE.md 与各 skill 的术语一致性（项目名、prefix、关键约定）
- 检查 knowledge/pitfalls/ 中的踩坑记录是否已被 debug skill 的速查索引吸收
- 若发现不一致，作为「可改进项」展示给用户（不自动修复）

### 审查模式（`/skill-evo review`）

触发：`$ARGUMENTS` 含 `review` 或 `审查`。可选指定 skill 名（如 `/skill-evo review {prefix}-debug`）。

**步骤 1：确定范围**
- 指定了 skill 名 → 只审查该 skill
- 未指定 → `ls .claude/skills/*/SKILL.md` 审查所有

**步骤 2：并行派发 4 个审查 Agent**（同一条消息启动，subagent_type=general）

| Agent | 维度 | 检查项 |
|-------|------|--------|
| Agent 1 — 结构完整性 | frontmatter 字段（name/description/version/source）、触发词、进化协议章节、层级 ≤4、行数 60-180、semver 格式 |
| Agent 2 — 内容可操作性 | 有路径/命令/示例、无模糊描述（"适当地"/"根据情况"）、表格非占位符、流程步骤清晰 |
| Agent 3 — 一致性 | 跨 skill 术语统一、prefix 格式统一、进化协议格式一致、路径引用格式一致 |
| Agent 4 — 安全性 | 无可执行代码（非示例）、无外部请求指令、无敏感信息收集、无 prompt injection、不修改全局配置 |

每个 Agent 的 prompt 格式：`你是专注 SKILL.md {维度} 的审查员。只输出问题列表，没有问题则输出：NO_ISSUES`，后跟具体检查项和 SKILL.md 内容。

**步骤 3：汇总**——安全问题（Critical）> 结构缺失 > 内容不可操作 > 一致性问题。全部 NO_ISSUES 则直接输出报告。

**步骤 4：逐项修复**——安全问题必须修复；结构和内容按建议修复；一致性以多数 skill 写法为准。

**步骤 5：输出审查报告**

```
📋 Skill 质量审查报告
审查范围：{N} 个 SKILL.md
🔴 安全：{N} 个  🟠 结构：{N} 个  🟡 内容：{N} 个  🔵 一致性：{N} 个
详细发现：{逐条列出}
```

---

## 执行流程

### 感知项目

信息源优先级：**$ARGUMENTS > README > 目录结构 > Git 信息**

从这些信息中理解项目，推断 prefix，向用户展示感知结果并确认。只问无法从项目中推断出的信息。

### 规划 skill 体系

从模板库中选择适合的 skill/command 组合。**根据项目特性裁剪**——不是所有模板都适合所有项目：

- 纯 Skill/文档项目可能不需要 debug
- 项目的核心产品本身是 skill 时，需要创建模板库之外的自定义 skill
- 向用户展示方案，让用户增减

### 构建

SubAgent 并行生成。每个 SubAgent 通过 Read 读取 `${CLAUDE_PLUGIN_ROOT}/templates/` 下的模板文件，结合项目上下文替换占位符。

Skill 类型还需 Read [reference/evolution-protocol.md](reference/evolution-protocol.md)，注入到末尾。

**SubAgent prompt 必须包含的上下文**（保证跨 session 生成质量一致）：
- `prefix`、项目名、技术栈（语言、框架、包管理器）
- 用户在问答阶段提供的回答（如启动命令、端口分配、依赖服务）
- 已有 skill 列表（避免内容重复或冲突）
- 模板文件的完整路径（`${CLAUDE_PLUGIN_ROOT}/templates/{name}.md`）
- 进化协议路径（`${CLAUDE_PLUGIN_ROOT}/reference/evolution-protocol.md`）

### 进化系统基础设施（首次初始化时）

生成 skill 文件之外，还需初始化进化系统。**直接运行安装脚本**：

```bash
bash ${CLAUDE_PLUGIN_ROOT}/evolution/install.sh
```

install.sh 会自动完成以下所有步骤：
1. 创建 `.claude/evolution/{raw,hooks}/` 目录结构
2. 从插件目录复制 `capture.sh` 和 `digest.py` 到 `.claude/evolution/hooks/`
3. 初始化 `session-meta.json` 和 `evolution-digest.md`
4. 将 hook 注册到 `.claude/settings.json`（自动备份原文件）
5. 更新 `.gitignore` 排除 `raw/`、`pending-signals.jsonl`、`session-meta.json`

**前置依赖**：jq、python3（install.sh 会自动检查）。

**禁止手动简化**：capture.sh（~120 行）和 digest.py（~480 行）包含置信度评分、信号聚类、失败-修正链检测等关键逻辑，不要从头重写简化版。

最终目录结构：
```
.claude/evolution/
├── raw/                    # hook 捕获的原始数据（.gitignore）
├── hooks/
│   ├── capture.sh          # Layer 1: 事件捕获（所有 hook 入口）
│   └── digest.py           # Layer 2: 信号提取（SessionEnd 触发）
├── session-meta.json       # 会话元数据（.gitignore）
└── evolution-digest.md     # 进化摘要（Layer 3 的检查点）
```

---

## 模板库

SubAgent 通过 Read 读取对应模板，结合项目上下文生成实际文件。

**Skills**（`.claude/skills/`，注入 [进化协议](reference/evolution-protocol.md)）：

| 模板 | 用途 |
|------|------|
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
