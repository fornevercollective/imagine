# imagine

Grok Imagine workspace for rapid style iteration and narrative video construction.

Live at: https://github.com/fornevercollective/imagine

See the genre/story menu + research overview at https://fornevercollective.github.io/overview/

## What this is

A structured library + tooling to:

1. **Batch one photo through dozens of styles** — both the official Grok "Featured Templates" and a large set of **extended prompt-based presets** (VSCO film emulations, Pinterest core aesthetics, cinematic genre LUTs / color grades).

2. **Tell stories that move through styles** — define story arcs with thematic beats. Generate (or assemble) a single flowing video where the visual language (film stock / LUT / aesthetic) changes in service of the narrative, with strong continuity on character/subject.

Everything lives in clean folder-per-style with `img/` and `vid/` so you can iterate fast, review, and keep outputs organized.

## Current structure

```
imagine/
├── featured_templates/          # The 23 official Grok UI Featured Templates (Chibi, Funky Dance, etc.)
│   ├── <slug>/
│   │   ├── img/
│   │   └── vid/
│   ├── sweep.py                 # (legacy) featured-only helper
│   └── templates.json
│
├── style_presets/               # 38+ extended LUT / aesthetic presets (the main expansion)
│   ├── <slug>/                  # e.g. kodak-portra-400, dark-academia, cyberpunk-neon, teal-orange-blockbuster...
│   │   ├── prompt.txt           # The exact style/LUT text to append to your prompt
│   │   ├── meta.json
│   │   ├── img/
│   │   └── vid/
│   ├── styles.json              # Full manifest
│   └── groups.json              # film_emulation | pinterest_aesthetic | cinematic_genre
│
├── stories/
│   ├── schema.json
│   ├── dusk-to-neon.json        # Example: 7-beat neo-noir → cyberpunk transformation arc
│   └── outputs/                 # Final stitched or per-beat videos land here
│
├── sweep.py                     # The main unified sweeper (featured + presets + groups)
├── story.py                     # Story arc loader / prepare / plan
├── inputs/                      # Drop your reference photo(s) here
├── create_style_presets.py      # Reproducible generator for the preset tree
└── README.md
```

## Quick start – batch one image through many styles

```bash
# See everything
python sweep.py list --source all

# Or just the film looks
python sweep.py list --source presets --group film_emulation

# Prepare prompts for a whole group (or all presets)
python sweep.py prepare --source presets --group cinematic_genre \
  -i inputs/my_photo.jpg \
  -p "a mysterious woman in a rainy alley at night, carrying a small glowing package"

# Same but using only official featured templates
python sweep.py prepare --source featured -i inputs/my_photo.jpg -p "..."
```

Then paste the generated blocks to me (or grok.com). I can execute large batches using the Imagine tools and drop results straight into the target `.../img/` and `.../vid/` folders for you.

## Quick start – story arcs that flow through styles

```bash
python story.py list
python story.py prepare stories/dusk-to-neon.json -i inputs/my_photo.jpg
python story.py plan stories/dusk-to-neon.json
```

Tell me: "render the dusk-to-neon story using inputs/hero.jpg" and I'll walk the beats, generate the clips (chaining image references for character consistency), and either hand you the concat command or assemble the final video.

The example story "Dusk to Neon" takes one character from warm Kodak Portra daylight → dark academia → classic neo-noir rain → full cyberpunk neon → blockbuster teal-orange climax → warm golden resolution → final vintage 35mm tag. All while advancing a 3-act mini-narrative with clear thematic beats.

## Adding more presets

Edit `create_style_presets.py` (the big `PRESETS` list), add your new film stock / aesthetic / LUT, then re-run:

```bash
python create_style_presets.py
```

New folders + prompt.txt + meta will be created. Update `sweep.py` / `story.py` if you add wild new categories.

## Tips for best results with one photo

- For **maximum likeness** across wildly different styles: use `image_edit` (reference photo) + very explicit "preserve exact face, clothing, pose, package, silver streak in hair..." in every prompt. The continuity_notes in story JSONs do this.
- For **video**: start with image-to-video on the styled still, or let the official template handle motion. Ask for "subtle cinematic camera move, 8-12 seconds".
- Chaining refs (previous clip's last frame or last still) dramatically helps consistency when the style changes drastically.
- VSCO/film presets love subtle grain + halation language. Cinematic ones love anamorphic flares, teal-orange, etc.
- Pinterest aesthetics are mood + color + texture first — describe the world/lighting more than "in the style of".

## Relation to https://fornevercollective.github.io/overview/

That is the live "genre & story format / menu". Use the research overview to pick or invent new arcs, then encode them as story JSONs here. The visual research (moodboards, references) can be generated using the exact presets in this repo.

## Git + contribution

This repo is intentionally lightweight — mostly the folder tree + prompt text + story definitions. The actual heavy assets (your generated images/videos) can be .gitignored or kept in a media/ or LFS if desired.

Current focus:
- Expand the preset library (more obscure film stocks, more niche Pinterest cores, more specific movie LUT homages without direct IP).
- More story examples (different arc shapes, multi-character, music-video style, horror escalation, etc.).
- Better automation for concat + basic audio sweetening.

Run `python sweep.py status` or `python story.py ...` after any generation session to see what you have.

Let's make some beautiful flowing style videos.
