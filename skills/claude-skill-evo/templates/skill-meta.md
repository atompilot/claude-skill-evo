<!-- 依赖：../reference/evolution-protocol.md（进化协议注入） -->

---
name: {prefix}-skill
description: >
  {项目名} Skill 管理元技能兼进化引擎。发现、检查、新建、更新所有项目级 skill。
  跨 skill 一致性检查，驱动整个 skill 体系的进化。
  触发词：skill 管理、查看 skill、skill 列表、新建 skill、更新 skill、skill 进化、
  进化、evolve、优化 skill、进化分析。
version: 1.0.0
source: claude-skill-evo
---

# {项目名} Skill 管理元技能

## 当前 Skill 目录速查

| Skill | 触发场景 | 版本 | 分类 |
|-------|---------|------|------|
{遍历所有已生成的 skills，含版本号}

## 功能一：发现

`ls .claude/skills/*/SKILL.md`（扫描所有项目级 skill，不限命名前缀）

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

### 5.1 主动进化分析

当用户触发 `/{prefix}-skill 进化` 或 `/{prefix}-skill 回顾` 时：

1. 读取所有 `.claude/skills/*/SKILL.md`（包括非 skill-evo 生成的 skill）
2. 扫描项目现状（目录结构、package.json、配置文件等）
3. 对比 skill 内容与项目现状，找出不一致
4. 检查各 skill 体积（>12KB 警告）
5. 检查跨 skill 一致性（术语、路径、命令是否统一）
6. 检查是否有 `<!-- STALE: -->` 标记未处理
7. 生成提议，逐条展示，等待用户确认
8. 确认后写入 skill（version patch +1）

### 5.2 Skill 进化日志

```
.claude/skills/{prefix}-skill/evolution.log
```

记录格式：
```
[YYYY-MM-DD] {skill-name} v{old} → v{new}: {变更摘要}
```

---

## 自我进化协议

{按注入模板生成，侧重点：新 skill 创建时更新目录表、跨 skill 一致性检查}

**元技能专属**：作为元技能，额外关注进化策略本身是否需要调整——进化信号是否噪音太多、好的发现是否被忽略、各 skill 体积增长是否健康。
