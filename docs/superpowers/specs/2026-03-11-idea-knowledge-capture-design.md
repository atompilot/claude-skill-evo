# Idea 知识捕获设计

**日期**：2026-03-11
**状态**：待实现
**范围**：`skills/claude-skill-evo/SKILL.md` + 生成的 `CLAUDE.md` 模板 + 知识库初始化逻辑

---

## 背景

当前知识库有 5 个类目（decisions / research / pitfalls / conventions / references），但缺少一个轻量的"想法暂存区"。用户在对话中产生的三类信号容易消失：

1. **用户反馈/抱怨** — 发现某个 skill 不对，但当时来不及改
2. **灵感/新特性** — 想到新 skill 模板或新机制
3. **改进点** — 发现生成产物有优化空间，但当前对话不适合立即改动 skill 本身

同时，CLAUDE.md 模板缺少"被动捕获"机制，Claude 不会主动识别这些信号并建议记录。

---

## 目标

- 提供一个低摩擦的 idea 暂存区，让想法不再消失
- 让生成的 CLAUDE.md 具备被动捕获能力，Claude 在对话中主动识别信号并询问用户是否记录
- 不增加系统复杂度，不改变现有 5 个知识类目结构

---

## 不在范围内

- 不改 digest skill
- 不设计 idea → research → decision 完整流水线
- 不加复杂 QA 流程
- 不引入数值评分或跨 session 状态

---

## 改动详情

### 改动 1：新增 `ideas/` 知识类目

**位置**：`skills/claude-skill-evo/SKILL.md` Phase 4（生成文件阶段）的知识库初始化逻辑

**新增目录**：`.claude/knowledge/ideas/`

**文件命名规范**：`YYYY-MM-DD-<slug>.md`

**文件格式模板**（使用 frontmatter 字段标记状态，便于 Claude 读取）：

```markdown
---
status: pending
date: YYYY-MM-DD
source: <对话中发现 / 用户主动提出 / 调研中产生>
---

# <想法标题>

**背景**：一句话描述为什么有这个想法

## 想法内容

...
```

状态值：`pending`（待评估）/ `to-research` / `to-decision` / `dropped`

**`index.md` 新增节**：

```markdown
## 待评估想法
<!-- 列出 ideas/ 下 status: pending 的想法链接 -->
```

---

### 改动 2：生成的 CLAUDE.md 新增「知识捕获触发器」章节

**位置**：主产品 SKILL.md 中，CLAUDE.md 模板的「进化提示」章节之后

**新增内容**（约 12 行）：

```markdown
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

---

### 改动 3：Phase 1 项目探测扫描 `ideas/`

**位置**：SKILL.md Phase 1（现状感知/项目探测）阶段

**新增逻辑**：扫描 `.claude/knowledge/ideas/` 目录，统计 `status: pending` 的文件数量（读取每个文件的 frontmatter 第一行），在探测结果摘要中展示：

```
- 💡 待评估想法：X 条（.claude/knowledge/ideas/）
```

若目录不存在，跳过此项展示。

目的：让用户在每次使用 skill-evo 时，顺带看到积压的 idea，形成自然的回顾习惯。

---

## 修改文件清单

| 文件 | 修改位置 |
|------|---------|
| `skills/claude-skill-evo/SKILL.md` | Phase 1 探测摘要：新增 ideas/ 扫描逻辑 |
| `skills/claude-skill-evo/SKILL.md` | Phase 4 知识库初始化：新增 ideas/ 目录 + index 占位节 |
| `skills/claude-skill-evo/SKILL.md` | CLAUDE.md 模板：新增「知识捕获触发器」章节 |

改动集中在主产品 SKILL.md 的三个位置，属于小幅增量修改。

---

## 验证标准

**静态产物验证**（可自动检查）：
1. 执行 `/claude-skill-evo` 后，生成的知识库包含 `ideas/` 目录
2. 生成的 `index.md` 包含「待评估想法」节
3. 生成的 `CLAUDE.md` 包含「知识捕获触发器」章节
4. 已有 `ideas/` 目录时，Phase 1 探测摘要展示 `status: pending` 的 idea 数量

**行为验证**（依赖 Claude 语义理解，人工验证）：
5. 在安装了生成的 `CLAUDE.md` 的项目中，当用户说"感觉这里有问题"时，Claude 在当次对话中建议记入 `pitfalls/`；说"要不要考虑 XX"时，建议记入 `ideas/`
   - 注：触发器有效性基于 Claude 语义理解，非关键词匹配，少数情况下可能不触发，属正常现象
