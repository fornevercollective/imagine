#!/usr/bin/env python3
"""
pot.py — Python module form of the Point of Truth
Import: from pot.exports.pot import POT, TIMELINE, search_tags, etc.
Or: import pot.exports.pot as pot

The actual data lives in sibling pot.json (single source of truth).
This wrapper makes `import pot` ergonomics nice while staying 100% faithful.
"""
from __future__ import annotations
import json
from pathlib import Path

_HERE = Path(__file__).parent
with open(_HERE / "pot.json", encoding="utf-8") as f:
    POT = json.load(f)

META = POT["meta"]
TIMELINE = POT["timeline"]
PROVENANCE_STAGES = POT["provenance_stages"]
TAG_CATEGORIES = POT["tag_categories"]
ALL_TAGS = POT["all_tags_flat"]

def get_tags_by_category(cat: str):
    return TAG_CATEGORIES.get(cat, [])

def get_timeline_entry(tid: str):
    for t in TIMELINE:
        if t.get("id") == tid:
            return t
    return None

def search_tags(q: str):
    qq = q.lower()
    return [t for t in ALL_TAGS if qq in t.lower()]

def get_provenance_stage(n: int):
    for s in PROVENANCE_STAGES:
        if s.get("stage") == n:
            return s
    return None

if __name__ == "__main__":
    print("PoT version:", META["version"])
    print("Timeline entries:", len(TIMELINE))
    print("Total flat tags:", len(ALL_TAGS))
    print("Example search 'roman':", search_tags("roman")[:3])
