# Idea 知识捕获 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在主产品 SKILL.md 的三个位置做小幅增量修改，让生成出来的项目具备 idea 暂存区和被动捕获能力。

**Architecture:** 纯 Markdown 内容修改，无代码逻辑。三处改动各自独立，按顺序修改 `skills/claude-skill-evo/SKILL.md` 的三个不同位置。

**Tech Stack:** Markdown，Edit 工具精确修改（不全量覆盖）

---

## Chunk 1: Phase 4 知识库初始化 — 新增 ideas/ 目录

**Files:**
- Modify: `skills/claude-skill-evo/SKILL.md:478-495`

### Task 1: 新增 ideas/ 到 mkdir 命令

- [ ] **Step 1: 读取当前内容，确认行号**

  读取 `skills/claude-skill-evo/SKILL.md` 第 475-496 行，确认 `mkdir` 命令和 `index.md` 模板的当前内容。

- [ ] **Step 2: 修改 mkdir 命令，加入 ideas/**

  将：
  ```
  mkdir -p .claude/knowledge/{decisions,research,pitfalls,conventions,references}
  ```
  改为：
  ```
  mkdir -p .claude/knowledge/{decisions,research,pitfalls,conventions,references,ideas}
  ```

- [ ] **Step 3: 修改 index.md 模板，加入「待评估想法」节**

  将 index.md 模板：
  ```markdown
  # {项目名} 知识库索引

  ## 技术决策

  ## 调研结论

  ## 踩坑记录

  ## 隐式规范

  ## 外部参考
  ```
  改为：
  ```markdown
  # {项目名} 知识库索引

  ## 技术决策

  ## 调研结论

  ## 踩坑记录

  ## 隐式规范

  ## 外部参考

  ## 待评估想法
  <!-- 列出 ideas/ 下 status: pending 的想法链接 -->
  ```

- [ ] **Step 4: 在 4.1.1 节末尾加 ideas/ 文件格式说明**

  在 `### 4.1.1 知识库初始化` 节的 index.md 模板代码块之后，插入以下内容（注意：外层用普通 markdown 行，内层模板用缩进代码块表示）：

~~~
**`ideas/` 文件格式**（命名：`YYYY-MM-DD-<slug>.md`）：

    ---
    status: pending
    date: YYYY-MM-DD
    source: <对话中发现 / 用户主动提出 / 调研中产生>
    ---

    # <想法标题>

    **背景**：一句话描述为什么有这个想法

    ## 想法内容

    ...

状态值：`pending`（待评估）/ `to-research` / `to-decision` / `dropped`
~~~

- [ ] **Step 5: 验证修改**

  读取修改后的 478-510 行，肉眼确认：
  - mkdir 命令包含 `ideas`
  - index.md 模板末尾有「待评估想法」节
  - ideas/ 文件格式说明已插入

- [ ] **Step 6: Commit**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "feat: 知识库初始化新增 ideas/ 目录和文件格式"
  ```

---

## Chunk 2: CLAUDE.md 模板 — 新增「知识捕获触发器」章节

**Files:**
- Modify: `skills/claude-skill-evo/SKILL.md:600-606`（`## 知识沉淀` 章节）

### Task 2: 在「知识沉淀」段落之后插入触发器章节

- [ ] **Step 1: 读取当前内容，确认位置**

  读取 `skills/claude-skill-evo/SKILL.md` 第 598-610 行，确认 `## 知识沉淀` 段落的末尾位置（代码块结束的 ` ``` ` 行）。

- [ ] **Step 2: 在 CLAUDE.md 模板代码块内部插入**

  **重要**：`## 知识沉淀` 整段内容位于一个更大的 markdown 代码块内部（这段 CLAUDE.md 模板是用代码块包裹的）。新增内容同样插入到该代码块**内部**，在 `## 知识沉淀` 原有内容之后、代码块闭合 ` ``` ` 之前。

  将代码块内部的：

  ```markdown
  ## 知识沉淀

  对话中出现以下内容时，提议使用 `/{prefix}-digest` 沉淀：
  - 做出了技术决策（选型、架构方案）→ 建议记录到 decisions/
  - 完成了技术调研或深度分析 → 建议记录到 research/
  - 发现了项目的隐式惯例 → 建议记录到 conventions/
  ```

  改为：

  ```markdown
  ## 知识沉淀

  对话中出现以下内容时，提议使用 `/{prefix}-digest` 沉淀：
  - 做出了技术决策（选型、架构方案）→ 建议记录到 decisions/
  - 完成了技术调研或深度分析 → 建议记录到 research/
  - 发现了项目的隐式惯例 → 建议记录到 conventions/

  ## 知识捕获触发器

  在对话中识别以下信号，主动建议记录（询问用户，不强制）：

  | 信号 | 建议记入 |
  |------|---------|
  | "这里有个问题"/"感觉不对" | `.claude/knowledge/pitfalls/` |
  | "要不要试试"/"可以考虑" | `.claude/knowledge/ideas/` |
  | "记住这个"/"以后要做" | `.claude/knowledge/ideas/`（若 todo skill 已安装则优先记入 `todo.md`）|
  | 调研结论/技术选型依据 | `.claude/knowledge/research/` |

  记录格式：日期 + 一句话背景 + 内容，文件放对应目录。
  ```

- [ ] **Step 3: 验证修改**

  读取修改后的 598-625 行，肉眼确认：
  - 原「知识沉淀」段落内容完整保留
  - 新增「知识捕获触发器」章节在其后
  - 表格格式正确，4 行信号映射完整

- [ ] **Step 4: Commit**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "feat: CLAUDE.md 模板新增知识捕获触发器章节"
  ```

---

## Chunk 3: Phase 1 探测摘要 — 新增 ideas/ 扫描

**Files:**
- Modify: `skills/claude-skill-evo/SKILL.md:193-201`（Phase 1 探测结果展示区）

### Task 3: 在探测摘要中加入 ideas 数量

- [ ] **Step 1: 读取当前内容，确认位置**

  读取 `skills/claude-skill-evo/SKILL.md` 第 190-225 行，确认探测结果展示模板的位置（即 `📁 项目类型` 到 `📛 推荐前缀` 的展示区）。

- [ ] **Step 2: 在 Phase 1 的自动扫描（§1.1）末尾加扫描逻辑**

  在 `### 1.1 自动扫描` 的 bash 代码块中，在 `git remote` 和 `find` 命令之后，补充：

  ```bash
  # 检测知识库状态
  ls .claude/knowledge/ideas/ 2>/dev/null | wc -l   # idea 总数
  grep -rl "status: pending" .claude/knowledge/ideas/ 2>/dev/null | wc -l  # pending 数量
  ```

- [ ] **Step 3: 在探测结果摘要模板里加一行**

  找到探测结果展示模板（`📁 项目类型`、`🛠️ 框架` 等行），在 `📛 推荐前缀` 行之前，加入：

  ```
  💡 待评估想法：[X 条 / 目录不存在]（.claude/knowledge/ideas/）
  ```

  完整展示区变为：
  ```
  📁 项目类型：[探测结果]
  🛠️ 框架：[探测结果]
  📦 包管理器：[探测结果]
  🐳 Docker：[有/无]
  🔄 CI/CD：[探测结果]
  💡 待评估想法：[X 条 / 目录不存在]（.claude/knowledge/ideas/）
  📛 推荐前缀：[推断结果]
  ```

  **注意**：若 `.claude/knowledge/ideas/` 不存在，**跳过此行，不展示**；若存在但无 pending 条目，展示"0 条"。

- [ ] **Step 4: 验证修改**

  读取修改后的 118-230 行，肉眼确认：
  - bash 扫描命令中包含 ideas/ 目录检测
  - 探测摘要模板中有 `💡 待评估想法` 行
  - 行位置在 `🔄 CI/CD` 和 `📛 推荐前缀` 之间

- [ ] **Step 5: Commit**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "feat: Phase 1 探测摘要展示待评估 idea 数量"
  ```

---

## Chunk 4: 最终验证

### Task 4: 端到端验证

- [ ] **Step 1: 读取完整修改区域**

  读取 SKILL.md 三个修改区域，逐一核对改动是否符合设计文档。

- [ ] **Step 2: 检查 Markdown 语法**

  确认：
  - 代码块开关配对（` ``` ` 数量匹配）
  - 表格列对齐
  - 无多余空行或缩进错误

- [ ] **Step 3: 参考设计文档的验证标准逐条检查**

  对照 `docs/superpowers/specs/2026-03-11-idea-knowledge-capture-design.md` 的验证标准 1-4 逐条验证：

  1. 生成的知识库初始化命令包含 `ideas` 目录 ✓/✗
  2. 生成的 `index.md` 包含「待评估想法」节 ✓/✗
  3. 生成的 `CLAUDE.md` 包含「知识捕获触发器」章节 ✓/✗
  4. Phase 1 探测摘要展示区包含 `💡 待评估想法` ✓/✗

- [ ] **Step 4: 最终 Commit（若有遗漏修改）**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "fix: 补齐 idea 捕获功能的细节修改"
  ```

  若无遗漏，跳过此步。
