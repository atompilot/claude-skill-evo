#!/bin/bash
# Claude Skill Evo — Evolution System Standalone Installer
# For projects that already have skills but want cross-session evolution.
# https://github.com/atompilot/claude-skill-evo
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/atompilot/claude-skill-evo/main/evolution/install.sh | bash
#   # or
#   bash /path/to/install.sh

set -euo pipefail

EVOLUTION_DIR=".claude/evolution"
SETTINGS=".claude/settings.json"
BASE_URL="https://raw.githubusercontent.com/atompilot/claude-skill-evo/main/evolution"

# Global hook script location — path-independent, works for all users/machines
GLOBAL_HOOKS_DIR="$HOME/.claude/evolution/hooks"
GLOBAL_CAPTURE="$GLOBAL_HOOKS_DIR/capture.sh"
GLOBAL_DIGEST="$GLOBAL_HOOKS_DIR/digest.py"

echo "🧬 Claude Skill Evo — Evolution System Installing..."

# Check prerequisites
if ! command -v jq &>/dev/null; then
    echo "❌ jq is required but not installed. Install it first:"
    echo "   brew install jq  # macOS"
    echo "   apt install jq   # Linux"
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    echo "❌ python3 is required but not installed."
    exit 1
fi

# Check we're in a project with .claude/
if [ ! -d ".claude" ]; then
    echo "❌ No .claude/ directory found. Run this from your project root."
    echo "   If you haven't set up skills yet, use /skill-evo first."
    exit 1
fi

# 1. Install hook scripts to global location (~/.claude/evolution/hooks/)
#    Using a global path avoids hardcoding per-project absolute paths,
#    making this portable across all users and machines.
echo "📁 Installing hook scripts to $GLOBAL_HOOKS_DIR ..."
mkdir -p "$GLOBAL_HOOKS_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/capture.sh" ] && [ -f "$SCRIPT_DIR/digest.py" ]; then
    echo "   Copying from local plugin..."
    cp "$SCRIPT_DIR/capture.sh" "$GLOBAL_CAPTURE"
    cp "$SCRIPT_DIR/digest.py" "$GLOBAL_DIGEST"
else
    echo "   Downloading..."
    if command -v curl &>/dev/null; then
        curl -fsSL "$BASE_URL/capture.sh" > "$GLOBAL_CAPTURE"
        curl -fsSL "$BASE_URL/digest.py" > "$GLOBAL_DIGEST"
    else
        wget -q "$BASE_URL/capture.sh" -O "$GLOBAL_CAPTURE"
        wget -q "$BASE_URL/digest.py" -O "$GLOBAL_DIGEST"
    fi
fi
chmod +x "$GLOBAL_CAPTURE"

# 2. Create per-project data directory (no scripts here, just data)
echo "📁 Creating project data directory..."
mkdir -p "$EVOLUTION_DIR/raw"

# 3. Initialize session metadata
echo "📊 Initializing metadata..."
cat > "$EVOLUTION_DIR/session-meta.json" << 'EOF'
{
  "total_sessions": 0,
  "last_digest_session": 0,
  "pending_signal_count": 0
}
EOF

# 4. Initialize empty digest (skip if already exists)
if [ -f "$EVOLUTION_DIR/evolution-digest.md" ]; then
    echo "   evolution-digest.md already exists, skipping (preserving your data)"
else
cat > "$EVOLUTION_DIR/evolution-digest.md" << 'EOF'
# Evolution Digest

## Last Updated
(not yet)

## Confirmed Patterns
(none yet)

## Pending Proposals
(none yet)

## Deferred (Low Confidence)
(none yet — signals with confidence < 0.5 accumulate here until reinforced)

## Correction History
(none yet)

## Failure-Correction Chains
(none yet — linked failure→correction sequences with root cause analysis)

## Tool Usage Patterns
(none yet)

## Evolution Log
(none yet)

## Meta-Evolution (进化策略自身的改进记录)
> 记录进化系统本身的调整：触发阈值、信心评分规则、信号检测模式等。
> 每次 Evolve 分析后，评估进化过程本身是否有改进空间。

(none yet)

## Size Report
> 每次 Evolve 后记录各 skill 文件的体积，超过 12KB 的标记 ⚠️。

(none yet)
EOF
fi

# 5. Merge hooks into .claude/settings.json
#    Hook command uses $HOME so it's portable — no hardcoded absolute paths.
echo "🔧 Configuring hooks..."
if [ -f "$SETTINGS" ]; then
    cp "$SETTINGS" "$SETTINGS.bak.$(date +%Y%m%d_%H%M%S)"
    echo "   Backed up $SETTINGS"
fi
python3 << 'PYEOF'
import json
import os

settings_path = ".claude/settings.json"
settings = {}
if os.path.exists(settings_path):
    with open(settings_path, 'r') as f:
        settings = json.load(f)

hooks = settings.setdefault("hooks", {})

# Use $HOME so the path is portable across all users and machines.
# The script itself reads `cwd` from the hook payload to identify the project.
capture_cmd = "bash $HOME/.claude/evolution/hooks/capture.sh"
hook_short = {"hooks": [{"type": "command", "command": capture_cmd, "timeout": 5}]}
hook_long  = {"hooks": [{"type": "command", "command": capture_cmd, "timeout": 30}]}
hook_start = {"hooks": [{"type": "command", "command": capture_cmd, "timeout": 10}]}
hook_tool  = {"matcher": "Edit|Write|Bash|Read", "hooks": [{"type": "command", "command": capture_cmd, "timeout": 5}]}

def has_evolution_hook(event_hooks):
    for h in event_hooks:
        for inner in h.get("hooks", []):
            if "evolution" in inner.get("command", ""):
                return True
    return False

for event, hook_entry in [
    ("SessionStart",      hook_start),
    ("UserPromptSubmit",  hook_short),
    ("Stop",              hook_short),
    ("SessionEnd",        hook_long),
]:
    event_hooks = hooks.setdefault(event, [])
    if not has_evolution_hook(event_hooks):
        event_hooks.append(hook_entry)

post_hooks = hooks.setdefault("PostToolUse", [])
if not has_evolution_hook(post_hooks):
    post_hooks.append(hook_tool)

with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)
PYEOF

# 6. Update .gitignore
echo "📝 Updating .gitignore..."
GITIGNORE=".gitignore"
touch "$GITIGNORE"

add_gitignore() {
    if ! grep -qF "$1" "$GITIGNORE" 2>/dev/null; then
        echo "$1" >> "$GITIGNORE"
    fi
}

add_gitignore ".claude/evolution/raw/"
add_gitignore ".claude/evolution/pending-signals.jsonl"
add_gitignore ".claude/evolution/session-meta.json"

echo ""
echo "✅ Evolution system installed! (v3.1)"
echo ""
echo "Hook scripts installed to: $GLOBAL_HOOKS_DIR"
echo "Project data directory:    $(pwd)/$EVOLUTION_DIR"
echo ""
echo "What happens now:"
echo "  - Hook scripts will automatically capture interaction data"
echo "  - After each session, signals are extracted and accumulated"
echo "  - When ≥5 signals accumulate (or ≥3 sessions pass), Claude will"
echo "    be prompted to analyze and propose skill updates"
echo ""
echo "v3.1 features:"
echo "  - 🎯 Confidence scoring (0.3-0.9) for all signals"
echo "  - 🔗 Failure-correction chain detection"
echo "  - 📊 Signal clustering by domain/pattern"
echo "  - 📏 Size Guard — warns when skills exceed 12KB"
echo "  - 🧬 Meta-evolution — the evolution system improves itself"
echo ""
echo "Manual commands (if you have evolve/digest skills):"
echo "  /{prefix}-evolve   — Trigger evolution analysis now"
echo "  /{prefix}-digest   — View evolution status"
echo ""
echo "No evolve/digest skills? Run /skill-evo to generate them."
