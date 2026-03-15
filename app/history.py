"""
AlvGolf AI Analysis History — Persistence & Comparison

Saves timestamped copies of each AI analysis for historical tracking.
Supports listing, loading, and comparing analyses across dates.

Directory: output/ai_history/
Index:     output/ai_history/index.json
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from loguru import logger


# ── Paths ─────────────────────────────────────────────────────────────────────

HISTORY_DIR = Path(__file__).parent.parent / "output" / "ai_history"
INDEX_PATH = HISTORY_DIR / "index.json"


# ── Agent type → output key mapping ──────────────────────────────────────────

AGENT_OUTPUT_KEYS = {
    "ux_writer":  "content",
    "coach":      "report",
    "analista":   "analysis",
    "tecnico":    "analysis",
    "estratega":  "program",
    "full":       None,  # Full /analyze workflow
}


def _ensure_dir():
    """Create history directory if it doesn't exist."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def _load_index() -> list:
    """Load the history index. Returns empty list if not found."""
    if INDEX_PATH.exists():
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_index(index: list):
    """Save the history index."""
    _ensure_dir()
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def _make_timestamp() -> str:
    """Generate ISO-like timestamp safe for filenames."""
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")


# ── Public API ────────────────────────────────────────────────────────────────

def save_analysis(
    agent_type: str,
    user_id: str,
    content: dict | str,
    metadata: Optional[dict] = None,
) -> dict:
    """
    Save an analysis to the history.

    Args:
        agent_type: One of 'ux_writer', 'coach', 'analista', 'tecnico', 'estratega', 'full'
        user_id: User identifier
        content: The analysis content (dict for JSON agents, str for text agents)
        metadata: Optional metadata from the agent response

    Returns:
        dict with 'id', 'filename', 'timestamp'
    """
    _ensure_dir()
    ts = _make_timestamp()
    entry_id = f"{agent_type}_{ts}"

    # Determine file extension
    if isinstance(content, str):
        ext = "md"
        filename = f"{entry_id}.md"
    else:
        ext = "json"
        filename = f"{entry_id}.json"

    filepath = HISTORY_DIR / filename

    # Write content
    if ext == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    # Build index entry
    entry = {
        "id": entry_id,
        "agent_type": agent_type,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "filename": filename,
        "size_chars": len(json.dumps(content)) if isinstance(content, dict) else len(content),
    }
    if metadata:
        # Extract useful metadata fields
        for key in ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens", "model"):
            if key in metadata:
                entry[key] = metadata[key]

    # Append to index
    index = _load_index()
    index.append(entry)
    _save_index(index)

    logger.info(f"[History] Saved {agent_type} analysis: {filename} ({entry['size_chars']} chars)")
    return entry


def list_analyses(
    agent_type: Optional[str] = None,
    user_id: Optional[str] = None,
    limit: int = 50,
) -> list:
    """
    List saved analyses, optionally filtered by agent_type and/or user_id.

    Returns:
        List of index entries, most recent first
    """
    index = _load_index()

    if agent_type:
        index = [e for e in index if e["agent_type"] == agent_type]
    if user_id:
        index = [e for e in index if e["user_id"] == user_id]

    # Most recent first
    index.sort(key=lambda e: e["timestamp"], reverse=True)
    return index[:limit]


def load_analysis(entry_id: str) -> dict:
    """
    Load a specific analysis by its ID.

    Returns:
        dict with 'entry' (index metadata) and 'content' (the analysis)
    """
    index = _load_index()
    entry = next((e for e in index if e["id"] == entry_id), None)

    if not entry:
        raise FileNotFoundError(f"Analysis '{entry_id}' not found in history")

    filepath = HISTORY_DIR / entry["filename"]
    if not filepath.exists():
        raise FileNotFoundError(f"Analysis file '{entry['filename']}' not found on disk")

    if entry["filename"].endswith(".json"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = json.load(f)
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

    return {"entry": entry, "content": content}


def compare_analyses(id1: str, id2: str) -> dict:
    """
    Compare two analyses side by side.

    Returns a structured comparison with:
    - both entries' metadata
    - both contents
    - diff summary (sections added/removed/changed)
    """
    a1 = load_analysis(id1)
    a2 = load_analysis(id2)

    # Ensure same agent type for meaningful comparison
    if a1["entry"]["agent_type"] != a2["entry"]["agent_type"]:
        return {
            "error": f"Cannot compare different agent types: {a1['entry']['agent_type']} vs {a2['entry']['agent_type']}",
            "entry_1": a1["entry"],
            "entry_2": a2["entry"],
        }

    result = {
        "entry_1": a1["entry"],
        "entry_2": a2["entry"],
        "content_1": a1["content"],
        "content_2": a2["content"],
        "diff": _compute_diff(a1["content"], a2["content"], a1["entry"]["agent_type"]),
    }
    return result


def _compute_diff(content1, content2, agent_type: str) -> dict:
    """
    Compute a semantic diff between two analyses.

    For JSON content: compares keys and values.
    For text content: compares line counts and section headers.
    """
    if isinstance(content1, dict) and isinstance(content2, dict):
        return _diff_json(content1, content2)
    elif isinstance(content1, str) and isinstance(content2, str):
        return _diff_text(content1, content2)
    else:
        return {"note": "Mixed content types, cannot compute structured diff"}


def _diff_json(c1: dict, c2: dict) -> dict:
    """Diff two JSON analyses — section-level comparison."""
    keys1 = set(c1.keys())
    keys2 = set(c2.keys())

    added = list(keys2 - keys1)
    removed = list(keys1 - keys2)
    common = keys1 & keys2

    changed = []
    unchanged = []
    for key in sorted(common):
        v1 = json.dumps(c1[key], ensure_ascii=False, sort_keys=True)
        v2 = json.dumps(c2[key], ensure_ascii=False, sort_keys=True)
        if v1 != v2:
            changed.append({
                "section": key,
                "old_length": len(v1),
                "new_length": len(v2),
                "delta_chars": len(v2) - len(v1),
            })
        else:
            unchanged.append(key)

    return {
        "sections_added": added,
        "sections_removed": removed,
        "sections_changed": changed,
        "sections_unchanged": unchanged,
        "total_sections_1": len(keys1),
        "total_sections_2": len(keys2),
    }


def _diff_text(c1: str, c2: str) -> dict:
    """Diff two text analyses — section headers and length."""
    import re

    def extract_headers(text):
        return re.findall(r'^#{1,3}\s+(.+)$', text, re.MULTILINE)

    h1 = extract_headers(c1)
    h2 = extract_headers(c2)

    return {
        "headers_1": h1,
        "headers_2": h2,
        "lines_1": c1.count("\n") + 1,
        "lines_2": c2.count("\n") + 1,
        "chars_1": len(c1),
        "chars_2": len(c2),
        "delta_chars": len(c2) - len(c1),
        "headers_added": [h for h in h2 if h not in h1],
        "headers_removed": [h for h in h1 if h not in h2],
    }
