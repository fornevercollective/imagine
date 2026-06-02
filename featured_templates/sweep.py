#!/usr/bin/env python3
"""
Quick sweep helper for Grok Imagine Featured Templates.

Usage:
  python sweep.py list
  python sweep.py prepare --input inputs/photo.jpg --prompt "your base prompt here"

The script lists templates and can prepare per-style prompt suggestions.
When ready to generate, paste the suggestions into chat with Grok (this CLI supports direct image_edit/video_gen tool calls and will place results in the correct img/vid folders).

Drop source photos in inputs/.
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
TEMPLATES_FILE = ROOT / "templates.json"
INPUTS_DIR = ROOT / "inputs"


def load_templates():
    with open(TEMPLATES_FILE) as f:
        data = json.load(f)
    return data["templates"]


def cmd_list(args):
    templates = load_templates()
    print(f"Featured Templates ({len(templates)}):\n")
    for t in templates:
        print(f"  {t['slug']:25}  {t['display']:25}  [{t['category']}]")
        if args.verbose:
            print(f"    notes: {t['notes']}")
    print("\nFolders already exist with img/ + vid/ for each.")


def cmd_prepare(args):
    templates = load_templates()
    input_path = Path(args.input).resolve() if args.input else None
    base_prompt = args.prompt or "Transform the subject while preserving identity, pose, and key details."

    if input_path and not input_path.exists():
        print(f"Warning: input {input_path} not found. Still generating prompt suggestions.")

    print("# Prepared sweep prompts for one photo across all styles")
    print(f"# Input: {input_path or 'YOUR_PHOTO.jpg'}")
    print(f"# Base prompt: {base_prompt}")
    print(f"# Generated: {datetime.now().isoformat()}\n")
    print("Copy/paste these (or ask me in chat to run the whole sweep):\n")

    for t in templates:
        slug = t["slug"]
        display = t["display"]
        print(f"## {display} ({slug})")
        print(f"### Image")
        if input_path:
            print(f"Use image_edit on {input_path} with prompt:")
        print(f'  "Apply the {display} featured template. {base_prompt} Keep faithful to the reference photo subject."')
        print(f"Target: {slug}/img/\n")

        print(f"### Video (if the template supports motion or you want animation)")
        print(f'  "Using the photo + {display} style, create a short video. {base_prompt} Add natural motion."')
        print(f"Target: {slug}/vid/\n")
        print("-" * 60 + "\n")


def cmd_status(args):
    templates = load_templates()
    print("Current population status (count of files in img/ and vid/):\n")
    for t in templates:
        slug = t["slug"]
        img_dir = ROOT / slug / "img"
        vid_dir = ROOT / slug / "vid"
        imgs = [f for f in (img_dir.glob("*") if img_dir.exists() else []) if f.name != ".gitkeep"]
        vids = [f for f in (vid_dir.glob("*") if vid_dir.exists() else []) if f.name != ".gitkeep"]
        print(f"{slug:25}  img: {len(imgs):3}   vid: {len(vids):3}")
    print("\n(Files excluding .gitkeep.)")


def main():
    parser = argparse.ArgumentParser(description="Grok Imagine Featured Templates sweep helper")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List all templates")
    p_list.add_argument("-v", "--verbose", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_prep = sub.add_parser("prepare", help="Print ready-to-use per-template prompts for a sweep")
    p_prep.add_argument("--input", "-i", help="Path to source photo (in inputs/ or elsewhere)")
    p_prep.add_argument("--prompt", "-p", help="Base prompt to apply on top of each template style")
    p_prep.set_defaults(func=cmd_prepare)

    p_stat = sub.add_parser("status", help="Show how many outputs currently in each style's folders")
    p_stat.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if args.cmd is None:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
