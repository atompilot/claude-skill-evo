<!-- 依赖：../reference/evolution-protocol.md（进化协议注入） -->
<!-- 关联：knowledge-index.md（知识库目录结构定义） -->

---
name: {prefix}-digest
description: >
  {项目名} 知识沉淀工作流。将技术决策、调研结论、踩坑记录、隐式惯例、外部参考
  统一归档到项目知识库，跨会话持久化。
  触发词：digest、沉淀、记录、知识、总结、归档、决策记录、经验、笔记。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} 知识沉淀

> 知识库路径：`.claude/knowledge/`

## 知识库结构

```
.claude/knowledge/
├── index.md              # 知识索引（按类型分章节）
├── decisions/            # 技术决策记录
├── research/             # 调研结论
├── pitfalls/             # 踩坑记录（与 debug skill 共享）
├── conventions/          # 发现的隐式规范
└── references/           # 外部知识精炼摘要
```

## 内容类型与模板

所有文件统一命名：`YYYY-MM-DD-{topic}.md`

### decisions/ — 技术决策

```markdown
# 决策：{标题}
**日期**：YYYY-MM-DD
**状态**：✅ 已采纳 / ⏳ 待讨论 / ❌ 已废弃

## 背景
{为什么需要做这个决策}

## 方案对比
| 方案 | 优点 | 缺点 |
|------|------|------|

## 结论
{最终选择及理由}

## 影响范围
{哪些模块/文件受影响}
```

### pitfalls/ — 踩坑记录

```markdown
# 踩坑：{标题}
**日期**：YYYY-MM-DD
**关键词**：{用于检索}

## 错误现象
{描述}

## 根本原因
{机制层面的分析}

## 修复方案
{代码或操作步骤}

## 预防措施
- [ ] {规范约束}
```

### research/ — 调研结论

```markdown
# 调研：{标题}
**日期**：YYYY-MM-DD

## 结论
{一句话结论}

## 关键发现
{要点列表}

## 推荐方案
{推荐什么、为什么}
```

### conventions/ — 隐式规范

```markdown
# 惯例：{标题}
**日期**：YYYY-MM-DD
**来源**：{从哪次对话/代码中发现的}

## 规范内容
{具体规范描述}

## 示例
{正确 vs 错误示例}
```

### references/ — 外部知识摘要

```markdown
# 参考：{标题}
**日期**：YYYY-MM-DD
**原始来源**：{URL 或文档名}

## 摘要
{精炼后的要点}

## 与本项目的关联
{如何应用到项目中}
```

## index.md 格式

```markdown
# {项目名} 知识库索引

## 技术决策
- YYYY-MM-DD [{标题}](decisions/YYYY-MM-DD-{topic}.md) — {一句话摘要}

## 调研结论
- YYYY-MM-DD [{标题}](research/YYYY-MM-DD-{topic}.md) — {一句话摘要}

## 踩坑记录
- YYYY-MM-DD [{标题}](pitfalls/YYYY-MM-DD-{topic}.md) — {一句话摘要}

## 隐式规范
- YYYY-MM-DD [{标题}](conventions/YYYY-MM-DD-{topic}.md) — {一句话摘要}

## 外部参考
- YYYY-MM-DD [{标题}](references/YYYY-MM-DD-{topic}.md) — {一句话摘要}
```

## 操作流程

### 写入知识

1. 判断内容类型（决策/调研/踩坑/惯例/参考）
2. 用对应模板创建 `.claude/knowledge/{type}/YYYY-MM-DD-{topic}.md`
3. 更新 `.claude/knowledge/index.md` 对应章节

### 查看知识

1. 读取 `.claude/knowledge/index.md`
2. 按类型或关键词筛选
3. 读取具体文件展示详情

---

## 自我进化协议

> 本 skill 在日常使用中自动进化。

### 何时提议进化

| 信号 | 行为 |
|------|------|
| 出现新的知识类型 | 提议新增子目录和模板 |
| 索引结构不够清晰 | 提议优化 index.md 格式 |
| 模板字段缺失 | 提议补充模板字段 |
| 用户纠正分类 | 提议调整分类标准 |

### Size Guard — ≤ 15KB

> index.md 体积守护：> 50 条时建议归档旧条目。
