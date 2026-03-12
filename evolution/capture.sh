#!/bin/bash
# Claude Skill Evo — Evolution System Unified Hook Entry Point
# All hook events route through this script. Runs async, zero-latency.
# https://github.com/atompilot/claude-skill-evo

set -euo pipefail

INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

# Resolve evolution directory
EVOLUTION_DIR="${CWD:-.}/.claude/evolution"
RAW_DIR="$EVOLUTION_DIR/raw"
META="$EVOLUTION_DIR/session-meta.json"
PENDING="$EVOLUTION_DIR/pending-signals.jsonl"
DIGEST="$EVOLUTION_DIR/evolution-digest.md"

# Bail if evolution dir doesn't exist (not configured)
[ -d "$EVOLUTION_DIR" ] || exit 0

mkdir -p "$RAW_DIR"

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

case "$EVENT" in

  SessionStart)
    # Read session metadata
    TOTAL=$(jq -r '.total_sessions // 0' "$META" 2>/dev/null || echo 0)
    LAST=$(jq -r '.last_digest_session // 0' "$META" 2>/dev/null || echo 0)
    PENDING_COUNT=0
    [ -f "$PENDING" ] && PENDING_COUNT=$(wc -l < "$PENDING" 2>/dev/null | tr -d ' ')

    # Increment session counter
    NEW_TOTAL=$((TOTAL + 1))
    if [ -f "$META" ]; then
      jq --argjson n "$NEW_TOTAL" '.total_sessions = $n' "$META" > "$META.tmp" && mv "$META.tmp" "$META"
    else
      echo "{\"total_sessions\":$NEW_TOTAL,\"last_digest_session\":0,\"pending_signal_count\":$PENDING_COUNT}" > "$META"
    fi

    # Check trigger conditions
    SESSIONS_SINCE=$((NEW_TOTAL - LAST))
    if [ "$PENDING_COUNT" -ge 5 ] || [ "$SESSIONS_SINCE" -ge 3 ] && [ "$PENDING_COUNT" -gt 0 ]; then
      # Output to stdout → injected into Claude's context
      cat <<INJECT
<evolution-trigger>
Skill 进化系统检测到 ${PENDING_COUNT} 条待分析信号（距上次分析已过 ${SESSIONS_SINCE} 个会话）。
请在本次会话的适当时机（不要打断用户的主要任务），执行进化分析：
1. 读取 .claude/evolution/evolution-digest.md（上次总结 checkpoint）
2. 读取 .claude/evolution/pending-signals.jsonl（新增信号）
3. 对比 .claude/skills/ 中的现有 skill 内容
4. 向用户提议更新
分析完成后更新 digest 和 session-meta。
用户也可以随时执行对应的 evolve/digest skill 手动触发。
</evolution-trigger>
INJECT
    fi
    ;;

  UserPromptSubmit)
    # Capture full prompt text (needed for correction semantic analysis)
    echo "$INPUT" | jq -c \
      --arg ts "$TS" \
      '{ts: $ts, prompt: .prompt}' \
      >> "$RAW_DIR/prompts-$SESSION_ID.jsonl" 2>/dev/null
    ;;

  PostToolUse)
    TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
    case "$TOOL" in
      Edit|Write)
        echo "$INPUT" | jq -c \
          --arg ts "$TS" \
          '{ts: $ts, tool: .tool_name,
            file: (.tool_input.file_path // .tool_input.path // "unknown"),
            input_preview: (.tool_input | tostring | .[0:200]),
            elapsed_ms: .elapsed_ms}' \
          >> "$RAW_DIR/tools-$SESSION_ID.jsonl" 2>/dev/null
        ;;
      Bash)
        echo "$INPUT" | jq -c \
          --arg ts "$TS" \
          '{ts: $ts, tool: "Bash",
            command: (.tool_input.command // ""),
            result_preview: (.tool_result // "" | tostring | .[0:300]),
            elapsed_ms: .elapsed_ms}' \
          >> "$RAW_DIR/tools-$SESSION_ID.jsonl" 2>/dev/null
        ;;
      Read)
        # Only capture file path, no result
        echo "$INPUT" | jq -c \
          --arg ts "$TS" \
          '{ts: $ts, tool: "Read",
            file: (.tool_input.file_path // "unknown")}' \
          >> "$RAW_DIR/tools-$SESSION_ID.jsonl" 2>/dev/null
        ;;
    esac
    ;;

  Stop)
    echo "$INPUT" | jq -c \
      --arg ts "$TS" \
      '{ts: $ts, response_preview: (.response_text // "" | tostring | .[0:500])}' \
      >> "$RAW_DIR/responses-$SESSION_ID.jsonl" 2>/dev/null
    ;;

  SessionEnd)
    # Trigger Layer 2 digest (run in background)
    # digest.py lives in the global hooks dir (~/.claude/evolution/hooks/)
    DIGEST_PY="$HOME/.claude/evolution/hooks/digest.py"
    if command -v python3 &>/dev/null && [ -f "$DIGEST_PY" ]; then
      python3 "$DIGEST_PY" "$EVOLUTION_DIR" "$SESSION_ID" &
    fi
    ;;

esac

exit 0
