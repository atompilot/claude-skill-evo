# Todo Skill 实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `skills/claude-skill-evo/SKILL.md` 中新增 `{prefix}-todo` 通用 skill 模板，使 claude-skill-evo 生成的项目具备项目级待办任务管理能力。

**Architecture:** 只修改一个文件（SKILL.md），在 4 个位置插入内容：模板库表格、目录树展示、Phase 3 提问、模板详细设计。会话级 TODO 沿用 Claude Code 内置 TodoWrite，项目级 TODO 持久化到 `.claude/knowledge/todo.md`。

**Tech Stack:** Markdown（SKILL.md 模板），无代码依赖

---

## Chunk 1: 模板库 + 目录树 + Phase 3 提问

**文件：**
- Modify: `skills/claude-skill-evo/SKILL.md`（三处小修改）

### Task 1: 在 Skill 模板库表格中新增 todo 行

当前第 297 行：
```
| `research` | `{prefix}-research` | 技术选型评估 + 源码深度分析（含 shallow clone） |
```

- [ ] **Step 1.1：在该行后追加 todo 行**

  在 `research` 行下方插入：
  ```
  | `todo` | `{prefix}-todo` | 项目级待办管理，持久化到 `.claude/knowledge/todo.md` |
  ```

- [ ] **Step 1.2：在「首次初始化模式」目录树中新增 todo**

  当前第 313 行：
  ```
  └── {prefix}-research/SKILL.md ✅ 技术调研
  ```

  改为：
  ```
  ├── {prefix}-research/SKILL.md ✅ 技术调研
  └── {prefix}-todo/SKILL.md     ✅ 项目待办（持久化）
  ```

- [ ] **Step 1.3：在 Phase 3 的提问区块中新增 todo 提问段落**

  在第 415 行（`#### 其他 skill 的提问同理：…` 的上方）、`#### {prefix}-digest：无需提问` 之后插入：

  ```markdown
  #### `{prefix}-todo`：无需提问

  待办文件固定在 `.claude/knowledge/todo.md`，无需用户选择。
  自我感知提醒默认开启。
  ```

- [ ] **Step 1.4：验证三处修改正确**

  ```bash
  grep -n "todo" skills/claude-skill-evo/SKILL.md | head -20
  ```

  预期看到：模板库行、目录树行、Phase 3 段落各 1 处。

- [ ] **Step 1.5：提交**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "feat: 新增 todo 到 skill 模板库和目录树"
  ```

---

## Chunk 2: todo 模板详细设计

**文件：**
- Modify: `skills/claude-skill-evo/SKILL.md`（在 `### 模板：research` 之后新增 `### 模板：todo`）

### Task 2: 新增 todo 模板（约 80 行）

在 `### 模板：research` 结尾的 ` ``` ` 和下一个 `### 模板：` 之间插入完整模板内容。

- [ ] **Step 2.1：在 `### 模板：experiment` 之前插入 todo 模板**

  插入内容（完整）：

  ````markdown
  ### 模板：todo

  ```markdown
  ---
  name: {prefix}-todo
  description: >
    {项目名} 项目级待办管理。查看/添加/完成/清理待办项，
    持久化到 .claude/knowledge/todo.md，对话中自动感知待办意图。
    触发词：todo、待办、任务、记录todo、查看任务、添加任务、完成任务。
  version: 1.0.0
  source: claude-skill-evo
  ---

  # {项目名} 项目待办

  > 会话级临时 TODO 请使用 Claude Code 内置任务面板（TodoWrite）。
  > 本 skill 只管项目级持久化待办：记录、追踪、归档。

  ## 操作速查

  | 指令 | 效果 |
  |------|------|
  | `/{prefix}-todo` | 展示当前所有待完成项 |
  | `/{prefix}-todo 添加 描述` | 追加一条待办到「待完成」区 |
  | `/{prefix}-todo 完成 #N` | 将第 N 条移至「已完成」区 |
  | `/{prefix}-todo 清理` | 归档已完成项，删除 30 天前的旧记录 |

  ## 执行流程

  ### 查看（默认行为）

  1. 读取 `.claude/knowledge/todo.md`
  2. 若文件不存在，则创建（写入标准模板）
  3. 格式化展示「待完成」区所有条目（编号从 1 开始）

  ### 添加

  1. 在「待完成」区末尾追加：`- [ ] {描述} ({今日日期})`
  2. 展示追加结果

  ### 完成

  1. 找到第 N 条（按展示顺序）
  2. 将 `- [ ]` 改为 `- [x]`，移动到「已完成」区开头
  3. 提示：是否将本次完成内容沉淀到知识库？（触发 `/{prefix}-digest`）

  ### 清理

  1. 展示当前「已完成」区所有条目
  2. 删除 30 天前的已完成条目（按日期判断）
  3. 展示清理结果

  ## todo.md 标准格式

  ```markdown
  # 项目待办

  ## 待完成

  - [ ] 描述 (YYYY-MM-DD)

  ## 已完成

  - [x] 描述 (YYYY-MM-DD)
  ```

  ## 自我感知：被动检测

  在任意对话中，若检测到以下信号，主动提议记录：

  - 用户说「之后要做」「下次记得」「TODO:」「待办」「先跳过」
  - 当前修复了问题但留有后续工作（「暂时先这样，之后要…」）

  提议格式（简短，不打断工作流）：
  ```
  📌 检测到待办，要记录到项目 todo 吗？
  > {提炼的描述}
  ```

  ---

  ## 自我进化协议

  {按注入模板生成，侧重点：待办分类优化、自我感知触发词扩充、与 digest 协作模式改进}
  ```
  ````

- [ ] **Step 2.2：验证模板结构完整**

  ```bash
  grep -n "模板：todo\|prefix.*todo\|todo.md" skills/claude-skill-evo/SKILL.md
  ```

  预期：能看到模板标题、name 字段、todo.md 路径引用。

- [ ] **Step 2.3：检查 todo.md 格式示例是否渲染正确（嵌套代码块）**

  手动检查 todo 模板中 `todo.md 标准格式` 的代码块是否用反引号正确闭合。

- [ ] **Step 2.4：提交**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "feat: 新增 todo skill 模板详细设计"
  ```

---

## Chunk 3: sf-skill 本项目同步（可选）

本项目自用的 `sf-skill` 元技能目录表应同步更新，让本项目开发时也能用 `/sf-todo`。

**文件：**
- Modify: `.claude/skills/sf-skill/SKILL.md`

- [ ] **Step 3.1：读取 sf-skill/SKILL.md，找到 skill 目录表**

  ```bash
  grep -n "sf-" .claude/skills/sf-skill/SKILL.md | head -20
  ```

- [ ] **Step 3.2：在目录表中新增 sf-todo 条目**

  在 `sf-research` 行后插入：
  ```
  | `/sf-todo` | 项目待办管理 |
  ```

- [ ] **Step 3.3：提交**

  ```bash
  git add .claude/skills/sf-skill/SKILL.md
  git commit -m "feat: sf-skill 目录表新增 sf-todo 条目"
  ```
