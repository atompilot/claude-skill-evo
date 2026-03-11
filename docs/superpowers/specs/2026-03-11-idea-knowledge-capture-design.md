# Idea 知识捕获设计

**日期**：2026-03-11
**状态**：待实现
**范围**：`skills/claude-skill-evo/SKILL.md` + 生成的 `CLAUDE.md` 模板 + 知识库初始化逻辑

---

## 背景

当前知识库有 5 个类目（decisions / research / pitfalls / conventions / references），但缺少一个轻量的"想法暂存区"。用户在对话中产生的三类信号容易消失：

1. **用户反馈/抱怨** — 发现某个 skill 不对，但当时来不及改
2. **灵感/新特性** — 想到新 skill 模板或新机制
3. **改进点** — 发现生成产物逻辑不好，不在状态里马上改

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

**文件格式模板**：

```markdown
# <想法标题>

**日期**：YYYY-MM-DD
**来源**：<对话中发现 / 用户主动提出 / 调研中产生>
**背景**：一句话描述为什么有这个想法

## 想法内容

...

## 状态

- [ ] 待评估
- [ ] 已转 research
- [ ] 已转 decision
- [ ] 已放弃（原因：...）
```

**`index.md` 新增节**：

```markdown
## 待评估想法
<!-- 列出 ideas/ 下状态为"待评估"的想法链接 -->
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
| "记住这个"/"以后要做" | `.claude/knowledge/ideas/` 或 `todo.md` |
| 调研结论/技术选型依据 | `.claude/knowledge/research/` |

记录格式：日期 + 一句话背景 + 内容，文件放对应目录。
```

---

### 改动 3：Phase 1 项目探测扫描 `ideas/`

**位置**：SKILL.md Phase 1（现状感知/项目探测）阶段

**新增逻辑**：扫描 `.claude/knowledge/ideas/` 目录，统计"待评估"状态的想法数量，在探测结果摘要中展示：

```
- 💡 待评估想法：X 条（.claude/knowledge/ideas/）
```

目的：让用户在每次使用 skill-evo 时，顺带看到积压的 idea，形成自然的回顾习惯。

---

## 修改文件清单

| 文件 | 修改位置 | 修改量 |
|------|---------|--------|
| `skills/claude-skill-evo/SKILL.md` | Phase 1 探测摘要 | +3 行 |
| `skills/claude-skill-evo/SKILL.md` | Phase 4 知识库初始化 | +5 行（新增 ideas/ 目录 + index 占位节） |
| `skills/claude-skill-evo/SKILL.md` | CLAUDE.md 模板章节 | +14 行（知识捕获触发器） |

总计：**约 +22 行**，改动集中在主产品 SKILL.md 的三个位置。

---

## 验证标准

1. 执行 `/claude-skill-evo` 后，生成的知识库包含 `ideas/` 目录
2. 生成的 `index.md` 包含「待评估想法」节
3. 生成的 `CLAUDE.md` 包含「知识捕获触发器」章节
4. Phase 1 探测摘要能展示 `ideas/` 的 idea 数量（当目录存在时）
