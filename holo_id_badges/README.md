# Holo ID Badges — Ancestory Lineage Iteration

Self-contained interactive prototype for holographic ID badge concepts.

## Usage
- **Primary UI:** [holo-viewer.html](../featured_templates/holo-skull-badge/holo-viewer.html#data-enrichment) (lineage enrichment sections consolidated there).
- `index.html` in this folder redirects to the viewer `#data-enrichment` anchor.
- Use timeline buttons, arrow keys, or "Random Stage" to iterate through 0-10 (Sahelanthropus → modern sapiens).
- Each card shows the **unified_migration_lineage** (the single "solid column" for genetic migration estimations).
- Copy bible snippets or full prompts for Grok Imagine (they lock face/body/bones from the fossil refs + pose/IK from Mixamo/Three.js guidance).
- "Generate Imagine Prompt" gives a ready-to-use string referencing exact casts (Bone Clones, Smithsonian 3D, Australian Museum).
- The Three.js canvas is a minimal skinning + additive blending demo (inspired by the linked example).

## Data Source
Full structured data lives in `../character_bibles/ancestory/hominin_data/hominin_lineage_timeline.json` (loaded subset here for standalone use). The JSON has per-stage:
- `unified_migration_lineage` (solid column)
- `fossil_refs` (direct links + specimen names)
- `bible_snippet` + `prompt_traits` (for madlibs / character_bibles)
- `mixamo_threejs` (rig/pose/shape/animation instructions)
- `genetic_admixture_estimates`

## Holo Concepts
References the provided links for visual language (iridescent glass cards, floating 3D ancestor portraits, timeline scrubbing, genetic viz).

Production flow:
1. Use a stage's bible_snippet + fossil ref in Imagine (with style_preset e.g. kodak-portra or panavision).
2. Generate "holographic ID badge, iridescent, spline 3D, floating portrait of [stage]" variations.
3. Composite or import into Spline (or Three.js + the Mixamo FBX) for true interactive holo badge with scrubber over the lineage column.
4. Repeat verbatim bible for series consistency across "ancestor cards".

## Integration
- Pairs with `character_bibles/ancestory/` (madlibs + traits + this lineage JSON).
- Tags now in `pot/` (hominin_ancestry, fossil_refs, mixamo_threejs, holo_id_badge, lineage_migration).
- Use in `stories/*.json` or `sweep.py` / `story.py` outputs by injecting the appropriate stage bible.

Run `python3 -m http.server` in this folder for local testing if needed.

All the way from 7mya fossil casts to modern Mixamo-rigged + Three.js blended holograms.
