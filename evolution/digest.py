#!/usr/bin/env python3
"""
Claude Skill Evo — Evolution System Layer 2: Session Digest
Runs at SessionEnd. Extracts evolution signals from raw captured data.
https://github.com/atompilot/claude-skill-evo

v3.1 — Enhanced with:
  - Confidence scoring (0.3-0.9) for all signals
  - Failure-correction chain detection
  - Signal clustering by domain/pattern
  - Deduplication against existing signals
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from hashlib import md5
from pathlib import Path

# --- Signal Detection Patterns ---

CORRECTION_PATTERNS = [
    # Chinese
    r'不对|不要这样|不是这样|应该是|错了|改成|别用|不应该|用错了',
    # English
    r'wrong|not like that|should be|don\'t use|instead of|fix this|that\'s incorrect',
    # Redo signals
    r'重新|再来|不行|换一种|撤回|回退|换个方式',
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


def signal_fingerprint(signal: dict) -> str:
    """Generate a dedup fingerprint for a signal."""
    key_parts = [signal.get('type', '')]
    if signal['type'] == 'correction':
        # Normalize: take first 50 chars of prompt
        key_parts.append(signal.get('prompt', '')[:50])
    elif signal['type'] == 'instruction':
        key_parts.append(signal.get('prompt', '')[:50])
    elif signal['type'] == 'pattern':
        key_parts.append(signal.get('subtype', ''))
        key_parts.append(signal.get('file', signal.get('command', '')))
    elif signal['type'] == 'failure':
        key_parts.append(signal.get('command', '')[:100])
    elif signal['type'] == 'chain':
        key_parts.append(signal.get('failure_command', '')[:50])
        key_parts.append(signal.get('correction_prompt', '')[:50])
    return md5('|'.join(key_parts).encode()).hexdigest()[:12]


# --- Confidence Scoring ---

def compute_confidence(signal_type: str, count: int = 1, **kwargs) -> float:
    """Compute confidence score for a signal.

    Args:
      signal_type: One of 'instruction', 'correction', 'chain', 'pattern', 'failure'.
      count: Recurrence count. For 'pattern', this is the number of times the
             pattern was observed (e.g., file edits or command executions).
             For 'correction'/'failure', this is the recurrence count across sessions.

    Scoring rules:
      instruction: 0.9 (user explicit intent)
      correction:  0.5 base, +0.1 per recurrence (cap 0.8)
      chain:       0.8 (failure→correction has clear causation)
      pattern:     0.3 + 0.1*max(count-3, 0), cap 0.8
                   (stays at 0.3 until count > 3, then grows)
      failure:     0.4 base, +0.1 per recurrence (cap 0.7)
    """
    if signal_type == 'instruction':
        return 0.9
    elif signal_type == 'correction':
        return min(0.5 + 0.1 * (count - 1), 0.8)
    elif signal_type == 'chain':
        return 0.8
    elif signal_type == 'pattern':
        return min(0.3 + 0.1 * max(count - 3, 0), 0.8)
    elif signal_type == 'failure':
        return min(0.4 + 0.1 * (count - 1), 0.7)
    return 0.3


# --- Signal Extraction ---

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
                'confidence': compute_confidence('correction'),
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
                    'confidence': compute_confidence('instruction'),
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
                'confidence': compute_confidence('pattern', count),
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
                'confidence': compute_confidence('pattern', count),
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
                    'ts': t.get('ts', ''),
                    'command': t.get('command', '')[:200],
                    'error_preview': result[:300],
                    'confidence': compute_confidence('failure'),
                })
    return signals


# --- Failure-Correction Chain Detection ---

def detect_failure_correction_chains(
    prompts: list[dict],
    tools: list[dict],
    session_id: str,
) -> list[dict]:
    """Detect failure→correction chains: a tool fails, then user corrects.

    Heuristic: if a Bash failure occurs and the next user prompt contains
    a correction pattern, they are likely causally linked.
    """
    chains = []

    # Build a timeline of events sorted by timestamp
    events = []
    for t in tools:
        if t.get('tool') == 'Bash' and matches_any(t.get('result_preview', ''), FAILURE_INDICATORS):
            events.append({
                'kind': 'failure',
                'ts': t.get('ts', ''),
                'command': t.get('command', '')[:200],
                'error': t.get('result_preview', '')[:300],
            })
    for p in prompts:
        if matches_any(p.get('prompt', ''), CORRECTION_PATTERNS):
            events.append({
                'kind': 'correction',
                'ts': p.get('ts', ''),
                'prompt': p.get('prompt', ''),
            })

    events.sort(key=lambda e: e.get('ts', ''))

    # Find failure→correction pairs (within adjacency)
    i = 0
    while i < len(events) - 1:
        if events[i]['kind'] == 'failure' and events[i + 1]['kind'] == 'correction':
            chains.append({
                'type': 'chain',
                'subtype': 'failure_correction',
                'session_id': session_id,
                'ts': events[i + 1]['ts'],
                'failure_command': events[i]['command'],
                'error_preview': events[i]['error'],
                'correction_prompt': events[i + 1]['prompt'],
                'confidence': compute_confidence('chain'),
            })
            i += 2  # Skip both events
        else:
            i += 1

    return chains


# --- Signal Clustering ---

def cluster_signals(signals: list[dict]) -> list[dict]:
    """Assign cluster_id to signals based on domain/pattern similarity.

    Clustering rules:
      - Same file path → same cluster
      - Same command prefix → same cluster
      - Correction prompts with overlapping keywords → same cluster
      - Otherwise → unique cluster
    """
    clusters = defaultdict(list)

    for sig in signals:
        cluster_key = _compute_cluster_key(sig)
        sig['cluster_id'] = cluster_key
        clusters[cluster_key].append(sig)

    # Boost confidence for clustered signals (same pattern seen multiple times)
    for cluster_key, group in clusters.items():
        if len(group) >= 2:
            boost = min(0.1 * (len(group) - 1), 0.2)
            for sig in group:
                sig['confidence'] = min(sig.get('confidence', 0.3) + boost, 0.9)
                sig['cluster_size'] = len(group)

    return signals


def _compute_cluster_key(sig: dict) -> str:
    """Compute a cluster key for a signal."""
    sig_type = sig.get('type', '')

    if sig_type == 'pattern':
        subtype = sig.get('subtype', '')
        if subtype == 'hot_file':
            # Cluster by directory
            file_path = sig.get('file', '')
            return f"file:{os.path.dirname(file_path)}"
        elif subtype == 'frequent_cmd':
            # Cluster by command root (first token)
            cmd = sig.get('command', '')
            return f"cmd:{cmd.split()[0] if cmd else 'unknown'}"

    elif sig_type == 'failure':
        cmd = sig.get('command', '')
        return f"fail:{cmd.split()[0] if cmd else 'unknown'}"

    elif sig_type == 'chain':
        cmd = sig.get('failure_command', '')
        return f"chain:{cmd.split()[0] if cmd else 'unknown'}"

    elif sig_type in ('correction', 'instruction'):
        # Cluster by keyword extraction (simple: first meaningful word after trigger)
        prompt = sig.get('prompt', '')
        # Remove trigger words, take first noun-like token
        cleaned = re.sub(r'不对|应该|错了|记住|以后|always|never|should', '', prompt).strip()
        token = cleaned.split()[0] if cleaned.split() else 'general'
        return f"{sig_type}:{token[:20]}"

    return f"misc:{sig.get('session_id', '')}"


# --- Deduplication ---

def deduplicate_signals(
    new_signals: list[dict],
    existing_signals: list[dict],
) -> list[dict]:
    """Remove duplicate signals, both within new_signals and against existing.

    Two-phase dedup:
      1. Internal: deduplicate within new_signals (same session may produce dupes)
      2. External: deduplicate against existing pending signals

    If a duplicate is found, boost the existing/first signal's confidence instead.
    """
    existing_fps = {}
    for sig in existing_signals:
        fp = signal_fingerprint(sig)
        existing_fps[fp] = sig

    # Phase 1: Internal dedup within new_signals
    deduped_new = []
    seen_new_fps = {}
    for sig in new_signals:
        fp = signal_fingerprint(sig)
        if fp in seen_new_fps:
            # Boost the first occurrence's confidence
            first = seen_new_fps[fp]
            first_conf = first.get('confidence', 0.3)
            first['confidence'] = min(first_conf + 0.1, 0.9)
            first['recurrence_count'] = first.get('recurrence_count', 1) + 1
        else:
            seen_new_fps[fp] = sig
            deduped_new.append(sig)

    # Phase 2: External dedup against existing signals
    unique = []
    for sig in deduped_new:
        fp = signal_fingerprint(sig)
        if fp in existing_fps:
            # Boost existing signal confidence (recurrence)
            old = existing_fps[fp]
            old_conf = old.get('confidence', 0.3)
            old['confidence'] = min(old_conf + 0.1, 0.9)
            old['recurrence_count'] = old.get('recurrence_count', 1) + 1
        else:
            unique.append(sig)
            existing_fps[fp] = sig

    return unique, existing_signals


# --- Cleanup ---

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


# --- Main ---

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

    # 2. Extract signals (with confidence scoring)
    signals = []
    signals.extend(extract_corrections(prompts, session_id))
    signals.extend(extract_instructions(prompts, session_id))
    signals.extend(extract_tool_patterns(tools, session_id))
    signals.extend(detect_failures(tools, session_id))

    # 3. Detect failure-correction chains
    chains = detect_failure_correction_chains(prompts, tools, session_id)
    signals.extend(chains)

    # 4. Cluster signals
    signals = cluster_signals(signals)

    # 5. Deduplicate against existing pending signals
    pending_path = os.path.join(evolution_dir, 'pending-signals.jsonl')
    existing_signals = read_jsonl(pending_path)
    new_signals, updated_existing = deduplicate_signals(signals, existing_signals)

    # 6. Write back: updated existing + new signals
    all_signals = updated_existing + new_signals
    if all_signals:
        with open(pending_path, 'w', encoding='utf-8') as f:
            for signal in all_signals:
                f.write(json.dumps(signal, ensure_ascii=False) + '\n')

    # 7. Update session-meta.json
    meta_path = os.path.join(evolution_dir, 'session-meta.json')
    meta = {}
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r') as f:
                meta = json.load(f)
        except (json.JSONDecodeError, IOError):
            meta = {}

    # Count pending signals
    pending_count = len(all_signals)
    meta['pending_signal_count'] = pending_count
    meta['last_session_end'] = datetime.now(timezone.utc).isoformat()

    # Track signal statistics for meta-evolution
    stats = meta.setdefault('signal_stats', {})
    for sig in new_signals:
        sig_type = sig.get('type', 'unknown')
        stats[sig_type] = stats.get(sig_type, 0) + 1
    meta['signal_stats'] = stats

    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)

    # 8. Cleanup old raw files
    cleanup_old_raw(raw_dir, days=30)


if __name__ == '__main__':
    main()
