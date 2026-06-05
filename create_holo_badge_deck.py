#!/usr/bin/env python3
"""
Turnkey Holo Ancestor Badge / Digital Playing Card Deck Creator
Uses Product Showcase featured template + ancestry lineage for accurate skull/bone reveals.

Usage examples:
  python create_holo_badge_deck.py --headshot 0/grok-image-651d93c1-202b-4cc5-b642-1927af80d4c6.jpg --stage 7 --out holo-deck/
  python create_holo_badge_deck.py --headshot inputs/person.jpg --stage random --count 5

It outputs:
- Ready-to-paste full prompt for Grok Imagine (select "Product Showcase" template, upload headshot, paste prompt).
- Per-card JSON with lineage data (the "solid column"), bible used, fossil refs.
- Suggested file layout in out_dir/ for the generated img/vid.
- Optional: basic HTML index for the deck (viewable digital cards).

Requires the hominin_lineage_timeline.json from character_bibles/ancestory/hominin_data/
"""

import argparse
import json
import random
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
LINEAGE_PATH = ROOT / "character_bibles/ancestory/hominin_data/hominin_lineage_timeline.json"
HOLO_TEMPLATE_DIR = ROOT / "featured_templates/holo-skull-badge"
PRODUCT_SHOWCASE = "Product Showcase"

def load_lineage():
    with open(LINEAGE_PATH) as f:
        return json.load(f)

def get_stage(data, stage_arg):
    stages = data["stages"]
    if stage_arg == "random":
        return random.choice(stages)
    try:
        idx = int(stage_arg)
        return next(s for s in stages if s["stage_index"] == idx)
    except:
        return stages[7]  # default Neanderthal for dramatic skull

def build_prompt(stage, headshot_path, data):
    bible = stage.get("bible_snippet", "")
    fossil = stage.get("fossil_refs", "real fossil hominin reconstruction from Bone Clones / Smithsonian 3D / Australian Museum")
    migration = stage.get("unified_migration_lineage", "")
    era = stage.get("era", "")
    name = stage.get("name", "")

    prompt = f"""Apply the {PRODUCT_SHOWCASE} featured template.

[PRESET GOAL: Premium holographic ancestor ID badge / digital playing card in clean Product Showcase framing. The skull MUST match the input headshot's exact size and shape.]

CRITICAL: Analyze the uploaded headshot photo first to estimate the real skull:
- Cranial height/width ratio, overall head shape, brow projection, jaw width/angle, temple width, etc.
- The revealed skull must be precisely morphed/scaled to fit those measurements exactly (like a real anatomical underlayer for this specific person). Do not use a generic skull.

The card has glossy iridescent holographic glass material with rainbow refraction, scanlines, floating 3D depth.

Sequence (video especially): clear headshot portrait -> shimmering holo left pan/morph revealing the photo-accurate skull (with hominin fossil traits from the stage below, but proportions forced to match the photo) -> continued pan to upper skeleton/bones in the same holo style.

Use precise hominin fossil anatomy: {fossil}. {bible}

Motion: 5-7s smooth cinematic left pan matching the reference holo skull pan video style in the preset folder. High production value.

Stills: finished holographic badge in perfect Product Showcase product photography (centered, soft studio lighting, clean backdrop).

Reference photo likeness 100% locked in the portrait state. Holo/bone layers are stylistic transparent reveals only.

Stage for traits: {name} ({era}). Solid lineage column: {migration}

Small text: {name} • {era}"""

    return prompt.strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headshot", required=True, help="Path to headshot ref photo (jpg/png)")
    parser.add_argument("--stage", default="random", help="Stage index (0-10), 'random', or specific number from lineage")
    parser.add_argument("--out", default="holo-deck", help="Output directory for prompts and layout")
    parser.add_argument("--count", type=int, default=1, help="Number of cards to prepare (cycle stages if >1)")
    args = parser.parse_args()

    data = load_lineage()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    headshot = Path(args.headshot)
    if not headshot.exists():
        print(f"Warning: headshot {headshot} not found. Using placeholder in prompts.")

    print(f"Preparing {args.count} holo badge card(s) using Product Showcase + ancestry lineage...\n")

    cards = []
    stages = data["stages"]

    for i in range(args.count):
        if args.count > 1:
            stage = stages[i % len(stages)]
        else:
            stage = get_stage(data, args.stage)

        prompt = build_prompt(stage, headshot, data)

        card = {
            "card_id": f"card-{datetime.now().strftime('%Y%m%d')}-{i:03d}",
            "headshot_ref": str(headshot),
            "stage_index": stage["stage_index"],
            "stage_name": stage["name"],
            "era": stage["era"],
            "unified_migration_lineage": stage["unified_migration_lineage"],
            "genetic_admixture": stage.get("genetic_admixture_estimates", stage.get("admixture", "")),
            "fossil_refs": stage.get("fossil_refs", ""),
            "prompt_for_grok_imagine": prompt,
            "usage": f"1. In Grok Imagine / grok.com/imagine select the '{PRODUCT_SHOWCASE}' featured template.\n2. Upload the headshot ref.\n3. Paste the prompt above as the additional instruction.\n4. Generate image first (for the card still), then request video for the holo pan sequence.\n5. Save outputs to {out_dir / f'card-{i:03d}'}/img/ and /vid/",
            "lineage_data": stage
        }
        cards.append(card)

        # Write per-card files
        card_dir = out_dir / f"card-{i:03d}"
        card_dir.mkdir(exist_ok=True)
        (card_dir / "prompt.txt").write_text(prompt)
        (card_dir / "card.json").write_text(json.dumps(card, indent=2))

        print(f"Card {i}: Stage {stage['stage_index']} - {stage['name']}")
        print(f"  Solid column: {stage['unified_migration_lineage'][:100]}...")
        print(f"  Prompt written to {card_dir / 'prompt.txt'}")
        print(f"  Ready for Grok Imagine Product Showcase + this prompt + the headshot.\n")

    # Deck index
    deck_meta = {
        "deck_name": "Holo Ancestor Playing Cards",
        "created": datetime.now().isoformat(),
        "headshot_source": str(headshot),
        "num_cards": len(cards),
        "lineage_source": str(LINEAGE_PATH),
        "cards": [{"id": c["card_id"], "stage": c["stage_index"], "name": c["stage_name"]} for c in cards]
    }
    (out_dir / "deck.json").write_text(json.dumps(deck_meta, indent=2))

    # Simple HTML viewer stub (copy from holo_id_badges or minimal)
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Holo Deck</title>
<style>body{{font-family:system-ui;background:#111;color:#eee;padding:20px}} .card{{background:#1a1d24;margin:10px;padding:10px;border-radius:8px}} </style>
</head><body>
<h1>Holo Ancestor Deck</h1>
<p>Generated from headshot: {headshot.name} — {len(cards)} cards using Product Showcase + hominin lineage.</p>
"""
    for c in cards:
        html += f"<div class='card'><strong>{c['stage_name']}</strong> ({c['era']})<br><small>{c['unified_migration_lineage']}</small><br><pre style='font-size:10px'>{c['prompt_for_grok_imagine'][:300]}...</pre></div>"
    html += "</body></html>"
    (out_dir / "deck.html").write_text(html)

    print(f"Deck prepared in {out_dir}/")
    print(f"- deck.json + deck.html for overview")
    print(f"- Each card-XXX/ has prompt.txt and card.json with full lineage data (the solid column)")
    print("For automatic haze holo combined cards (dupe regular var, vertical flip, blur+stretch sides for anaglyph red/blue 3D holo + iridescence center, prompt built-in):")
    print("  python3 featured_templates/holo-skull-badge/create_haze_holo_cards.py --all")
    print("  Then load the full deck in holo-viewer.html — it will prefer the *haze-holo-card.jpg images for the larger combined collector cards.")
    print("\n=== IMPORTANT: View the cards properly ===")
    print("Do NOT open the HTML files directly as file:/// (images/videos/3D will be empty or broken).")
    print("Best: cd into the output folder and run:")
    print(f"  cd {out_dir}")
    print("  python ../featured_templates/holo-skull-badge/launch-viewer.py")
    print("Or from imagine root:")
    print("  python -m http.server 8000")
    print("Then open:")
    print(f"  http://localhost:8000/{out_dir}/deck.html   (or the holo-viewer.html in the template folder)")
    print("\nOpen deck.html or use the prompts directly in Grok Imagine with Product Showcase template + your headshot upload.")
    print("For video pans: after image, ask for video version using the same prompt + 'animate the holo left pan sequence matching the reference video styles'.")
    print("Repeat for new headshots to build the full playing card deck metric.")

if __name__ == "__main__":
    main()
