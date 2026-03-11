# Todo Skill 设计文档

**日期**: 2026-03-11
**项目**: claude-skill-evo
**状态**: 待实现

---

## 背景

claude-skill-evo 目前生成 7 个通用 skill（dev/commit/debug/skill/digest/review/research），缺少项目级待办任务管理能力。用户希望新增 `{prefix}-todo` skill，使生成的项目具备持久化 TODO 追踪能力。

---

## 设计目标

- 会话级 TODO：使用 Claude Code 内置 TodoWrite 工具（任务面板），不重复造轮子
- 项目级 TODO：持久化到 `.claude/knowledge/todo.md`，跨 session 可查
- 轻量职责：todo skill 只管任务状态，沉淀时调用 digest skill
- 自我感知：对话中检测到待办意图时主动提议记录

---

## 方案

### 不做的事（边界）

- 不管会话级 TODO（Claude Code 内置 TodoWrite 负责）
- 不强行打通任务面板与 todo.md（两套独立）
- 不自动在 session 开始时清空任何内容

### todo.md 格式

```markdown
# 项目待办

## 待完成

- [ ] 描述 (2026-03-11)
- [ ] 描述 (2026-03-10)

## 已完成

- [x] 描述 (2026-03-09)
```

### 生成的 `{prefix}-todo` skill 功能

| 操作 | 触发方式 | 行为 |
|------|---------|------|
| 查看 | `/todo` 或 `查看 todo` | 读取 todo.md，格式化展示当前待完成项 |
| 添加 | `todo: 描述` | 追加到「待完成」区，带日期 |
| 完成 | `完成 todo #N` | 将对应项移到「已完成」区，可选触发 digest |
| 清理 | `清理 todo` | 归档已完成项，可选删除 30 天前的已完成项 |

### 自我感知规则

对话中出现以下信号时，主动提议记录：
- 用户说"之后要做"、"下次记得"、"TODO:"、"待办"
- 修复了 bug 但留有后续工作（"暂时先这样，之后要..."）

提议格式：
```
检测到待办事项，要记录到项目 todo 吗？
> [描述]
```

---

## 实现范围

### 需要修改的文件

只需修改一个文件：`skills/claude-skill-evo/SKILL.md`

### 修改内容

1. **Phase 2 Skill 模板库**：新增 `todo` 行

   ```
   | `todo` | `{prefix}-todo` | 项目级待办管理，持久化到 knowledge/todo.md |
   ```

2. **Phase 2.2 展示规划**：在目录树中加入 `{prefix}-todo/SKILL.md`

3. **Phase 3 内容共创**：新增 `{prefix}-todo` 的细化问答（1 个问题：是否需要自我感知提醒）

4. **新增 todo 生成模板**：约 60-80 行，包含触发词、操作说明、自我感知规则、进化协议

---

## 进化协议注入点

todo skill 的进化信号侧重：
- 发现记录的 TODO 已过时（功能已实现但未标记完成）
- 用户频繁手动记录某类待办 → 可能需要更细的分类

---

## 验收标准

- [ ] SKILL.md 模板库包含 `todo` 条目
- [ ] 生成的 `{prefix}-todo` skill 包含查看/添加/完成/清理四个操作
- [ ] 包含自我感知规则
- [ ] 包含进化协议章节
- [ ] todo.md 格式符合规范（待完成/已完成两区）
- [ ] 与 digest skill 的协作点有说明
