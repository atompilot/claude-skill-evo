#!/usr/bin/env python3
"""
SkillForge Evolution System — Layer 2: Session Digest
Runs at SessionEnd. Extracts evolution signals from raw captured data.
https://github.com/atompilot/skillforge
"""

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- Signal Detection Patterns ---

CORRECTION_PATTERNS = [
    # Chinese
    r'不对|不要这样|不是这样|应该是|错了|改成|别用|不应该|用错了',
    # English
    r'wrong|not like that|should be|don\'t use|instead of|fix this|that\'s incorrect',
    # Redo signals
    r'重新|再来|不行|换一种|撤回|回退',
]

INSTRUCTION_PATTERNS = [
    # Chinese
    r'记住|以后都|以后要|从现在开始|以后别|永远不要',
    # English
    r'always|remember|never|from now on',
    # Skill-specific
    r'写入.*skill|更新.*skill|加到.*规范|添加到.*规范',
]

FAILURE_INDICATORS = [
    r'error|Error|ERROR',
    r'failed|Failed|FAILED',
    r'command not found',
    r'No such file',
    r'Permission denied',
    r'Exit code [1-9]',
]


def read_jsonl(path: str) -> list[dict]:
    """Read a JSONL file, returning list of dicts. Tolerant of missing files."""
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def matches_any(text: str, patterns: list[str]) -> bool:
    """Check if text matches any of the given regex patterns."""
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def extract_corrections(prompts: list[dict], session_id: str) -> list[dict]:
    """Extract correction signals from user prompts."""
    signals = []
    for i, p in enumerate(prompts):
        prompt_text = p.get('prompt', '')
        if matches_any(prompt_text, CORRECTION_PATTERNS):
            signals.append({
                'type': 'correction',
                'session_id': session_id,
                'ts': p.get('ts', ''),
                'prompt': prompt_text,
                'prev_prompt': prompts[i - 1].get('prompt', '') if i > 0 else None,
            })
    return signals


def extract_instructions(prompts: list[dict], session_id: str) -> list[dict]:
    """Extract explicit instruction signals from user prompts."""
    signals = []
    for p in prompts:
        prompt_text = p.get('prompt', '')
        if matches_any(prompt_text, INSTRUCTION_PATTERNS):
            # Skip if already detected as correction (avoid duplicates)
            if not matches_any(prompt_text, CORRECTION_PATTERNS):
                signals.append({
                    'type': 'instruction',
                    'session_id': session_id,
                    'ts': p.get('ts', ''),
                    'prompt': prompt_text,
                })
    return signals


def extract_tool_patterns(tools: list[dict], session_id: str) -> list[dict]:
    """Extract tool usage patterns: hot files and frequent commands."""
    signals = []

    # Hot files: Edit/Write to same file >= 3 times
    edit_files = [t.get('file', '') for t in tools if t.get('tool') in ('Edit', 'Write') and t.get('file')]
    file_counts = Counter(edit_files)
    for file_path, count in file_counts.items():
        if count >= 3:
            signals.append({
                'type': 'pattern',
                'subtype': 'hot_file',
                'session_id': session_id,
                'file': file_path,
                'edit_count': count,
            })

    # Frequent commands: same command prefix >= 3 times
    commands = []
    for t in tools:
        if t.get('tool') == 'Bash' and t.get('command'):
            # Normalize: take first 3 tokens as command signature
            cmd = t['command'].strip()
            sig = ' '.join(cmd.split()[:3])
            commands.append(sig)

    cmd_counts = Counter(commands)
    for cmd, count in cmd_counts.items():
        if count >= 3:
            signals.append({
                'type': 'pattern',
                'subtype': 'frequent_cmd',
                'session_id': session_id,
                'command': cmd,
                'count': count,
            })

    return signals


def detect_failures(tools: list[dict], session_id: str) -> list[dict]:
    """Detect failed Bash commands."""
    signals = []
    for t in tools:
        if t.get('tool') == 'Bash':
            result = t.get('result_preview', '')
            if matches_any(result, FAILURE_INDICATORS):
                signals.append({
                    'type': 'failure',
                    'session_id': session_id,
                    'command': t.get('command', '')[:200],
                    'error_preview': result[:300],
                })
    return signals


def cleanup_old_raw(raw_dir: str, days: int = 30):
    """Delete raw files older than N days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    raw_path = Path(raw_dir)
    if not raw_path.exists():
        return
    for f in raw_path.iterdir():
        if f.is_file() and f.suffix == '.jsonl':
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                f.unlink()


def main():
    if len(sys.argv) < 3:
        print("Usage: digest.py <evolution_dir> <session_id>", file=sys.stderr)
        sys.exit(1)

    evolution_dir = sys.argv[1]
    session_id = sys.argv[2]
    raw_dir = os.path.join(evolution_dir, 'raw')

    # 1. Read raw data for this session
    prompts = read_jsonl(os.path.join(raw_dir, f'prompts-{session_id}.jsonl'))
    tools = read_jsonl(os.path.join(raw_dir, f'tools-{session_id}.jsonl'))

    # 2. Extract signals
    signals = []
    signals.extend(extract_corrections(prompts, session_id))
    signals.extend(extract_instructions(prompts, session_id))
    signals.extend(extract_tool_patterns(tools, session_id))
    signals.extend(detect_failures(tools, session_id))

    # 3. Append to pending-signals.jsonl
    if signals:
        pending_path = os.path.join(evolution_dir, 'pending-signals.jsonl')
        with open(pending_path, 'a', encoding='utf-8') as f:
            for signal in signals:
                f.write(json.dumps(signal, ensure_ascii=False) + '\n')

    # 4. Update session-meta.json
    meta_path = os.path.join(evolution_dir, 'session-meta.json')
    meta = {}
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r') as f:
                meta = json.load(f)
        except (json.JSONDecodeError, IOError):
            meta = {}

    # Count pending signals
    pending_path = os.path.join(evolution_dir, 'pending-signals.jsonl')
    pending_count = 0
    if os.path.exists(pending_path):
        with open(pending_path, 'r') as f:
            pending_count = sum(1 for line in f if line.strip())

    meta['pending_signal_count'] = pending_count
    meta['last_session_end'] = datetime.now(timezone.utc).isoformat()

    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)

    # 5. Cleanup old raw files
    cleanup_old_raw(raw_dir, days=30)


if __name__ == '__main__':
    main()
