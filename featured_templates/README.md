# Grok Imagine Featured Templates (subset)

The 23 official templates from grok.com/imagine.

**Prefer the root `sweep.py` and `style_presets/` for most work** — they give you way more granular VSCO/film/Pinterest/cinematic control + story arcs.

This subdir is kept for direct "one-click template" usage in the Grok UI and for legacy compatibility.

Use `python ../sweep.py prepare --source featured ...` from the project root for unified batching that also includes the extended presets.

## Structure

```
featured_templates/
├── inputs/                 # Drop your source photo(s) here (e.g. photo.jpg)
├── <template-name>/        # One folder per featured template
│   ├── img/                # Generated stills / edited images for this style
│   └── vid/                # Generated videos / animations for this style
├── README.md
└── templates.json          # Machine-readable list of all templates
```

## Current Featured Templates (23)

1. chibi
2. professional-headshot
3. logo-editor
4. 70s-street-style
5. quality-enhancer
6. comic-book
7. object-remover
8. product-showcase
8b. holo-skull-badge (custom — Product Showcase framing for holographic skull/bone/skeleton ancestor ID badge reveals using ancestry lineage data; turnkey for digital playing card decks). Open `holo-skull-badge/holo-viewer.html` to browse the assets, videos, lineage data, and prompt.
9. glossy-product-shot
10. 80s-anime
11. watercolor-portrait
12. video-game
13. 3d-animation
14. spaghetti-western
15. haze-portrait
16. funky-dance
17. future-past
18. roman-empire
19. ad-astra
20. add-girlfriend
21. future-family
22. laser-fight
23. sunny-morning

## How to quickly iterate one photo across all styles

1. Put your source image in `inputs/` (e.g. `inputs/my_photo.jpg`).
2. Decide on a **base prompt** describing the desired transformation or scene (the template will supply the style).
3. Ask Grok (in this CLI or on grok.com) to generate for each template, e.g.:
   - "Using the photo at inputs/my_photo.jpg, apply the Chibi template style. Save the image output to chibi/img/ and if it produces video also to chibi/vid/. Base prompt: <your prompt here>"
   - Repeat for other templates (or ask me to batch a few at a time).
4. For video-focused: many templates animate the photo; request video output explicitly.

### Using me (Grok in this session) to generate

I have direct access to Imagine via tools:
- `image_gen` (text-to-image)
- `image_edit` (image-to-image with reference photo + prompt; perfect for templates)
- `video_gen` (text-to-video; for img2vid you may describe the input or use follow-up edits)

Example request:
"Take the photo in inputs/photo.jpg and generate a version in 'Funky Dance' style using image_edit. Place the result in funky-dance/img/. Then generate a matching short video into funky-dance/vid/."

I can do multiple in parallel by calling tools together, then move the generated files (from session caches) into the target subfolders for you.

### Manual workflow (grok.com / app)

- Go to grok.com/imagine (or the Imagine tab).
- Select a Featured Template (Chibi, Funky Dance, etc.).
- Upload your photo from `inputs/`.
- Enter an optional additional prompt / instruction.
- Generate image(s) and/or video.
- Download and drop the results into the matching `<template>/img/` or `/vid/`.

## Tips for good results with one photo + style sweep

- Keep the **subject / composition** description consistent across runs.
- Let the template name drive the **style** (e.g. don't over-specify "in chibi style" if using the Chibi template).
- For video: start with image-to-video via the template, or add motion instructions like "gentle camera push in, subtle head movement".
- Use `inputs/` variants (different crops, lighting refs) for A/B testing a prompt.
- After a batch, review in `*/img/` and `*/vid/`, then refine the shared prompt and re-run only the weak ones.

## Updating the list

If new Featured Templates appear on grok.com/imagine, add matching folders + update this README + templates.json.

Run `ls -d */ | grep -v inputs` to see current template folders.

## templates.json

See templates.json for a scriptable list (name + display name + suggested category hints).

Happy style-sweeping! 🚀

## Batch Runs & Editor Contact Sheet (2026-06-02)

This directory now contains a full batch run across all 23 featured templates using the master watercolor reference character (rugged man, top knot, silver beard, glasses, denim + camo).

- `batch-runs/FT-2026-0602-prepare.txt` — Complete ready-to-paste `image_edit` + video prompts for the entire batch (from `python ../sweep.py prepare --source featured`).
- `batch-runs/FT-2026-0602-metadata.json` — Per-template timing (seconds), cost factor (relative), image/video counts, status, and aggregates (total time ~6min, ~29× cost factor, 25+ outputs in this run).
- `proof-sheet.html` — The repeatable photographer’s contact sheet / Vogue-style editorial proof sheet. Open in any browser. Film negative aesthetic + editor comment fields + exportable JSON log for feeding feedback back to Grok or other users.

**How to reuse / repeat:**
1. Drop a new reference photo in `inputs/`.
2. `python ../sweep.py prepare --source featured -i inputs/your.jpg -p "your base description..."`
3. Run the suggested `image_edit` calls (or ask Grok "run the full featured batch").
4. `python make_proof_sheet.py` — regenerates `proof-sheet.html` with fresh thumbs, times, and the new editor notes area.

The proof sheet is deliberately designed as a portable artifact: copy the whole `featured_templates/` tree (or just the HTML + the relevant `*/img/` folders) into new projects. The editor JSON export is perfect context for the next Grok session ("Here is the marked-up proof sheet...").

See root `sweep.py` for the unified version that also sweeps the extended style_presets/.

**Current batch aggregates (as of last make_proof_sheet.py run):**
- Total development time: ~362s
- Images produced: 25 (bases + developed proofs)
- Est. relative cost factor: 29.1×
