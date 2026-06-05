/**
 * Shared chrome: unified header, lineage stage navigator, collapsible skull hero gallery.
 * Used by holo-viewer.html and holo_id_badges/index.html
 */
(function (global) {
  'use strict';

  const STORAGE_KEY = 'holo-chrome-stage-index';
  const SKULL_GALLERY_COLLAPSED_KEY = 'holo-chrome-skull-gallery-collapsed';
  const LINEAGE_URL = '/character_bibles/ancestory/hominin_data/hominin_lineage_timeline.json';
  const VIEWER_SEGMENT = '/featured_templates/holo-skull-badge/';
  const IMG_BASE = '/featured_templates/holo-skull-badge/img';
  const STAGE_PERSON_SLUG = {
    0: 'sahelanthropus',
    1: 'sahelanthropus',
    2: 'australopithecus',
    3: 'australopithecus',
    4: 'erectus',
    5: 'erectus',
    6: 'erectus',
    7: 'neanderthal',
    8: 'erectus',
    9: 'base-headshot',
    10: 'base-headshot'
  };
  const NAV_SECTIONS = {
    shop: { targetId: 'hero', title: 'Product showcase — import photo + ID card' },
    code: { targetId: 'data-enrichment', expand: ['enrich-section-controls'], title: 'Timeline controls + full prompt' },
    edit: { targetId: 'enrich-section-live', expand: ['enrich-section-live'], title: 'Live lenticular holo card' }
  };
  /** @deprecated use NAV_SECTIONS — kept for external hash redirects */
  const PAGES = {
    badges: '/featured_templates/holo-skull-badge/holo-viewer.html#data-enrichment',
    viewer: '/featured_templates/holo-skull-badge/holo-viewer.html'
  };

  const callbacks = [];
  let stages = [];
  let stageIndex = 7;
  let activePage = null;
  let activeNavSection = 'shop';
  let mounted = false;
  let stageNavBound = false;
  let navScrollSpyBound = false;
  let scrollSpyPaused = false;

  function readSavedStage(fallback) {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved !== null && saved !== '') {
        const n = parseInt(saved, 10);
        if (!Number.isNaN(n)) return n;
      }
    } catch (_) {}
    return fallback;
  }

  function persistStage(idx) {
    try {
      localStorage.setItem(STORAGE_KEY, String(idx));
    } catch (_) {}
  }

  function notifyStageChange(idx, source) {
    callbacks.forEach((fn) => {
      try {
        fn(idx, source);
      } catch (e) {
        console.warn('[HoloChrome] stage callback error', e);
      }
    });
  }

  function setStageIndex(idx, options = {}) {
    const max = stages.length ? stages.length - 1 : 10;
    const clamped = Math.max(0, Math.min(max, idx));
    stageIndex = clamped;
    persistStage(clamped);
    renderStageNavigator();
    if (!options.silent) notifyStageChange(clamped, options.source || 'stage-nav');
    return clamped;
  }

  function getStageIndex() {
    return stageIndex;
  }

  function getStages() {
    return stages;
  }

  function getStageByIndex(idx) {
    if (stages.length) {
      const found = stages.find((s) => (s.stage_index ?? s.i) === idx);
      if (found) return found;
      if (stages[idx]) return stages[idx];
    }
    return { stage_index: idx, name: `Stage ${idx}`, era: '' };
  }

  function onStageChange(fn) {
    if (typeof fn === 'function') callbacks.push(fn);
  }

  function resolveViewerAssetPaths() {
    const pathname = location.pathname || '';
    if (pathname.includes(VIEWER_SEGMENT)) {
      const base = pathname.substring(0, pathname.indexOf(VIEWER_SEGMENT) + VIEWER_SEGMENT.length);
      return {
        skullTypesUrl: base + 'data/skull_types.json',
        skullImgBase: base + 'img/skulls/'
      };
    }
    const dir = pathname.lastIndexOf('/') >= 0
      ? pathname.substring(0, pathname.lastIndexOf('/') + 1)
      : './';
    return {
      skullTypesUrl: dir + 'data/skull_types.json',
      skullImgBase: dir + 'img/skulls/'
    };
  }

  function setSkullGalleryCollapsed(collapsed) {
    const section = document.getElementById('holo-chrome-skull-gallery');
    const toggle = document.getElementById('holo-chrome-skull-gallery-toggle');
    if (!section || !toggle) return;
    section.classList.toggle('collapsed', collapsed);
    toggle.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
    try {
      localStorage.setItem(SKULL_GALLERY_COLLAPSED_KEY, collapsed ? '1' : '0');
    } catch (_) {}
  }

  function toggleSkullGallery() {
    const section = document.getElementById('holo-chrome-skull-gallery');
    if (!section) return;
    setSkullGalleryCollapsed(!section.classList.contains('collapsed'));
  }

  function initSkullGalleryCollapse() {
    const section = document.getElementById('holo-chrome-skull-gallery');
    if (!section) return;
    let collapsed = true;
    try {
      const saved = localStorage.getItem(SKULL_GALLERY_COLLAPSED_KEY);
      if (saved !== null) collapsed = saved === '1';
    } catch (_) {}
    setSkullGalleryCollapsed(collapsed);
    const toggle = document.getElementById('holo-chrome-skull-gallery-toggle');
    if (toggle) toggle.addEventListener('click', toggleSkullGallery);
  }

  function specimenLabel(stage) {
    if (stage.key_fossils && stage.key_fossils.length) {
      const k = stage.key_fossils[0];
      return String(k).split(',')[0].trim().substring(0, 18);
    }
    return '—';
  }

  function truncateText(text, maxLen) {
    if (!text) return '—';
    const s = String(text).replace(/\s+/g, ' ').trim();
    return s.length <= maxLen ? s : s.slice(0, maxLen - 1) + '…';
  }

  function normalizeStage(st) {
    if (!st) return { stage_index: 0, name: 'Stage 0', era: '', unified_migration_lineage: '', admixture: 'N/A', fossil_refs: '', bible_snippet: '', mixamo: '' };
    return {
      stage_index: st.stage_index ?? st.i ?? 0,
      name: st.name || '',
      era: st.era || '',
      unified_migration_lineage: st.unified_migration_lineage || '',
      admixture: st.genetic_admixture_estimates || st.admixture || 'N/A',
      fossil_refs: Array.isArray(st.fossil_refs) ? st.fossil_refs.join('; ') : (st.fossil_refs || ''),
      bible_snippet: st.bible_snippet || '',
      mixamo: st.mixamo_threejs || st.mixamo || st.ik_pose_shapes || '',
      key_fossils: st.key_fossils || []
    };
  }

  function getSpecimenId(stage) {
    const label = specimenLabel(stage);
    if (label !== '—') return label;
    if (stage.fossil_refs) {
      const refs = Array.isArray(stage.fossil_refs) ? stage.fossil_refs[0] : stage.fossil_refs;
      const match = String(refs).match(/['"]([^'"]+)['"]|([A-Z]{2,}\s*\d+|[A-Z]+-\w+-\d+)/);
      if (match) return (match[1] || match[2] || '').trim();
    }
    return '—';
  }

  function getCardArtUrl(idx) {
    if (idx === 7) return IMG_BASE + '/example-holo-card.jpg';
    return IMG_BASE + '/holo-card-still.jpg';
  }

  function getStagePersonSlug(idx) {
    if (STAGE_PERSON_SLUG[idx] !== undefined) return STAGE_PERSON_SLUG[idx];
    const stage = getStageByIndex(idx);
    const name = (stage.name || '').toLowerCase();
    if (name.includes('neanderthal')) return 'neanderthal';
    if (name.includes('sapiens') || name.includes('modern')) return 'base-headshot';
    if (name.includes('australopith') || name.includes('paranthropus')) return 'australopithecus';
    if (name.includes('sahelanthropus') || name.includes('ardipithecus')) return 'sahelanthropus';
    if (name.includes('erectus') || name.includes('habilis') || name.includes('heidelberg') || name.includes('denisovan')) {
      return 'erectus';
    }
    const first = name.split(' ')[0].replace(/[^a-z]/g, '');
    return first || 'neanderthal';
  }

  function getPersonPortraitUrl(idx) {
    const slug = getStagePersonSlug(idx);
    if (slug === 'base-headshot') return IMG_BASE + '/base-headshot-ref.jpg';
    if (global.getPersonImg) return global.getPersonImg(slug);
    return IMG_BASE + '/variations/01.persons/' + slug + '-person.jpg';
  }

  function getStageList() {
    return stages.length
      ? stages
      : Array.from({ length: 11 }, (_, i) => ({ stage_index: i, name: `Stage ${i}`, era: '' }));
  }

  function getStageCount() {
    return getStageList().length;
  }

  function goPrevStage() {
    const count = getStageCount();
    setStageIndex((stageIndex - 1 + count) % count, { source: 'stage-nav' });
  }

  function goNextStage() {
    const count = getStageCount();
    setStageIndex((stageIndex + 1) % count, { source: 'stage-nav' });
  }

  function expandEnrichSections(sectionIds) {
    if (global.LineageEnrichment && global.LineageEnrichment.expandEnrichSections) {
      global.LineageEnrichment.expandEnrichSections(sectionIds);
      return;
    }
    (sectionIds || []).forEach((id) => {
      const section = document.getElementById(id);
      if (!section || !section.classList.contains('collapsed')) return;
      if (global.LineageEnrichment && global.LineageEnrichment.toggleEnrichSection) {
        global.LineageEnrichment.toggleEnrichSection(id);
      } else if (typeof global.toggleEnrichSection === 'function') {
        global.toggleEnrichSection(id);
      } else {
        section.classList.remove('collapsed');
        const toggle = section.querySelector('.enrichment-toggle');
        if (toggle) toggle.setAttribute('aria-expanded', 'true');
      }
    });
  }

  function smoothScrollToElement(el) {
    if (!el) return;
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function scrollToNavSection(nav) {
    const cfg = NAV_SECTIONS[nav];
    if (!cfg) return;
    if (cfg.expand) expandEnrichSections(cfg.expand);
    const el = document.getElementById(cfg.targetId);
    if (el) smoothScrollToElement(el);
    else if (nav === 'shop') window.scrollTo({ top: 0, behavior: 'smooth' });
    updateNavActive(nav);
    pauseScrollSpy(900);
  }

  function updateNavActive(nav) {
    activeNavSection = nav || activeNavSection;
    document.querySelectorAll('[data-holo-nav]').forEach((btn) => {
      const key = btn.getAttribute('data-holo-nav');
      const isActive = key === activeNavSection;
      btn.classList.toggle('is-active', isActive);
      btn.classList.toggle('is-inactive', !isActive);
      btn.classList.toggle('btn-featured-primary', isActive);
      btn.classList.toggle('btn-featured-secondary', !isActive);
      btn.setAttribute('aria-current', isActive ? 'true' : 'false');
    });
  }

  function computeActiveSectionFromScroll() {
    const probe = 120;
    const order = [
      { nav: 'shop', el: document.getElementById('hero') },
      { nav: 'code', el: document.getElementById('data-enrichment') },
      { nav: 'edit', el: document.getElementById('enrich-section-live') }
    ];
    let active = 'shop';
    order.forEach(({ nav, el }) => {
      if (el && el.getBoundingClientRect().top <= probe) active = nav;
    });
    return active;
  }

  function pauseScrollSpy(ms) {
    scrollSpyPaused = true;
    setTimeout(() => { scrollSpyPaused = false; }, ms);
  }

  function initNavScrollSpy() {
    if (navScrollSpyBound) return;
    navScrollSpyBound = true;

    let ticking = false;
    const onScroll = () => {
      if (scrollSpyPaused || ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        if (scrollSpyPaused) return;
        const next = computeActiveSectionFromScroll();
        if (next !== activeNavSection) updateNavActive(next);
      });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  function bindNavFromHash() {
    const hash = (location.hash || '').replace(/^#/, '');
    if (!hash) return;
    setTimeout(() => {
      if (hash === 'hero') scrollToNavSection('shop');
      else if (hash === 'data-enrichment' || hash === 'enrichment') scrollToNavSection('code');
      else if (hash === 'enrich-section-live' || hash === 'edit') scrollToNavSection('edit');
    }, 250);
  }

  function initNavHandlers(root) {
    root.querySelectorAll('[data-holo-nav]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        persistStage(stageIndex);
        const nav = btn.getAttribute('data-holo-nav');
        if (global.LineageEnrichment) {
          if (nav === 'shop' && global.LineageEnrichment.scrollToShopSection) {
            global.LineageEnrichment.scrollToShopSection();
          } else if (nav === 'code' && global.LineageEnrichment.scrollToCodeSection) {
            global.LineageEnrichment.scrollToCodeSection();
          } else if (nav === 'edit' && global.LineageEnrichment.scrollToEditSection) {
            global.LineageEnrichment.scrollToEditSection();
          } else {
            scrollToNavSection(nav);
          }
        } else {
          scrollToNavSection(nav);
        }
        updateNavActive(nav);
        pauseScrollSpy(900);
      });
    });
    initNavScrollSpy();
    bindNavFromHash();
  }

  function renderNavButtons() {
    return Object.entries(NAV_SECTIONS).map(([key, cfg]) => {
      const isActive = key === activeNavSection;
      const stateClass = isActive ? 'is-active btn-featured-primary' : 'is-inactive btn-featured-secondary';
      return `<button type="button" class="btn-featured ${stateClass}" data-holo-nav="${key}" title="${cfg.title}" aria-current="${isActive ? 'true' : 'false'}">${key}</button>`;
    }).join('');
  }

  function renderHeader(root, page) {
    const titles = {
      badges: { logo: 'HOLO∴SKULL', title: 'Holo Skull Badge', sub: 'Lineage Data • Lenticular Cards • Solid Column' },
      viewer: { logo: 'HOLO∴SKULL', title: 'Holo Skull Badge', sub: 'Product Showcase Template • Skull Reveal' }
    };
    const t = titles[page] || titles.viewer;

    root.innerHTML = `
      <header class="holo-chrome-header">
        <div style="display:flex;align-items:center;gap:14px;min-width:0">
          <div class="holo-chrome-logo">${t.logo}</div>
          <div style="min-width:0">
            <div style="font-weight:600;font-size:15px;color:var(--holo-text,#e6e8ee)">${t.title}</div>
            <div class="holo-chrome-tagline">${t.sub}</div>
          </div>
        </div>
        <nav class="holo-chrome-nav" aria-label="Page sections">
          ${renderNavButtons()}
        </nav>
      </header>
      <div class="holo-chrome-bar">
        <div class="holo-chrome-bar-inner">
          <div class="holo-chrome-section-title">Lineage Stage Navigator</div>
          <div id="holo-chrome-stage-nav" class="holo-chrome-stage-nav" role="region" aria-label="Lineage stage navigator">
            <button type="button" id="holo-chrome-prev" class="holo-chrome-nav-btn" aria-label="Previous stage">◀ Prev</button>
            <div class="holo-chrome-card-column">
              <div id="holo-chrome-flip-card" class="holo-chrome-flip-card" tabindex="0" aria-live="polite"></div>
              <div id="holo-chrome-stage-portrait" class="holo-chrome-stage-portrait" aria-live="polite"></div>
            </div>
            <div id="holo-chrome-stage-data-panel" class="data-panel holo-chrome-stage-data-panel" aria-live="polite">
              <div id="holo-chrome-stage-name" class="holo-chrome-data-stage-name"></div>
              <div id="holo-chrome-stage-era" class="holo-chrome-data-stage-era"></div>
              <div class="holo-chrome-section-title">Unified Migration Lineage (solid column)</div>
              <div class="migration" id="holo-chrome-solid-column"></div>
              <div class="holo-chrome-info-grid">
                <div>
                  <div class="holo-chrome-section-title">Genetic Admixture</div>
                  <div id="holo-chrome-admixture" class="holo-chrome-admixture"></div>
                </div>
                <div>
                  <div class="holo-chrome-section-title">Fossil Refs</div>
                  <div id="holo-chrome-fossil-refs" class="holo-chrome-fossil-refs"></div>
                </div>
              </div>
              <div class="holo-chrome-data-block">
                <div class="holo-chrome-section-title">Prompt-ready Bible Snippet</div>
                <div class="prompt-box" id="holo-chrome-bible-snippet"></div>
              </div>
              <div class="holo-chrome-data-block">
                <div class="holo-chrome-section-title">Mixamo + Three.js IK / Pose / Shape</div>
                <div id="holo-chrome-mixamo-threejs" class="holo-chrome-mixamo"></div>
              </div>
              <div class="data-panel-actions">
                <button type="button" id="holo-chrome-btn-imagine" class="holo-chrome-action-btn holo-chrome-action-btn-primary">Generate Imagine Prompt</button>
                <button type="button" id="holo-chrome-btn-spline" class="holo-chrome-action-btn">View Source Spline</button>
                <button type="button" id="holo-chrome-btn-copy-bible" class="holo-chrome-action-btn">Copy Prompt Snippet</button>
                <button type="button" id="holo-chrome-btn-copy-full" class="holo-chrome-action-btn">Copy Full Prompt</button>
              </div>
            </div>
            <button type="button" id="holo-chrome-next" class="holo-chrome-nav-btn" aria-label="Next stage">Next ▶</button>
          </div>
          <div class="holo-chrome-stage-meta">
            <div id="holo-chrome-stage-dots" class="holo-chrome-stage-dots" role="tablist" aria-label="Stage indicators"></div>
            <span id="holo-chrome-stage-counter" class="holo-chrome-stage-counter"></span>
          </div>
        </div>
      </div>
      <div class="holo-chrome-bar">
        <div class="holo-chrome-bar-inner">
          <div class="holo-chrome-skull-gallery collapsed" id="holo-chrome-skull-gallery">
            <button type="button" class="holo-chrome-skull-gallery-toggle" id="holo-chrome-skull-gallery-toggle" aria-expanded="false">
              <span>All Skull Types (Hominin + Animal + Mythical/Animorph)</span>
              <span class="holo-chrome-skull-gallery-chevron" aria-hidden="true">▲</span>
            </button>
            <div class="holo-chrome-skull-gallery-body" id="holo-chrome-skull-gallery-body">
              <p class="holo-chrome-skull-gallery-desc">All supported skull types for holo badge generation — hominin, animal, and mythical/animorph. Click any to copy a ready prompt for Grok Imagine (Product Showcase + this skull type). Includes specimen IDs for lineage tracking.</p>
              <div id="skull-hero-grid" class="holo-chrome-skull-hero-grid" role="list" aria-label="Skull types hero gallery"></div>
              <p class="holo-chrome-skull-gallery-footnote">Animal skulls (chimp, gorilla, wolf…) and animorphs/mythical (vampire, werewolf, orc, fairy, satyr, etc.) for fantasy character bibles and cards. Stage selection persists across shop / code / edit.</p>
            </div>
          </div>
        </div>
      </div>
    `;

    initNavHandlers(root);
  }

  function renderFlipCard(stage, idx) {
    const shortName = (stage.name || `Stage ${idx}`).split('(')[0].trim();
    const artUrl = getCardArtUrl(idx);
    const hasExampleArt = idx === 7;
    return `
      <div class="holo-chrome-flip-card-inner holo-chrome-flip-card-glow">
        <div class="holo-chrome-flip-card-head">
          <span>HOLO∴ANCESTORY</span>
          <span class="holo-chrome-flip-card-index">${String(idx).padStart(2, '0')}</span>
        </div>
        <div class="holo-chrome-flip-card-art${hasExampleArt ? ' has-example-art' : ' is-generic'}">
          <div class="holo-chrome-flip-card-stage-bg" aria-hidden="true">${idx}</div>
          <img src="${artUrl}" alt="${shortName} holo card" loading="lazy">
        </div>
        <div class="holo-chrome-flip-card-foot">
          <div class="holo-chrome-flip-card-name">${shortName}</div>
          <div class="holo-chrome-flip-card-era">${stage.era || ''}</div>
        </div>
      </div>`;
  }

  function renderStagePortrait(stage, idx) {
    const shortName = (stage.name || `Stage ${idx}`).split('(')[0].trim();
    const portraitUrl = getPersonPortraitUrl(idx);
    return `
      <div class="holo-chrome-stage-portrait-inner holo-chrome-flip-card-glow">
        <div class="holo-chrome-stage-portrait-head">
          <span>STAGE PORTRAIT</span>
          <span class="holo-chrome-flip-card-index">${String(idx).padStart(2, '0')}</span>
        </div>
        <div class="holo-chrome-stage-portrait-art">
          <img src="${portraitUrl}" alt="${shortName} stage portrait" loading="lazy">
          <div class="holo-chrome-stage-portrait-placeholder" aria-hidden="true">
            <span class="holo-chrome-stage-portrait-placeholder-icon">◇</span>
            <span>No portrait for this stage</span>
          </div>
        </div>
        <div class="holo-chrome-stage-portrait-foot">
          <div class="holo-chrome-flip-card-name">${shortName}</div>
          <div class="holo-chrome-flip-card-era">${stage.era || ''}</div>
        </div>
      </div>`;
  }

  function bindStagePortraitImage(portraitEl) {
    if (!portraitEl) return;
    const img = portraitEl.querySelector('.holo-chrome-stage-portrait-art img');
    if (!img) return;
    portraitEl.classList.remove('is-missing');
    img.onerror = () => {
      portraitEl.classList.add('is-missing');
    };
    img.onload = () => {
      if (img.naturalWidth > 0) portraitEl.classList.remove('is-missing');
    };
  }

  function populateStageDataPanel(stageOrIdx) {
    const raw = typeof stageOrIdx === 'number' ? getStageByIndex(stageOrIdx) : stageOrIdx;
    const s = normalizeStage(raw);
    const set = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.textContent = text;
    };
    const setHtml = (id, html) => {
      const el = document.getElementById(id);
      if (el) el.innerHTML = html;
    };

    set('holo-chrome-stage-name', s.name);
    set('holo-chrome-stage-era', s.era);
    set('holo-chrome-solid-column', s.unified_migration_lineage);
    setHtml('holo-chrome-admixture', `<strong>${s.admixture}</strong>`);
    setHtml('holo-chrome-fossil-refs', String(s.fossil_refs || '').replace(/;/g, '<br>'));
    set('holo-chrome-bible-snippet', s.bible_snippet);
    set('holo-chrome-mixamo-threejs', s.mixamo);
  }

  function copyBibleSnippet() {
    const s = normalizeStage(getStageByIndex(stageIndex));
    navigator.clipboard.writeText(s.bible_snippet).then(
      () => alert('Prompt snippet copied. Paste into madlibs [MASTER ANCESTRY + ANATOMY BIBLE] block.'),
      () => prompt('Copy bible snippet:', s.bible_snippet)
    );
  }

  function copyFullPrompt() {
    const s = normalizeStage(getStageByIndex(stageIndex));
    const p = `[MASTER ANCESTRY + ANATOMY BIBLE - REPEAT VERBATIM]:\n${s.bible_snippet}\n\nFace/body/bones from ${s.fossil_refs}. Pose/IK: ${s.mixamo}. Reference the exact fossil casts/scans in prompt for accuracy. Holo ID badge style if generating card.`;
    navigator.clipboard.writeText(p).then(
      () => alert('Full prompt context copied for Grok Imagine.'),
      () => prompt('Copy full prompt:', p)
    );
  }

  function generateImaginePrompt() {
    const s = normalizeStage(getStageByIndex(stageIndex));
    const prompt = `Photoreal portrait of ${s.name} (${s.era}), ${s.bible_snippet}. Highly detailed face and cranium exactly matching ${String(s.fossil_refs).split(';')[0]}. Body proportions and posture from postcranial evidence. ${String(s.mixamo).split('.')[0]}. Cinematic lighting, film grain, accurate to fossil reconstruction, neutral background for reference.`;
    navigator.clipboard.writeText(prompt).then(
      () => alert('Imagine prompt copied. Use with style_presets + repeat prompt snippet for holo badge series consistency.'),
      () => prompt('Copy Imagine prompt:', prompt)
    );
  }

  function showSplineLinks() {
    alert('Holo ID badge / 3D card concepts:\n\n• https://www.instagram.com/tadericson/p/CzsYfNVL2XX/\n• https://community.spline.design/file/599304aa-55a7-431e-86ee-b3d8cd6ecca0\n• https://app.spline.design/file/3a0e7933-4ce5-47d7-aa9c-cdfdd973f9b5\n• https://app.spline.design/file/999700e2-df6d-4afc-8150-85b06fd64008');
  }

  let dataPanelActionsBound = false;

  function initDataPanelActions() {
    if (dataPanelActionsBound) return;
    dataPanelActionsBound = true;
    const bind = (id, fn) => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('click', fn);
    };
    bind('holo-chrome-btn-imagine', () => {
      if (global.LineageEnrichment && global.LineageEnrichment.generateImaginePrompt) {
        global.LineageEnrichment.generateImaginePrompt();
      } else {
        generateImaginePrompt();
      }
    });
    bind('holo-chrome-btn-spline', () => {
      if (global.LineageEnrichment && global.LineageEnrichment.showSplineLinks) {
        global.LineageEnrichment.showSplineLinks();
      } else {
        showSplineLinks();
      }
    });
    bind('holo-chrome-btn-copy-bible', () => {
      if (global.LineageEnrichment && global.LineageEnrichment.copyBible) {
        global.LineageEnrichment.copyBible();
      } else {
        copyBibleSnippet();
      }
    });
    bind('holo-chrome-btn-copy-full', () => {
      if (global.LineageEnrichment && global.LineageEnrichment.copyPrompt) {
        global.LineageEnrichment.copyPrompt();
      } else {
        copyFullPrompt();
      }
    });
  }

  function renderStageDots() {
    const dotsEl = document.getElementById('holo-chrome-stage-dots');
    if (!dotsEl) return;
    const list = getStageList();
    dotsEl.innerHTML = '';
    list.forEach((s, i) => {
      const idx = s.stage_index ?? i;
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'holo-chrome-stage-dot' + (idx === stageIndex ? ' is-active' : '');
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-selected', idx === stageIndex ? 'true' : 'false');
      dot.setAttribute('aria-label', `Stage ${idx}: ${(s.name || '').split('(')[0].trim()}`);
      dot.title = s.name || `Stage ${idx}`;
      dot.addEventListener('click', () => setStageIndex(idx, { source: 'stage-nav' }));
      dotsEl.appendChild(dot);
    });
  }

  function renderStageNavigator() {
    const cardEl = document.getElementById('holo-chrome-flip-card');
    const portraitEl = document.getElementById('holo-chrome-stage-portrait');
    const counterEl = document.getElementById('holo-chrome-stage-counter');
    const prevBtn = document.getElementById('holo-chrome-prev');
    const nextBtn = document.getElementById('holo-chrome-next');
    if (!cardEl) return;

    const stage = getStageByIndex(stageIndex);
    const list = getStageList();
    const count = list.length;
    const pos = list.findIndex((s, i) => (s.stage_index ?? i) === stageIndex);
    const displayNum = pos >= 0 ? pos + 1 : stageIndex + 1;

    cardEl.innerHTML = renderFlipCard(stage, stageIndex);
    if (portraitEl) {
      portraitEl.innerHTML = renderStagePortrait(stage, stageIndex);
      bindStagePortraitImage(portraitEl);
    }
    populateStageDataPanel(stage);

    if (counterEl) {
      counterEl.textContent = `${displayNum} / ${count}`;
    }
    if (prevBtn) prevBtn.disabled = count <= 1;
    if (nextBtn) nextBtn.disabled = count <= 1;

    renderStageDots();
  }

  function initStageNavigator() {
    if (stageNavBound) return;
    stageNavBound = true;

    const prevBtn = document.getElementById('holo-chrome-prev');
    const nextBtn = document.getElementById('holo-chrome-next');
    const cardEl = document.getElementById('holo-chrome-flip-card');

    if (prevBtn) prevBtn.addEventListener('click', goPrevStage);
    if (nextBtn) nextBtn.addEventListener('click', goNextStage);

    if (cardEl) {
      cardEl.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
          e.preventDefault();
          e.stopPropagation();
          goPrevStage();
        } else if (e.key === 'ArrowRight') {
          e.preventDefault();
          e.stopPropagation();
          goNextStage();
        }
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      const root = document.getElementById('holo-chrome-root');
      if (!root) return;
      e.preventDefault();
      e.stopPropagation();
      if (e.key === 'ArrowLeft') goPrevStage();
      else goNextStage();
    }, true);
  }

  function buildSkullHeroPrompt(type) {
    return `Apply the Product Showcase featured template. Clean high-end studio product photography of a futuristic holographic ID badge / digital playing card as the central "product". The badge has glossy iridescent holographic glass-like material with rainbow refraction, scanlines, floating 3D depth.
The card prominently features the exact person from the reference headshot photo (preserve 100% identity, face shape, skin tone, hair, expression, and likeness in the initial clear portrait layer).
The design shows a smooth cinematic holographic left pan / morph transition: starting with the sharp clear headshot portrait on the card -> shimmering iridescent holo dissolve and left pan revealing a highly detailed ${type.display} skull (Specimen ID: ${type.specimen_id}) with ${type.traits}, then continued pan to upper bones and skeleton in the same holographic iridescent floating style with subtle glowing bone landmarks.
For the skull layer use: ${type.prompt_addition}
Motion for video: 5-7 second fluid sequence with gentle left pan showing the full holo transition. Match the holographic skull pan motion style of the reference videos in this folder.
Stills: the finished holographic badge perfectly framed in Product Showcase style — centered on clean minimal dark gradient backdrop, soft studio lighting, tack sharp, luxurious collectible card product shot.
Reference photo subject must remain perfectly recognizable in the portrait state. Holo and bone layers are stylistic reveals only.`;
  }

  function matchStageForSkullSlug(slug) {
    const s = (slug || '').toLowerCase();
    const matchIdx = stages.findIndex((st) => {
      const name = (st.name || '').toLowerCase();
      if (name.includes(s)) return true;
      if (s === 'neanderthal' && (st.stage_index ?? -1) === 7) return true;
      if (s === 'erectus' && (st.stage_index ?? -1) === 5) return true;
      if (s === 'australopithecus' && (st.stage_index ?? -1) === 2) return true;
      if (s === 'sahelanthropus' && (st.stage_index ?? -1) === 0) return true;
      return false;
    });
    if (matchIdx >= 0) {
      const idx = stages[matchIdx].stage_index ?? matchIdx;
      setStageIndex(idx, { source: 'skull-gallery' });
    }
  }

  async function populateSkullHeroGallery() {
    const grid = document.getElementById('skull-hero-grid');
    if (!grid) return;

    const { skullTypesUrl, skullImgBase } = resolveViewerAssetPaths();

    try {
      const res = await fetch(skullTypesUrl);
      const data = await res.json();
      const types = data.skull_types || [];
      grid.innerHTML = '';

      types.forEach((type) => {
        const card = document.createElement('div');
        card.className = 'holo-chrome-skull-hero-card';
        card.setAttribute('role', 'listitem');
        card.tabIndex = 0;

        const img = document.createElement('img');
        img.src = `${skullImgBase}${type.slug}-skull.jpg`;
        img.alt = type.display;
        img.loading = 'lazy';
        img.onerror = () => {
          img.style.background = '#222';
          img.alt = '[Image]';
        };

        const info = document.createElement('div');
        info.className = 'holo-chrome-skull-hero-info';
        info.innerHTML = `
          <div class="holo-chrome-skull-hero-name">${type.display}</div>
          <div class="holo-chrome-skull-hero-spec">${type.specimen_id}</div>
          <div class="holo-chrome-skull-hero-meta">${type.type} • ${type.era || ''}</div>
        `;

        card.appendChild(img);
        card.appendChild(info);

        const copyPrompt = () => {
          const base = buildSkullHeroPrompt(type);
          navigator.clipboard.writeText(base).then(
            () => alert(`Prompt for ${type.display} (Specimen: ${type.specimen_id}) copied to clipboard! Use with your headshot ref in Product Showcase template.`),
            () => prompt('Copy this prompt for ' + type.display + ':', base)
          );
          matchStageForSkullSlug(type.slug);
        };

        card.addEventListener('click', copyPrompt);
        card.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            copyPrompt();
          }
        });

        grid.appendChild(card);
      });
    } catch (e) {
      grid.innerHTML = '<div class="holo-chrome-skull-hero-error">Could not load skull types or images. Serve from project root (e.g. python -m http.server 8000).</div>';
      console.error('[HoloChrome] Skull gallery error:', e);
    }
  }

  async function loadStages() {
    try {
      const res = await fetch(LINEAGE_URL);
      const full = await res.json();
      if (full && full.stages && full.stages.length >= 8) {
        stages = full.stages;
        return stages;
      }
    } catch (_) {}
    stages = [];
    return stages;
  }

  async function init(config) {
    const mount = config.mount || document.getElementById('holo-chrome-root');
    if (!mount) {
      console.warn('[HoloChrome] mount element not found');
      return;
    }

    activePage = config.page || 'viewer';
    const fallback = config.defaultStage ?? 7;
    stageIndex = readSavedStage(fallback);

    if (!mounted) {
      renderHeader(mount, activePage);
      mounted = true;
    }

    await loadStages();
    initStageNavigator();
    initDataPanelActions();
    renderStageNavigator();
    initSkullGalleryCollapse();
    await populateSkullHeroGallery();

    const initial = setStageIndex(stageIndex, { silent: true, source: 'init' });
    notifyStageChange(initial, 'init');

    console.log('%c[HoloChrome] Ready — stage ' + initial + ' (' + activePage + ')', 'color:#0af');
  }

  global.HoloChrome = {
    init,
    getStageIndex,
    setStageIndex,
    getStages,
    getStageByIndex,
    normalizeStage,
    populateStageDataPanel,
    getStagePersonSlug,
    getPersonPortraitUrl,
    onStageChange,
    toggleSkullGallery,
    populateSkullHeroGallery,
    STORAGE_KEY,
    SKULL_GALLERY_COLLAPSED_KEY,
    PAGES,
    NAV_SECTIONS,
    scrollToNavSection,
    updateNavActive
  };
})(window);
