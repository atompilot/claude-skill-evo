#!/bin/bash
# SkillForge Evolution System — Standalone Installer
# For projects that already have skills but want cross-session evolution.
# https://github.com/atompilot/skillforge
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/atompilot/skillforge/main/evolution/install.sh | bash
#   # or
#   bash /path/to/install.sh

set -euo pipefail

EVOLUTION_DIR=".claude/evolution"
HOOKS_DIR="$EVOLUTION_DIR/hooks"
SETTINGS=".claude/settings.json"
BASE_URL="https://raw.githubusercontent.com/atompilot/skillforge/main/evolution"

echo "🧬 SkillForge Evolution System — Installing..."

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
    echo "   If you haven't set up skills yet, use /skillforge first."
    exit 1
fi

# 1. Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$EVOLUTION_DIR/raw"
mkdir -p "$HOOKS_DIR"

# 2. Download hook scripts
echo "📥 Downloading hook scripts..."
if command -v curl &>/dev/null; then
    curl -fsSL "$BASE_URL/capture.sh" > "$HOOKS_DIR/capture.sh"
    curl -fsSL "$BASE_URL/digest.py" > "$HOOKS_DIR/digest.py"
else
    wget -q "$BASE_URL/capture.sh" -O "$HOOKS_DIR/capture.sh"
    wget -q "$BASE_URL/digest.py" -O "$HOOKS_DIR/digest.py"
fi
chmod +x "$HOOKS_DIR/capture.sh"

# 3. Initialize session metadata
echo "📊 Initializing metadata..."
cat > "$EVOLUTION_DIR/session-meta.json" << 'EOF'
{
  "total_sessions": 0,
  "last_digest_session": 0,
  "pending_signal_count": 0
}
EOF

# 4. Initialize empty digest
cat > "$EVOLUTION_DIR/evolution-digest.md" << 'EOF'
# Evolution Digest

## Last Updated
(not yet)

## Confirmed Patterns
(none yet)

## Pending Proposals
(none yet)

## Correction History
(none yet)

## Tool Usage Patterns
(none yet)

## Evolution Log
(none yet)
EOF

# 5. Merge hooks into .claude/settings.json
echo "🔧 Configuring hooks..."
python3 << 'PYEOF'
import json
import os

settings_path = ".claude/settings.json"
settings = {}
if os.path.exists(settings_path):
    with open(settings_path, 'r') as f:
        settings = json.load(f)

hooks = settings.setdefault("hooks", {})

capture_cmd = "bash .claude/evolution/hooks/capture.sh"
hook_short = {"hooks": [{"type": "command", "command": capture_cmd, "timeout": 5}]}
hook_long = {"hooks": [{"type": "command", "command": capture_cmd, "timeout": 30}]}
hook_start = {"hooks": [{"type": "command", "command": capture_cmd, "timeout": 10}]}
hook_tool = {"matcher": "Edit|Write|Bash|Read", "hooks": [{"type": "command", "command": capture_cmd, "timeout": 5}]}

# Check if evolution hooks already exist (avoid duplicates)
def has_evolution_hook(event_hooks):
    for h in event_hooks:
        for inner in h.get("hooks", []):
            if "evolution" in inner.get("command", ""):
                return True
    return False

for event, hook_entry in [
    ("SessionStart", hook_start),
    ("UserPromptSubmit", hook_short),
    ("Stop", hook_short),
    ("SessionEnd", hook_long),
]:
    event_hooks = hooks.setdefault(event, [])
    if not has_evolution_hook(event_hooks):
        event_hooks.append(hook_entry)

# PostToolUse with matcher
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
echo "✅ Evolution system installed!"
echo ""
echo "What happens now:"
echo "  - Hook scripts will automatically capture interaction data"
echo "  - After each session, signals are extracted and accumulated"
echo "  - When ≥5 signals accumulate (or ≥3 sessions pass), Claude will"
echo "    be prompted to analyze and propose skill updates"
echo ""
echo "Manual commands (if you have evolve/digest skills):"
echo "  /{prefix}-evolve   — Trigger evolution analysis now"
echo "  /{prefix}-digest   — View evolution status"
echo ""
echo "No evolve/digest skills? Run /skillforge to generate them."
