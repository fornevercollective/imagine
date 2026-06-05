# Ancestry & Anatomical Character Bible Madlibs Template

Source: Integrated from https://fornevercollective.github.io/ancestory/ research + standard anthropological/character design frameworks (face shapes, somatotypes, hair typing, skin science).

**Purpose**: Expand the core Character Bible in the main README madlibs for hyper-detailed, consistent, scientifically-grounded human (and hominin-admixed) characters in Grok Imagine. Use for single images, video clips, or full story arcs (pair with `stories/*.json` beats and `style_presets/` LUTs/lenses).

Copy the template, fill the {} blanks. **Repeat the entire [MASTER ANCESTRY + ANATOMY BIBLE] block verbatim** (or 95%+ identical) in every prompt for a character series to lock face, body, hair, skin, and ancestral traits against style drift.

## Master Ancestry + Anatomy Bible Madlibs (insert at top of prompts)

```
[MASTER ANCESTRY + ANATOMY BIBLE - REPEAT VERBATIM FOR CONSISTENCY]:
{Character Name}, a {age}-year-old {gender/presentation} of predominantly {primary sapiens ancestry e.g. recent West African / East African / Eurasian steppe / Andamanese / etc.} with {hominin_tree_relation e.g. 12% Neanderthal-derived archaic admixture expressing as moderately robust supraorbital torus / brow ridge contribution, thicker cranial vault, and cold-adapted limb proportions with lower crural index; minor Denisovan input visible in skin vascular patterning and high-altitude melanin plasticity}.

Face shape: {face_shapes e.g. oval with soft heart taper at chin, or square-jawed with diamond cheekbones and slight Neanderthal-like brow projection, or heart-shaped with high forehead tapering to delicate point}.

Hair details:
- Scalp: {texture e.g. type 4 coily/kinky dense} {density} {color with melanin note} {length and styling e.g. natural voluminous afro with defined coils or tight cornrows pulled back revealing hairline}.
- Face: {micro_fuzz e.g. fine vellus peach fuzz across cheeks and upper lip for soft texture and light catch; macro terminal beard if applicable: full but groomed with {curl pattern matching scalp}, density on jawline and mustache area}.
- Upper torso: {chest/abdominal/shoulder/back hair: e.g. light terminal patches on chest tapering to micro vellus fuzz on upper back and shoulders for subtle texture under lighting}.
- Under arms: {axillary: moderate to dense terminal curls of {length}, or trimmed micro for clean look}.
- Lower torso & legs: {pubic pattern e.g. triangular dense terminal; leg hair: macro terminal on lower legs/calves with {density}, transitioning to micro vellus fuzz on thighs and upper legs for natural gradient; foot hair minimal}.

Body shapes, proportions & styling:
- Overall: {somatotype + hominin e.g. tall ectomorphic with long limbs and high crural index typical of equatorial recent sapiens adaptations for heat dissipation; or mesomorphic athletic with broad shoulders and narrow waist reflecting mixed Neanderthal robust + sapiens gracile; or endomorphic with steatopygous gluteal fat storage from Khoisan-related ancestry lines}.
- Upper torso: {shoulder width relative to hips e.g. wide mesomorphic shoulders with developed deltoids and pectorals tapering to defined waist; ribcage shape, lat spread}.
- Lower torso: {hip/waist/glute: e.g. moderate waist with wider hips and rounded glutes for female dimorphism or powerlifter build; thigh/calf proportions}.
- Arms & hands: {length, muscle/fat distribution, hand size relative to body}.
- Legs & feet: {inseam proportion, muscle definition or softness, foot shape}.
- Styling notes: {grooming e.g. natural body hair retained for micro/macro fuzz texture and subsurface light interaction; or groomed smooth on arms/legs/underarms to emphasize clean skin refraction; posture/muscle tone from lifestyle e.g. lean hunter-gatherer endurance build vs. stocky agricultural robustness; any cultural body modifications like scarification aligned with ancestry}.

Skin science (subsurface, melanin, irradiance, tiger stripes - critical for realistic SSS, glow, and lighting response under all LUTs/lenses):
- Melanin dispersion: {e.g. high eumelanin density in basal and spinous layers with even dispersion for deep rich tone typical of equatorial ancestries; or mixed eumelanin/pheomelanin with clustered dispersion producing warm undertones}.
- Subsurface IR tiger stripes & refraction: visible tiger-stripe (melanin band / Blaschko-line / vascular patterning) subsurface scattering enhanced in raking/side light and simulated IR; {e.g. 25-40% of incident irradiance refracts and scatters in the dermis producing soft internal glow and depth, with faint tiger striping most apparent on temples, collarbones, inner arms, and upper chest}.
- Irradiance percentage & overall: {e.g. 15% surface reflectance with 35% subsurface refraction/scatter for medium-deep skin under golden hour; calibrated to ancestry and current lighting/LUT (higher absorption/lower reflectance in high-UV adapted lines, richer color from multiple internal bounces)} . Skin shows natural micro texture, pore variation by area, and realistic response to film grain/LUTs (e.g. "creamy highlights with subsurface color pop in shadows on Kodak Vision3 500T").

[Continue with the rest of the standard madlibs from README: Medium/Camera/LUT/Lens, Action, Environment, Lighting/Mood/Color Correction, Camera Move/Edit Timeline, etc. Always lead with or prominently include this full Ancestry + Anatomy Bible block.]
```

## How to Use with Existing System

1. Fill the {} from `ancestry_traits.json` (face_shapes, hair categories, body_shapes_and_proportions, hominin_tree_relation examples, skin_science_subsurface details).

2. Paste the completed [MASTER ... BIBLE] block at the beginning of any prompt generated by `sweep.py prepare` or `story.py`.

3. For stories: Add an "ancestry_bible" key to character definitions in your `stories/*.json` and have story.py / manual prompts inject it.

4. Combine with `style_presets/` (e.g. append a kodak-vision3-500t or panavision-c-series-anamorphic prompt.txt after the bible for the visual treatment while keeping anatomy locked).

5. For video / multi-beat: The bible ensures the same person appears across wildly different film LUTs, eras, or aesthetics (e.g. from golden-hour-romance to cyberpunk-neon).

6. Advanced: Use percentages explicitly ("with 2.4% Neanderthal admixture expressing as...") and irradiance numbers ("28% subsurface irradiance refraction with prominent tiger striping") — Grok Imagine handles numeric + scientific descriptors very well for precision.

## Example Filled Snippet (for a dusk-to-neon style character)

[MASTER ANCESTRY + ANATOMY BIBLE...]:
Elena Voss, a 29-year-old woman of primarily recent East African sapiens ancestry with 8% Neanderthal introgression manifesting as moderately prominent brow ridge contribution and robust jaw potential, plus minor Denisovan input in skin patterning...

Face shape: heart-shaped with high forehead and soft taper to chin, softened by sapiens gracile traits.

Hair details: ... (full as above)

Body shapes...: tall ectomorphic with long legs (high crural index from savanna-adapted hominin lines), narrow waist, athletic but lean upper torso...

Skin science: high eumelanin dispersion in basal layer for rich deep tone with warm undertones from pheomelanin contribution; subsurface scattering with 32% irradiance refraction producing soft glow and visible faint tiger-stripe melanin patterning (most apparent in side light on cheekbones, inner wrists, and décolletage) calibrated for high-UV equatorial ancestry with excellent multiple-scatter color depth under film LUTs.

Then continue with the rainy alley action + Panavision C-Series + heavy grain + teal-orange etc.

This level of detail dramatically improves consistency and "aliveness" of skin/hair/body under all the cinematic presets and lighting changes.

## Maintenance

- Expand `ancestry_traits.json` with more options from ongoing ancestory research.
- For deep historical / genetic migration iteration: use `hominin_data/hominin_lineage_timeline.json` (11 stages from Sahelanthropus ~7mya to modern global). Each stage has `unified_migration_lineage` (the "one solid column" for lineage estimations), `bible_snippet`, `prompt_traits`, `fossil_refs` (exact links to 3d.si.edu, Australian Museum casts, Bone Clones), `mixamo_threejs` (IK/pose/shape guidance), `genetic_admixture_estimates`.
- When adding new hominin branches or skin metrics, mirror in the madlibs template and the main README's Character Bible section.
- Test generations: Generate a master reference with neutral lighting + one of the film LUT presets, then vary only style/LUT while keeping the full bible fixed. Iterate lineage by swapping stage bible_snippet (e.g. "ancestor at Turkana Boy erectus stage" vs "same character with full modern sapiens + 1.8% Neanderthal overlay").
- Holo ID badges: See `holo_id_badges/` prototype (self-contained HTML that loads the lineage JSON, timeline scrubber/iterator, genetic % , migration path viz, holo card UI inspired by the provided Spline + Instagram concepts). Use generated portraits (via the bibles + "holographic ID badge, iridescent, floating 3D portrait, spline style") as assets.

See also the main project README.md for the core madlibs + how it integrates with sweep.py / story arcs. Also `pot/` for tagging (add hominin-stage, fossil-ref, mixamo-ik, lineage-migration, holo-badge categories as needed and re-run generator).
