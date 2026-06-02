#!/usr/bin/env python3
"""
Unified sweep / batch helper for Grok Imagine (imagine project).

Supports:
- Official Grok Featured Templates (in featured_templates/)
- Extended style presets / film LUTs / VSCO / Pinterest / cinematic (in style_presets/)

Usage examples:
  python sweep.py list --source presets
  python sweep.py list --source all -v
  python sweep.py prepare --source presets --group film_emulation --input inputs/photo.jpg --prompt "A mysterious woman in a rainy alley at night"
  python sweep.py prepare --source featured --input inputs/photo.jpg
  python sweep.py status
  python sweep.py groups   # show categories for batching

The prepare command outputs ready-to-copy prompts for image_edit / video.
In this Grok CLI environment I can execute full batches for you (using image_edit + video_gen tools) and automatically place results in the correct */img/ and */vid/ folders.

Drop base photos in inputs/ (project root or featured_templates/inputs).
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

ROOT = Path(__file__).parent
FEATURED_DIR = ROOT / "featured_templates"
PRESETS_DIR = ROOT / "style_presets"
INPUTS_DIR = ROOT / "inputs"

def load_featured():
    f = FEATURED_DIR / "templates.json"
    if not f.exists():
        return []
    data = json.loads(f.read_text())
    return data.get("templates", [])

def load_presets():
    f = PRESETS_DIR / "styles.json"
    if not f.exists():
        return []
    data = json.loads(f.read_text())
    return data.get("presets", [])

def load_preset_prompt(slug: str) -> str:
    p = PRESETS_DIR / slug / "prompt.txt"
    if p.exists():
        return p.read_text().strip()
    return ""

def load_groups() -> Dict[str, List[str]]:
    f = PRESETS_DIR / "groups.json"
    if f.exists():
        return json.loads(f.read_text())
    # fallback build
    groups = {}
    for p in load_presets():
        groups.setdefault(p.get("category", "other"), []).append(p["slug"])
    return groups

def get_all_sources() -> List[Dict[str, Any]]:
    items = []
    for t in load_featured():
        items.append({
            "source": "featured",
            "slug": t["slug"],
            "display": t.get("display", t["slug"]),
            "category": t.get("category", "featured"),
            "path": FEATURED_DIR / t["slug"],
        })
    for p in load_presets():
        items.append({
            "source": "presets",
            "slug": p["slug"],
            "display": p.get("display", p["slug"]),
            "category": p.get("category", "preset"),
            "path": PRESETS_DIR / p["slug"],
        })
    return items

def cmd_list(args):
    if args.source in ("featured", "all"):
        featured = load_featured()
        print(f"=== Featured Templates ({len(featured)}) ===")
        for t in featured:
            line = f"  {t['slug']:28} {t.get('display','')[:28]:28} [{t.get('category','')}]"
            print(line)
            if args.verbose:
                print(f"      notes: {t.get('notes','')}")
        print()

    if args.source in ("presets", "all"):
        presets = load_presets()
        print(f"=== Extended Style Presets / LUTs ({len(presets)}) ===")
        groups = load_groups()
        if args.group:
            presets = [p for p in presets if p.get("category") == args.group or args.group in p.get("tags", [])]
        for p in presets:
            line = f"  {p['slug']:28} {p.get('display','')[:28]:28} [{p.get('category','')}]"
            print(line)
            if args.verbose:
                print(f"      tags: {', '.join(p.get('tags', []))}")
        print(f"\nAvailable groups for --group: {', '.join(sorted(groups.keys()))}")

    if args.source == "all":
        print("Total styles available for batching:", len(load_featured()) + len(load_presets()))

def cmd_groups(args):
    print("=== Preset Groups (for --group in prepare) ===")
    groups = load_groups()
    for g, slugs in sorted(groups.items()):
        print(f"{g}: {len(slugs)} presets")
        print("   " + ", ".join(slugs[:6]) + (" ..." if len(slugs)>6 else ""))
    print("\nFeatured is its own group.")

def cmd_status(args):
    print("Population status (non-.gitkeep files):\n")
    items = get_all_sources()
    if args.source != "all":
        items = [i for i in items if i["source"] == args.source]
    if args.group:
        items = [i for i in items if i.get("category") == args.group]

    for item in items:
        slug = item["slug"]
        base = item["path"]
        img_d = base / "img"
        vid_d = base / "vid"
        imgs = [f for f in img_d.glob("*") if f.name != ".gitkeep"] if img_d.exists() else []
        vids = [f for f in vid_d.glob("*") if f.name != ".gitkeep"] if vid_d.exists() else []
        src = item["source"][:3].upper()
        print(f"[{src}] {slug:28}  img:{len(imgs):3}  vid:{len(vids):3}")
    print(f"\nTotal items shown: {len(items)}")

def build_full_prompt(base: str, style_text: str, is_featured: bool, display: str) -> str:
    base = base.strip()
    if is_featured:
        return f'Apply the {display} featured template. {base} Keep faithful to the reference photo subject, identity, pose, clothing, lighting.'
    else:
        # extended LUT style
        return f'{base}. {style_text}. Preserve exact subject likeness, face, expression, pose, clothing, and key details from the reference image. High fidelity to input photo.'

def cmd_prepare(args):
    base_prompt = args.prompt or "Transform the subject into a compelling character while preserving identity, pose, clothing and core details from the photo."
    input_path = Path(args.input).resolve() if args.input else None

    if input_path and not input_path.exists():
        print(f"Warning: {input_path} does not exist yet. Prompts will still be generated.")

    items = get_all_sources()
    if args.source != "all":
        items = [i for i in items if i["source"] == args.source]
    if args.group:
        items = [i for i in items if i.get("category") == args.group or (args.source == "featured" and args.group in ("featured",)) ]

    print("#" * 70)
    print(f"# Grok Imagine BATCH PREPARE  | source={args.source} group={args.group or 'all'}")
    print(f"# Input photo: {input_path or 'inputs/YOUR_PHOTO.jpg (drop one here)'}")
    print(f"# Base prompt: {base_prompt}")
    print(f"# Generated: {datetime.now().isoformat()}")
    print(f"# Total styles in this sweep: {len(items)}")
    print("#" * 70 + "\n")

    print("INSTRUCTIONS:")
    print("  1. Copy a photo into inputs/ (or use absolute path).")
    print("  2. For each style below, ask me (Grok) or paste into grok.com/imagine:")
    print("     - Use image_edit (best for consistency) with the reference photo + the full prompt.")
    print("     - Or use the official template in UI for 'featured' ones.")
    print("  3. I can run the entire batch for you in one go if you say: 'run the full prepare sweep for inputs/photo.jpg with prompt \"...\" using source presets'")
    print("  4. Results will be saved to the matching <slug>/img/ and <slug>/vid/ .\n")

    for item in items:
        slug = item["slug"]
        display = item["display"]
        is_feat = item["source"] == "featured"
        style_text = load_preset_prompt(slug) if not is_feat else ""

        full_img = build_full_prompt(base_prompt, style_text, is_feat, display)

        print(f"## {display}  ({slug})  [{item['source']}/{item.get('category','')}]")
        print("### IMAGE")
        if input_path:
            print(f"image_edit( image=['{input_path}'], prompt=\"{full_img}\" )")
        else:
            print(f'prompt: "{full_img}"')
        print(f"Target folder: {item['path'].relative_to(ROOT)}/img/\n")

        # Video variant
        vid_add = "Create a short cinematic video clip (8-12s) with natural subtle motion, gentle camera move or subject action. " if not is_feat else "Animate with the template's signature motion. "
        full_vid = build_full_prompt(base_prompt, style_text, is_feat, display) + " " + vid_add + "Preserve likeness across frames."

        print("### VIDEO (image-to-video or template video)")
        if input_path:
            print(f'video_gen or image_to_video ref + prompt: "{full_vid}"')
        else:
            print(f'prompt: "{full_vid}"')
        print(f"Target folder: {item['path'].relative_to(ROOT)}/vid/\n")
        print("-" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Grok Imagine unified batch sweeper for featured + extended presets")
    sub = parser.add_subparsers(dest="cmd", required=False)

    # list
    p_list = sub.add_parser("list", help="List available styles")
    p_list.add_argument("--source", choices=["featured", "presets", "all"], default="all",
                        help="Which set of styles to operate on")
    p_list.add_argument("--group", help="Filter by category e.g. film_emulation")
    p_list.add_argument("-v", "--verbose", action="store_true")
    p_list.set_defaults(func=cmd_list)

    # prepare
    p_prep = sub.add_parser("prepare", help="Generate ready-to-use batch prompts for one photo + base prompt")
    p_prep.add_argument("--source", choices=["featured", "presets", "all"], default="all")
    p_prep.add_argument("--group", help="Filter by category e.g. film_emulation, pinterest_aesthetic, cinematic_genre")
    p_prep.add_argument("--input", "-i", help="Path to reference photo")
    p_prep.add_argument("--prompt", "-p", help="Base creative prompt (the story/subject part)")
    p_prep.set_defaults(func=cmd_prepare)

    # status
    p_stat = sub.add_parser("status", help="Count current outputs in img/vid across styles")
    p_stat.add_argument("--source", choices=["featured", "presets", "all"], default="all")
    p_stat.add_argument("--group", help="Filter by category")
    p_stat.set_defaults(func=cmd_status)

    # groups
    p_grp = sub.add_parser("groups", help="Show available --group filters")
    p_grp.set_defaults(func=cmd_groups)

    args = parser.parse_args()
    if args.cmd is None:
        parser.print_help()
        print("\nQuick start: python sweep.py prepare --source presets --group film_emulation -i inputs/my.jpg -p 'mysterious character'")
        return
    args.func(args)

if __name__ == "__main__":
    main()
