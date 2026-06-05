# The Psychological Loop: Real Life → EXIF Source Shoot → AI Concept Content

This document models the full chain (and the looping psychological processes) that produce AI-generated "concept content" (still images, video, gifs, stylized film, product viz, character portraits, cinematic scenes, etc.) from grounded real-world source material.

The goal of the PoT tags/taxonomy/timeline is to **make every layer of this loop explicit, taggable, queryable, and traceable**.

## High-Level Stages (Provenance Levels)

```
Real Life / Event / Memory
        │
        ▼  (perception, emotion, selection)
Photo Shoot (Camera, Film/Digital, Lighting, Direction, EXIF)
        │
        ▼  (curation, scanning, metadata enrichment, tagging)
Reference Asset Curation (sidecar JSON, tags, bibles, style refs)
        │
        ▼  (narrative construction, intertextuality, idealization)
Concept Formation + Literary / Film Parallel Selection
        │
        ▼  (prompt crafting, ref image weighting, negative space, seed choice)
AI Generation (Grok Imagine / video / edit / upscale)
        │
        ▼  (review, "ghosting", iteration, composite)
Post-Production + Iteration
        │
        ▼
Final Output (published image/video, proof sheet, template)
        │
        └────── feedback ───────┐
                                │
                   (new memory / new shoot / derivative work)
```

Each arrow is a site of **psychological transformation** and a place where tags from the PoT apply.

## Detailed Stage Breakdown + Example Tags / EXIF Relevance

### 0. Real Life / Psychological Ground
- **Psych elements**: lived experience, memory distortion, emotional charge, cultural lens, personal myth.
- **Tags**: `real-life-event`, `memory`, `autobiographical`, `witnessed`, `dreamt`, `cultural-archetype`, `roman-empire-fantasy`, `western-myth`, `noir-urban-alienation`
- No EXIF yet. This is the "source code" of the human.

### 1. Photo Shoot (The Critical Grounding Layer)
This is where the **exif source photo shoot material** is created — the "point of truth" the AI will later build off of (directly or via memory/trace).

**Artifacts**:
- RAW / JPEG / HEIC / negative
- Full EXIF + MakerNotes + IPTC + XMP
- Lighting diagram / notes (natural, strobe, practical, golden hour, etc.)
- Contact sheet / selects
- Model release, location permit, prop list
- Camera + lens + film stock metadata
- Photographer intent notes

**Key EXIF / metadata fields we care about tagging**:
- `Make`, `Model` (Leica M6, Hasselblad 500CM, iPhone 15 Pro, Arri Alexa, Sony A7R, etc.)
- `LensModel`, `FocalLength`, `FNumber`, `ExposureTime`, `ISOSpeedRatings`
- `DateTimeOriginal`, `OffsetTime`
- `GPSLatitude`, `GPSLongitude` (or reverse-geocoded place tags)
- `FilmStock` (custom: "Kodak Portra 400", "Cinestill 800T", "Ilford HP5")
- `Developer`, `PushPull`, `ScanSource` (Imacon, Epson V850, Noritsu, drum scan)
- `Artist`, `Copyright`, `ImageDescription`
- Custom XMP: `pot:provenanceStage`, `pot:loopTags[]`, `pot:litParallel`, `pot:filmGenreRef`

**Psychological moves here**:
- Selection of what/who/when/where to shoot (framing the world)
- Direction / performance (how much "real" vs performed)
- Technical choices that encode aesthetics (shallow DOF = intimacy/heroism, grain = authenticity/memory, anamorphic flares = epic/cinematic longing)
- The "decisive moment" vs constructed tableau

**Tags**: `photo-shoot`, `exif-grounded`, `film-stock:<name>`, `35mm`, `medium-format`, `large-format`, `golden-hour`, `practical-light`, `studio`, `location`, `candid`, `posed`, `environmental-portrait`

See `data/example-shoot.json` for a full sample sidecar.

### 2. Digitization / Ingestion / First Tagging
- Scan or import.
- Initial keywording, face tagging, color profile embed.
- **Psych**: nostalgia filter, first idealization, "this is the one".

**Tags**: `scanned`, `raw-import`, `color-managed`, `first-pass-tags`, `contact-sheet-select`

### 3. Reference Asset Curation (The Library Layer)
Assets are organized, grouped into bibles (character, style, color), composites created (see `assets/composites/*AI-GHOSTED*`).

In this repo we see:
- `assets/references/original-watercolor-ref.jpg` + reconstruction
- `assets/iterations/` multiple style passes from same base
- "AI-GHOSTED" layers indicating where real photo was used as structure but then AI overpainted / restyled heavily.

**Tags**: `reference-asset`, `character-bible`, `style-ref`, `base-for-iteration`, `ai-ghosted`, `composite-source`, `master-ref`

### 4. Concept Formation + Literary / Film Parallel Injection (The Magic / The Lie)
This is where the **psychological loop** becomes most visible and powerful.

You look at the real photo (or memory of the shoot) and you **map it onto**:
- A film genre (spaghetti-western, film-noir, roman-empire epic, cyberpunk-neon)
- A literary parallel (hardboiled detective voice, mythic hero's journey, gothic romance, picaresque, magical realism)
- An aesthetic movement or subculture (dark-academia, cottagecore, y2k, brutalist photography)

**Why psychological?**
- **Idealization / Myth-making**: The real person/place is made more beautiful, more dramatic, more archetypal.
- **Intertextuality**: You are not just rendering the photo; you are quoting 100 years of cinema + literature.
- **Narrative compression**: A single frame now carries a whole story world (the "Roman Empire" jawline hyper-masculine hero in colosseum at dawn; the lonely neon detective; the faded Kodachrome family that never quite existed).
- **Desire projection**: The tags chosen reveal what the creator (or client) *wants* the world to be.

**Timeline / Genre data in `pot.json` is the shared language for this stage.**

**Tags**: `literary-parallel:<author/work>`, `film-genre:<slug>`, `crossover:<genre+lit>`, `archetype:hero`, `mood:melancholy`, `narrative:origin-story`, `intertextual`

From source convo examples seen in page: "Transform the person... into a cinematic chromatic haze portrait", "roman carving level jawline", "Roman Empire" with colosseum, "classic 1960s-1970s American comic book", product into "fresh natural real-world lifestyle scene".

### 5. Prompt Engineering & Ref Selection
- Choose which real refs to upload (and how heavily to weight them vs text).
- Choose style_preset slugs (from `style_presets/`).
- Choose featured_templates (roman-empire, spaghetti-western, etc.).
- Write the long descriptive prompt that weaves the real description + genre + lit parallel + technical (anamorphic, grain, halation, LUT).
- Decide on "preserve identity" vs "transform".

**Psych**: This is negotiation between fidelity to source and the desire for the idealized fiction.

**Tags**: `prompt-engineered`, `ref-weighted:<n>`, `style-preset:<slug>`, `template:<slug>`, `preserve-identity`, `heavy-transform`, `seed-fixed`, `negative-prompt`

### 6. AI Generation
The model (Grok Imagine etc.) consumes the refs + prompt + hidden training data (which itself contains vast film + literary corpus).

Output may feel "haunted" by the source shoot or completely detached.

**Tags**: `grok-imagine`, `video-gen`, `img2img`, `inpainting`, `upscaled`, `seed:xxxx`, `model:grok-...`, `steps`, `guidance`

### 7. Review, Ghosting, Iteration (The Loop Proper)
- Human judges: "too real", "not cinematic enough", "wrong jaw", "needs more film grain", "make it feel like a still from a 1972 Sergio Leone film".
- Then edit (object remover, quality enhancer, manual composite) or re-prompt with stronger refs / new parallel.
- "AI-GHOSTED" composites in this repo are perfect artifacts of this stage: the original photo is still structurally present but visually erased/overwritten.

**Psychological loop closes here**:
- Satisfaction / catharsis when the idealized version matches the internal image better than the real photo ever could.
- Or disappointment when the AI can't quite capture the ineffable thing from the shoot.
- Then new shoot or new memory is formed from the generated image itself (the generated becomes part of the "real" reference library for next time).

**Tags**: `iteration:<n>`, `ghosted`, `composite`, `human-review-pass`, `rejected`, `approved-for-proof`, `feedback:<note>`

### 8. Final Output + Distribution + New Memory
- Proof sheets (`featured_templates/proof-sheet.html`)
- Templates registered
- Published to client / social / portfolio
- The final image now enters the culture and can become someone else's "real life" reference (or training data).

**Tags**: `final`, `proof-sheet`, `template-registered`, `public`, `client-delivery`, `training-source-potential`

## The Loop as Psychological Phenomenon
- **Selection & Framing** (what gets shot, what gets cropped out)
- **Myth Injection** (genre + literary parallel as ready-made meaning machines)
- **Idealization Pressure** (real skin vs Portra 400 skin, real jaw vs "roman carving level")
- **Technological Mediation** (film stock as memory prosthetic, anamorphic as emotional width)
- **AI as Collaborative Dreamer** (the model completes the fantasy the prompt only sketched)
- **Iteration as Ritual** (re-prompting until the external image matches the internal one closely enough for the psyche to rest)
- **Ghosting & Erasure** (the real photo shoot is both the foundation and what gets aesthetically "killed" to achieve the higher truth of the concept)

The tags in this PoT exist to name every node and every transformation in this loop so that we can:
- Audit where a generated piece is "lying" vs grounded.
- Reproduce a look from a specific real shoot + specific lit/film refs.
- Build better character bibles and style systems that declare their provenance.
- Study our own desires as creators (what parallels we keep reaching for reveals us).

## Connection to the Source Conversation
The shared Grok conversation "Film Genres: Literary Parallels Timeline" + the follow-up request for "every film/video/gif/stream of content tag ... in a downloadable format" was exactly the act of surfacing and structuring this loop's vocabulary at scale.

This `pot/` is the local, versioned, multi-format, extensible realization of that request.

See `pot.json` for the structured data (timeline entries, full tag sets, stage definitions, project sync).

See `exports/pot.html` for an interactive version of the loop + tag browser.
