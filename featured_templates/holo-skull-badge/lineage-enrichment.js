/**
 * Lineage data enrichment panels for holo-viewer (merged from holo_id_badges).
 * Syncs with HoloChrome stage index — single-page mode.
 */
(function (global) {
  'use strict';

  const INLINE_STAGES = [
    { stage_index: 0, name: 'Sahelanthropus tchadensis', era: '~7-6 mya', unified_migration_lineage: 'Africa (Central) | 7mya LCA split | 0% sapiens-admixture (pre-split) | arboreal + some terrestrial foraging', admixture: 'N/A (pre-split)', fossil_refs: 'Australian Museum early hominin casts; Bone Clones early hominin', bible_snippet: 'of deep early hominin (Sahelanthropus tchadensis ~7mya) ancestry expressing as small ~360cc braincase, thick continuous supraorbital torus, moderately projecting face with thick enamel dentition, stocky short-statured build with retained arboreal adaptations and emerging bipedalism', mixamo: 'Mixamo: primate or chimp-like rig base, forward-leaning facultative biped pose, short strides. Three.js: additive base locomotion + foraging reach.' },
    { stage_index: 1, name: 'Ardipithecus ramidus (Ardi)', era: '~4.4 mya', unified_migration_lineage: 'East Africa (Afar) | 4.4mya | facultative biped in forests | 0% later admixture (foundational) | mosaic locomotion', admixture: 'N/A foundational', fossil_refs: 'Smithsonian 3D (Ardi if avail); Bone Clones early hominin', bible_snippet: 'with Ardipithecus ramidus (~4.4 mya) deep ancestry expressing in transitional features: modest supraorbital development, less projecting face, reduced canine size, pelvis hints of bipedalism combined with arboreal foot adaptations (grasping big toe potential), long arms short legs', mixamo: 'Mixamo: human base with modified foot (grasping), hip for bipedal but bent-knee. Poses: upright on branch to ground biped shuffle. Three.js additive arboreal suspension + bipedal stance.' },
    { stage_index: 2, name: 'Australopithecus afarensis (Lucy)', era: '~3.9-2.9 mya', unified_migration_lineage: 'East/South Africa | 3.2mya | obligate biped with arboreal remnant | foundational for Homo line | 0% archaic sapiens admixture', admixture: 'Foundational (no direct %)', fossil_refs: 'Australian Museum Lucy + Mrs Ples casts; Bone Clones Australopithecus afarensis / postcranial sets; Smithsonian 3D', bible_snippet: 'predominantly recent sapiens with deep Australopithecus afarensis (~3.2mya Lucy lineage) foundational ancestry expressing as small stature potential, long arms relative to legs (high intermembral), valgus knee bipedal posture with efficient striding capability, moderately prognathic face with moderate supraorbital development, small cranium on robust neck, wide pelvis, curved phalanges hint in hands', mixamo: 'Mixamo: petite female rig, short stride Lucy walk (slight waddle or efficient). IK arms for forage or carry. Three.js: biped locomotion base + arm balance swing + climb remnant.' },
    { stage_index: 3, name: 'Paranthropus boisei (robust)', era: '~2.3-1.2 mya', unified_migration_lineage: 'East/South Africa | 2-1.2mya | specialized megadont herbivore biped | sister to Homo line | 0% direct in sapiens', admixture: 'Extinct side branch', fossil_refs: 'Australian Museum Paranthropus boisei (Zinjanthropus) casts; Bone Clones robust australopith skulls/sets', bible_snippet: 'with Paranthropus boisei (~1.8mya) robust side-branch ancestry manifesting as hyper-robust \'nutcracker\' craniofacial features: prominent sagittal crest, flaring zygomatic arches, massive post-canine dentition, dish-shaped face, very heavy brow ridge and nuchal musculature, stocky powerful build with barrel chest and thick limb bones', mixamo: 'Mixamo: heavy mesomorph, power stance or heavy forage/chew with IK on jaw/spine. Three.js: locomotion + strong additive crest/jaw power flex + torso thickness.' },
    { stage_index: 4, name: 'Homo habilis (early Homo)', era: '~2.4-1.4 mya', unified_migration_lineage: 'East Africa Rift | ~2mya | tool-making biped, larger brain | bridge to erectus | pre-migration core', admixture: 'Direct ancestor line', fossil_refs: 'Australian Museum Homo habilis 1813 cast; Bone Clones early Homo skulls', bible_snippet: 'Homo habilis early tool-making Homo ancestry (~2-1.6mya) expressing as larger braincase (~600-700cc) with higher vault and reduced brow compared to australopiths, less prognathic face, precision-grip capable hands, improved bipedal proportions for ranging, smaller body size ~1.3m with some retained arboreal upper body strength, first cultural (Oldowan) expression', mixamo: 'Mixamo: early human small rig, tool use / chopper animations + walk. IK for dexterous hands. Three.js: precision grip hold + biped + subtle facial focus.' },
    { stage_index: 5, name: 'Homo erectus / ergaster (Turkana Boy)', era: '~1.9 mya - 110 kya', unified_migration_lineage: 'East Africa -> Eurasia (Levant/Georgia/Asia) | 1.8mya first exodus | long persistence in Asia | core ancestor to heidelbergensis | 0% Neanderthal yet (pre-split)', admixture: 'Core ancestor to later archaics', fossil_refs: 'Australian Museum Turkana Boy + many erectus (Sangiran, Solo); Bone Clones erectus/ergaster skulls + full skeletons/postcranial; Smithsonian 3D hominin-fossils', bible_snippet: 'Homo erectus/ergaster deep ancestry (~1.6mya Turkana Boy + Dmanisi/Sangiran lines) expressing as low-vaulted cranium with prominent heavy supraorbital torus/brow ridge, receding forehead, robust but less prognathic face, modern body proportions (long legs, short arms, narrow pelvis for efficient striding bipedalism), barrel chest, thick bones, ~1.7m stature, first true long-distance endurance capabilities, dark equatorial skin with high irradiance refraction capacity', mixamo: 'Mixamo: standard human rig (scale 1.65m); striding walk, run, throw, dig. Full IK. Three.js: striding biped base + spear thrust / fire use additive + facial heavy brow torus morph. Ideal for holo.' },
    { stage_index: 6, name: 'Homo heidelbergensis (archaic LCA)', era: '~800-200 kya', unified_migration_lineage: 'Africa + Eurasia | 600-400kya | large-brained archaic | last common ancestor sapiens/Neanderthal/Denisovan | pre-admixture for sapiens line', admixture: 'LCA ~550-750kya', fossil_refs: 'Australian Museum Kabwe/Broken Hill, Swanscombe, Steinheim, Arago; Bone Clones archaic/heidelbergensis', bible_snippet: 'Homo heidelbergensis (~600-400kya) common archaic ancestry (LCA to sapiens and Neanderthals/Denisovans) expressing as large braincase (1200cc+), prominent heavy double-arched supraorbital torus, receding forehead, large robust face with projecting midface and broad nose, thick vault, powerful robust tall build with strong neck and shoulders, modern bipedal proportions but thicker bones and muscle mass potential', mixamo: 'Mixamo: tall robust male; spear hunt, butcher, heavy labor. IK powerful. Three.js: power movements + facial robust torus + barrel chest breathing additive.' },
    { stage_index: 7, name: 'Homo neanderthalensis', era: '~400-40 kya', unified_migration_lineage: 'Eurasia (Europe/Levant) | 400kya split from sapiens line | cold-adapted | 1-2% introgression into non-African sapiens ~50-60kya | extinct ~40kya', admixture: '1-2% (up to 4% some) in non-Africans', fossil_refs: 'Australian Museum multiple (Amud 1, Le Moustier, Gibraltar, youth); Bone Clones extensive Neanderthal skulls/skeletons (Sawyer/Maley recon)', bible_snippet: 'with 1.8% Neanderthal archaic admixture (from ~50kya Eurasian contact) expressing as long low-vaulted cranium with prominent double-arched supraorbital torus and occipital bun, receding forehead, large robust midface with broad nose and midfacial prognathism, weak or absent chin, stocky cold-adapted body with barrel chest, short distal limbs, thick bones, powerful build, pale-medium skin with excellent multiple scattering subsurface and tiger-stripe potential under side light, robust hair patterns', mixamo: 'Mixamo: stocky short-limbed robust rig; power crouch, close spear thrust, hide scrape. IK for stocky power. Three.js: wide power stance + heavy tool + strong brow+bun+nose morphs. Perfect holo.' },
    { stage_index: 8, name: 'Denisovans', era: '~200-50 kya', unified_migration_lineage: 'Asia (Altai + high plateau/Tibet) | ~400kya split | high-altitude/UV adaptations | 2-6% in Oceanians/Papuans + trace Asians | extinct', admixture: '2-6% Papuans/Oceanians; trace East Asians', fossil_refs: 'Limited fossils (Denisova Cave); use Bone Clones / Australian archaic Asian or heidelbergensis proxies + DNA-informed recon', bible_snippet: 'with 3.2% Denisovan archaic admixture (high in Oceanian/Papuan lines from ~50-40kya Asian contact) expressing as robust jaw and large post-canine dentition, possible high-altitude/UV adapted skin vascularity and dispersed melanin clusters producing unique tiger-stripe subsurface scattering, robust but efficient build for endurance in varied Asian/highland environments, dark skin with excellent multiple internal refraction for rich color depth', mixamo: 'Mixamo: robust build (Asian cranial base); high endurance / mountain poses + thin air breathing emphasis. Three.js: high-altitude posture/breathing + robust jaw + unique skin micro-pattern morph.' },
    { stage_index: 9, name: 'Early Homo sapiens (Africa + early exits)', era: '~300-100 kya', unified_migration_lineage: 'Africa (Morocco/Ethiopia) | 300kya emergence | early pulses to Levant/Asia | main global ~55kya + archaic admixture | all living humans descend from this + admixture', admixture: 'Base recent sapiens + variable archaic (0% pure African to 2%+ N/D)', fossil_refs: 'Australian Museum Skhul 5, Liujiang, Cro-Magnon, early sapiens; Bone Clones anatomically modern / early sapiens', bible_snippet: 'primarily recent Homo sapiens sapiens (~300kya African origin, Jebel Irhoud/Herto lineage) with {X}% archaic admixture (Neanderthal/Denisovan as appropriate to migration path) expressing as high vaulted cranium with vertical forehead and minimal brow, flat face with chin, small teeth, fully modern body proportions (long legs, balanced intermembral index, narrow pelvis for efficient striding bipedalism and birth), skin science exactly as calibrated in traits with admixture-specific melanin dispersion and tiger striping', mixamo: 'Mixamo: full modern human rigs (any base); entire animation library. Three.js: full skinning + morph targets for high forehead/chin/reduced torus + body proportions + any additive layers.' },
    { stage_index: 10, name: 'Anatomically Modern + Regional (Upper Paleo to now)', era: '~50 kya - present', unified_migration_lineage: 'Global post-55kya | multiple waves + founder effects + archaic input | all living humans | ongoing micro-evolution + culture', admixture: 'Varies by path (see stages 7-8 + recent admixtures)', fossil_refs: 'Australian Museum Cro-Magnon + global regional sapiens; Bone Clones full modern human range', bible_snippet: 'fully anatomically modern Homo sapiens of {detailed admixture e.g. primarily recent East African sapiens with 1.8% Neanderthal + 0.4% Denisovan + recent Eurasian/African blend} expressing the complete modern package: high vaulted forehead vertical and gracile, reduced brow to none, flat face with chin, small teeth, modern body proportions varying by specific lineage (long legs high crural index for heat dissipation or stocky cold adapted short limbs), full range of face shapes and hair textures per the ancestry_traits, skin science exactly as calibrated in traits with admixture-specific melanin dispersion and tiger striping', mixamo: 'Mixamo: ultimate — any body type, 1000s animations, perfect auto-rig for your generated meshes, full IK. Three.js: the linked additive blending example + morph targets for face shapes + body. End of the evolutionary line for rigs/poses.' }
  ];

  const SKULL_IMG_FOR = {
    '0': 'sahelanthropus-skull.jpg', sahelanthropus: 'sahelanthropus-skull.jpg',
    '1': 'australopithecus-skull.jpg', australopithecus: 'australopithecus-skull.jpg',
    '2': 'australopithecus-skull.jpg', lucy: 'australopithecus-skull.jpg',
    '3': 'australopithecus-skull.jpg',
    '4': 'erectus-skull.jpg', erectus: 'erectus-skull.jpg',
    '5': 'erectus-skull.jpg', turkana: 'erectus-skull.jpg',
    '6': 'erectus-skull.jpg',
    '7': 'neanderthal-skull.jpg', neanderthal: 'neanderthal-skull.jpg',
    '8': 'erectus-skull.jpg',
    '9': 'australopithecus-skull.jpg', sapiens: 'australopithecus-skull.jpg',
    '10': 'australopithecus-skull.jpg',
    chimpanzee: 'chimpanzee-skull.jpg', gorilla: 'gorilla-skull.jpg',
    wolf: 'wolf-skull.jpg', vampire: 'vampire-skull.jpg', werewolf: 'werewolf-skull.jpg',
    orc: 'orc-skull.jpg', fairy: 'fairy-skull.jpg', satyr: 'satyr-skull.jpg', satyrnohorns: 'satyr-skull.jpg'
  };

  const DEFAULT_MEASUREMENTS = [
    { y: 0.11, label: 'C. vault', val: '—' },
    { y: 0.28, label: 'Brow', val: '—' },
    { y: 0.46, label: 'Orbit', val: '—' },
    { y: 0.62, label: 'Nasal', val: '—' },
    { y: 0.8, label: 'Alveol.', val: '—' }
  ];

  const SKULL_MEASUREMENTS = {
    neanderthal: [
      { y: 0.09, label: 'Vault', val: '138' },
      { y: 0.26, label: 'Supraorb', val: '47' },
      { y: 0.44, label: 'Biorb.', val: '109' },
      { y: 0.6, label: 'Nasal ht', val: '59' },
      { y: 0.78, label: 'Mand.', val: '—' }
    ],
    erectus: [
      { y: 0.1, label: 'Vault', val: '128' },
      { y: 0.27, label: 'Torus', val: '38' },
      { y: 0.47, label: 'Face', val: '—' },
      { y: 0.63, label: 'Nasal', val: '51' },
      { y: 0.81, label: 'Dent.', val: '—' }
    ]
  };

  const IMG_SKULLS = '/featured_templates/holo-skull-badge/img/skulls/';
  const IMG_STILL = '/featured_templates/holo-skull-badge/img/holo-card-still.jpg';
  const IMG_VARIATIONS = '/featured_templates/holo-skull-badge/img/variations/01.persons/';
  const IMG_HAZE_BASE = '/featured_templates/holo-skull-badge/img/variations/00.haze/';

  function getPersonImg(slug) {
    const key = String(slug || '').toLowerCase();
    return IMG_VARIATIONS + key + '-person.jpg';
  }

  function getHazeHoloCard(slug) {
    const key = String(slug || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    // organized under 00.haze/02.id-holo/ for the combined cards
    return IMG_HAZE_BASE + '02.id-holo/' + key + '-haze-holo-card.jpg';
  }

  let STAGES = INLINE_STAGES.slice();
  let current = 7;
  let liteDeckLoaded = false;
  let skinDemoTimer = null;
  let holo3d = null;
  const IS_MOBILE = /Mobi|Android|iPhone|iPad|iPod|Opera Mini/i.test(navigator.userAgent) || (global.innerWidth < 768);

  function normalizeStage(st) {
    return {
      stage_index: st.stage_index,
      name: st.name,
      era: st.era,
      unified_migration_lineage: st.unified_migration_lineage || '',
      admixture: st.genetic_admixture_estimates || st.admixture || 'N/A',
      fossil_refs: Array.isArray(st.fossil_refs) ? st.fossil_refs.join('; ') : (st.fossil_refs || ''),
      bible_snippet: st.bible_snippet || '',
      mixamo: st.mixamo_threejs || st.mixamo || st.ik_pose_shapes || '',
      key_fossils: st.key_fossils || [],
      cranial_face_bones: st.cranial_face_bones,
      body_postcranial_pose: st.body_postcranial_pose,
      shapes_morphs: st.shapes_morphs,
      migration_notes: st.migration_notes,
      genetic_admixture_estimates: st.genetic_admixture_estimates || st.admixture
    };
  }

  function syncStagesFromChrome() {
    const chromeStages = global.HoloChrome && global.HoloChrome.getStages();
    if (chromeStages && chromeStages.length >= 8) {
      STAGES = chromeStages.map(normalizeStage);
      return true;
    }
    return false;
  }

  async function loadFullLineage() {
    if (syncStagesFromChrome()) return true;
    try {
      const res = await fetch('/character_bibles/ancestory/hominin_data/hominin_lineage_timeline.json');
      const full = await res.json();
      if (full && full.stages && full.stages.length >= 8) {
        STAGES = full.stages.map(normalizeStage);
        return true;
      }
    } catch (_) {}
    STAGES = INLINE_STAGES.slice();
    return false;
  }

  function getStages() {
    return STAGES;
  }

  function getStage(idx) {
    const found = STAGES.find((s) => s.stage_index === idx);
    return found || STAGES[idx] || STAGES[0];
  }

  function getSkullImg(stageOrSlug) {
    const key = String(stageOrSlug || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    return SKULL_IMG_FOR[key] || 'neanderthal-skull.jpg';
  }

  function getMeasurements(slug) {
    const key = String(slug || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    return SKULL_MEASUREMENTS[key] || DEFAULT_MEASUREMENTS;
  }

  function setCurrent(idx, options = {}) {
    current = Math.max(0, Math.min(STAGES.length - 1, idx));
    renderAll();
    if (options.silent) return;
    if (global.HoloChrome) {
      global.HoloChrome.setStageIndex(current, { source: options.source || 'enrichment' });
    } else if (global.holoViewerSelectStage) {
      global.holoViewerSelectStage(current, { fromEnrichment: true });
    }
  }

  function renderTimeline() {
    const el = document.getElementById('enrich-timeline');
    if (!el) return;
    el.innerHTML = '';
    STAGES.forEach((s, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'enrich-stage-btn' + (i === current ? ' active' : '');
      b.textContent = `${s.stage_index} ${s.name.split('(')[0].trim()}`;
      b.onclick = () => setCurrent(i, { source: 'timeline' });
      el.appendChild(b);
    });
  }

  function renderStageDataPanel(s) {
    if (global.HoloChrome && global.HoloChrome.populateStageDataPanel) {
      global.HoloChrome.populateStageDataPanel(s);
    }

    const cardStage = document.getElementById('enrich-card-stage');
    if (cardStage) cardStage.textContent = String(s.stage_index).padStart(2, '0');
    set('enrich-card-name', s.name);
    set('enrich-card-era', s.era);
    set('enrich-card-solid', s.unified_migration_lineage);

    const statsEl = document.getElementById('enrich-card-stats');
    if (statsEl) {
      statsEl.innerHTML = `
        <span class="stat">STAGE ${s.stage_index}</span>
        <span class="stat">${s.era}</span>
        <span class="stat">${String(s.admixture).includes('%') ? s.admixture : 'Foundational'}</span>
      `;
    }
  }

  function updateDelineationInEnrichment(idx) {
    const panel = document.getElementById('enrich-delineation-panel');
    if (!panel) return;
    const s = getStage(idx);
    const prev = getStage(idx - 1) || STAGES[0];
    const next = getStage(idx + 1) || STAGES[STAGES.length - 1];
    const keyFossil = (s.key_fossils && s.key_fossils[0]) ? String(s.key_fossils[0]).split(',')[0] : 'N/A';

    let html = `<strong>Current: ${s.name} (Specimen focus: ${keyFossil})</strong><br>`;
    html += '<div style="margin:8px 0;font-size:12px;">Delineates from other trees via:</div>';
    html += '<ul style="margin:4px 0;padding-left:18px;font-size:12px;line-height:1.3;">';
    html += `<li><strong>vs ${prev.name}:</strong> ${s.cranial_face_bones && prev.cranial_face_bones ? (String(s.cranial_face_bones).length > String(prev.cranial_face_bones).length ? 'More derived cranial vault' : 'More robust features') : 'Different cranial architecture'}. Migration: ${String(s.unified_migration_lineage).split('|')[0].trim()} vs ${String(prev.unified_migration_lineage).split('|')[0].trim()}.</li>`;
    html += `<li><strong>vs ${next.name}:</strong> Admixture ${s.genetic_admixture_estimates ? String(s.genetic_admixture_estimates).substring(0, 60) : 'baseline'} vs later regional variation.</li>`;
    html += `<li><strong>From the broader tree:</strong> ${s.migration_notes ? String(s.migration_notes).substring(0, 80) : 'Unique dispersal pattern'}.</li>`;
    html += '</ul>';
    html += `<div style="font-size:10px;opacity:0.6;margin-top:6px;">Use in prompts: holographic lenticular card, tilt reveals skull from ${s.name}, Specimen ID ${keyFossil}</div>`;
    panel.innerHTML = html;
  }

  function renderAll() {
    const s = getStage(current);
    renderStageDataPanel(s);
    renderTimeline();
    updateDelineationInEnrichment(current);
    drawSimpleThreeDemo(s);
    updateLiveHoloCard(current);
  }

  function syncFromChrome(idx) {
    current = Math.max(0, Math.min(STAGES.length - 1, idx));
    renderAll();
  }

  function prevStage() {
    setCurrent((current - 1 + STAGES.length) % STAGES.length, { source: 'controls' });
  }

  function nextStage() {
    setCurrent((current + 1) % STAGES.length, { source: 'controls' });
  }

  function randomStage() {
    setCurrent(Math.floor(Math.random() * STAGES.length), { source: 'controls' });
  }

  function copyBible() {
    const s = getStage(current);
    navigator.clipboard.writeText(s.bible_snippet).then(() => {
      alert('Prompt snippet copied. Paste into madlibs [MASTER ANCESTRY + ANATOMY BIBLE] block.');
    });
  }

  function copyPrompt() {
    const s = getStage(current);
    const p = `[MASTER ANCESTRY + ANATOMY BIBLE - REPEAT VERBATIM]:\n${s.bible_snippet}\n\nFace/body/bones from ${s.fossil_refs}. Pose/IK: ${s.mixamo}. Reference the exact fossil casts/scans in prompt for accuracy. Holo ID badge style if generating card.`;
    navigator.clipboard.writeText(p).then(() => alert('Full prompt context copied for Grok Imagine.'));
  }

  function generateImaginePrompt() {
    const s = getStage(current);
    const prompt = `Photoreal portrait of ${s.name} (${s.era}), ${s.bible_snippet}. Highly detailed face and cranium exactly matching ${String(s.fossil_refs).split(';')[0]}. Body proportions and posture from postcranial evidence. ${String(s.mixamo).split('.')[0]}. Cinematic lighting, film grain, accurate to fossil reconstruction, neutral background for reference.`;
    navigator.clipboard.writeText(prompt).then(() => {
      alert('Imagine prompt copied. Use with style_presets + repeat prompt snippet for holo badge series consistency.');
    });
  }

  function showSplineLinks() {
    alert('Holo ID badge / 3D card concepts:\n\n• https://www.instagram.com/tadericson/p/CzsYfNVL2XX/\n• https://community.spline.design/file/599304aa-55a7-431e-86ee-b3d8cd6ecca0\n• https://app.spline.design/file/3a0e7933-4ce5-47d7-aa9c-cdfdd973f9b5\n• https://app.spline.design/file/999700e2-df6d-4afc-8150-85b06fd64008');
  }

  function drawSimpleThreeDemo(stage) {
    const canvas = document.getElementById('enrich-three-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#0a0c10';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = 90;
    ctx.strokeStyle = '#555';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.ellipse(cx, cy - 10, 38, 48, 0, 0, Math.PI * 2);
    ctx.stroke();
    if (stage.stage_index <= 5) {
      ctx.beginPath();
      ctx.moveTo(cx - 30, cy - 25);
      ctx.lineTo(cx + 30, cy - 25);
      ctx.stroke();
    }
    ctx.fillStyle = stage.stage_index <= 4 ? '#3a2f1f' : '#c9b8a0';
    ctx.beginPath();
    ctx.ellipse(cx, cy + 5, 22, 28, 0, 0, Math.PI * 2);
    ctx.fill();
    const t = (Date.now() / 400) % (Math.PI * 2);
    ctx.strokeStyle = '#00f0ff';
    ctx.beginPath();
    ctx.moveTo(cx + 25, cy + 20);
    ctx.quadraticCurveTo(cx + 55 + Math.sin(t) * 8, cy - 10, cx + 70, cy + 40 + Math.cos(t) * 6);
    ctx.stroke();
    ctx.fillStyle = '#666';
    ctx.font = '10px monospace';
    ctx.fillText(`Stage ${stage.stage_index} • ${stage.name.split(' ')[0]} • additive blend demo`, 12, 170);
  }

  function initHolo3DCard() {
    const canvas = document.getElementById('holo-3d-card');
    const wrap = document.getElementById('holo-portrait-wrap');
    if (!canvas || !wrap || canvas.dataset.inited || typeof global.THREE === 'undefined') return;
    canvas.dataset.inited = '1';

    const THREE = global.THREE;
    const w = wrap.clientWidth || 320;
    const h = 240;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(w, h, false);
    renderer.setPixelRatio(Math.min(global.devicePixelRatio || 1, 2));

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 100);
    camera.position.set(0, 0, 2.65);

    const cardGroup = new THREE.Group();
    scene.add(cardGroup);

    const loader = new THREE.TextureLoader();
    const cardGeo = new THREE.PlaneGeometry(1.75, 1.05);

    const headMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 1 });
    const headMesh = new THREE.Mesh(cardGeo, headMat);
    cardGroup.add(headMesh);

    const skullMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0 });
    const skullMesh = new THREE.Mesh(cardGeo, skullMat);
    skullMesh.position.z = 0.002;
    cardGroup.add(skullMesh);

    const augMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0 });
    const augMesh = new THREE.Mesh(cardGeo, augMat);
    augMesh.position.z = 0.004;
    cardGroup.add(augMesh);

    const holoMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0,
      blending: THREE.AdditiveBlending
    });
    const holoMesh = new THREE.Mesh(new THREE.PlaneGeometry(1.78, 1.08), holoMat);
    holoMesh.position.z = 0.006;
    cardGroup.add(holoMesh);

    const rimMat = new THREE.MeshBasicMaterial({
      color: 0xff00aa,
      transparent: true,
      opacity: 0.12,
      side: THREE.DoubleSide
    });
    const rim = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.1), rimMat);
    rim.position.z = -0.002;
    cardGroup.add(rim);

    const ambient = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambient);

    function loadTextures(headUrl, skullUrl) {
      loader.load(headUrl, (tex) => {
        headMat.map = tex;
        headMat.needsUpdate = true;
        augMat.map = tex;
        augMat.needsUpdate = true;
      });
      loader.load(skullUrl, (tex) => {
        skullMat.map = tex;
        skullMat.needsUpdate = true;
      });
    }

    const initSlug = (STAGES && STAGES[0] && STAGES[0].name ? (STAGES.find(s => s.stage_index === current) || STAGES[0]).name.toLowerCase().split(' ')[0].replace(/[^a-z0-9]/g,'') : 'neanderthal');
    loadTextures(getPersonImg(initSlug), IMG_SKULLS + (getSkullImg(initSlug) || getSkullImg(current)));

    function applyTilt(rxDeg, ryDeg) {
      const rx = rxDeg * (Math.PI / 180);
      const ry = ryDeg * (Math.PI / 180);
      cardGroup.rotation.x = rx;
      cardGroup.rotation.y = ry;
      const p = Math.max(0, Math.min(1, (ryDeg + 30) / 60));
      headMat.opacity = Math.max(0.15, 1 - p * 1.45);
      skullMat.opacity = Math.max(0, p < 0.5 ? (0.5 - p) * 1.9 : (p - 0.5) * 1.9);
      augMat.opacity = Math.min(0.85, p > 0.45 && p < 0.82 ? (p - 0.45) * 2.2 : 0);
      if (augMat.opacity > 0) {
        augMat.color.setHex(0xaaeeff);
      }
      holoMat.opacity = p > 0.22 && p < 0.72 ? 0.08 + Math.sin(Date.now() / 160) * 0.06 : 0;
    }

    function onTiltMove(clientX, clientY) {
      const rect = wrap.getBoundingClientRect();
      let ry = ((clientX - (rect.left + rect.width / 2)) / (rect.width / 2)) * 28;
      let rx = ((clientY - (rect.top + rect.height / 2)) / (rect.height / 2)) * -18;
      applyTilt(Math.max(-20, Math.min(20, rx)), Math.max(-30, Math.min(30, ry)));
    }

    wrap.addEventListener('mousemove', (e) => onTiltMove(e.clientX, e.clientY));
    wrap.addEventListener('mouseleave', () => applyTilt(0, 0));
    let touchActive = false;
    wrap.addEventListener('touchstart', (e) => {
      touchActive = true;
      onTiltMove(e.touches[0].clientX, e.touches[0].clientY);
    }, { passive: true });
    wrap.addEventListener('touchmove', (e) => {
      if (!touchActive) return;
      onTiltMove(e.touches[0].clientX, e.touches[0].clientY);
      e.preventDefault();
    }, { passive: false });
    wrap.addEventListener('touchend', () => {
      touchActive = false;
      applyTilt(0, 0);
    });

    function resize() {
      const nw = wrap.clientWidth || 320;
      renderer.setSize(nw, h, false);
      camera.aspect = nw / h;
      camera.updateProjectionMatrix();
    }
    global.addEventListener('resize', resize);

    function animate() {
      requestAnimationFrame(animate);
      if (holoMat.opacity > 0) {
        const ryDeg = cardGroup.rotation.y * (180 / Math.PI);
        const p = Math.max(0, Math.min(1, (ryDeg + 30) / 60));
        if (p > 0.22 && p < 0.72) {
          holoMat.opacity = 0.08 + Math.sin(Date.now() / 160) * 0.06;
        }
      }
      renderer.render(scene, camera);
    }
    animate();
    applyTilt(0, 0);

    holo3d = {
      applyTilt,
      setSkullTexture(url) {
        loader.load(url, (tex) => {
          skullMat.map = tex;
          skullMat.needsUpdate = true;
        });
      },
      setHeadTexture(url) {
        loader.load(url, (tex) => {
          headMat.map = tex;
          headMat.needsUpdate = true;
          if (augMat) {
            augMat.map = tex;
            augMat.needsUpdate = true;
          }
        });
      },
      pulseTilt() {
        applyTilt(4, 22);
        setTimeout(() => applyTilt(-3, -18), 700);
        setTimeout(() => applyTilt(0, 0), 1400);
      }
    };
  }

  function initLiveHoloCard() {
    initHolo3DCard();
  }

  function updateLiveHoloCard(idx) {
    const s = getStage(idx);
    if (!s) return;
    const specimenRaw = s.key_fossils && s.key_fossils[0] ? s.key_fossils[0] : '—';
    const specimen = String(specimenRaw).split(',')[0].trim();
    const slug = (s.name || '').toLowerCase().split(' ')[0].replace(/[^a-z]/g, '') || idx;
    const skullUrl = IMG_SKULLS + (getSkullImg(idx) || getSkullImg(slug));
    const headUrl = getPersonImg(slug);
    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };
    set('enrich-card-header-text', `HOLO BADGE • ${s.name.split('(')[0].trim().toUpperCase()}`);
    set('enrich-card-specimen', `SPECIMEN: ${specimen}`);
    if (holo3d && holo3d.setSkullTexture) {
      holo3d.setSkullTexture(skullUrl);
    }
    if (holo3d && holo3d.setHeadTexture) {
      holo3d.setHeadTexture(headUrl);
    }
  }

  async function loadFullLiteDeck() {
    const container = document.getElementById('enrich-full-lite-deck');
    if (!container) return;
    if (liteDeckLoaded && container.children.length > 0) {
      container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      return;
    }
    container.innerHTML = '<div style="font-size:10px;opacity:0.6;padding:4px;">Loading full haze holo deck — automatic duplicated+vertically-flipped blurred stretched side panels + iridescent regular variation center (red/blue glasses for pronounced 3D holo). Prompt/content built into cards.</div>';
    let types = [];
    try {
      const res = await fetch('/featured_templates/holo-skull-badge/data/skull_types.json');
      const data = await res.json();
      types = data.skull_types || [];
    } catch (_) {
      types = [{ slug: 'neanderthal', display: 'Neanderthal', specimen_id: 'Amud 1', type: 'hominin' }];
    }
    container.innerHTML = '';
    container.style.gap = '12px';
    // Allow larger combined haze cards
    types.forEach((t, i) => container.appendChild(createLiteHoloCard(t, i)));
    liteDeckLoaded = true;
  }

  function createLiteHoloCard(typeInfo) {
    const el = document.createElement('div');
    const hazeUrl = getHazeHoloCard(typeInfo.slug);
    // Use the automatically generated larger combined haze holo card (center = regular iridescent person variation of base-ref;
    // sides = duplicated + vertically-flipped (horizontal mirror) + blurred + stretched haze versions of the sides for
    // pronounced red/blue anaglyph holographic 3D + iridescence effect). Prompt/content/metadata built into the card image.
    el.style.cssText = `width:320px; min-height:210px; background:#111; border:1px solid #333; border-radius:6px; overflow:hidden; cursor:pointer; flex-shrink:0; position:relative; box-shadow:0 8px 24px -6px rgba(0,0,0,0.6)`;
    el.innerHTML = `
      <img src="${hazeUrl}" style="width:100%; height:auto; display:block; background:#000; image-rendering: -webkit-optimize-contrast;" alt="${typeInfo.display} haze holo card (center regular variation + mirrored blurred stretched sides for anaglyph holo)">
      <div style="position:absolute; bottom:0; left:0; right:0; height:18px; background:rgba(17,17,17,0.85); font-size:6px; color:#0ff; padding:1px 4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; border-top:1px solid #222;">
        HAZE HOLO • ${typeInfo.display} • ${typeInfo.specimen_id || ''}
      </div>`;
    el.addEventListener('click', () => {
      const match = STAGES.findIndex((st) => (st.name || '').toLowerCase().includes(typeInfo.slug) || (typeInfo.slug === 'neanderthal' && st.stage_index === 7) || (typeInfo.slug === 'erectus' && st.stage_index === 5));
      if (match >= 0) setCurrent(match, { source: 'lite-deck' });
      const live = document.getElementById('holo-portrait-wrap');
      if (live) live.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
    // Fallback if haze not generated: simple person + meas (previous behavior)
    const img = el.querySelector('img');
    if (img) {
      img.onerror = () => {
        // rebuild as tech card with person var + meas (for cases where haze not present)
        el.style.width = '158px';
        el.style.minHeight = '134px';
        const personUrl = getPersonImg(typeInfo.slug);
        const skullUrl = IMG_SKULLS + `${typeInfo.slug}-skull.jpg`;
        const meas = getMeasurements(typeInfo.slug);
        let lineEls = '';
        const artH = 82; const photoW = 112; const chartW = 42; const artW = photoW + chartW;
        meas.forEach((m, mi) => {
          const y = Math.max(6, Math.min(artH - 6, Math.round(m.y * artH)));
          const accent = mi % 2 === 0 ? '#00f0ff' : '#e6e8ee';
          lineEls += `<line x1="4" y1="${y}" x2="${artW - 3}" y2="${y}" stroke="${accent}" stroke-width="1" />`;
          lineEls += `<text x="${photoW + 5}" y="${y - 2}" font-size="3.8" fill="#ccc" font-family="monospace">${m.label}</text>`;
          if (m.val && m.val !== '—') lineEls += `<text x="${photoW + 5}" y="${y + 5}" font-size="3.4" fill="#0ff" font-family="monospace">${m.val}</text>`;
        });
        const measSvg = `<svg class="meas" width="${artW}" height="${artH}" style="position:absolute;left:0;top:0;pointer-events:none" viewBox="0 0 ${artW} ${artH}">${lineEls}</svg>`;
        el.innerHTML = `
          <div style="height:15px;background:#1a1d24;font-size:5.5px;padding:0 4px;color:#00f0ff;display:flex;justify-content:space-between;border-bottom:1px solid #222">
            <span>HOLO • VAR</span><span style="color:#fff;font-family:monospace">${(typeInfo.specimen_id || '').substring(0, 12)}</span>
          </div>
          <div style="height:82px;position:relative;background:#000;display:flex">
            <img src="${personUrl}" style="width:112px;height:100%;object-fit:contain;background:#000" alt="">
            ${measSvg}
          </div>
          <div style="height:33px;padding:2px 4px;background:#111;font-size:5.5px;border-top:1px solid #222">
            <div style="font-weight:600;color:#fff;font-size:6.5px">base-ref as ${typeInfo.display}</div>
            <div style="color:#888;font-size:4.8px">${typeInfo.type} • ${typeInfo.specimen_id || ''}</div>
          </div>`;
      };
    }
    return el;
  }

  const ENRICH_COLLAPSE_KEYS = {
    controls: 'holo-enrich-controls-collapsed',
    live: 'holo-enrich-live-collapsed',
    lenticular: 'holo-enrich-lenticular-collapsed',
    skinning: 'holo-enrich-skinning-collapsed',
    refs: 'holo-enrich-refs-collapsed'
  };

  function setEnrichSectionCollapsed(sectionId, collapsed) {
    const section = document.getElementById(sectionId);
    const toggle = section && section.querySelector('.enrichment-toggle');
    if (!section || !toggle) return;
    section.classList.toggle('collapsed', collapsed);
    toggle.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
    const key = ENRICH_COLLAPSE_KEYS[sectionId.replace('enrich-section-', '')];
    if (key) {
      try {
        localStorage.setItem(key, collapsed ? '1' : '0');
      } catch (_) {}
    }
  }

  function toggleEnrichSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (!section) return;
    setEnrichSectionCollapsed(sectionId, !section.classList.contains('collapsed'));
  }

  function initEnrichCollapse(sectionId, defaultCollapsed) {
    const section = document.getElementById(sectionId);
    if (!section) return;
    const keyPart = sectionId.replace('enrich-section-', '');
    let collapsed = defaultCollapsed;
    try {
      const saved = localStorage.getItem(ENRICH_COLLAPSE_KEYS[keyPart]);
      if (saved !== null) collapsed = saved === '1';
    } catch (_) {}
    setEnrichSectionCollapsed(sectionId, collapsed);
  }

  function expandEnrichSections(sectionIds) {
    (sectionIds || []).forEach((id) => setEnrichSectionCollapsed(id, false));
  }

  function scrollToShopSection() {
    const el = document.getElementById('hero');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function scrollToCodeSection() {
    expandEnrichSections(['enrich-section-controls']);
    const el = document.getElementById('enrich-section-controls') || document.getElementById('data-enrichment');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function scrollToEditSection() {
    expandEnrichSections(['enrich-section-live']);
    const el = document.getElementById('enrich-section-live');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function scrollToEnrichment() {
    scrollToCodeSection();
    setEnrichSectionCollapsed('enrich-section-live', false);
  }

  function onChromeStage(idx, source) {
    if (idx === current && source !== 'init') return;
    current = idx;
    renderAll();
    if ((source === 'stage-nav' || source === 'deck' || source === 'skull-tile') && !IS_MOBILE && holo3d && holo3d.pulseTilt) {
      holo3d.pulseTilt();
    }
  }

  async function init() {
    await loadFullLineage();
    if (global.HoloChrome) {
      global.HoloChrome.onStageChange(onChromeStage);
      current = global.HoloChrome.getStageIndex();
    }
    initEnrichCollapse('enrich-section-controls', false);
    initEnrichCollapse('enrich-section-live', false);
    initEnrichCollapse('enrich-section-lenticular', true);
    initEnrichCollapse('enrich-section-skinning', true);
    initEnrichCollapse('enrich-section-refs', true);
    initLiveHoloCard();
    if (!holo3d && typeof global.THREE !== 'undefined') {
      setTimeout(initLiveHoloCard, 150);
    }
    renderAll();
    if (skinDemoTimer) clearInterval(skinDemoTimer);
    skinDemoTimer = setInterval(() => drawSimpleThreeDemo(getStage(current)), 120);

    document.addEventListener('keydown', (e) => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
      if (e.key === 'ArrowLeft') prevStage();
      if (e.key === 'ArrowRight') nextStage();
      if (e.key.toLowerCase() === 'r' && !e.metaKey && !e.ctrlKey) randomStage();
      if (e.key.toLowerCase() === 'c' && e.shiftKey) copyBible();
    });

    if (location.hash === '#enrichment' || location.hash === '#data-enrichment') {
      setTimeout(() => {
        scrollToCodeSection();
        if (global.HoloChrome) global.HoloChrome.updateNavActive('code');
      }, 200);
    } else if (location.hash === '#edit' || location.hash === '#enrich-section-live') {
      setTimeout(() => {
        scrollToEditSection();
        if (global.HoloChrome) global.HoloChrome.updateNavActive('edit');
      }, 200);
    } else if (location.hash === '#hero') {
      setTimeout(() => {
        scrollToShopSection();
        if (global.HoloChrome) global.HoloChrome.updateNavActive('shop');
      }, 200);
    }
  }

  global.LineageEnrichment = {
    init,
    renderAll,
    syncFromChrome,
    setCurrent,
    getStages,
    getStage,
    getCurrent: () => current,
    prevStage,
    nextStage,
    randomStage,
    copyBible,
    copyPrompt,
    generateImaginePrompt,
    showSplineLinks,
    loadFullLiteDeck,
    scrollToEnrichment,
    scrollToShopSection,
    scrollToCodeSection,
    scrollToEditSection,
    expandEnrichSections,
    toggleEnrichSection
  };

  global.prevStage = prevStage;
  global.nextStage = nextStage;
  global.randomStage = randomStage;
  global.copyBible = copyBible;
  global.copyPrompt = copyPrompt;
  global.generateImaginePrompt = generateImaginePrompt;
  global.showSplineLinks = showSplineLinks;
  global.loadFullLiteDeck = loadFullLiteDeck;
  global.getPersonImg = getPersonImg;
  global.getHazeHoloCard = getHazeHoloCard;
  global.toggleEnrichSection = function (sectionId) {
    toggleEnrichSection(sectionId);
  };
})(window);
