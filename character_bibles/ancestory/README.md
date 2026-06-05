# Ancestory Character Bibles

Detailed anatomical, hair, body morphology, and hominin ancestry descriptors for Grok Imagine.

See https://fornevercollective.github.io/ancestory/ for the source research/charts.

**New deep-time expansion**: `hominin_data/hominin_lineage_timeline.json` (full face/body/bones/IK/poses/shapes + historical timeline with "one solid column" `unified_migration_lineage` per stage, fossil refs to the exact 3D collections, Mixamo/Three.js guidance, prompt bibles). Use for iterating genetic migration lineage estimations from Sahelanthropus ~7mya through erectus exodus, Neanderthal/Denisovan, early sapiens OOA, to modern regional + admixture.

Holo ID badge prototypes in sibling `holo_id_badges/` (self-contained HTML that loads/iterates the lineage for card concepts matching the Spline/IG references).

**Turnkey holo skull/bone playing cards**: See `../featured_templates/holo-skull-badge/` (uses Product Showcase template framing + the exact user video refs for holo pan style + generated examples from the provided headshot). Run `python ../create_holo_badge_deck.py --headshot YOUR_HEADSHOT.jpg --stage random --count 10 --out my-deck/` to batch a full deck. Each card includes the unified migration lineage solid column, accurate fossil skull/bones from the timeline JSON, and ready prompts. Perfect repeatable metric for digital collectible ancestor cards.

## Files

- `ancestry_traits.json`: Structured options and examples for all categories (face shapes, hair micro/macro by body zone, body shapes with hominin variations, skin subsurface + tiger stripes + melanin/irradiance science).
- `ancestry_bible_madlibs_template.md`: Ready-to-use fill-in-the-blank template to drop into prompts or expand the main project madlibs.

## Integration

Use these to flesh out the [MASTER CHARACTER BIBLE] block in the main `/README.md` madlibs outline and in `stories/*.json`.

Always repeat the filled bible verbatim for cross-style / cross-beat consistency (face, body proportions, hair patterns, skin subsurface behavior).

Combine with `../style_presets/` for the "look" (LUT, lens, grain, edit feel) while these control the "who" (the physical person from the hominin tree).

## Quick Example Usage in a Prompt

Take any output from `sweep.py prepare` or `story.py`, then prefix or replace the subject description with the full filled Ancestry + Anatomy Bible from the template.

Example full prompt starter:
"[MASTER ANCESTRY + ANATOMY BIBLE... full filled text from the madlibs] ... [rest of style/LUT/camera/action from preset or story beat]"

This gives production-level control over diversity and realism while leveraging the cinematic power of the existing presets and story arcs.

Add more traits to the JSON as the ancestory research expands.
