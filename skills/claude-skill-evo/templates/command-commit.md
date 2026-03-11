<!-- 无进化协议依赖，Command 为轻量过程文件 -->

---
description: 代码提交工作流。精确暂存、VERSION 管理、生成规范提交信息、自动推送。
argument-hint: 可选：--major/--minor/--patch 强制版本类型
---

# {项目名} 代码提交工作流

**ARGUMENTS**: $ARGUMENTS

```
/{prefix}-commit                   # 默认：提交所有 git 变更
/{prefix}-commit --minor           # 强制 minor 版本
```

> **职责边界**：本 command 只负责提交。代码审查请在提交前单独运行 `/{prefix}-review`。

## 步骤 1：查看当前变更

```bash
git status
git diff HEAD
git diff --cached
```

## 步骤 2：精确暂存

**不使用 `git add -A`**，改为精确暂存：

```bash
git status --short
# 按以下规则暂存文件：
# M（已修改）→ 全部暂存
# ?（新增）→ 排除 .env*、*.log 后暂存
# D（删除）→ 全部暂存
git add <精确列出的文件路径>
git reset HEAD -- .env .env.local .env.* 2>/dev/null || true
git diff --cached --stat  # 确认暂存内容
```

## 步骤 3：VERSION 管理（如果项目有 VERSION 文件）

```bash
current=$(cat VERSION 2>/dev/null)
```

若 VERSION 文件不存在 → 跳过本步骤。

**版本类型判断**（优先以 $ARGUMENTS 参数为准，无参数则自动判断）：

| 触发条件 | 版本类型 | 示例 |
|---------|---------|------|
| `--major` 或破坏性变更 | major | 1.2.3 → 2.0.0 |
| `--minor` 或 `feat` 类提交 | minor | 1.2.3 → 1.3.0 |
| `--patch` 或 fix/docs/chore 等 | patch | 1.2.3 → 1.2.4 |

```bash
new=<计算后的新版本>
echo $new > VERSION
git add VERSION
```

## 步骤 4：生成提交信息

基于 `git diff --cached` 分析变更，按以下规则生成：

| type | 适用场景 |
|------|---------|
| `feat` | 新功能、新页面、新接口 |
| `fix` | 修复 bug |
| `refactor` | 重构（无功能变化） |
| `docs` | 文档、注释更新 |
| `chore` | 依赖、配置、构建脚本 |
{用户自定义 type}

**格式**：
```
<type>: <{中文/英文}描述>（版本号如有 VERSION 文件则附上 vX.Y.Z）

- <细节1>（多文件时列出）
- <细节2>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

## 步骤 5：执行提交

```bash
git commit -m "$(cat <<'EOF'
<生成的提交信息>
EOF
)"
git log --oneline -1  # 验证提交
```

## 步骤 6：推送

```bash
git push origin <当前分支>
# 若失败（远程有新提交）：
# git pull --rebase origin <当前分支> && git push origin <当前分支>
```

## 完成输出

```
## {prefix}-commit 完成

暂存文件：N 个，+X -Y 行
VERSION：{old} → {new}（已更新）/ 未变更
提交信息：<type>: <subject>
Commit：<hash>
推送：已推送
```
