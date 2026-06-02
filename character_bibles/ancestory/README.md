# Ancestory Character Bibles

Detailed anatomical, hair, body morphology, and hominin ancestry descriptors for Grok Imagine.

See https://fornevercollective.github.io/ancestory/ for the source research/charts.

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
