#!/usr/bin/env python3
"""
Story arc runner for imagine project.
Loads a story JSON (see stories/dusk-to-neon.json and schema), prepares full prompts per beat,
supports chaining refs, and can output a ready-to-generate plan or (in this env) drive generations.

Usage:
  python story.py list
  python story.py prepare stories/dusk-to-neon.json --input inputs/hero.jpg
  python story.py plan stories/dusk-to-neon.json   # shows exact sequence + continuity strategy

When you say "render the dusk-to-neon story with this photo", I will walk the beats, generate
each clip (using image_edit for stills if needed + video_gen or image-to-video), feeding
previous outputs as refs where specified, then give you concat instructions or assemble.
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
STORIES_DIR = ROOT / "stories"
INPUTS_DIR = ROOT / "inputs"
OUTPUTS_DIR = STORIES_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def load_story(path: Path) -> dict:
    data = json.loads(path.read_text())
    # very light validation
    assert "beats" in data and len(data["beats"]) >= 3
    return data

def load_style_prompt(story_beat: dict) -> str:
    slug = story_beat["style_slug"]
    src = story_beat["source"]
    if src == "presets":
        p = ROOT / "style_presets" / slug / "prompt.txt"
    else:
        # featured don't have a raw prompt.txt (they are UI templates), we just name them
        return f"Apply the {slug.replace('-', ' ').title()} featured template."
    if p.exists():
        return p.read_text().strip()
    return ""

def build_beat_prompt(story: dict, beat: dict, base_input_desc: str = "") -> str:
    base = story["base_prompt"]
    ancestry_bible = story.get("character_ancestry_bible", "").strip()
    style_p = load_style_prompt(beat)
    add = beat.get("prompt_add", "")
    cont = story.get("continuity_notes", "Preserve exact likeness of the main subject across styles.")

    # Prepend full ancestry bible (face/body/hair/skin/hominin) for lock-in if provided
    prefix = f"{ancestry_bible}. " if ancestry_bible else ""
    full = f"{prefix}{base}. {style_p}. {add}. {cont}"
    if base_input_desc:
        full += f" Reference photo: {base_input_desc}"
    return full.strip()

def cmd_list(args):
    stories = list(STORIES_DIR.glob("*.json"))
    print("Available story arcs:")
    for s in stories:
        if s.name == "schema.json": continue
        data = json.loads(s.read_text())
        print(f"  {s.name:30}  '{data.get('title')}'  ({data.get('genre')})  {len(data.get('beats',[]))} beats")

def cmd_prepare(args):
    story_path = Path(args.story)
    story = load_story(story_path)
    input_path = Path(args.input).resolve() if args.input else None

    print(f"# STORY PREPARE: {story['title']}")
    print(f"# Genre: {story['genre']} | Arc: {story.get('arc_type')}")
    print(f"# Base subject: {story['base_prompt'][:80]}...")
    if story.get("character_ancestry_bible"):
        print(f"# Ancestry Bible: present (full face/body/hair/skin/hominin details prepended to every beat)")
    print(f"# Input ref: {input_path or 'TBD'}")
    print(f"# Beats: {len(story['beats'])} | Target duration: {story.get('total_duration_sec')}s\n")

    for i, beat in enumerate(story["beats"], 1):
        full_p = build_beat_prompt(story, beat, str(input_path) if input_path else "")
        print(f"{i}. [{beat['beat_id']}] {beat['name']}  —  style: {beat['style_slug']} ({beat['source']})  [{beat['duration_sec']}s]")
        print(f"   Narrative: {beat['narrative_beat']}")
        print(f"   Prompt: {full_p[:220]}...")
        print(f"   Transition in: {beat.get('transition', 'n/a')}")
        print(f"   Ref strategy: {beat.get('ref_strategy', 'base_photo')}")
        print(f"   Target: stories/outputs/{story_path.stem}-{beat['beat_id']}.mp4 (or .jpg still)\n")

def cmd_plan(args):
    story_path = Path(args.story)
    story = load_story(story_path)
    print(json.dumps({
        "title": story["title"],
        "beats": [
            {
                "order": i+1,
                "beat": b["beat_id"],
                "style": b["style_slug"],
                "sec": b["duration_sec"],
                "ref": b.get("ref_strategy"),
                "transition": b.get("transition")
            } for i, b in enumerate(story["beats"])
        ],
        "post": "Use ffmpeg to concat the generated clips with crossfades according to transitions. Or ask Grok to generate a single longer video describing the full sequence."
    }, indent=2))

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list")
    p_list.set_defaults(func=cmd_list)

    p_prep = sub.add_parser("prepare")
    p_prep.add_argument("story", help="Path to story json e.g. stories/dusk-to-neon.json")
    p_prep.add_argument("--input", "-i")
    p_prep.set_defaults(func=cmd_prepare)

    p_plan = sub.add_parser("plan")
    p_plan.add_argument("story")
    p_plan.set_defaults(func=cmd_plan)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
