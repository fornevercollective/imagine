# Point of Truth (PoT): Film Genres • Literary Parallels • AI Content Provenance

**Source**: Pulled / reconstructed from https://grok.com/share/bGVnYWN5LWNvcHk_99ba3a1a-72bf-4ec1-96c9-bf9e145e8665  
**Title of source convo**: Film Genres: Literary Parallels Timeline  
**User intent (from meta)**: "that's every film/video/gif/stream of content tag through all this document in a downloadable format"

This directory is the **canonical point-of-truth** for tags, taxonomies, timelines, and the full provenance/psychological loop of turning real-life source material (photo shoots with full EXIF + notes) into AI-generated concept content (images, video, gifs, streams, film emulations, style presets, etc.).

## Purpose
- Single source of truth for all classification tags used in this imagine repo and Grok Imagine workflows.
- Traceability from **real life → photo shoot (EXIF) → reference assets → literary/film parallel selection → prompt engineering → generation → iteration → final**.
- Easy iteration: edit master data → re-run generator → all formats (md/js/json/py/txt/csv/xlsx/binary/html) update.
- Conceptual model of the "psychological loop" of AI-assisted creative content making.

## Contents
- `pot.json` — Master canonical data (edit this).
- `pot.yaml` — YAML mirror (if generated).
- `exports/` — All generated artifacts in requested formats (md, js, json, py, txt, csv, xlsx, .pkl binary, html).
- `generators/build_all.py` — The generator script. Run after editing `pot.json`.
- `loop.md` — Detailed writeup of the psychological + provenance loop.
- `data/` — Supporting structured data (e.g. exif examples, tag hierarchies).
- `examples/` — Sample source shoot records, prompt traces, etc.

## How to Iterate on Tags
1. Edit `pot.json` (add/remove tags, extend timeline, update loop stages, sync with `style_presets/groups.json` etc.).
2. `cd pot && python generators/build_all.py`
3. Review diffs in `exports/`.
4. Commit the exports (or treat exports as build artifacts).

## Formats Generated
- `pot.md` — Human-readable full documentation + tables + timeline.
- `pot.js` — ES module: `import { POT } from './pot.js'`
- `pot.json` — Clean data JSON for APIs/tools.
- `pot.py` — Python module: `from pot.exports.pot import POT`
- `pot.txt` — Raw Apache-style / plain text tag lists (as requested in source convo).
- `pot.csv` — Flat tabular for spreadsheets / analysis.
- `pot.xlsx` — Multi-sheet professional workbook (timeline, tags, loop, provenance, project sync).
- `pot.pkl` — Python pickle binary (full object graph).
- `pot.html` — Self-contained interactive explorer (timeline, searchable/filterable tags, loop diagram, provenance visualizer, one-click "download" of other formats via data: URLs).

## Integration with this repo
- Mirrors + extends `style_presets/groups.json`, `featured_templates/templates.json`, `style_presets/*.json`, character bibles, assets/references (note the "AI-GHOSTED" provenance markers on some composites).
- Film emulation presets, cinematic_genre, pinterest_aesthetic are incorporated.
- EXIF-aware source references live in `assets/`, `inputs/`, `0/`, `featured_templates/inputs/`.

## Next Steps / Ideas
- Link actual image/video assets by SHA or path + their source EXIF JSON sidecars.
- Add "usage count" fields by scanning prompts / generations.
- GraphQL or MCP tool exposure of the PoT.
- Version the PoT and have "ghost" layers (what was AI-hallucinated vs grounded in real shoot).

See [loop.md](./loop.md) for the core conceptual model.

Generated artifacts are in `exports/`. Rebuild anytime.

## Usage Examples

### Python
```python
import sys
sys.path.insert(0, "pot/exports")
from pot import POT, search_tags, get_provenance_stage
print(POT["meta"]["version"])
print(search_tags("exif")[:5])
print(get_provenance_stage(1)["name"])  # Photo Shoot (EXIF Source Material)
```

### JS (browser or node)
```js
import { POT, searchTags } from "./pot/exports/pot.js";
console.log(POT.meta.version);
console.log(searchTags("ghosted"));
```

### Shell / Apache-style tags
```bash
grep -i roman pot/exports/pot.txt
# or feed into other scripts
```

### HTML explorer
Open `pot/exports/pot.html` in a browser. Full interactive timeline + tag search + loop visual + download buttons (data: urls for most formats).

### Iterate
1. `edit pot/pot.json` (add tags, new timeline era, new psych stage, sync more project groups)
2. `python pot/generators/build_all.py`
3. `git diff pot/exports/` (or treat as build output)
4. Update `pot/loop.md` or `data/example-shoot.json` as real shoots are done.

The xlsx has 6 sheets: Timeline, Provenance Loop, Tags by Category, Flat Tags, Meta+Loop, Project Sync.

Binary `pot.pkl` is the full Python object for fast loading in tools/scripts.

This structure directly addresses the original share request: every tag in downloadable multi-format PoT, now grounded in the full real-life-to-EXIF-to-AI psychological loop.
