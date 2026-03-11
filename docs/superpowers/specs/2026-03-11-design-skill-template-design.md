# Design Skill Template — 设计方案

**日期**：2026-03-11
**状态**：已批准
**作者**：Brainstorming Session

---

## 背景

`splaz-design` 是 Splaz 项目中一个成熟的、项目专属的设计系统 skill（v4.2.0，543 行）。
目标：将其结构提炼为通用模版，作为 `claude-skill-evo` 生成 design skill 时的蓝本。

---

## 目标

当 `claude-skill-evo` 在含有设计系统的项目中运行时，自动生成一个**项目专属的 design skill**，覆盖：
- React Native / Expo 项目
- Web（React/Vue/Next.js）项目
- SwiftUI 项目

---

## 方案选择

| 方案 | 描述 | 结论 |
|------|------|------|
| A：独立模版文件 | `templates/design-*.md` 分平台存储 | 否决：引入额外文件维护负担 |
| **B：内嵌主 SKILL.md（选定）** | 检测与生成逻辑直接嵌入 `claude-skill-evo/SKILL.md` | ✅ 保持单文件分发简洁性 |
| C：子 skill | 新建 `sf-design-template` | 否决：对用户项目引入开发辅助 skill |

---

## 详细设计

### 1. 设计系统检测逻辑（集成到 Phase 1）

在 Phase 1（项目探测）末尾新增**设计系统嗅探**步骤：

```
检测顺序（按优先级）：

注 1：检查 package.json 时，范围为 dependencies + devDependencies + peerDependencies 合集。
注 2：以下检测互斥，按顺序逐一判断，首个命中即停止，不继续检测后续平台。

1. React Native / Expo
   主信号：package.json 中 expo 包存在（最具区分性）
   备用信号：package.json 中 react-native 包存在
   Token 文件候选（按优先级尝试）：
     src/lib/design.ts
     src/theme.ts
     src/styles/tokens.ts
     src/theme/colors.ts
     constants/Colors.ts          ← Expo 官方模板默认位置
   Fallback（以上均不存在时）：
     glob 搜索 **/theme*.ts, **/color*.ts, **/token*.ts（深度 ≤ 3 层，取前 2 个命中文件）

2. Web（React/Vue/Next.js）
   信号：package.json 含 react / vue / next，且 expo 和 react-native 均不存在（即第 1 条完全未命中）
   Token 文件候选（按优先级尝试）：
     tailwind.config.ts / tailwind.config.js
     src/tokens.json
     src/styles/tokens.css
     src/theme/index.ts
   Fallback（以上均不存在时）：
     glob 搜索 **/token*.{ts,js,json,css}, **/theme*.{ts,js}（深度 ≤ 3 层，取前 2 个命中文件）

3. SwiftUI
   主信号：*.xcodeproj 文件存在
   备用信号：任意 *.swift 文件中出现 `import SwiftUI`（grep 深度 ≤ 3 层，取首个命中）
   Token 文件候选：
     */DesignSystem/*.swift
     */Theme/*.swift
     */Tokens/*.swift
   Fallback：
     glob 搜索 **/*Color*.swift, **/*Token*.swift（深度 ≤ 3 层，取前 2 个命中文件）

4. 未检测到支持的平台（即 package.json 无 expo/react-native/react/vue/next，且无 *.xcodeproj，
   且 *.swift 中无 import SwiftUI）→ 跳过，不生成 design skill。
   注：平台命中但 token 文件全部未找到，仍生成 design skill（全部使用占位符）。
```

### 2. Token 扫描策略（混合模式）

```
扫描步骤：
1. 按优先级读取候选 Token 文件（最多 2-3 个文件）
2. 提取：
   - 颜色语义 token（主色、背景、文字、边框、overlay 等）
   - 间距 token（spacing scale）
   - 字号 / 行高 token（typography）
   - 圆角 token（radius）
   - Light / Dark 双模式（如有）
3. 扫描到的字段直接写入 skill
4. 扫描不到的字段使用占位符格式：{{TOKEN_NAME: 说明}}
   占位符仅供用户手动替换，不作为结构化标记自动识别。
   格式锁定为 {{KEY: 说明}}，不得变更为其他形式（如 <> 或 []）。
```

### 3. 生成的 Design Skill 结构

所有平台共用以下 6 章结构，平台差异体现在各章内容：

```
## 实现顺序规范
  → 先查哪些 skill，再查 design（内容由生成时 Phase 2 的 skill 列表自动填入；
    若生成时尚无其他 skill，则写"暂无依赖，直接参考 design skill"）

## 调用方式
  → Figma URL / 截图 / 文字描述 三路处理规则
  → "实现前必须先搜索现有组件"规则

## Light/Dark 模式规范（RN/Web）/ 颜色适配规范（SwiftUI）
  → 颜色必须用 token，不得硬编码
  → 从截图映射颜色到 token 的规则
  → 禁止行为清单

## 颜色 Token 速查
  → auto-scan 填入实际值
  → 扫不到：{{COLOR_TOKEN: 填入你的颜色 token 名称}}

## 间距 / 字号 / 圆角 Token
  → auto-scan 填入实际值
  → 扫不到：{{SPACING_TOKEN: 填入你的间距 scale}}

## 禁止事项
  → 通用：禁硬编码颜色/尺寸、禁跳过现有组件搜索、禁自行猜测设计意图

## 自我进化协议
  → 标准格式
  → 侧重：token 文件变更时触发 STALE 检测
```

**平台差异对照：**

| 章节 | React Native | Web | SwiftUI |
|------|-------------|-----|---------|
| 颜色使用方式 | `useThemeColors()` + StyleSheet 分离规则 | CSS variables / Tailwind class | Color assets / Environment |
| 间距使用方式 | `spacing[N]` token | Tailwind `p-N` / CSS token | SwiftUI `.padding()` token |
| 禁止行为 | 禁 `backgroundColor: "#fff"` 等硬编码 | 禁裸 hex / 裸 `px` 值 | 禁 `.foregroundColor(.white)` 硬编码 |

### 4. 集成到主 SKILL.md 的位置

**文件**：`skills/claude-skill-evo/SKILL.md`（仅改动此文件）

| 位置 | 改动 |
|------|------|
| Phase 1 末尾 | 新增"设计系统嗅探"步骤（~15 行） |
| Phase 2（Skill 规划）| 新增 design skill 判断分支（~10 行） |
| 新增章节 | `## Design Skill 生成指南`（~120 行，含三平台模版） |

---

## 体积说明

实际量测：`skills/claude-skill-evo/SKILL.md` 当前为 3,398 行 / 97KB。

原 brainstorming 估算（300-400 行）基于错误假设，已废弃。

新增内容估算：
| 新增项目 | 行数 |
|---------|------|
| Phase 1 嗅探步骤 | ~30 行 |
| Phase 2 分支 | ~10 行 |
| Design Skill 生成指南（三平台） | ~130 行 |
| **合计新增** | **~170 行 / ~5KB** |

新增内容相对于 97KB 基准体积，增量合理，不需要压缩现有内容。

---

## 不涉及的改动

- `.claude/skills/sf-*/SKILL.md`（开发辅助 skill 不变）
- `.claude-plugin/marketplace.json`（无需注册新 skill）
- 任何新增模版文件

---

## 成功标准

1. `claude-skill-evo` 在 Splaz（RN）项目中运行，能自动扫描 `design.ts` 并生成含实际 token 的 design skill
2. 在有 react 依赖但无 token 文件的 Web 项目中运行（平台命中，token 扫描无结果），能生成含占位符的 design skill 框架
3. 在非 UI 项目（如纯 CLI 工具，package.json 无 react/vue/next/expo/react-native）中运行，不生成 design skill，流程正常
4. 主 SKILL.md 新增内容 ≤ 200 行（实际文件已为 97KB，新增量合理即可）
