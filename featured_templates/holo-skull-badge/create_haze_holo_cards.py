#!/usr/bin/env python3
"""
Haze Holo Card Prompt Generator for Grok Imagine (to match manual Haze Portrait + multi-template process).

For ancestry (hominin/person variations) and sports teams.

This generates ready-to-paste prompts for Grok Imagine (using the Haze Portrait featured template + sunny-morning/professional-headshot/quality-enhancer/glossy-product-shot + duplication + vertical axis flip + multi-exposure + blur/stretch sides + combine into Holographic ID/Playing Card using Product Showcase / holo framing).

The prompts include the user's specific content/prompt (ancestry traits or sports team prompt) built in.

The process replicates the manual Grok Imagine workflow the user described:
- Apply Haze Portrait for cinematic chromatic haze, soft double-exposure chromatic offset, dreamy optic.
- Duplicate the image, flip the copy on the vertical axis.
- Multi-exposure edit the copy with the other styles for the blurred stretched haze sides of the center photo.
- Center uses the regular iridescent variation.
- Frame as larger combined playing/collectors/character card with pronounced holo effect for blue/red glasses.

Run: python3 create_haze_holo_cards.py --all
This will create prompt-*.txt files in the 00.haze/00.prompts/ subfolder for each slug.

Then, for each, upload the corresponding regular variation (e.g. neanderthal-person.jpg from 01.persons/) as reference image to Grok Imagine, paste the prompt, generate the haze holo card.

The target is ancestry (current skull/person variations) and sports teams (create analogous "team" data with headshot refs and team-specific prompts for player/trading/collector cards).

Once generated, put the output jpgs in variations/00.haze/02.id-holo/{slug}-haze-holo-card.jpg and the deck will pick them up for the larger combined cards.
"""

import os
import json
import argparse

BASE_DIR = 'featured_templates/holo-skull-badge'
VARIATIONS_DIR = os.path.join(BASE_DIR, 'img', 'variations')
PERSONS_DIR = os.path.join(VARIATIONS_DIR, '01.persons')
HAZE_DIR = os.path.join(VARIATIONS_DIR, '00.haze')
SKULL_TYPES_PATH = os.path.join(BASE_DIR, 'data', 'skull_types.json')

os.makedirs(os.path.join(HAZE_DIR, '00.prompts'), exist_ok=True)

HAZE_PORTRAIT_BASE = """Apply the Haze Portrait featured template. Transform the person in the input image into a cinematic chromatic haze portrait of the same person... subtle three-quarter side portrait... soft double-exposure-like chromatic offset... dreamy optic. Use additional styles from sunny-morning, professional-headshot, quality-enhancer, glossy-product-shot for the haze effect, lighting, and dreamy optic."""

COMBINE_INSTRUCTIONS = """
Duplicate the resulting hazy image. Flip the copy on the vertical axis (horizontal mirror). Apply multi-exposure editing, blur and stretch to create a blurred stretched version of both sides of the center photo for the left and right side panels, with chromatic haze and offset for a really pronounced holographic effect when viewed with blue/red 3D glasses.

Keep the center as the sharp regular variation with iridescence from the regular (non-haze) version.

Combine the center regular iridescent variation with the left and right haze side panels into a larger combined Holographic ID/Playing Card / collectors / character card.

Use the Product Showcase featured template (or Holo Skull Badge template) for the framing of the entire wide card: glossy iridescent holographic glass-like material with rainbow refraction, scanlines, floating 3D depth, as a premium collectible playing/collectors/character card.

Preserve the exact identity, face shape, proportions, skin tone, hair, expression, and head size/scale from the reference photo 100% in the center and overall.

The final image should be a wide larger card (approximately 16:9 or 2:1 aspect) suitable for a holographic playing/collectors/character card.

Add text framing: top header "HOLO HAZE • [DISPLAY] • [SPECIMEN_ID]", bottom footer with era, unified migration lineage or team info, traits, and key prompt excerpt.
"""

def build_haze_prompt(type_info, is_sports=False):
    """Build the full prompt incorporating the user's content/prompt."""
    display = type_info.get("display", type_info["slug"])
    specimen = type_info.get("specimen_id", "")
    era = type_info.get("era", "")
    traits = type_info.get("traits", "")
    prompt_add = type_info.get("prompt_addition", type_info.get("description", ""))

    if is_sports:
        content = f"Sports team / player collector card for {display} (team/player: {specimen}). {prompt_add} {traits}."
    else:
        content = f"Ancestry / hominin variation: {display} ({specimen}), {era}. {prompt_add} {traits}. Accurate to fossil refs like Bone Clones, Smithsonian 3d.si.edu, Australian Museum."

    title = f"HOLO HAZE • {display} • {specimen}"
    footer = f"{era} | {traits}"
    prompt = f"""{HAZE_PORTRAIT_BASE}

{content}

{COMBINE_INSTRUCTIONS}

Specific for this card: {content}

Use this exact text for the card framing:
Top header: "{title}"
Bottom footer: "{footer} | {prompt_add[:100]}..."
"""
    return prompt.strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', help='Specific slug')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--sports', action='store_true', help='Treat as sports teams data (use different data file if exists)')
    args = parser.parse_args()

    data_path = SKULL_TYPES_PATH
    if args.sports:
        sports_path = os.path.join(BASE_DIR, 'data', 'sports_teams.json')
        if os.path.exists(sports_path):
            data_path = sports_path
        else:
            print("No sports_teams.json yet. Using skull_types as example. Create one with similar structure for your sports team player headshots and team prompts.")
            # For now fall back, user can provide headshots later.

    with open(data_path) as f:
        data = json.load(f)
    types = data.get('skull_types', data.get('types', data.get('teams', [])))

    if args.slug:
        types = [t for t in types if t.get('slug') == args.slug or t.get('team') == args.slug]
        if not types:
            print("Slug not found")
            return

    for t in types:
        slug = t.get('slug', t.get('team', 'unknown'))
        prompt = build_haze_prompt(t, is_sports=args.sports or 'team' in t)

        out_path = os.path.join(HAZE_DIR, '00.prompts', f"{slug}-haze-prompt.txt")
        with open(out_path, 'w') as f:
            f.write(prompt)
        print(f"Created prompt for {slug}: {out_path}")

        # Also print the ref image to use
        ref = os.path.join(PERSONS_DIR, f"{slug}-person.jpg")
        if not os.path.exists(ref):
            ref = t.get('base_ref', 'your-headshot.jpg or the regular variation')
        print(f"  -> Upload ref: {ref} to Grok Imagine with the prompt above to generate the haze holo card.")
        print(f"  -> Save output as {slug}-haze-holo-card.jpg in the 00.haze/02.id-holo/ folder.")
        print()

    print("\nDone. These prompts are built with the user's content/prompt (ancestry or sports team) + the exact Haze Portrait + duplication/flip/multi-exposure/blur/stretch sides + holo card combine process you described from your manual Grok Imagine sessions.")
    print("This will produce the same cinematic chromatic haze dreamy optic double-exposure effect as your manual ones, not the local PIL approximation.")
    print("Target: ancestry (current) and sports teams (create sports_teams.json with player refs and team prompts for collector/trading cards).")

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
