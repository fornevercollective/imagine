# Agent Prompts

Self-contained, project-aware super prompts designed to be pasted into Grok (chat or Imagine) along with a reference image + the repo link.

## superheavy_grok_imagine_repo_aware.md

The main one. It instructs Grok to:

- Browse the live GitHub (raw README, character_bibles/ancestory JSON + madlibs template, style_presets manifests, stories, etc.).
- Analyze the attached image using **every** system in the repo (full ancestry + anatomy bible with face shapes, micro/macro hair by face/upper torso/lower torso/under arms/legs, body shapes + hominin tree relations, subsurface IR tiger stripes, melanin dispersion + irradiance refraction %, etc.).
- Build perfect, locked prompts following the madlibs + character bible frameworks + all the film technical language (LUTs, lenses + distortions, grain/weave/dirt, edit timeline concepts like J/L-cuts, etc.).
- Choose appropriate `style_presets/` or build story arcs.
- Explicitly output the **appropriate paths** in the project structure so you can organize results correctly (e.g. `style_presets/kodak-vision3-500t/img/`, `stories/my-arc/outputs/`, etc.).
- Maintain maximum consistency by repeating the full ancestry bible verbatim.

Usage (paste + image + `repo: https://github.com/fornevercollective/imagine`).

This is the "yes" to the question of whether Grok Imagine + a superheavy agent prompt can read the GitHub project, infer everything, and make the appropriate path/prompt based on an image + the repo link.

Future agent prompts for specific workflows can live here.