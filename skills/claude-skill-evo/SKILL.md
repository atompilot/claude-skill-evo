---
name: skill-evo
description: >
  交互式锻造项目专属 Claude Code skills。每次执行都会扫描项目现状，
  首次运行初始化完整 skill 体系，后续运行优化完善现有 skills。
  所有生成的 skill 内置自我感知与进化协议。
  触发词：初始化 skills、init skills、创建 skills、项目初始化、setup skills、
  生成 CLAUDE.md、skill-evo、锻造 skill、优化 skill、完善 skill、进化 skill。
version: 3.0.0
source: claude-skill-evo
license: MIT
author: Atompilot
keywords: ["init", "setup", "skills", "project", "scaffold", "CLAUDE.md", "evolution", "self-aware"]
---

# Claude Skill Evo — 锻造会进化的项目 Skill

> 每次执行都会扫描项目现状：首次初始化，后续持续优化。可反复执行，越用越好。

---

## 触发方式

```
/skill-evo                              # 扫描项目，初始化或优化 skills
/skill-evo 补充 API 规范                 # 带提示词，重点关注指定方向
/skill-evo 根据 README 完善 dev skill    # 指定参考内容和优化目标
```

**ARGUMENTS**: $ARGUMENTS

---

## 总体流程

```
Phase 0: 现状感知（判断初始化 vs 优化）
    ↓
Phase 1: 项目探测（自动扫描 + 智能问答）
    ↓
Phase 2: Skill 规划（新建 / 补充 / 更新）
    ↓
Phase 3: 内容共创（引导式问答细化）
    ↓
Phase 4: 生成/更新文件
    ↓
Phase 5: 验证 & 完成
```

---

## Phase 0: 现状感知

**每次执行的第一步**，判断当前项目的 skill 状态：

```bash
# 检查是否已有 skill 体系
ls .claude/CLAUDE.md 2>/dev/null
ls .claude/skills/*/SKILL.md 2>/dev/null
```

根据结果进入不同模式：

| 现状 | 模式 | 行为 |
|------|------|------|
| 无 `.claude/` 目录 | **首次初始化** | 完整走 Phase 1-5，从零创建 |
| 有 CLAUDE.md 但无 skills | **补充模式** | 读取 CLAUDE.md 了解项目，只创建 skills |
| 有 CLAUDE.md 和 skills | **优化模式** | 扫描现有 skills，找出可改进点 |

### 优化模式详细逻辑

进入优化模式时，先做全面扫描：

```bash
# 读取所有现有 skill
cat .claude/skills/*/SKILL.md

# 读取 CLAUDE.md
cat .claude/CLAUDE.md

# 检查 skill 版本
grep -h "^version:" .claude/skills/*/SKILL.md

# 检查是否有 STALE 标记
grep -rl "<!-- STALE:" .claude/skills/ 2>/dev/null

# 检查进化日志
cat .claude/skills/*-skill/evolution.log 2>/dev/null
```

然后结合 $ARGUMENTS（用户的提示词）和扫描结果，判断本次优化方向：

| 用户提示词 | 优化方向 |
|-----------|---------|
| 无（空） | 全面巡检：检查过期内容、缺失 skill、可改进点 |
| "补充 API 规范" | 重点检查/创建 api skill |
| "根据 README 完善" | 读取 README.md，对比 skills 内容，补充缺失信息 |
| "更新 dev 命令" | 重点扫描代码中的实际命令，更新 dev skill |
| "添加测试 skill" | 扫描测试框架，新建 test skill |

**优化模式的输出格式**：

```
📊 Skill 体系巡检报告

现有 skills：
  ✅ {prefix}-dev      v1.0.2  — 健康
  ✅ {prefix}-commit   v1.0.0  — 健康
  ⚠️ {prefix}-bugfix   v1.0.1  — 发现 1 处过期内容
  ✅ {prefix}-api      v1.0.0  — 健康

发现的改进机会：
  1. 🆕 检测到项目使用了 Vitest，但没有 test skill → 建议创建
  2. 🔄 {prefix}-bugfix 中 records/ 路径引用与实际不符 → 建议更新
  3. 📝 README.md 中有启动命令，但 dev skill 中缺少 → 建议补充
  4. 🆕 检测到 docker-compose.yml，但没有 cloud skill → 建议创建

要处理哪些？（输入编号，如 "1,3" / "全部" / "跳过"）
```

---

## Phase 1: 项目探测

### 1.1 自动扫描（每次都做）

**在向用户提问之前**，自动扫描当前项目：

```bash
# 检测项目类型
ls package.json 2>/dev/null          # Node.js / JavaScript / TypeScript
ls requirements.txt pyproject.toml setup.py 2>/dev/null  # Python
ls go.mod 2>/dev/null                # Go
ls Cargo.toml 2>/dev/null            # Rust
ls *.xcodeproj *.xcworkspace Package.swift 2>/dev/null   # Swift/iOS
ls build.gradle* pom.xml 2>/dev/null  # Java/Kotlin
ls Gemfile 2>/dev/null               # Ruby

# 检测框架
grep -l "next\|react\|vue\|angular\|svelte" package.json 2>/dev/null
grep -l "django\|flask\|fastapi\|hono\|express" package.json requirements.txt 2>/dev/null
grep -l "expo" package.json app.json 2>/dev/null

# 检测项目结构
ls -d apps/ packages/ libs/ 2>/dev/null   # monorepo
ls docker-compose* Dockerfile 2>/dev/null  # Docker
ls .github/workflows/ 2>/dev/null          # CI/CD
ls .env .env.example 2>/dev/null           # 环境变量
ls justfile Makefile 2>/dev/null           # 构建工具

# 读取项目文档（重要信息来源）
cat README.md 2>/dev/null | head -100
cat CONTRIBUTING.md 2>/dev/null | head -50

# 检测 Git 信息
git log --oneline -5 2>/dev/null           # 最近提交
git remote -v 2>/dev/null                  # 远程仓库

# 分析代码结构
find . -maxdepth 3 -type d | grep -v node_modules | grep -v .git | grep -v __pycache__ | head -30
```

**如果 $ARGUMENTS 指定了重点内容**（如"根据 README 完善"），额外深度扫描指定内容。

### 1.2 自动推断 prefix

按以下优先级尝试推断，取第一个成功的结果：

| 优先级 | 来源 | 提取方式 |
|-------|------|---------|
| 1 | 已有 skills 的 prefix | 从 `.claude/skills/` 下的目录名提取（优化模式直接复用） |
| 2 | `package.json` 的 `name` 字段 | `jq -r '.name' package.json`，去掉 `@scope/` 前缀 |
| 3 | `go.mod` 的 module 名 | 取最后一段路径 |
| 4 | `Cargo.toml` 的 `[package] name` | 直接读取 |
| 5 | `pyproject.toml` 的 `[project] name` | 直接读取 |
| 6 | `setup.py` / `setup.cfg` 的 name | 正则提取 |
| 7 | `*.xcodeproj` 目录名 | 去掉 `.xcodeproj` 后缀 |
| 8 | `build.gradle*` 的 rootProject.name | 正则提取 |
| 9 | Git remote URL | 从 `origin` URL 提取仓库名 |
| 10 | 当前目录名 | `basename $(pwd)` |

**后处理规则**：
- 转小写
- 空格/下划线/点号 → 连字符
- 去掉 `-app`、`-project`、`-repo` 等无意义后缀
- 如果结果超过 12 个字符，取有意义的缩写（展示给用户确认）

### 1.3 向用户确认 & 补充（引导式问答）

**以下问题分两轮提问，每轮等待用户回答后再继续。**

**优化模式下**：跳过已知信息，只问新增/变化的部分。

#### 第一轮：项目基础

将自动探测结果展示给用户，然后只问缺失的：

```
我扫描了项目目录，以下是我了解到的：

📁 项目类型：[探测结果，如 "TypeScript monorepo"]
🛠️ 框架：[探测结果，如 "Next.js + tRPC"]
📦 包管理器：[探测结果，如 "pnpm"]
🐳 Docker：[有/无]
🔄 CI/CD：[探测结果]
📛 推荐前缀：[推断结果]（来源：[推断来源，如 "package.json name"]）

请确认以上信息是否正确，并回答以下问题：

1. **Skill 前缀**：上面推荐的 `[推断结果]` 可以吗？
   💡 前缀会出现在所有 skill 命令中（如 `/myapp-dev`、`/myapp-commit`），
   建议 3-8 个字符，简短好记。
   （回车确认 / 输入新的前缀）

2. **一句话描述**这个项目是做什么的？
   💡 好的描述能帮我生成更精准的 skill。举几个例子：
   - "SaaS 协作平台，支持实时文档编辑和团队管理"
   - "个人 AI 研究项目，测试各种大模型和工具"
   - "电商后端 API，服务移动端和 Web 前端"
   不用很正式，用你自己的话说就行。

3. **你的角色**？这决定了 skill 的侧重方向：
   a) 全栈 — 前后端都写，skill 会覆盖全链路
   b) 前端 — 侧重组件、状态管理、UI 规范
   c) 后端 — 侧重 API、数据库、部署
   d) ML/AI — 侧重实验、模型训练、数据处理
   e) 其他 — 请描述，我来适配
```

**如果 prefix 推断成功**，问题 1 只需用户回车确认。
**如果 prefix 推断失败**（所有来源都没命中），则展示：

```
📛 前缀：未能自动推断

1. **给你的 skill 起个前缀名**？
   💡 这个前缀会出现在所有命令中，比如你输入 "myapp"，就会生成：
   /myapp-dev（开发）、/myapp-commit（提交）、/myapp-bugfix（修复）
   建议用项目名的缩写，3-8 个字符，全小写。
```

#### 第二轮：开发流程

```
接下来了解一下你的开发流程，帮我生成更贴合实际的 skill：

4. **数据库**（如有）：
   💡 如果项目还没用数据库但计划会用，也可以告诉我，我先生成 db skill 占位。
   [PostgreSQL / MySQL / MongoDB / SQLite / 无 / 计划用但还没决定]

5. **部署方式**：
   💡 如果还没确定也没关系，选"未定"即可，后续再执行 /skill-evo 补充。
   [Vercel / AWS / Fly.io / 自建服务器 / Docker / 未定]

6. **测试框架**（如有）：
   💡 如果目前没有测试但希望建立测试规范，也可以选一个——
   我会帮你生成测试 skill 作为起步指南。
   [Jest / Vitest / pytest / go test / XCTest / 无 / 想建立但还没选]

7. **Git 提交风格**：
   💡 如果你不确定，我推荐 Conventional Commits——它是目前最主流的规范，
   格式是 `feat: 添加用户登录` / `fix: 修复支付bug`，
   好处是能自动生成 changelog、方便 code review。
   a) Conventional Commits（推荐，结构化提交信息）
   b) 自由格式（不限制格式）
   c) 不确定（我帮你选一个合适的）

8. **有没有希望 Claude 帮你规范化的工作流？**
   💡 以下是常见的选择，根据你的项目勾选即可（可多选）：
   a) 📋 代码审查 — 提交前自动检查代码质量、安全、规范
   b) 🔌 API 设计 — 统一接口风格、错误码、认证方式
   c) 🗄️ 数据库迁移 — Schema 变更有流程保障，防止数据丢失
   d) 🧪 测试规范 — 明确测试策略、覆盖率要求
   e) 🔬 技术调研 — 结构化的技术选型评估报告
   f) 📖 参考代码分析 — 阅读开源代码时有系统化的分析流程
   g) 🧫 实验管理 — AI/ML 实验的设计、执行、记录（AI 项目适用）
   h) 其他 — 请描述，我来判断是否适合做成 skill

   不确定的话也没关系，先不选——后面再执行 /skill-evo 时可以补充，
   或者 skill 的进化协议也会在使用中自动发现并提议。
```

### 提问原则

| 原则 | 说明 |
|------|------|
| **给出选项而非开放提问** | 用户面对选项比面对空白更容易回答 |
| **每个选项附带一句话解释** | 帮用户理解选了之后会怎样 |
| **给出推荐和理由** | "不确定"时有明确的默认推荐 |
| **允许"还没想好"** | 明确告诉用户可以下次 /skill-evo 时补充 |
| **用具体例子引导** | 比起抽象描述，例子更能帮用户对号入座 |
| **不追问** | 用户回答"不确定"或跳过时，用合理默认值，不要反复追问 |

---

## Phase 2: Skill 规划

### 2.1 Skill 模板库

根据收集到的项目信息，从以下模板中选择适用的 skill：

#### 通用 Skills（几乎所有项目都需要）

| Skill 模板 | 生成名 | 内容 |
|-----------|--------|------|
| `dev` | `{prefix}-dev` | 本地开发命令、环境配置、端口分配 |
| `commit` | `{prefix}-commit` | Git 提交规范（Conventional Commits） |
| `bugfix` | `{prefix}-bugfix` | 深度 Bug 修复工作流 + 经验记录库 |
| `skill` | `{prefix}-skill` | 元技能，管理所有 skills，含进化引擎 |
| `evolve` | `{prefix}-evolve` | 手动触发进化分析，跨会话积累优化 |
| `digest` | `{prefix}-digest` | 查看进化摘要和进化状态 |

#### 条件 Skills（根据技术栈选择）

| 条件 | Skill 模板 | 内容 |
|------|-----------|------|
| 有后端 API | `api` | API 路由规范、错误处理、认证 |
| 有前端 | `frontend` | 组件规范、状态管理、Design Token |
| 有移动端 | `mobile` | React Native / Swift / Flutter 规范 |
| 有数据库 | `db` | Schema 设计、迁移规范、查询优化 |
| 有 Docker/部署 | `cloud` | 部署流程、环境管理、监控 |
| 有测试框架 | `test` | 测试规范、测试命令 |
| 需要代码审查 | `review` | 代码审查工作流（多 agent 并行审查） |
| 需要技术调研 | `research` | 技术选型评估 + 源码深度分析（含 shallow clone） |
| 有参考代码目录 | `ref` | 参考源码分析工作流（轻量，纯阅读） |
| 有 AI/ML 相关 | `experiment` | 实验设计与执行 |
| 有 Admin 后台 | `admin` | 后台管理开发规范 |
| 有产品设计需求 | `product` | 产品设计文档索引、功能模块管理、设计规范 |
| Monorepo | `migration` | 跨包迁移规范 |

### 2.2 向用户展示规划

#### 首次初始化模式

```
根据你的项目信息，我建议锻造以下 skills：

📂 .claude/skills/
├── {prefix}-skill/SKILL.md    ✅ 元技能（推荐）
├── {prefix}-dev/SKILL.md      ✅ 本地开发（推荐）
├── {prefix}-commit/SKILL.md   ✅ Git 提交（推荐）
├── {prefix}-bugfix/SKILL.md   ✅ Bug 修复（推荐）
├── {prefix}-api/SKILL.md      ✅ API 规范（检测到后端框架）
├── {prefix}-db/SKILL.md       ✅ 数据库规范（检测到数据库）
├── {prefix}-review/SKILL.md   ⚡ 代码审查（你提到了这个需求）
└── {prefix}-test/SKILL.md     ⚡ 测试规范（检测到测试框架）

同时生成：
├── .claude/CLAUDE.md          # 项目级 Claude 指令
└── .gitignore                 # 更新（如果需要）

✅ = 推荐  ⚡ = 可选
🧬 所有 skill 将内置「自我进化协议」

要增加或去掉哪些？确认后开始锻造。
```

#### 优化模式

```
基于巡检结果，本次计划执行以下操作：

🆕 新建：
  1. {prefix}-test/SKILL.md — 检测到 Vitest，建议创建测试规范

🔄 更新：
  2. {prefix}-dev/SKILL.md — README 中有新的启动命令，补充到 dev skill
  3. {prefix}-bugfix/SKILL.md — 修复 records/ 路径引用

📝 完善：
  4. {prefix}-api/SKILL.md — 根据代码中的错误处理模式，充实 API 规范

确认要执行哪些？（编号 / 全部 / 跳过）
```

---

## Phase 3: 内容共创

### 3.1 逐个 Skill 细化（引导式问答）

**不是简单套模板，而是针对每个 skill 询问项目特有规范。**

对每个确认要创建/更新的 skill，快速问 1-2 个关键问题。

**提问策略**：先根据自动探测给出推荐答案，让用户确认或修改。用户越少思考越好。

#### `{prefix}-dev` 要问的：

```
🛠️ 关于本地开发环境：

1. 启动项目的主要命令是什么？
   💡 我检测到你用的是 [包管理器]，常见的启动方式有：
   - `[包管理器] run dev`（开发模式）
   - `[包管理器] run start`（生产模式）
   - `docker compose up`（容器化启动）
   {如果 README 中有启动命令: "我在 README 中看到了 `xxx` 命令，是这个吗？"}
   如果有多个服务需要分别启动，都列出来即可。

2. 有没有需要先启动的依赖服务？
   💡 {如果检测到 docker-compose: "我看到你有 docker-compose.yml，
   里面的服务需要先启动吗？" / 如果没有: "比如本地数据库、Redis、
   消息队列等——如果都不需要，直接跳过"}
```

#### `{prefix}-api` 要问的：

```
🔌 关于 API 规范：

1. 错误处理用什么模式？
   💡 常见做法，看哪个最接近你的情况：
   a) 标准 HTTP 状态码 + JSON body（最常见，如 `{ "error": "Not Found" }`）
   b) 自定义错误码（如 `{ "code": 10001, "message": "用户不存在" }`）
   c) 框架内置（如 tRPC error、FastAPI HTTPException）
   d) 还没统一 — 💡 建议选 (a) 或 (b)，我帮你在 skill 中定好规范
   {如果扫描到代码中的错误处理模式: "我在代码中看到你用的是 [模式]，以此为准吗？"}

2. 认证方案？
   💡 如果还没实现认证，告诉我你**计划用**哪种，我先写进规范：
   a) JWT（前后端分离最常用）
   b) Session/Cookie（传统服务端渲染）
   c) OAuth 第三方登录（Google/GitHub 等）
   d) API Key（面向开发者的 API）
   e) 还没想好 — 💡 我先留个占位，下次 /skill-evo 时再补充
```

#### `{prefix}-db` 要问的：

```
🗄️ 关于数据库：

1. ORM 用的什么？
   💡 根据你的技术栈 [{框架名}]，常见搭配是：
   {TypeScript: "Drizzle（轻量）/ Prisma（全能）/ TypeORM（老牌）"}
   {Python: "SQLAlchemy（最主流）/ Django ORM / Tortoise ORM"}
   {Go: "GORM（最常用）/ Ent / sqlx（偏裸 SQL）"}
   {如果从依赖中检测到: "我在依赖中看到了 [ORM名]，是用这个吗？"}
   如果直接写裸 SQL 也可以，告诉我就行。

2. 迁移方式？
   💡 简单说就是"数据库结构变了怎么更新"：
   a) 自动迁移 — ORM 检测到代码变化自动同步（开发方便，生产慎用）
   b) 手动迁移文件 — 每次写 migration 文件（生产安全，推荐）
   c) push 命令 — 如 `prisma db push`、`drizzle-kit push`（适合早期快速迭代）
   d) 不确定 — 💡 如果项目还在早期，建议先用 (c)，稳定后切 (b)

3. 主键策略？
   💡 简单选择：
   a) 自增 ID — 简单直接，但分布式环境不好用
   b) UUID — 全局唯一，URL 安全，推荐大多数项目
   c) ULID/cuid — 有序 + 全局唯一，性能更好
   d) 不确定 — 💡 新项目建议用 UUID，够用且通用
```

#### `{prefix}-commit` 要问的：

```
📝 关于 Git 提交：

1. 除了标准的 feat/fix/chore，你的项目有没有特殊的 commit type？
   💡 标准类型已覆盖大部分场景：
   feat（新功能）、fix（修复）、chore（杂务）、docs（文档）、
   refactor（重构）、test（测试）、style（格式）、perf（性能）

   一些项目会加自定义类型，比如：
   - AI 项目：`exp:` 表示实验
   - 数据项目：`data:` 表示数据变更
   - 基础设施：`infra:` 表示基础设施变更
   {如果 git log 中检测到特殊 type: "我在 git 历史中看到你用过 `xxx:`，要加进规范吗？"}
   如果没有特殊需求，回车跳过即可。

2. commit message 用中文还是英文？
   💡 两种都可以，看团队习惯：
   - 中文示例：`feat: 添加用户登录功能`
   - 英文示例：`feat: add user login`
   {如果 git log 中能看出: "你最近的提交用的是 [中文/英文]，继续用这个？"}
   如果团队有外国成员或项目会开源，建议英文。
```

#### `{prefix}-review` 要问的：

```
📋 关于代码审查：

1. 有没有项目特有的审查规则？
   💡 举些常见的例子，看哪些适合你的项目（可多选）：
   a) 数据库相关："所有表必须有 created_at 和 updated_at"
   b) 安全相关："禁止硬编码密钥/密码"
   c) 代码风格："组件必须用函数式写法"、"禁止硬编码颜色/字号"
   d) 性能相关："禁止在循环中做数据库查询"
   e) 目前没有 — 💡 没关系，进化协议会在日常审查中逐步积累规则

2. 审查范围？
   a) 仅变更文件 — 速度快，适合日常提交
   b) 变更文件 + 直接关联文件 — 更全面，能发现连锁影响（推荐）
   c) 不确定 — 💡 建议选 (b)，多看一层关联很有价值
```

#### `{prefix}-product` 要问的：

```
📦 关于产品设计文档：

1. 用一句话描述产品的核心定位？
   💡 举例：
   - "面向北美市场的社交+游戏化应用"
   - "B2B SaaS 项目管理工具"
   - "个人健康追踪 iOS 应用"

2. 目前已有哪些功能模块？（列举主要的即可）
   💡 比如：用户认证、内容发布、消息系统、支付……
   如果还在规划阶段，告诉我计划中的模块也行。

3. 产品文档的维护者？
   a) 我自己 — 产品和开发都是我
   b) 有专门的产品经理 — skill 会侧重冲突处理和协作规范
   c) 团队协作 — 多人共同维护
```

#### 其他 skill 的提问同理：给选项、给例子、给推荐、允许跳过。

**核心原则**：
- **尽量从扫描结果中提取答案**，展示给用户确认，而不是让用户从零填写
- **用户回答"不确定"或"没有"时**，使用合理的默认值，不要追问
- **用户回答模糊时**（如"差不多"），根据上下文选最接近的选项，展示选择结果让用户确认
- **用户跳过时**，明确告知"已用默认值，下次 /skill-evo 可以补充"

### 3.2 批量确认

收集完所有答案后，展示即将生成/更新的文件清单：

#### 首次初始化

```
即将锻造以下文件：

1. .claude/CLAUDE.md                       (~120 行)
2. .claude/skills/{prefix}-skill/SKILL.md  (~150 行，含进化引擎)
3. .claude/skills/{prefix}-dev/SKILL.md    (~100 行)
4. .claude/skills/{prefix}-commit/SKILL.md (~60 行)
5. .claude/skills/{prefix}-bugfix/SKILL.md (~150 行，含经验记录库)
6. .claude/skills/{prefix}-api/SKILL.md    (~100 行)
...

是否开始锻造？（Y/直接回车 = 生成全部）
```

#### 优化更新

```
即将执行以下变更：

🆕 新建：
  1. .claude/skills/{prefix}-test/SKILL.md

🔄 更新（仅修改标注的部分，其余不动）：
  2. {prefix}-dev/SKILL.md — 「常用命令速查」章节补充 2 条命令
  3. {prefix}-bugfix/SKILL.md — 修复 records/ 路径

是否执行？（Y/直接回车 = 全部执行）
```

---

## Phase 4: 生成/更新文件

### 4.1 首次初始化的生成顺序

1. **CLAUDE.md**（最先，因为 skills 会引用它）
2. **{prefix}-skill**（元技能，包含目录速查表 + 进化引擎）
3. **{prefix}-evolve + {prefix}-digest**（进化触发 + 进化摘要查看）
4. **其他 skills**（按依赖顺序，每个注入进化协议）
5. **进化系统配置**（hooks + 脚本 + 目录结构）
6. **.gitignore 更新**（追加，不覆盖）

### 4.1.1 进化系统配置（首次初始化时自动执行）

创建进化系统的基础设施：

```bash
# 1. 创建目录结构
mkdir -p .claude/evolution/{raw,hooks}

# 2. 写入 capture.sh（统一 hook 入口）
# 3. 写入 digest.py（SessionEnd 预处理）
# 4. 初始化 session-meta.json
echo '{"total_sessions":0,"last_digest_session":0,"pending_signal_count":0}' \
  > .claude/evolution/session-meta.json

# 5. 初始化空 evolution-digest.md
# 6. 合并 hook 配置到 .claude/settings.json（不覆盖已有 hooks）
```

**Hook 注册**（合并到 `.claude/settings.json`）：

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

**.gitignore 追加**：

```
.claude/evolution/raw/
.claude/evolution/pending-signals.jsonl
.claude/evolution/session-meta.json
reference/
```

### 4.2 优化模式的更新规则

| 操作类型 | 规则 |
|---------|------|
| 新建 skill | 完整创建，注入进化协议 |
| 更新 skill | **只修改需要变化的章节**，保留用户已有的自定义内容 |
| 补充内容 | 在现有章节末尾追加，不改动原有内容 |
| 修复过期 | 替换过期内容，清除 `<!-- STALE: -->` 标记 |

**关键**：优化模式下，绝不全量覆盖已有 skill。用 Edit 工具精确修改。

### 4.3 CLAUDE.md 生成模板

```markdown
# {项目名} 开发规范

## 项目概述

{用户提供的一句话描述}

## 技术栈

| 层 | 技术 |
|----|------|
{根据探测和问答填充}

## Skill 体系

所有 skill 使用 `{prefix}-` 前缀，内置自我进化能力。

| Skill | 场景 |
|-------|------|
{遍历所有已确认的 skills}

## 目录结构

```
{根据探测结果生成}
```

## {根据项目类型生成的规范章节}

{比如 Python 项目生成"Python 开发规范"，TypeScript 项目生成"TypeScript 规范"等}

## 安全规范

{根据项目类型生成，如 API Key 管理、环境变量等}

## Git 提交规范

{如果选了 commit skill，在此放简版引用}
```

### 4.4 Skill 生成规则

每个 Skill 的 SKILL.md 必须包含：

```yaml
---
name: {prefix}-{name}
description: >
  {一句话描述}。
  触发词：{逗号分隔的触发关键词}。
version: 1.0.0
source: claude-skill-evo
---
```

**内容原则**：

| 原则 | 说明 |
|------|------|
| **具体 > 通用** | 填入项目真实的路径、命令、框架名，不用占位符 |
| **精简 > 冗长** | 每个 skill 控制在 60-180 行，核心指令优先 |
| **可操作 > 概念性** | 读完就知道怎么做，避免模糊描述 |
| **有触发词** | description 必须包含多个触发关键词 |
| **有进化协议** | 每个 skill 末尾注入自我进化协议 |

### 4.5 Bugfix Skill 特殊处理

bugfix skill 需要额外创建记录库目录：

```bash
mkdir -p .claude/skills/{prefix}-bugfix/records
```

并生成 `records/template.md`：

```markdown
# Bug 记录：{标题}

**日期**：YYYY-MM-DD
**分类**：{api/frontend/db/infra/common}
**关键词**：{用于预扫描匹配}

## 错误现象

{描述}

## 根本原因

{机制层面的分析}

## 修复方案

### Before

```{lang}
{修复前代码}
```

### After

```{lang}
{修复后代码}
```

## 预防措施

- [ ] {规范约束}
```

---

## ★ 自我进化协议（注入到每个生成的 skill 中）

### 核心理念

> 锻造出的 skill 不是静态文档，而是活的知识体——能感知自身状态，能从经验中学习，能主动提议更新。进化有信心梯度、有体积边界、有安全门控。

每个生成的 skill 末尾必须包含以下「自我进化协议」章节。根据 skill 类型适当调整措辞，但协议结构保持一致。

### 注入模板

以下内容追加到每个生成的 SKILL.md 末尾：

```markdown
---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。以下规则在每次使用时自动生效。

### Auto-Learn（主动学习）

**触发信号**：

| 信号 | 触发条件 | 信心 | 行为 |
|------|---------|------|------|
| 用户纠正 | 用户说"不对"、"应该是..." | 🟠 0.5 | 提议将正确做法写入本 skill |
| 失败-纠正链 | 命令失败后用户纠正 | 🔴 0.8 | 提议写入失败根因 + 正确做法 |
| 重复模式 | 同一操作方式出现 ≥2 次 | 🟡~🔴 0.3~0.8 | 提议写入本 skill 作为规范 |
| 显式指令 | 用户说"记住这个"、"以后都这样做" | ⚫ 0.9 | 直接提议写入本 skill |
| 新发现 | 发现项目中存在但 skill 未记录的规范 | 🟡 0.3 | 标记为试探性，待确认后提升 |
| 命令失败 | 命令执行失败（exit code ≠ 0） | 🟡 0.4 | 检查是否需要更新 dev skill |
| 工具变更 | 检测到项目依赖/工具链发生变化 | 🟠 0.5 | 提议更新相关 skill 内容 |

**信心等级**（决定提议的优先级和措辞强度）：

| 标记 | 范围 | 含义 | 行为 |
|------|------|------|------|
| 🟡 | 0.3-0.4 | 试探性 | 仅记录，不主动提议；积累到 ≥2 次后升级 |
| 🟠 | 0.5-0.6 | 中等信心 | 提议但语气温和："我注意到可能需要..." |
| 🔴 | 0.7-0.8 | 强信心 | 明确提议："建议写入以下规范..." |
| ⚫ | 0.9 | 确定性 | 强烈提议："这是一条确定的规范，建议立即写入" |

**信心变化规则**：
- **升高**：相同模式再次出现 (+0.1)、用户未纠正建议的行为 (+0.05)、跨 session 重复 (+0.15)
- **降低**：用户明确否定 (-0.2)、长期未再观察到 (-0.1/月)、出现矛盾证据 (-0.15)

**确认流程**（不擅自修改）：

```
🔔 [信心: {等级}] 我注意到一个可以写入 skill 的规范：

{描述发现的规范}
{如果是失败-纠正链：附上根因分析}

建议写入：{prefix}-{skill}/SKILL.md 的「{章节名}」
内容预览：
---
{将写入的具体内容}
---

是否写入？(Y/N)
```

**写入质量标准**：
- 新规则必须具体、可操作（有 Before/After 示例）
- 新规则不得与现有规则矛盾（如矛盾，需同时处理）
- 写入后 version 的 patch 号 +1（如 1.0.0 → 1.0.1）
- 每条写入的规则标注信心等级标记

### Stale Detection（过期检测）

**触发信号**：

| 信号 | 判断方式 | 行为 |
|------|---------|------|
| 路径失效 | skill 引用的文件/目录不存在 | 标记并提议更新 |
| 命令失败 | skill 中的命令执行报错 | 标记并提议更新 |
| API 变更 | 框架/库 API 已改名或废弃 | 标记并提议更新 |
| 版本过时 | skill 引用的版本号与实际不符 | 标记并提议更新 |
| 规范冲突 | skill 规范与代码实际做法不一致 | 标记并询问以哪个为准 |

**处理原则**：
- **不要沉默**：发现过期内容必须告知用户，不得默默忽略
- **不要擅改**：提出更新建议，等用户确认后再修改
- **及时标记**：在 skill 文件中用 `<!-- STALE: {原因} -->` 标记过期内容

**过期处理流程**：

```
⚠️ 检测到 skill 内容可能过期：

文件：{prefix}-{skill}/SKILL.md
位置：{章节名}
问题：{具体问题描述}

建议更新为：
---
{新内容}
---

是否更新？(Y/N)
```

### Size Guard（体积守护）

> 防止 skill 文件无限膨胀，保持上下文窗口高效利用。

**守护线**：每个 SKILL.md ≤ 15KB（约 400 行）

**触发压缩的条件**：
- 文件体积 > 12KB → 提前警告
- 文件体积 > 15KB → 写入前必须先压缩

**压缩策略**：
1. 合并相似规则（Before/After 示例保留最典型的 1 个）
2. 低信心 (🟡) 且超过 30 天未被引用的规则 → 移入归档注释 `<!-- ARCHIVED: ... -->`
3. 经验条目超过 20 条时 → 保留 Top 10 高信心 + 将其余压缩为 1 行摘要
4. 移除已被更高信心规则覆盖的旧规则

**压缩流程**：
```
📏 体积守护：{prefix}-{skill}/SKILL.md 当前 {size}KB，超过 12KB 警戒线。
建议压缩以下内容：
1. [🟡 0.3] {规则A} — 30天未引用，建议归档
2. [🟠 0.5] {规则B} 和 {规则C} — 内容相似，建议合并

是否执行压缩？(Y/N)
```

### Session Review（会话回顾）

每次长会话结束前（用户说"好了"、"结束"、"就这样"），主动检查：

1. **本次会话中是否发现了新的项目规范？** → 提议写入相关 skill
2. **本次会话中是否有失败-纠正链值得沉淀？** → 提议写入根因 + 修复方案
3. **本次会话中是否修正了 skill 中的错误？** → 提议更新
4. **本次会话中是否有值得记录的经验？** → 提议写入 bugfix records 或对应 skill

```
📝 会话回顾——我在本次会话中发现了以下可以沉淀的内容：

1. [🔴 新规范] {描述} → 建议写入 {prefix}-{skill}
2. [🔴 失败链] {失败→纠正} → 建议写入根因分析
3. [🟠 经验] {描述} → 建议写入 {prefix}-bugfix/records/

是否写入？逐条确认还是全部写入？
```
```

### 各 Skill 的进化侧重

不同 skill 的进化协议侧重点不同：

| Skill 类型 | Auto-Learn 侧重 | 失败链侧重 | 体积警戒 |
|-----------|----------------|-----------|---------|
| `dev` | 新命令发现、环境变量变更、依赖服务变化 | 构建/启动失败 → 环境修复 | 15KB |
| `commit` | 新的 commit type 涌现、message 风格演变 | hook 失败 → 规范调整 | 10KB |
| `bugfix` | 每次修复自动沉淀记录、更新速查索引 | 修复回退 → 根因分析 | 20KB（含 records） |
| `skill`（元技能） | 新 skill 创建时自动更新目录表、跨 skill 一致性检查 | 进化冲突 → 规则仲裁 | 15KB |
| `api` | 新端点模式、错误码扩展、认证方案变更 | 请求失败 → 接口变更 | 15KB |
| `db` | Schema 变更记录、新的查询模式、迁移经验 | 迁移失败 → 回滚方案 | 15KB |
| `review` | 新的审查规则发现、误报规则剔除 | 审查遗漏 → 规则补充 | 15KB |
| `test` | 新的测试模式、覆盖率变化、断言风格演变 | 测试误报 → 断言修正 | 15KB |
| `research` | 评估维度扩展、新的对比指标 | — | 15KB |

### Evolution System Integration（进化系统集成）

如果项目配置了进化系统（`.claude/evolution/` 目录存在），每个生成的 skill 的进化协议中额外注入以下内容：

```markdown
### Evolution System Integration

本项目已配置跨会话进化系统（v3.1），与 Auto-Learn 协作方式如下：

**分工**：
- **Auto-Learn**：实时的、会话内的即时提议（用户纠正 → 立刻提议写入）
- **进化系统**：跨会话的、积累分析（多次会话的数据 → 批量提议 + 信心评分）

**当收到 `<evolution-trigger>` 注入时**：
1. 不打断用户当前任务
2. 在任务完成后或合适时机读取进化数据
3. 读取 `.claude/evolution/evolution-digest.md`（上次总结 + 元进化记录）
4. 读取 `.claude/evolution/pending-signals.jsonl`（带信心评分的信号）
5. **信心优先**：先处理 ⚫/🔴 高信心信号，🟡 低信心信号标记为 deferred
6. **聚类处理**：相同 cluster_id 的信号一起分析，避免重复提议
7. **体积检查**：写入前检查目标 skill 文件体积，超过 12KB 先触发压缩
8. 对比本 skill 内容，生成进化提议
9. 等待用户确认后写入
10. **元进化**：分析完成后，评估进化过程本身是否有改进空间

**进化分析完成后必须更新**：
- `evolution-digest.md`：写入本次确认的 Patterns / Corrections / Deferred 信号
- `session-meta.json`：更新 `last_digest_session`
- 清除已消费的 pending signals
- 在 `Meta-Evolution` 章节记录进化策略的任何调整

**手动触发**：
- `/{prefix}-evolve` — 立即执行进化分析
- `/{prefix}-digest` — 查看当前进化状态
```

### 进化系统数据流

```
用户日常使用 skills
    ↓ (hooks 自动捕获，零延迟)
raw/ 原始数据（prompt、tool 调用、响应）
    ↓ (SessionEnd 自动预处理 — digest.py)
pending-signals.jsonl
  ├── correction (🟠 0.5)     — 用户纠正
  ├── instruction (⚫ 0.9)    — 显式指令
  ├── chain (🔴 0.8)          — 失败→纠正链（含根因）
  ├── pattern (🟡 0.3~🔴 0.8) — 热文件/高频命令
  └── failure (🟡 0.4)        — 命令失败
  + cluster_id 聚类标识
  + 去重（重复信号 → 信心 +0.1）
    ↓ (积累 ≥5 条 或 ≥3 个会话 → 触发)
Claude 读取 digest + signals
  → 信心优先排序
  → 聚类合并分析
  → 生成进化提议
  → 体积守护检查
    ↓ (用户确认)
写入 skill（带信心标记） + 更新 digest + 元进化记录
    ↓
digest 成为下次分析的起点（增量，不从零开始）
```

---

## Skill 模板详细设计

### 模板：dev

```markdown
---
name: {prefix}-dev
description: >
  {项目名} 本地开发环境规范。{包管理器}命令速查、依赖服务、
  环境变量配置、常用开发命令。
  触发词：本地开发、启动服务、环境配置、环境变量、.env、开发命令。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 本地开发规范

## 常用命令速查

```bash
{用户提供的启动命令}
```

## 依赖服务

{Docker/数据库/Redis 等}

## 环境变量

{从 .env.example 或用户输入提取}

## 目录结构

{从自动探测结果生成}

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新命令发现、环境变量变更、依赖服务变化

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：命令路径变更、环境变量增删、服务端口变化

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：commit

```markdown
---
name: {prefix}-commit
description: >
  {项目名} 代码提交规范。Conventional Commits 格式，{中文/英文}描述。
  触发词：提交代码、git commit、commit、提交、commit message。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 代码提交规范

## Commit 格式

{根据用户选择生成}

## Type 类型

| type | 说明 |
|------|------|
{标准 + 用户自定义 type}

## 示例

{根据项目类型生成具体示例}

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新 commit type 涌现、message 风格演变

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：commit 规范与实际提交不一致

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：bugfix

```markdown
---
name: {prefix}-bugfix
description: >
  {项目名} 深度 Bug 修复工作流。彻底修复，不打补丁，沉淀经验记录。
  触发词：bug、报错、错误、修复、fix、崩溃、{框架特有错误关键词}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 深度 Bug 修复

> 记录库路径：`.claude/skills/{prefix}-bugfix/records/`

## 核心原则

**彻底修复，不打补丁。**

## 第 0 步：预扫描记录库

{标准预扫描流程}

## 第 1 步：深度调查

### 常见 Bug 类型

{根据技术栈定制}

## 第 2 步：修复

{标准修复流程}

## 第 3 步：沉淀

### 记录路径

```
.claude/skills/{prefix}-bugfix/records/
├── {根据项目模块拆分子目录}
```

## 已知 Bug 速查索引

| 关键词 | 分类 | 文件 | 摘要 |
|--------|------|------|------|

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：每次修复自动沉淀记录、更新速查索引

每次 bug 修复完成后，**必须**：
1. 将修复经验写入 `records/` 目录
2. 更新「已知 Bug 速查索引」表
3. 如果发现重复 bug 模式（≥2 次相似问题），提议写入预防规范

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：记录中的代码片段与当前代码不匹配

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：skill (元技能)

```markdown
---
name: {prefix}-skill
description: >
  {项目名} Skill 管理元技能兼进化引擎。发现、检查、新建、更新所有 {prefix}-* skill。
  跨 skill 一致性检查，驱动整个 skill 体系的进化。
  触发词：skill 管理、查看 skill、skill 列表、新建 skill、更新 skill、skill 进化。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} Skill 管理元技能

## 当前 Skill 目录速查

| Skill | 触发场景 | 版本 | 分类 |
|-------|---------|------|------|
{遍历所有已生成的 skills，含版本号}

## 功能一：发现

`ls .claude/skills/ | grep "^{prefix}-"`

## 功能二：健康检查

- 验证每个 skill 的 frontmatter 字段（name, description, version）
- 检查触发词覆盖率（是否有场景没有对应 skill）
- 检查跨 skill 一致性（术语、路径、命令是否统一）
- 检查是否有 `<!-- STALE: -->` 标记未处理

## 功能三：新建

`mkdir -p .claude/skills/{prefix}-<name>` + 填写 SKILL.md（自动注入进化协议）

## 功能四：快速路由

根据任务类型推荐正确的 skill。

## 功能五：进化引擎（元级进化）

作为元技能，负责驱动整个 skill 体系的进化：

### 5.1 跨 Skill 一致性检查

定期（或在 skill 更新时）检查：
- 各 skill 中引用的路径是否一致
- 各 skill 中引用的命令是否一致
- 各 skill 中的术语是否统一

### 5.2 Skill 进化日志

```
.claude/skills/{prefix}-skill/evolution.log
```

记录格式：
```
[YYYY-MM-DD] {prefix}-{skill} v{old} → v{new}: {变更摘要}
```

### 5.3 Skill 体系回顾

当用户触发 `/{prefix}-skill 回顾` 时：
1. 扫描所有 skill 版本号
2. 列出最近变更（从 evolution.log）
3. 检查是否有 STALE 标记
4. 提出整体优化建议

---

## 自我进化协议

> 本 skill 作为元技能，承担进化引擎职责 + 元进化（进化策略本身的进化）。

### Auto-Learn — 侧重：新 skill 创建时更新目录表、检测 skill 间矛盾

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：目录表与实际 skill 不一致、版本号过旧

{标准 Stale Detection 表格 + 处理流程}

### Meta-Evolution（元进化）

> 元技能的独有职责：评估进化策略本身是否需要调整。

每次 Evolve 分析完成后，额外检查：
1. **信心阈值**：当前的信心评分规则是否合理？（噪音太多 → 提高基础信心；好信号被忽略 → 降低阈值）
2. **触发频率**：≥5 信号触发是否合适？（太频繁 → 调高；太稀疏 → 调低）
3. **检测模式**：correction/instruction 的正则是否遗漏了新的表达方式？
4. **体积趋势**：各 skill 的体积增长是否健康？
5. **进化效果**：上次写入的规则是否被用户遵循？（如果没有 → 可能是错误进化）

记录到 `evolution-digest.md` 的 `Meta-Evolution` 章节。

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}

### Session Review

{标准 Session Review 流程}
```

### 模板：evolve

```markdown
---
name: {prefix}-evolve
description: >
  触发 Skill 进化分析。读取跨会话积累的交互信号，对比现有 skill 内容，
  生成进化提议并等待确认。
  触发词：进化、evolve、优化 skill、skill 进化、skill 更新、进化分析。
version: 1.0.0
source: claude-skill-evo
---

# Skill 进化分析

> 读取进化系统积累的信号，分析并提议 skill 更新。

## 执行步骤

1. **读取 checkpoint**：`.claude/evolution/evolution-digest.md`
2. **读取新信号**：`.claude/evolution/pending-signals.jsonl`（带信心评分和聚类标识）
3. **读取统计**：`.claude/evolution/session-meta.json`
4. **信心优先排序**：⚫/🔴 (≥0.7) → 直接提议；🟠 (0.5-0.6) → 温和提议；🟡 (<0.5) → 标记 deferred
5. **聚类合并**：相同 cluster_id 的信号归组分析，避免重复提议
6. **逐个对比**：`.claude/skills/{prefix}-*/SKILL.md`
7. **体积检查**：目标 skill >12KB → 先压缩再写入
8. **生成提议**，等待用户确认
9. 确认后写入 skill（带信心标记）、更新 digest、清空已消化信号
10. **元进化检查**：评估进化策略本身是否需要调整，记录到 digest

## 信号类型

| 类型 | 来源 | 基础信心 | 处理方式 |
|------|------|---------|---------|
| `instruction` | 显式指令（"记住"、"以后都"） | ⚫ 0.9 | 直接提议写入对应 skill |
| `chain` | 失败→纠正链 | 🔴 0.8 | 提议写入根因 + 修复方案 |
| `correction` | 用户纠正（"不对"、"应该是"） | 🟠 0.5 | 提议写入对应 skill |
| `pattern` | 重复操作模式（热点文件、常用命令） | 🟡 0.3+ | ≥2 次或信心≥0.5才提议 |
| `failure` | 命令执行失败 | 🟡 0.4 | 检查是否需要更新 dev skill |

## 提议展示格式

```
🧬 Skill 进化分析（基于最近 {N} 个会话的 {M} 条信号）

📊 信号分布：⚫ {n1} 条 | 🔴 {n2} 条 | 🟠 {n3} 条 | 🟡 {n4} 条（deferred）

📝 建议更新（按信心排序）：
1. {prefix}-{skill} v{old} → v{new} [{信心标记}]
   来源：[S#{session}] {信号描述}
   变更：在「{章节名}」{添加/修改/删除} {内容摘要}
   预览：
   ---
   {将写入的具体内容}
   ---

⏭️ Deferred（🟡 低信心，继续积累）：
N. {描述} — 信心 {score}，再观察 {N} 个会话

📏 体积报告：
- {prefix}-{skill}: {size}KB {✅/⚠️}

逐条确认？全部写入？跳过？
```

**输出示例**：

```
🧬 Skill 进化分析（基于最近 3 个会话的 7 条信号）

📊 信号分布：⚫ 1 条 | 🔴 2 条 | 🟠 2 条 | 🟡 2 条（deferred）

📝 建议更新（按信心排序）：
1. app-dev v1.2.0 → v1.2.1 [⚫ 0.9]
   来源：[S#a3f2] 用户说"以后 API 调用都用 async/await，不用 callback"
   变更：在「网络请求规范」添加 async/await 为默认模式
   预览：
   ---
   ### 网络请求
   - 使用 async/await 模式，不使用 callback
   - 错误处理使用 do-catch
   ---

2. app-bugfix v1.0.0 → v1.0.1 [🔴 0.8]
   来源：[S#b7d1] `pod install` 失败 → 用户纠正"先删 Podfile.lock 再装"
   变更：在「已知 Bug 速查索引」添加 CocoaPods 安装失败修复
   预览：
   ---
   | pod install | 依赖 | pod-install-fix.md | 删除 Podfile.lock 后重新安装 |
   ---

⏭️ Deferred（🟡 低信心，继续积累）：
3. 检测到 SwiftUI Preview 频繁使用 — 信心 0.3，再观察 2 个会话
4. 检测到 git stash 使用 2 次 — 信心 0.4，再观察 1 个会话

📏 体积报告：
- app-dev: 8.2KB ✅
- app-bugfix: 3.1KB ✅
- app-commit: 2.8KB ✅

逐条确认？全部写入？跳过？
```

## 质量控制

| 规则 | 说明 |
|------|------|
| 信心优先 | ⚫/🔴 (≥0.7) 先处理，🟠 (0.5-0.6) 次之，🟡 (<0.5) deferred |
| 证据阈值 | 指令/链：单次即提议。纠正：单次提议。模式：≥2 次或信心≥0.5 |
| 不重复提议 | 对比 digest 的 Confirmed Patterns，已存在的跳过 |
| 矛盾检测 | 新规则与现有 skill 矛盾 → 展示冲突让用户选择 |
| 暂缓机制 | 低信心 → 标记为 Deferred，在 digest 中记录，继续积累 |
| 体积守护 | 写入前检查目标 skill 体积；>12KB 警告，>15KB 先压缩 |
| 元进化 | 分析完成后评估进化策略是否需要调整 |

## 写入后操作

1. 更新 skill 文件（version patch +1，规则标注信心标记）
2. 更新 `evolution-digest.md`：
   - Confirmed Patterns 追加已确认条目（带信心标记）
   - Deferred 追加低信心信号
   - Correction History 追加纠正记录
   - Failure-Correction Chains 追加链式记录
   - Tool Usage Patterns 更新统计
   - Pending Proposals 移除已处理的
   - Evolution Log 追加版本变更
   - Meta-Evolution 记录策略调整（如有）
   - Size Report 更新各 skill 体积
3. 更新 `session-meta.json`（last_digest_session、pending_signal_count）
4. 清空 `pending-signals.jsonl` 中已消化的信号
5. 追加到 `{prefix}-skill/evolution.log`
```

### 模板：digest

```markdown
---
name: {prefix}-digest
description: >
  查看 Skill 进化摘要。展示已确认规范、待处理提议、纠正历史、
  工具使用热点、进化日志。只读操作，不做任何修改。
  触发词：digest、进化摘要、进化记录、skill 状态、进化历史、进化报告。
version: 1.0.0
source: claude-skill-evo
---

# Skill 进化摘要

> 展示进化系统的当前状态，只读不修改。

## 执行步骤

1. 读取 `.claude/evolution/evolution-digest.md`
2. 读取 `.claude/evolution/session-meta.json`
3. 统计 `.claude/evolution/pending-signals.jsonl` 行数
4. 格式化展示

## 输出格式

```
📊 Skill 进化状态

会话总数：{total_sessions}
上次分析：Session #{last_digest_session}（{日期}）
待处理信号：{pending_signal_count} 条
  ⚫ {n1} | 🔴 {n2} | 🟠 {n3} | 🟡 {n4}

📏 体积报告：
  {prefix}-dev: {size}KB {✅/⚠️}
  {prefix}-api: {size}KB {✅/⚠️}
  ...

───────────────────────────────────

{evolution-digest.md 的完整内容，格式化展示}

───────────────────────────────────

💡 执行 /{prefix}-evolve 可触发进化分析
```

## 无进化数据时

```
📊 Skill 进化状态

进化系统已配置，但还没有积累数据。
正常使用 skills 即可——系统会自动在后台捕获交互信号。

积累 ≥5 条信号后，会在 SessionStart 时自动提示进化分析。
也可以随时执行 /{prefix}-evolve 手动触发。
```
```

### 模板：api

```markdown
---
name: {prefix}-api
description: >
  {项目名} API 开发规范。路由结构、类型安全链路、错误处理、认证鉴权、
  分页模式、文件上传、后台任务。
  触发词：API、接口、路由、endpoint、错误处理、认证、分页、{框架名}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} API 开发规范

## 路由结构

{根据框架生成路由组织方式}

### 路由文件组织

```
{根据项目结构生成，如：}
src/
├── routes/        # 路由定义
│   ├── user.ts
│   └── order.ts
├── middleware/    # 中间件
├── validators/   # 请求验证
└── services/     # 业务逻辑
```

## 类型安全链路

{根据技术栈选择}

### TypeScript (tRPC/Hono)
- 从 schema → 路由 → 前端调用全链路类型安全
- 使用 Zod 做运行时验证 + 类型推导

### Python (FastAPI)
- Pydantic model → 路由参数 → 响应模型
- 使用 type hints 全链路类型检查

### Go
- 结构体定义 → handler 参数绑定 → JSON 响应

## 错误处理

### 错误分层

| 层级 | 职责 | 示例 |
|------|------|------|
| 业务错误 | 自定义错误类，带错误码 | `UserNotFound`, `PermissionDenied` |
| 框架错误 | 转换为框架标准格式 | HTTP 状态码 + JSON body |
| 未知错误 | 兜底处理，不暴露内部细节 | 500 + 通用错误信息 |

### 自定义错误类模板

```{lang}
{根据语言生成错误类示例}
```

### 错误码规范

| HTTP 状态码 | 含义 | 使用场景 |
|------------|------|---------|
| 400 | Bad Request | 参数校验失败 |
| 401 | Unauthorized | 未登录 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突（重复创建等） |
| 422 | Unprocessable | 业务逻辑校验失败 |
| 500 | Internal Error | 服务端未知错误 |

## 认证与鉴权

{根据用户选择的认证方案生成}

### 认证中间件

```{lang}
{认证中间件示例}
```

### 权限层级

| 层级 | 说明 |
|------|------|
| 公开 | 无需登录 |
| 已认证 | 需要有效 token |
| 授权 | 需要特定角色/权限 |

## 分页模式

{根据需求选择}

### 游标分页（推荐大数据量）

```{lang}
{游标分页示例}
```

### 偏移分页（简单场景）

```{lang}
{偏移分页示例}
```

## 文件上传

{如有文件上传需求}

## 新增 API 检查清单

- [ ] 路由路径符合 RESTful / RPC 命名规范
- [ ] 请求参数有验证（schema / validator）
- [ ] 错误处理完整（业务错误 + 未知错误）
- [ ] 认证/鉴权中间件已挂载
- [ ] 返回类型有明确定义
- [ ] 必要的日志记录

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新端点模式、错误码扩展、认证方案变更

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：API 路径变更、依赖框架 API 废弃、认证方式迭代

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：frontend

```markdown
---
name: {prefix}-frontend
description: >
  {项目名} 前端开发规范。组件结构、状态管理、Design Token、
  路由导航、UI 模式、新页面检查清单。
  触发词：前端、组件、页面、UI、样式、状态管理、路由、{框架名}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 前端开发规范

## 目录结构

```
{根据框架生成，如：}
src/
├── components/     # 可复用组件
│   ├── ui/         # 基础 UI 组件
│   └── business/   # 业务组件
├── pages/          # 页面组件
├── hooks/          # 自定义 hooks
├── stores/         # 状态管理
├── styles/         # 全局样式/token
├── utils/          # 工具函数
└── types/          # 类型定义
```

## 组件规范

### 命名规则

| 类型 | 命名 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserCard.tsx` |
| hooks | camelCase + use 前缀 | `useAuth.ts` |
| 工具函数 | camelCase | `formatDate.ts` |
| 样式文件 | 同组件名 | `UserCard.module.css` |

### 组件结构模板

```{lang}
{根据框架生成组件模板}
```

## 状态管理

{根据技术栈生成}

### 状态分层

| 层级 | 方案 | 适用场景 |
|------|------|---------|
| 组件内 | useState / ref | 仅当前组件使用 |
| 跨组件 | Context / provide | 父子组件共享 |
| 全局 | {状态库} | 多页面共享 |
| 服务端 | {数据获取库} | API 数据缓存 |

## Design Token

{如有设计系统}

### 颜色

| Token | 值 | 用途 |
|-------|---|------|
| `--color-primary` | {色值} | 主色调 |
| `--color-bg` | {色值} | 背景色 |
| `--color-text` | {色值} | 正文色 |

### 间距

| Token | 值 | 用途 |
|-------|---|------|
| `--space-xs` | 4px | 紧凑间距 |
| `--space-sm` | 8px | 小间距 |
| `--space-md` | 16px | 标准间距 |
| `--space-lg` | 24px | 大间距 |

### 字体

| Token | 大小 | 用途 |
|-------|------|------|
| `--text-xs` | 12px | 辅助信息 |
| `--text-sm` | 14px | 正文 |
| `--text-base` | 16px | 标准正文 |
| `--text-lg` | 18px | 小标题 |

## 路由与导航

{根据框架的路由方案生成}

## UI 模式速查

| 模式 | 组件 | 使用场景 |
|------|------|---------|
| 列表 | List / Table | 数据展示 |
| 表单 | Form | 数据录入 |
| 弹窗 | Modal / Dialog | 确认操作 |
| 加载 | Skeleton / Spinner | 等待数据 |
| 空状态 | Empty | 无数据展示 |
| 错误 | ErrorBoundary | 错误恢复 |

## 新页面检查清单

- [ ] 组件拆分合理（展示 vs 容器）
- [ ] 使用 Design Token，禁止硬编码颜色/字号
- [ ] 响应式适配（如有需求）
- [ ] 加载状态和错误状态处理
- [ ] 无障碍（a11y）基本支持
- [ ] 路由注册

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新组件模式、Design Token 扩展、UI 规范演变

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：组件 API 变更、废弃样式类、路由结构变化

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：mobile

```markdown
---
name: {prefix}-mobile
description: >
  {项目名} 移动端开发规范。目录结构、导航模式、组件规范、
  设计系统 Token、认证状态、文件处理、新页面检查清单。
  触发词：移动端、App、iOS、Android、页面、导航、{框架名}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 移动端开发规范

## 目录结构

```
{根据框架生成，如 React Native：}
app/
├── (tabs)/         # Tab 导航页面
├── (auth)/         # 认证相关页面
├── (modals)/       # 模态页面
└── _layout.tsx     # 根布局
components/
├── ui/             # 基础 UI 组件
└── business/       # 业务组件
hooks/
services/
constants/
```

## 导航规范

### 导航模式

| 模式 | 使用场景 | 呈现方式 |
|------|---------|---------|
| Stack Push | 进入详情 | 从右滑入 |
| Modal | 创建/编辑 | 从底部弹出 |
| Tab Switch | 主要模块切换 | 底部 Tab 栏 |
| Replace | 登录→首页 | 替换当前栈 |

### 导航参数

{根据框架生成导航参数传递方式}

## 组件规范

### 通用 Header

{如项目有统一 Header 组件}

### 列表组件

- 长列表必须使用 FlatList / LazyColumn / UITableView
- 禁止在 ScrollView 中嵌套大量子项
- 分页加载使用 onEndReached / 无限滚动

### 图片组件

- 统一使用 {推荐的图片库}
- 必须设置占位图和错误图
- 远程图片使用缓存策略

## 设计系统 Token

### 颜色（支持暗色模式）

| Token | Light | Dark | 用途 |
|-------|-------|------|------|
| `primary` | {色值} | {色值} | 主色调 |
| `background` | {色值} | {色值} | 背景色 |
| `text` | {色值} | {色值} | 正文色 |

### 间距

| Token | 值 | 用途 |
|-------|---|------|
| `xs` | 4 | 紧凑 |
| `sm` | 8 | 小间距 |
| `md` | 16 | 标准 |
| `lg` | 24 | 大间距 |

## 认证状态

{认证状态管理方式}

## 文件上传

{移动端文件上传流程}

## 新页面检查清单

- [ ] 使用正确的导航呈现模式
- [ ] 使用 Design Token，禁止硬编码
- [ ] 安全区域适配（SafeAreaView / safeAreaInsets）
- [ ] 加载/空/错误状态完整
- [ ] 长列表使用虚拟化组件
- [ ] 图片使用推荐库 + 缓存
- [ ] 返回/关闭按钮正确

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新页面模式、导航变更、设计 Token 扩展

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：导航路径变更、组件 API 废弃、设计 Token 不一致

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：db

```markdown
---
name: {prefix}-db
description: >
  {项目名} 数据库规范。Schema 设计、表结构模式、主键策略、
  索引规范、迁移流程、查询优化。
  触发词：数据库、表、Schema、迁移、migration、SQL、ORM、{ORM名}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 数据库规范

## 技术栈

- 数据库：{数据库类型}
- ORM：{ORM 名称}
- 迁移工具：{迁移工具}

## 通用字段规范

### 主键

{根据用户选择}
- 策略：{UUID / 自增 / ULID}

### 通用时间字段

每张表必须包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `created_at` | timestamp | 创建时间，自动生成 |
| `updated_at` | timestamp | 更新时间，自动更新 |
| `deleted_at` | timestamp? | 软删除标记（如使用软删除） |

### 字段命名

| 规则 | 示例 |
|------|------|
| 使用 snake_case | `user_name`, `created_at` |
| 布尔字段用 is_/has_ 前缀 | `is_active`, `has_verified` |
| 外键用 _id 后缀 | `user_id`, `order_id` |
| JSON 字段明确标注类型 | TypeScript: `$type<T>()` |

## 表结构模式

{根据项目需求选择适用模式}

### 模式 A：1:1 拆分

主表存核心标识，子表存特定领域数据。适用于字段过多需要分组的实体。

### 模式 B：行为/交互记录

记录用户行为、操作日志等。通常只增不改。

### 模式 C：不可变账本

财务流水、积分变动等。只插入，不更新，不删除。

### 模式 D：每日记录

统计快照、日报等按天聚合的数据。

## 索引规范

| 规则 | 说明 |
|------|------|
| 外键必须建索引 | 关联查询性能保障 |
| WHERE 常用字段建索引 | 查询频率高的字段 |
| 组合索引注意顺序 | 高选择性字段在前 |
| 唯一约束用 unique index | 业务唯一性保障 |

## 关系定义

{根据 ORM 生成关系定义方式}

## 迁移规范

### 迁移流程

1. 修改 schema 定义文件
2. 生成迁移文件：`{迁移命令}`
3. 检查生成的 SQL 是否符合预期
4. 执行迁移：`{执行命令}`

### 危险操作检查清单

- [ ] DROP TABLE / DROP COLUMN 前确认数据已备份
- [ ] ALTER TABLE 大表前评估锁表时间
- [ ] 添加 NOT NULL 字段时设置默认值
- [ ] 重命名字段需要确认所有引用已更新

## 查询优化

| 反模式 | 正确做法 |
|--------|---------|
| 循环内查询（N+1） | 使用 JOIN / 预加载 |
| SELECT * | 明确列出需要的字段 |
| 未加 LIMIT | 分页查询加 LIMIT |
| 字符串拼接 SQL | 使用参数化查询 |

## 文件组织

```
{根据 ORM 生成，如：}
src/db/
├── schema/         # 表定义
├── migrations/     # 迁移文件
├── queries/        # 自定义查询
└── seed/           # 种子数据
```

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：Schema 变更记录、新查询模式、迁移经验

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：Schema 定义与实际数据库不匹配、ORM API 变更

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：cloud

```markdown
---
name: {prefix}-cloud
description: >
  {项目名} 云服务与部署规范。部署流程、环境管理、容器配置、
  监控告警、CI/CD、基础设施检查。
  触发词：部署、云服务、Docker、CI/CD、环境、监控、生产环境、{云平台名}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 云服务与部署规范

## 部署架构

| 组件 | 服务 | 说明 |
|------|------|------|
| 应用 | {部署平台} | {说明} |
| 数据库 | {数据库服务} | {说明} |
| 缓存 | {缓存服务} | {说明} |
| 存储 | {对象存储} | {说明} |
| CDN | {CDN 服务} | {说明} |

## 环境管理

| 环境 | 分支 | URL | 用途 |
|------|------|-----|------|
| local | — | localhost | 本地开发 |
| dev | develop | {dev URL} | 开发联调 |
| staging | staging | {staging URL} | 预发验证 |
| prod | main | {prod URL} | 生产环境 |

## Docker 配置

{如使用 Docker}

### docker-compose 规范

```yaml
name: {项目名}-{环境}  # 必须声明 name

services:
  {服务定义}
```

## CI/CD 流程

{根据 CI/CD 工具生成}

### 部署流水线

```
代码推送 → 自动测试 → 构建 → 部署预发 → 验证 → 部署生产
```

## 执行操作前的决策逻辑

| 操作类型 | 影响范围 | 决策 |
|---------|---------|------|
| 读取/查询 | 只读 | 直接执行 |
| 配置变更 | 单个服务 | 确认后执行 |
| 数据变更 | 数据库 | 备份后执行 |
| 删除/重建 | 多个服务 | 详细评估后执行 |

## 基础设施检查清单

- [ ] SSL 证书有效期
- [ ] 数据库备份策略
- [ ] 日志收集和保留策略
- [ ] 监控告警配置
- [ ] 环境变量管理（密钥不硬编码）
- [ ] 水平扩展能力

## 常用运维命令

```bash
{根据部署平台生成常用命令}
```

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新服务上线、配置变更、运维经验沉淀

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：服务 URL 变更、废弃的部署命令、过期的环境配置

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：test

```markdown
---
name: {prefix}-test
description: >
  {项目名} 测试规范。测试策略、测试命令、断言规范、
  Mock 策略、集成测试、覆盖率要求。
  触发词：测试、test、单元测试、集成测试、覆盖率、mock、{测试框架名}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 测试规范

## 测试框架

- 框架：{测试框架}
- 断言库：{断言库}（如不同于框架自带）
- Mock 库：{Mock 库}

## 测试策略

| 层级 | 覆盖范围 | 占比 | 关注点 |
|------|---------|------|--------|
| 单元测试 | 函数/方法 | 70% | 逻辑正确性 |
| 集成测试 | 模块间交互 | 20% | 接口契约 |
| E2E 测试 | 完整流程 | 10% | 用户场景 |

## 常用命令

```bash
{测试运行命令}         # 运行全部测试
{单文件测试命令}       # 运行单个文件
{覆盖率命令}           # 生成覆盖率报告
{监听命令}             # 监听模式
```

## 文件组织

```
{根据项目习惯生成，如：}
src/
├── utils/
│   ├── format.ts
│   └── __tests__/
│       └── format.test.ts
tests/
├── integration/     # 集成测试
├── e2e/             # E2E 测试
└── helpers/         # 测试辅助函数
    └── _helpers.ts  # 共享 helper
```

## 命名规范

| 类型 | 命名规则 | 示例 |
|------|---------|------|
| 测试文件 | `*.test.{ext}` 或 `*.spec.{ext}` | `user.test.ts` |
| 测试描述 | 行为描述，非方法名 | `"应该返回已排序的列表"` |
| 测试变量 | 语义化命名 | `validUser`, `expiredToken` |

## 断言规范

### 优先使用的断言

```{lang}
{根据测试框架生成常用断言示例}
```

### 反模式

| 反模式 | 正确做法 |
|--------|---------|
| 无断言的测试 | 每个 test 至少一个断言 |
| 过于宽泛的断言 | 断言具体的值和结构 |
| 测试间相互依赖 | 每个测试独立运行 |
| 硬编码时间等待 | 使用 await / retry |

## Mock 策略

| 类型 | 何时 Mock | 示例 |
|------|----------|------|
| 外部 API | 始终 Mock | HTTP 请求、第三方 SDK |
| 数据库 | 单元测试 Mock，集成测试用真实 DB | ORM 查询 |
| 时间 | 涉及时间逻辑时 | `Date.now()`, 定时器 |
| 文件系统 | 涉及文件 I/O 时 | 读写文件 |

## API / 集成测试模板

```{lang}
{根据项目框架生成集成测试示例}
```

## 测试数据

{测试数据管理策略}

### 测试账号

{如有测试环境专用账号}

### 测试文件

{如需要测试文件，如上传测试}

```
tests/testfiles/
├── sample.jpg
├── sample.pdf
└── sample.csv
```

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新测试模式、覆盖率变化、断言风格演变

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：测试命令变更、框架 API 废弃、测试 helper 过时

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：review

```markdown
---
name: {prefix}-review
description: >
  {项目名} 代码审查工作流。多维度并行审查、项目规范检查、
  迭代修复循环、审查报告。
  触发词：代码审查、review、code review、CR、审查、检查代码。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 代码审查工作流

## 审查范围

{根据用户选择}
- 审查对象：{变更文件 / 变更+关联文件}
- 获取变更：`git diff --name-only HEAD~1` 或 `git diff --staged --name-only`

## 多维度并行审查

启动 5 个并行审查 Agent，各司其职：

### Agent 1：逻辑与边界

- 空值/null 处理是否完整
- 边界条件（空数组、超长字符串、并发冲突）
- 条件分支是否覆盖所有情况
- 循环终止条件是否正确

### Agent 2：类型安全与错误处理

- 类型转换是否安全（无 `as any`、无隐式转换）
- 错误是否被正确捕获和传播
- 异步操作是否有超时和错误处理
- 资源（连接、文件句柄）是否正确释放

### Agent 3：并发与资源

- 数据竞争风险
- 死锁可能性
- 内存泄漏（未取消的订阅、未清理的定时器）
- 连接池/资源池使用是否正确

### Agent 4：项目规范

{根据项目已有 skill 生成具体检查项}

- 是否遵循 {prefix}-api 中的错误处理规范
- 是否遵循 {prefix}-db 中的 Schema 规范
- 是否遵循 {prefix}-commit 中的提交规范
- 是否遵循 {prefix}-frontend/mobile 中的组件规范

### Agent 5：代码质量与复用

- 是否有可复用的现有工具函数未使用
- 是否有重复代码可以提取
- 命名是否清晰、一致
- 注释是否有价值（非显而易见的逻辑才加注释）

## 审查流程

```
1. 收集变更文件列表
2. 启动 5 个 Agent 并行审查
3. 汇总发现的问题
4. 按严重程度排序
5. 逐一修复或标记为"接受"
6. 修复后再次审查（最多 3 轮）
7. 生成审查报告
```

## 问题分级

| 级别 | 含义 | 处理 |
|------|------|------|
| 🔴 Critical | 会导致 bug / 安全漏洞 | 必须修复 |
| 🟡 Warning | 可能导致问题 / 不符合规范 | 建议修复 |
| 🔵 Info | 优化建议 / 最佳实践 | 可选 |

## 审查报告模板

```
📋 代码审查报告

变更文件：{N} 个
审查轮次：{轮次}/3

🔴 Critical: {N} 个（已全部修复 ✅ / 待修复 ❌）
🟡 Warning: {N} 个（已修复 {M} 个）
🔵 Info: {N} 个

详细发现：
{逐条列出}
```

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新审查规则发现、误报规则剔除

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：项目规范变更导致审查规则过时

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：research

```markdown
---
name: {prefix}-research
description: >
  {项目名} 技术调研工作流。结构化技术选型评估、多源信息收集、
  源码深度分析（shallow clone 到 reference/）、适配性评估、对比报告。
  触发词：技术调研、技术选型、对比、评估、research、选型、方案对比、
  源码分析、参考代码、学习代码。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 技术调研工作流

## 工作流总览

```
Step 1: 明确调研目标
    ↓
Step 2: 多源并行信息收集
    ↓
Step 3: 源码获取与深度阅读（按需）
    ↓
Step 4: 技术栈适配性评估
    ↓
Step 5: 结构化报告
    ↓
Step 6: 行动项整理
```

## Step 1: 明确目标

| 维度 | 需要明确的内容 |
|------|--------------|
| 要解决什么问题 | 具体的技术痛点或业务需求 |
| 评估范围 | 哪些候选方案需要对比 |
| 决策标准 | 优先考虑性能 / 开发效率 / 社区生态 / 成本 |
| 约束条件 | 必须兼容的技术栈、团队规模、时间限制 |
| 是否需要源码分析 | 仅文档级调研 / 需要阅读源码实现 |

## Step 2: 多源并行信息收集

同时从以下渠道获取信息：

| 信息源 | 获取方式 | 关注点 |
|--------|---------|--------|
| 官方文档 | Web 搜索 / Context7 | 功能特性、API 设计、版本路线 |
| npm/PyPI/pkg | 包管理器查看 | 下载量、更新频率、体积 |
| GitHub | 查看仓库 | Stars、Issues 活跃度、最近提交 |
| 社区讨论 | Web 搜索 | 已知问题、迁移经验、性能基准 |
| 项目适配 | 代码扫描 | 与当前技术栈的兼容性 |

## Step 3: 源码获取与深度阅读

> 当调研需要理解实现细节（而非仅看文档/API）时，将候选项目源码 clone 到本地深度阅读。

### 3.1 获取源码

```bash
# 创建 reference 目录（首次）
mkdir -p reference

# shallow clone 到 reference/（节省空间，保留完整目录结构）
git clone --depth 1 {repo_url} reference/{repo_name}

# 如果只需要特定分支/tag
git clone --depth 1 --branch {tag_or_branch} {repo_url} reference/{repo_name}
```

**reference/ 目录规范**：
- 路径：`reference/{repo_name}/`（与项目根目录平级）
- 已在 `.gitignore` 中排除（不提交到本项目仓库）
- 用完后可 `rm -rf reference/{repo_name}` 清理，或保留供后续参考

### 3.2 快速定位核心模块

优先查看：
1. `README.md` — 项目定位和架构概述
2. 入口文件 — main / index / app
3. 目录结构 — 理解模块划分
4. `package.json` / `go.mod` / `Cargo.toml` — 依赖关系

### 3.3 分析维度

根据调研目的选择维度：

| 维度 | 关注点 | 适用场景 |
|------|--------|---------|
| 架构设计 | 模块划分、依赖关系、设计模式 | 学习整体架构 |
| 核心功能实现 | 关键算法、数据流、状态管理 | 理解特定功能如何实现 |
| 工程实践 | 测试策略、CI/CD、错误处理、日志 | 学习工程规范 |
| API 设计 | 接口风格、版本管理、文档 | 设计 API 参考 |
| 性能优化 | 缓存策略、并发模型、数据结构选择 | 性能优化参考 |

### 3.4 分析深度指引

| 项目规模 | 建议深度 |
|---------|---------|
| < 1000 行 | 完整阅读 |
| 1000-10000 行 | 核心模块深读 + 周边模块浏览 |
| > 10000 行 | 目标模块精读 + 架构概览 |

### 3.5 源码分析记录

每个分析的项目输出简要记录（可写入调研报告的附录）：

```markdown
### 源码分析：{repo_name}

- 仓库：{URL}
- 本地路径：`reference/{repo_name}/`
- 技术栈：{语言/框架}
- 核心模块：{列出 2-3 个关键目录/文件}

**亮点**：
- {值得学习的设计 1}
- {值得学习的设计 2}

**局限**：
- {不适合直接照搬的地方}

**可借鉴点**：
| 模式/设计 | 适配难度 | 建议 |
|-----------|---------|------|
| {具体模式} | 低/中/高 | {如何应用到本项目} |
```

## Step 4: 适配性评估

### 评估维度

| 维度 | 权重 | 评估方法 |
|------|------|---------|
| 功能匹配度 | 高 | 需求 vs 特性对比 |
| 技术栈兼容性 | 高 | 与 {技术栈} 的集成难度 |
| 学习成本 | 中 | API 复杂度、文档质量 |
| 社区生态 | 中 | Stars、维护者活跃度、插件丰富度 |
| 代码质量 | 中 | 源码阅读后的实现质量评估（Step 3 提供） |
| 性能 | 按需 | 基准测试、官方数据 |
| 体积 | 按需 | bundle size、依赖数量 |

## Step 5: 结构化报告

### 报告模板

```markdown
# 技术调研报告：{调研主题}

## 背景

{为什么需要这次调研}

## 候选方案

| 方案 | 简介 | Stars | 更新频率 |
|------|------|-------|---------|
| A | ... | ... | ... |
| B | ... | ... | ... |
| C | ... | ... | ... |

## 对比矩阵

| 维度 | 方案 A | 方案 B | 方案 C |
|------|--------|--------|--------|
| 功能匹配 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| 兼容性 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 学习成本 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 社区生态 | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| 代码质量 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

## 源码分析（如有）

{Step 3.5 的源码分析记录}

## 推荐

**推荐方案 {X}**

理由：{1-3 句话说明}

## 注意事项

{已知风险、迁移成本、需要关注的 breaking changes}
```

## Step 6: 行动项

- [ ] {具体的下一步行动}
- [ ] 清理不再需要的 `reference/` 源码（或保留供后续参考）
- [ ] 更新 TODO.md（如有）

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：评估维度扩展、新的对比指标、源码分析模式优化

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：推荐方案已过时、reference/ 中的源码版本过旧

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：ref

```markdown
---
name: {prefix}-ref
description: >
  {项目名} 参考源码分析工作流。系统化阅读开源代码，提取可借鉴的模式、
  架构设计、最佳实践，输出结构化分析报告。
  触发词：参考代码、源码分析、开源项目、学习代码、ref、分析代码。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 参考源码分析工作流

## 分析流程

```
1. 获取源码（shallow clone / 在线浏览）
2. 快速定位核心模块
3. 按维度分析
4. 输出结构化报告
5. 提取可借鉴点
```

## Step 1: 获取源码

```bash
# shallow clone（节省空间和时间）
git clone --depth 1 {repo_url} /tmp/{repo_name}
```

## Step 2: 快速定位

优先查看：
1. README.md — 项目定位和架构概述
2. 入口文件 — main/index/app
3. 目录结构 — 理解模块划分
4. package.json / go.mod / Cargo.toml — 依赖关系

## Step 3: 分析维度

根据分析目的选择维度：

| 维度 | 关注点 | 适用场景 |
|------|--------|---------|
| 架构设计 | 模块划分、依赖关系、设计模式 | 学习整体架构 |
| 核心功能实现 | 关键算法、数据流、状态管理 | 理解特定功能 |
| 工程实践 | 测试策略、CI/CD、错误处理、日志 | 学习工程规范 |
| API 设计 | 接口风格、版本管理、文档 | 设计 API 参考 |
| 性能优化 | 缓存策略、并发模型、数据结构 | 性能优化参考 |

### 分析深度指引

| 项目规模 | 建议深度 |
|---------|---------|
| < 1000 行 | 完整阅读 |
| 1000-10000 行 | 核心模块深读 + 周边模块浏览 |
| > 10000 行 | 目标模块精读 + 架构概览 |

## Step 4: 分析报告模板

```markdown
# 参考分析报告：{项目名}

## 项目定位

- 仓库：{URL}
- 定位：{一句话描述}
- 技术栈：{语言/框架}
- Stars：{数量}

## 架构概述

{目录结构 + 模块关系图}

## 核心功能分析

### {功能 1}

- 实现方式：{描述}
- 亮点：{值得学习的设计}
- 局限：{不适合直接照搬的地方}

## 与本项目的关联

| 可借鉴点 | 适配难度 | 建议 |
|---------|---------|------|
| {模式/设计} | 低/中/高 | {具体建议} |

## 集成可行性

{如果是考虑集成的库，评估集成难度和风险}
```

## Step 5: 提取可借鉴点

分析完成后，将可借鉴的模式整理为可操作的建议，必要时同步到相关 skill。

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新的分析维度、更好的报告结构

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：参考项目已归档/重大重构

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：experiment

```markdown
---
name: {prefix}-experiment
description: >
  {项目名} 实验管理规范。实验设计、执行记录、结果分析、
  对照实验、参数追踪、结论归档。
  触发词：实验、experiment、测试模型、对比实验、A/B测试、调参、{领域关键词}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 实验管理规范

## 实验工作流

```
1. 实验设计（假设 + 指标 + 方案）
2. 环境准备（数据 + 配置 + 基线）
3. 执行实验（记录所有参数和中间结果）
4. 结果分析（对比基线 + 统计显著性）
5. 结论归档（写入实验记录）
```

## 实验设计模板

| 字段 | 内容 |
|------|------|
| 实验名称 | {描述性名称} |
| 日期 | YYYY-MM-DD |
| 假设 | {要验证的假设} |
| 自变量 | {改变什么} |
| 因变量 | {测量什么} |
| 控制变量 | {保持不变的} |
| 成功标准 | {达到什么指标算成功} |

## 实验记录模板

```markdown
# 实验记录：{实验名称}

## 基本信息

- 日期：{YYYY-MM-DD}
- 目标：{一句话描述}
- 状态：{进行中 / 完成 / 中止}

## 实验设计

### 假设
{要验证的假设}

### 方案
{具体的实验步骤}

### 基线
{对照基准}

## 参数配置

| 参数 | 值 | 说明 |
|------|---|------|
{列出所有关键参数}

## 执行过程

{按时间顺序记录关键节点}

## 结果

### 定量结果

| 指标 | 基线 | 实验值 | 变化 |
|------|------|--------|------|
{对比数据}

### 定性观察

{非量化的观察发现}

## 结论

{结论 + 下一步}

## 经验教训

{可复用的经验}
```

## 实验目录结构

```
{根据项目类型生成，如：}
experiments/
├── {YYYY-MM}/
│   ├── {实验名}/
│   │   ├── config.yaml     # 参数配置
│   │   ├── results/        # 结果数据
│   │   └── README.md       # 实验记录
│   └── ...
└── _templates/             # 实验模板
```

## 实验命名规范

格式：`{YYYY-MM-DD}-{简短描述}`

示例：`2024-03-15-gpt4-vs-claude-summarization`

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新的实验模式、评估指标扩展、工具链变化

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：实验工具/API 变更、指标计算方式过时

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：admin

```markdown
---
name: {prefix}-admin
description: >
  {项目名} 后台管理开发规范。路由结构、权限管理、
  通用 UI 模式、数据表格、表单、{框架名}规范。
  触发词：后台、管理后台、admin、管理端、运营后台、{框架名}。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 后台管理开发规范

## 技术栈

- 框架：{前端框架}
- UI 库：{UI 组件库}
- 路由：{路由方案}
- API 调用：{API 客户端}

## 目录结构

```
{根据框架生成，如：}
src/
├── pages/           # 页面组件
│   ├── dashboard/
│   ├── users/
│   └── orders/
├── components/      # 通用组件
├── layouts/         # 布局组件
├── services/        # API 调用
└── utils/           # 工具函数
```

## 路由规范

{根据框架生成路由定义方式}

### 路由结构

| 路径 | 页面 | 权限 |
|------|------|------|
| `/dashboard` | 仪表板 | 所有角色 |
| `/users` | 用户管理 | 管理员 |
| `/settings` | 系统设置 | 超级管理员 |

## 权限管理

### 角色定义

| 角色 | 权限范围 |
|------|---------|
| 超级管理员 | 全部功能 |
| 管理员 | 除系统设置外 |
| 运营 | 内容管理、数据查看 |
| 只读 | 仅查看 |

### 权限控制方式

{根据项目实际情况生成}

## 通用 UI 模式

### 数据表格页

```
┌─────────────────────────────────────┐
│ 页面标题                    [新增] [导出] │
├─────────────────────────────────────┤
│ 搜索栏：[关键词] [状态▼] [日期范围] [搜索] │
├─────────────────────────────────────┤
│ 表格                                │
│ □ | ID | 名称 | 状态 | 操作          │
│ □ | 1  | ...  | ...  | [编辑][删除]  │
├─────────────────────────────────────┤
│ 共 {N} 条  [<] 1 2 3 [>]            │
└─────────────────────────────────────┘
```

### 表单页

```
┌─────────────────────────────────────┐
│ 新增/编辑 {实体}                      │
├─────────────────────────────────────┤
│ 字段名：[输入框]                      │
│ 字段名：[下拉选择]                    │
│ 字段名：[日期选择]                    │
├─────────────────────────────────────┤
│               [取消] [保存]           │
└─────────────────────────────────────┘
```

### 详情页

```
┌─────────────────────────────────────┐
│ {实体} 详情               [编辑] [删除] │
├─────────────────────────────────────┤
│ 基本信息    操作记录    关联数据        │
│ ─────────────────────────           │
│ {Tab 内容}                          │
└─────────────────────────────────────┘
```

## 界面语言

{根据用户回答：中文 / 英文 / 多语言}

## 新页面检查清单

- [ ] 路由已注册
- [ ] 权限检查已配置
- [ ] 表格支持搜索、分页、排序
- [ ] 表单有验证
- [ ] 删除操作有二次确认
- [ ] 加载/空/错误状态完整

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新的 UI 模式、权限角色扩展、通用组件发现

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：路由结构变更、UI 组件库 API 变更、权限模型变化

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：migration

```markdown
---
name: {prefix}-migration
description: >
  {项目名} 迁移工作流。架构变更映射、数据迁移、API 迁移、
  渐进式迁移策略、回滚方案、验证检查清单。
  触发词：迁移、migration、架构变更、重构、升级、从...迁移到...。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 迁移工作流

## 迁移类型

| 类型 | 说明 | 风险等级 |
|------|------|---------|
| API 迁移 | 路由/接口从旧版迁移到新版 | 中 |
| 数据迁移 | 数据库 Schema 变更、数据转换 | 高 |
| 框架迁移 | 更换框架或框架大版本升级 | 高 |
| 架构迁移 | 单体→微服务、模块重组 | 极高 |
| 依赖迁移 | 替换第三方库 | 低-中 |

## 迁移工作流

```
1. 变更映射（旧 → 新的对应关系）
2. 影响评估（涉及的文件、依赖、下游）
3. 迁移计划（分步骤、可回滚）
4. 执行迁移（按计划逐步推进）
5. 验证（每步验证正确性）
6. 清理（删除旧代码、更新文档）
```

## Step 1: 变更映射

### 映射表模板

| 旧 | 新 | 状态 | 备注 |
|----|---|----|------|
| `旧路径/旧API` | `新路径/新API` | 待迁移/已迁移/已验证 | {说明} |

## Step 2: 影响评估

```bash
# 查找所有引用旧模块的文件
grep -r "旧模块名" --include="*.{ext}" -l

# 查找所有导入旧模块的文件
grep -r "import.*旧模块名" --include="*.{ext}" -l
```

### 影响范围

| 影响类型 | 文件数 | 风险 |
|---------|--------|------|
| 直接引用 | {N} | {高/中/低} |
| 间接依赖 | {N} | {高/中/低} |
| 测试文件 | {N} | 低 |
| 文档 | {N} | 低 |

## Step 3: 迁移策略

### 渐进式迁移（推荐）

```
Phase 1: 新旧并存（adapter/facade 模式）
Phase 2: 新代码使用新模块，旧代码保持不变
Phase 3: 逐步迁移旧代码到新模块
Phase 4: 移除旧代码和 adapter
```

### 大爆炸迁移（仅小规模变更）

```
1. 在分支上一次性完成所有变更
2. 全面测试
3. 一次性合并
```

## Step 4: 执行

### 决策确认机制

每一步执行前，展示变更预览：

```
📋 即将执行迁移步骤 {N}/{总步数}：

变更：{描述}
影响文件：{N} 个
不可逆操作：{有/无}

确认执行？(Y/N)
```

## Step 5: 验证检查清单

- [ ] 所有旧引用已更新
- [ ] 编译/构建通过
- [ ] 单元测试全部通过
- [ ] 集成测试通过
- [ ] 手动冒烟测试通过
- [ ] 性能无明显退化
- [ ] 无废弃代码残留

## 回滚方案

| 场景 | 回滚方式 |
|------|---------|
| 数据迁移失败 | 从备份恢复 |
| API 迁移失败 | 切回旧路由 |
| 依赖迁移失败 | 回退版本号 |
| 架构迁移失败 | git revert + 数据恢复 |

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：新的迁移模式、回滚经验、验证步骤完善

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：旧系统映射关系过时、迁移工具变更

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}
```

### 模板：product

```markdown
---
name: {prefix}-product
description: >
  {项目名} 产品设计文档索引。功能模块目录、设计规范、冲突处理、模糊意图处理。
  触发词：产品设计、功能设计、用户流程、业务逻辑、怎么做、该怎么设计。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 产品设计 Skill

> **子文档索引**
> - 功能模块：`.claude/skills/{prefix}-product/features/`

---

## 文档范围规范（必须遵守）

**{prefix}-product 是产品设计文档，不是技术文档。**

### 应该包含的内容

| 类型 | 示例 |
|------|------|
| 功能描述 | 用户可以执行哪些操作 |
| 业务规则 | 各功能的约束和限制条件 |
| 用户流程 | 操作的步骤顺序 |
| 交互逻辑 | 操作后的反馈和状态变化 |
| 可见性/权限规则 | 不同角色/状态下的功能可见性 |
| 数据的**语义描述** | 实体包含什么信息（不涉及数据库设计） |

### 禁止出现的内容

| 类型 | 示例 |
|------|------|
| ❌ 数据库表结构 | 字段列表、索引定义、外键关系 |
| ❌ 代码片段 | 类型定义、SQL、API 请求格式 |
| ❌ 技术实现细节 | 缓存策略、队列实现、第三方 SDK 用法 |
| ❌ 字段类型和约束 | `UUID`、`text`、`int`、`NOT NULL` |

**判断方法**：这条内容是"产品要做什么"，还是"开发者怎么实现"？后者不属于本 skill。

---

## Skill 维护规则（重要）

**每次产品功能发生变更时，必须同步更新本 skill：**

| 变更类型 | 需要更新的文件 |
|---------|-------------|
| 新增功能模块 | 在 `features/` 下新建对应文件，并在本文件目录中登记 |
| 修改现有功能逻辑 | 直接更新对应的 `features/<module>.md` |
| 新增/修改用户流程 | 在对应 `features/<module>.md` 中添加「完整流程」章节 |
| 调整核心产品定位 | 更新本文件「产品概述」部分 |
| 版本迭代 | 更新本文件 `version` 字段 |

**触发更新的时机**：
- 用户说"我们要加一个功能……"→ 设计完成后写入对应 features 文件
- 用户说"这个功能改成……"→ 修改对应 features 文件
- 代码与文档冲突，且用户明确指定方向 → 按指定执行
- 代码与文档冲突，用户未明确指定 → **先向用户确认**

---

## 产品概述

| 维度 | 定义 |
|------|------|
| 产品定位 | {产品定位} |
| 目标用户 | {目标用户} |
| 差异化 | {差异化} |
| 平台 | {平台} |

---

## 功能模块目录

| 模块 | 文件 | 状态 | 说明 |
|------|------|------|------|
| {模块名} | `features/{module}.md` | 📝 规划中 | {一句话说明} |

> 随产品发展逐步增加。每新增一个功能模块，在此表中登记并在 `features/` 下创建对应文件。

---

## 通用产品原则

### 交互设计原则

{根据产品定位填写，以下为示例：}

1. **低门槛参与**：核心功能 3 步以内可完成
2. **即时反馈**：操作后必须有视觉反馈
3. **一致性**：相同类型的操作使用相同的交互模式

### 数据与隐私

- 用户可控：用户对自己的内容有完整控制权
- 最小采集：只采集业务必需的数据

---

## 代码与设计文档冲突处理（必须遵守）

在检查代码时，若发现**现有代码实现与产品设计文档存在冲突**：

### 判断流程

```
发现代码与文档冲突
        ↓
用户是否在本次对话中明确指定了方向？
        ↓
   是 → 按用户指定执行（修改代码 or 更新文档）
   否 → 停下来，向用户确认
```

### 向用户确认的格式

```
发现代码与设计文档存在冲突，需要确认以哪个为准：

**冲突描述**：
- 设计文档（features/xxx.md）：[描述文档中的设计]
- 现有代码（path/to/file:行号）：[描述代码中的实现]

请确认：
A. 以设计文档为准 → 修改代码
B. 以代码为准 → 更新设计文档
C. 两者都需调整 → 说明新的期望行为
```

### 明确指定的识别规则

| 用户说的 | 视为 |
|---------|------|
| "按文档实现"、"文档说的是对的" | 以文档为准，修改代码 |
| "代码没问题"、"文档写错了" | 以代码为准，更新文档 |
| "帮我把代码改成……" | 修改代码（同时更新文档） |
| "文档里改成……" | 更新文档 |

### 禁止行为

- ❌ 发现冲突后默默选一个方向执行，不告知用户
- ❌ 仅凭"代码已实现"就断定代码优先
- ❌ 仅凭"文档更权威"就断定文档优先

---

## 模糊意图处理规范（必须遵守）

产品设计中的模糊和歧义是常态。**不得自行假设、脑补或凭直觉决定**。

### 何时必须提问

| 情况 | 示例 | 必须确认的问题 |
|------|------|--------------|
| 功能边界不清 | "加一个分享功能" | 分享到哪里？分享什么内容？ |
| 业务规则缺失 | "要有时间限制" | 限制多长时间？到期怎么处理？ |
| 权限逻辑不明 | "管理员可以管理" | 管理包含哪些操作？ |
| 状态/流程有分叉 | "用户取消操作" | 取消后如何恢复？数据如何处理？ |
| 与已有设计有冲突 | 新需求与已记录设计矛盾 | 指出冲突，确认以哪个为准 |

### 提问原则

1. **集中提问**：所有不清楚的点一次性列出
2. **给出选项**：提供 2-3 个候选方案，而非开放性问题
3. **标注影响**：说明不同选择会带来什么后果
4. **区分优先级**：先问核心逻辑，次要细节可暂时搁置

### 禁止行为

- ❌ 凭经验/直觉假设产品逻辑
- ❌ 用"通常来说"、"一般会"等模糊措辞蒙混过关
- ❌ 把多个不确定点拆成多轮对话逐个问

---

## 产品设计问题检查规范（必须遵守）

当用户要求检查产品设计是否有问题时：

### 问题定位要求

每个问题**必须**标注原文所在位置：

```
**问题描述**
位置：`features/xxx.md` > 章节名 > 具体条目
原文：「……」
```

### TODO / 待补充内容的处理

**除非用户明确要求检查 TODO**，否则：
- 标记为「待填写」「待补充」的内容**不作为问题点**列出
- 仅检查**已明确描述的内容**是否存在逻辑漏洞、自相矛盾

### 检查范围

| 检查点 | 说明 |
|--------|------|
| 内容自相矛盾 | 同一文件或跨文件的两处描述互相冲突 |
| 逻辑漏洞 | 某个操作/流程缺少必要的边界情况 |
| 描述不完整 | 某个已描述的功能缺少关键规则 |
| 跨文档不一致 | A 文件引用 B 文件，但两者描述对不上 |

---

## 如何使用本 Skill

1. **查找功能设计**：先看「功能模块目录」，找到对应 `features/xxx.md` 阅读
2. **新功能讨论**：参考产品原则，列出不确定点提问确认，设计完成后写入对应子文件
3. **子文件不存在**：说明该功能尚未设计，通过提问明确方案后再创建文件
4. **跨模块用户流程**：在主要 feature 文档里添加「完整流程」章节

---

## 自我进化协议

> 本 skill 具备自我感知与进化能力。

### Auto-Learn — 侧重：功能模块增删、设计原则演变、冲突处理经验

{标准 Auto-Learn 表格（含信心等级）+ 确认流程}

### Stale Detection — 侧重：功能模块目录与实际 features/ 文件不一致、产品定位变化

{标准 Stale Detection 表格 + 处理流程}

### Size Guard — ≤ 15KB 守护

{标准 Size Guard 压缩策略}

> **注意**：本 skill 主文件保持索引角色，功能细节分散到 `features/` 子文件中。
> 当主文件接近体积上限时，优先将内容拆分到子文件，而非删减。
```

---

## Phase 5: 验证 & 完成

### 5.1 生成后检查

```bash
# 验证所有 skill 文件存在
ls .claude/skills/{prefix}-*/SKILL.md

# 验证 CLAUDE.md 存在
ls .claude/CLAUDE.md

# 验证 frontmatter 格式
grep -h "^name:\|^version:" .claude/skills/{prefix}-*/SKILL.md

# 验证进化协议注入（含信心等级 + 体积守护）
grep -l "自我进化协议" .claude/skills/{prefix}-*/SKILL.md
grep -l "Size Guard" .claude/skills/{prefix}-*/SKILL.md
grep -l "信心" .claude/skills/{prefix}-*/SKILL.md
```

### 5.2 完成报告

#### 首次初始化

```
✅ Skills 锻造完成！

已生成：
📄 .claude/CLAUDE.md
📂 .claude/skills/{prefix}-skill/SKILL.md    — 元技能（含进化引擎）
📂 .claude/skills/{prefix}-dev/SKILL.md      — 本地开发
📂 .claude/skills/{prefix}-commit/SKILL.md   — Git 提交
📂 .claude/skills/{prefix}-bugfix/SKILL.md   — Bug 修复（含记录库）
📂 .claude/skills/{prefix}-api/SKILL.md      — API 规范
...

🧬 所有 skill 已注入「自我进化协议 v3.1」（信心评分 + 体积守护 + 元进化）

使用方式：
  /{prefix}-dev         查看本地开发命令
  /{prefix}-commit      提交代码
  /{prefix}-bugfix      修复 bug
  /{prefix}-skill       管理/进化所有 skills

💡 随时可以再次执行 /skill-evo 来优化和完善 skills。
```

#### 优化更新

```
✅ Skills 优化完成！

本次变更：
🆕 新建 1 个 skill：{prefix}-test
🔄 更新 2 个 skill：{prefix}-dev、{prefix}-bugfix
📝 version 变更：{prefix}-dev v1.0.0 → v1.0.1

💡 随时可以再次执行 /skill-evo 继续优化。
```

---

## 注意事项

### 多次执行安全

- **首次初始化**：如果 `.claude/CLAUDE.md` 已存在，**询问用户**是合并还是覆盖
- **优化模式**：只精确修改需要变化的部分，绝不全量覆盖
- **版本追踪**：每次更新自动递增 version patch 号，并记录到 evolution.log

### 保持精简

- 初始化生成的 skill 应为**起步版本**（v1.0.0）
- 内容宁少勿多，通过多次 /skill-evo 和进化协议逐步丰富
- 每个 skill 控制在 60-180 行，避免信息过载

### 文件安全

- 生成前先读取目标路径，确认不覆盖重要内容
- `.gitignore` 只追加不覆盖
- 不修改 `~/.claude.json` 或 `~/.claude/settings.json`

### 适配性

- 不假设特定的技术栈——skill 内容完全由扫描结果和问答驱动
- 对于不确定的答案，使用保守的默认值
- 用户说"不需要"的功能，不要强行添加

### 进化协议一致性

- 每个生成的 skill 必须包含「自我进化协议」章节
- 协议结构统一：Auto-Learn（含信心等级）+ Stale Detection + Size Guard
- 侧重点根据 skill 类型调整（参考进化侧重表）
- 元技能（{prefix}-skill）额外承担进化引擎 + 元进化职责
- 信心标记 (🟡/🟠/🔴/⚫) 贯穿所有进化产出物
