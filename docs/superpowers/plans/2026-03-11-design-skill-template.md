# Design Skill Template 实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `skills/claude-skill-evo/SKILL.md` 中内嵌设计系统检测与 design skill 生成能力，使 `claude-skill-evo` 能为 RN/Web/SwiftUI 项目自动生成项目专属的 design skill。

**Architecture:** 纯 Markdown 修改，不引入新文件。在现有 Phase 1 末尾添加设计系统嗅探步骤（§1.4），在 Phase 2 条件 Skills 表格添加 design 行，在文件末尾新增"Design Skill 生成指南"章节（含三平台模版）。

**Tech Stack:** Markdown、Claude Code Skill 语法

**Spec:** `docs/superpowers/specs/2026-03-11-design-skill-template-design.md`

**文件基线（实际量测）：** `skills/claude-skill-evo/SKILL.md` 当前为 3,398 行 / 97KB。新增内容约 170 行 / ~5KB，增量合理，无需压缩现有内容。

---

## Chunk 1: 确认改动锚点

### Task 1: 读取 SKILL.md，确认插入位置

**Files:**
- Read: `skills/claude-skill-evo/SKILL.md`

- [ ] **Step 1: 确认 Phase 1 子章节编号**

  读取 SKILL.md，找到 Phase 1 下的所有 `###` 子章节（已知有 1.1、1.2、1.3），确认最后一个编号。
  新子章节将命名为 `### 1.4 设计系统嗅探`，插入在 `## Phase 2` 标题之前。

- [ ] **Step 2: 确认 Phase 2 条件 Skills 表格位置**

  找到包含"有产品设计需求"的条件 Skills 表格行（在 Phase 2 的 `### 2.1 Skill 模板库` 中），
  记录该行。新的 `design` 行将插入在该行之后。

- [ ] **Step 3: 确认 Phase 2 首次初始化展示模板位置**

  找到 Phase 2 中以 ` ```  ` 包裹的首次初始化展示模板（含 `{prefix}-skill`、`{prefix}-dev` 等），
  确认 `✅ = 推荐  ⚡ = 可选` 所在行。design skill 注释说明将追加到该代码块内部的末尾。

- [ ] **Step 4: 确认文件末尾行**

  ```bash
  tail -5 skills/claude-skill-evo/SKILL.md
  ```

  确认文件最后几行，新的 `## Design Skill 生成指南` 章节将追加在此之后。

---

## Chunk 2: 添加 Phase 1 嗅探 + Phase 2 分支（一次 commit）

> 注：Chunk 2 包含 Task 2 和 Task 3，合并为一次 commit 避免 SKILL.md 处于不一致中间态。

### Task 2: 在 Phase 1 末尾插入 §1.4 设计系统嗅探

**Files:**
- Modify: `skills/claude-skill-evo/SKILL.md`

- [ ] **Step 1: 在 `## Phase 2` 之前插入以下内容**

  ```markdown
  ### 1.4 设计系统嗅探（自动，每次都做）

  在 Phase 1 扫描完成后，额外检测是否存在设计系统，以决定是否生成 design skill。

  **平台检测规则：**

  注 1：检查 package.json 时，范围为 dependencies + devDependencies + peerDependencies 合集。
  注 2：以下检测互斥，首个命中即停止，不继续检测后续平台。

  ```bash
  # 1. React Native / Expo（主信号：expo 包；备用：react-native 包）
  grep -E '"expo"|"react-native"' package.json 2>/dev/null

  # 2. Web（react/vue/next 存在，且 expo 和 react-native 均不存在）
  grep -E '"react"|"vue"|"next"' package.json 2>/dev/null
  # 仅在步骤 1 完全未命中时才检查此项

  # 3. SwiftUI（.xcodeproj 存在，或 *.swift 文件中有 import SwiftUI）
  ls *.xcodeproj 2>/dev/null
  grep -rl "import SwiftUI" --include="*.swift" --max-depth=3 . 2>/dev/null | head -1

  # 4. 未命中任何平台 → DESIGN_PLATFORM=none，跳过，不生成 design skill
  ```

  **Token 文件候选（命中平台后按序尝试，取首个存在的文件）：**

  | 平台 | 候选路径（优先级从高到低） | Fallback glob（深度 ≤ 3 层，取前 2 个） |
  |------|--------------------------|----------------------------------------|
  | RN/Expo | `src/lib/design.ts` → `src/theme.ts` → `src/styles/tokens.ts` → `src/theme/colors.ts` → `constants/Colors.ts` | `**/theme*.ts`, `**/color*.ts`, `**/token*.ts` |
  | Web | `tailwind.config.ts` → `tailwind.config.js` → `src/tokens.json` → `src/styles/tokens.css` → `src/theme/index.ts` | `**/token*.{ts,js,json,css}`, `**/theme*.{ts,js}` |
  | SwiftUI | `*/DesignSystem/*.swift` → `*/Theme/*.swift` → `*/Tokens/*.swift` | `**/*Color*.swift`, `**/*Token*.swift` |

  **传递给 Phase 2：**
  - `DESIGN_PLATFORM`：`rn` / `web` / `swiftui` / `none`
  - `DESIGN_TOKEN_FILES`：扫描到的 token 文件路径列表（可为空列表）

  > 重要：`DESIGN_PLATFORM ≠ none` 即进入 design skill 生成流程，即使 `DESIGN_TOKEN_FILES` 为空（此时所有 token 字段使用占位符 `{{KEY: 说明}}`）。
  ```

### Task 3: 在 Phase 2 添加 design skill 分支

**Files:**
- Modify: `skills/claude-skill-evo/SKILL.md`（同一编辑会话，与 Task 2 合并提交）

- [ ] **Step 2: 在条件 Skills 表格"有产品设计需求"行之后插入 design 行**

  ```markdown
  | 有设计系统（Phase 1 嗅探命中，`DESIGN_PLATFORM ≠ none`，即使 `DESIGN_TOKEN_FILES` 为空也生成） | `design` | Design Token 速查、Light/Dark 规范、禁止事项（空 token list 时全部使用占位符） |
  ```

- [ ] **Step 3: 在首次初始化展示模板的代码块内部追加 design skill 注释**

  找到 Phase 2 首次初始化模式的展示模板代码块（以 ` ``` ` 包裹），在 `✅ = 推荐  ⚡ = 可选` 行之后追加：

  ```
  # 若 Phase 1 嗅探命中设计系统，自动追加：
  # └── {prefix}-design/SKILL.md   🎨 Design Token 规范（平台：{DESIGN_PLATFORM}）
  ```

  注：此内容在代码块内部，Claude 执行 skill 时会读取代码块文本作为指令，行为正确。

- [ ] **Step 4: 合并提交 Chunk 2（Task 2 + Task 3）**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "feat: 添加设计系统嗅探（Phase 1 §1.4）及 design skill 分支（Phase 2）"
  ```

---

## Chunk 3: 新增 Design Skill 生成指南章节

### Task 4: 在文件末尾追加 Design Skill 生成指南

**Files:**
- Modify: `skills/claude-skill-evo/SKILL.md`（追加到文件末尾）

- [ ] **Step 1: 追加章节框架 + 通用生成规则**

  在 SKILL.md 文件末尾追加：

  ````markdown
  ---

  ## Design Skill 生成指南

  > 仅当 Phase 1 嗅探到设计系统（`DESIGN_PLATFORM ≠ none`）时执行本章节。
  > 生成文件：`.claude/skills/{prefix}-design/SKILL.md`

  ### 通用生成规则

  1. 读取 `DESIGN_TOKEN_FILES` 中的文件，提取颜色、间距、字号、圆角 token
  2. 扫描到的值直接写入 skill；扫描不到的字段用占位符 `{{KEY: 说明}}`
     - 占位符格式锁定为 `{{KEY: 说明}}`，仅供用户手动替换，不作结构化标记
     - `DESIGN_TOKEN_FILES` 为空时，所有 token 字段均使用占位符
  3. `## 实现顺序规范` 章节内容由生成时的已有 skill 列表自动填入；
     若尚无其他 skill，写"暂无依赖，直接参考 design skill"
  4. 所有平台均包含 `## 自我进化协议` 章节（标准格式），侧重：token 文件变更时触发 STALE 检测
  ````

- [ ] **Step 2: 追加平台 A（React Native / Expo）模版**

  ````markdown
  ---

  ### 平台 A：React Native / Expo

  > 当 `DESIGN_PLATFORM = rn` 时，按以下结构生成 design skill。

  ```markdown
  ---
  name: {prefix}-design
  description: >
    {项目名} 设计系统完整指南。实现 UI 组件、还原设计稿、查询 Design Token 时调用此 skill。
    触发词：实现UI、实现组件、设计还原、Figma、截图实现、token查询、颜色token、设计系统、Dark Mode。
  version: 1.0.0
  source: claude-skill-evo
  ---

  # {项目名} Design System Skill

  > Token 文件：{DESIGN_TOKEN_FILES[0] 或 "未检测到，请手动填入"}

  ## 实现顺序规范

  {Phase 2 已有 skill 列表自动填入}

  ## 调用方式

  **Figma URL** — 调用 Figma MCP 获取设计上下文，映射 token 后实现。
  **截图/图片** — 图片颜色必须映射到语义 token，不得硬编码 hex。图片默认为 Light 模式。
  **文字描述** — 找到代码位置，将描述转为 token 后修改。

  **共同规则：实现前必须先搜索现有组件**，确认无相同/相似组件后再新建。

  ## Light / Dark 模式规范

  - 颜色必须用语义 token，通过主题 hook 获取，不得放 `StyleSheet.create`
  - `StyleSheet.create` 只放静态 token（间距、字号、圆角），颜色必须内联
  - 禁止：`"#FFFFFF"`、`"rgba(0,0,0,0.1)"` 等，一律替换为对应 token

  ## 颜色 Token 速查

  | Token | Light | Dark | 用途 |
  |-------|-------|------|------|
  {{COLOR_TOKENS: 从 DESIGN_TOKEN_FILES 扫描填入；格式：token名 | light值 | dark值 | 用途}}

  ## 间距 / 字号 / 圆角 Token

  | 类型 | Token | 值 |
  |------|-------|-----|
  {{SPACING_TOKENS: 从 DESIGN_TOKEN_FILES 扫描填入}}
  {{TYPOGRAPHY_TOKENS: 从 DESIGN_TOKEN_FILES 扫描填入}}
  {{RADIUS_TOKENS: 从 DESIGN_TOKEN_FILES 扫描填入}}

  ## 禁止事项

  | 禁止 | 原因 |
  |------|------|
  | `backgroundColor: "#FFFFFF"` 等硬编码颜色 | 不跟随主题 |
  | 颜色放在 `StyleSheet.create` | Light/Dark 无法切换 |
  | 遇到不确定的设计自行猜测 | 必须向用户提问 |
  | 未搜索直接新建组件 | 优先复用现有实现 |

  ## 自我进化协议

  | 信号 | 行动 |
  |------|------|
  | skill 描述的 token 与 token 文件实际不符 | 立即说明「⚠️ skill 内容可能过时」|
  | 遇到 skill 未覆盖但需要规范的设计场景 | 记录为待补充 |
  | 用户纠正了 skill 描述的做法 | 标记，任务后提议更新 |

  高风险过时信号：token 文件新增/删除/改名 → 颜色速查表可能过时。
  ```
  ````

- [ ] **Step 3: 追加平台 B（Web）模版**

  ````markdown
  ---

  ### 平台 B：Web（React/Vue/Next.js）

  > 当 `DESIGN_PLATFORM = web` 时，按以下结构生成 design skill。

  ```markdown
  ---
  name: {prefix}-design
  description: >
    {项目名} 设计系统完整指南。实现 UI 组件、查询 Design Token 时调用此 skill。
    触发词：实现UI、实现组件、token查询、颜色token、设计系统、Dark Mode、Tailwind。
  version: 1.0.0
  source: claude-skill-evo
  ---

  # {项目名} Design System Skill

  > Token 文件：{DESIGN_TOKEN_FILES[0] 或 "未检测到，请手动填入"}

  ## 实现顺序规范

  {Phase 2 已有 skill 列表自动填入}

  ## 调用方式

  同 React Native 版，但图片颜色映射到 CSS variables / Tailwind class。
  实现前必须先搜索现有组件目录，确认无重复后再新建。

  ## 颜色使用规范

  - Tailwind 项目：使用 `className="text-{token}"` / `bg-{token}` 等 class
  - CSS Variables 项目：使用 `var(--color-{token})`
  - 禁止：`color: "#333"` / `background-color: rgba(0,0,0,0.5)` 等裸 hex/rgba

  ## Token 速查

  {{TAILWIND_CONFIG: 从 tailwind.config 扫描填入自定义颜色/间距 token；扫不到则为占位符}}

  ## 禁止事项

  | 禁止 | 原因 |
  |------|------|
  | 裸写 hex 颜色 / rgba 值 | 不使用 token，无法统一主题 |
  | 裸写 px 间距值 | 不使用 spacing scale |
  | 遇到不确定的设计自行猜测 | 必须向用户提问 |
  | 未搜索直接新建组件 | 优先复用现有实现 |

  ## 自我进化协议

  | 信号 | 行动 |
  |------|------|
  | skill 描述的 token 与 token 文件实际不符 | 立即说明「⚠️ skill 内容可能过时」|
  | 遇到 skill 未覆盖但需要规范的设计场景 | 记录为待补充 |
  | 用户纠正了 skill 描述的做法 | 标记，任务后提议更新 |

  高风险过时信号：tailwind.config 变更 → Token 速查可能过时。
  ```
  ````

- [ ] **Step 4: 追加平台 C（SwiftUI）模版**

  ````markdown
  ---

  ### 平台 C：SwiftUI

  > 当 `DESIGN_PLATFORM = swiftui` 时，按以下结构生成 design skill。

  ```markdown
  ---
  name: {prefix}-design
  description: >
    {项目名} 设计系统完整指南。实现 SwiftUI 组件、查询 Design Token 时调用此 skill。
    触发词：实现UI、实现组件、token查询、颜色token、设计系统、Dark Mode、Color asset。
  version: 1.0.0
  source: claude-skill-evo
  ---

  # {项目名} Design System Skill

  > Token 文件：{DESIGN_TOKEN_FILES[0] 或 "未检测到，请手动填入"}

  ## 实现顺序规范

  {Phase 2 已有 skill 列表自动填入}

  ## 调用方式

  同通用版，图片颜色映射到 Color asset 或 SwiftUI Color extension。
  实现前必须先搜索现有组件，确认无重复后再新建。

  ## 颜色适配规范

  - 使用 Color assets（Assets.xcassets）：`Color("tokenName")`
  - 使用 SwiftUI Environment：`@Environment(\.colorScheme)`
  - 使用自定义 Color extension：`Color.{tokenName}`（若项目有）
  - 禁止：`.foregroundColor(.white)` / `Color(red:green:blue:)` 等硬编码

  ## Token 速查

  {{COLOR_TOKENS: 从 Token 文件扫描填入；格式：asset名称 | 用途}}
  {{SPACING_TOKENS: 从 Token 文件扫描填入}}

  ## 禁止事项

  | 禁止 | 原因 |
  |------|------|
  | `.foregroundColor(.white)` 等硬编码颜色 | 不支持 Dark Mode 自适应 |
  | `.padding(16)` 等硬编码间距 | 不使用 spacing token |
  | 遇到不确定的设计自行猜测 | 必须向用户提问 |
  | 未搜索直接新建组件 | 优先复用现有实现 |

  ## 自我进化协议

  | 信号 | 行动 |
  |------|------|
  | skill 描述的 token 与 token 文件实际不符 | 立即说明「⚠️ skill 内容可能过时」|
  | 遇到 skill 未覆盖但需要规范的设计场景 | 记录为待补充 |
  | 用户纠正了 skill 描述的做法 | 标记，任务后提议更新 |

  高风险过时信号：Token 文件变更 → Token 速查可能过时。
  ```
  ````

- [ ] **Step 5: 验证追加内容格式**

  检查：
  - 所有平台模版的内层代码块（` ``` markdown ` ... ` ``` `）正确闭合
  - 三平台均含 `## 自我进化协议` 章节
  - `{{KEY: 说明}}` 格式一致

- [ ] **Step 6: 验证新增行数**

  ```bash
  git diff --stat skills/claude-skill-evo/SKILL.md
  ```

  预期：新增约 130-170 行，远低于 200 行上限。

- [ ] **Step 7: Commit**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "feat: 新增 Design Skill 生成指南（RN/Web/SwiftUI 三平台模版）"
  ```

---

## Chunk 4: 版本升级 & 验证

### Task 5: 更新版本号并验证所有场景

**Files:**
- Modify: `skills/claude-skill-evo/SKILL.md`（frontmatter version 字段）

- [ ] **Step 1: 更新版本号**

  将 frontmatter 中的 `version: 3.0.0` 改为 `version: 3.1.0`（minor bump，新增功能）。

- [ ] **Step 2: 验证场景 1 — Expo/RN 项目（有 token 文件）**

  ```
  模拟输入：
  - package.json 含 "expo": "~51.0.0"
  - src/lib/design.ts 存在

  预期路径：
  Phase 1 §1.4：grep expo → 命中 → DESIGN_PLATFORM=rn
  Token 扫描：src/lib/design.ts 存在 → DESIGN_TOKEN_FILES=[src/lib/design.ts]
  Phase 2：design 行命中，加入生成列表
  Phase 4：读取 design.ts，按平台 A 模版生成，token 字段填入实际值
  ```

- [ ] **Step 3: 验证场景 2 — Web 项目（有 react，无 token 文件）**

  ```
  模拟输入：
  - package.json 含 "react": "^18.0.0"，无 expo/react-native
  - 无任何候选 token 文件，Fallback glob 也无命中

  预期路径：
  Phase 1 §1.4：grep expo → 未命中；grep react → 命中；确认无 expo/react-native → DESIGN_PLATFORM=web
  Token 扫描：所有候选 + Fallback glob 均无命中 → DESIGN_TOKEN_FILES=[]
  Phase 2：design 行命中（DESIGN_PLATFORM≠none 即生成）
  Phase 4：按平台 B 模版生成，所有 token 字段使用占位符 {{KEY: 说明}}
  ```

- [ ] **Step 4: 验证场景 3 — 非 UI 项目（纯 Go CLI）**

  ```
  模拟输入：
  - 只有 go.mod，无 package.json，无 *.xcodeproj，无 *.swift

  预期路径：
  Phase 1 §1.4：所有平台检测均未命中 → DESIGN_PLATFORM=none → 跳过
  Phase 2：design 行不出现
  ```

- [ ] **Step 5: Final commit**

  ```bash
  git add skills/claude-skill-evo/SKILL.md
  git commit -m "feat: claude-skill-evo v3.1.0 — 支持自动生成 Design Skill（RN/Web/SwiftUI）"
  ```

---

## 快速参考

| 文件 | 改动类型 | 对应 Task |
|------|---------|----------|
| `skills/claude-skill-evo/SKILL.md` | 插入 §1.4（Phase 1 末尾） | Task 2 |
| `skills/claude-skill-evo/SKILL.md` | 添加 design 行（Phase 2 表格） | Task 3 |
| `skills/claude-skill-evo/SKILL.md` | 追加 Design Skill 生成指南 | Task 4 |
| `skills/claude-skill-evo/SKILL.md` | version 3.0.0 → 3.1.0 | Task 5 |

**体积预算：**
- 当前基线：3,398 行 / 97KB
- 新增上限：200 行
- 无需压缩现有内容
