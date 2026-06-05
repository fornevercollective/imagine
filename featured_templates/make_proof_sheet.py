#!/usr/bin/env python3
"""
Generate a repeatable, reusable Photographer's Contact Sheet / Vogue-style Editor Proof Sheet
for all Featured Templates.

Usage:
  python featured_templates/make_proof_sheet.py

Outputs:
  featured_templates/proof-sheet.html   (open in browser)

The HTML is designed to be:
- Beautiful raw film contact sheet + high-fashion editor proof (Vogue / Magnum / editorial style)
- Fully self-contained (Tailwind via CDN for polish + pure CSS film effects)
- Repeatable: re-run the script after any new batch/generations to refresh images + stats
- Reusable by users or Grok: the editor notes are contenteditable or textareas; "Export Editor Log" button produces clean JSON you can paste back to Grok ("Here is the marked-up proof sheet feedback...")

It reads:
- featured_templates/templates.json
- featured_templates/batch-runs/FT-*-metadata.json (times, costs, status)
- the actual images in each <slug>/img/ (prefers proof-*.jpg then base-ref.jpg)

All images in the sheet are linked relatively so the HTML works when the whole imagine/ tree is copied.
"""
import json
import os
from pathlib import Path
from datetime import datetime
from PIL import Image

ROOT = Path(__file__).parent
TEMPLATES_JSON = ROOT / "templates.json"
BATCH_DIR = ROOT / "batch-runs"
OUT_HTML = ROOT / "proof-sheet.html"
THUMBS_DIR = ROOT / "contact-thumbs"
THUMBS_DIR.mkdir(exist_ok=True)

def load_json(p):
    with open(p) as f:
        return json.load(f)

def find_hero_image(slug):
    imgdir = ROOT / slug / "img"
    if not imgdir.exists():
        return None
    candidates = sorted(imgdir.glob("proof-*.jpg")) + sorted(imgdir.glob("*-ref.jpg")) + sorted([f for f in imgdir.glob("*.jpg") if "gitkeep" not in f.name])
    for c in candidates:
        if c.is_file():
            return c
    return None

def make_thumb(src: Path, slug: str, size=(320, 320)):
    out = THUMBS_DIR / f"{slug}.jpg"
    try:
        im = Image.open(src)
        im.thumbnail(size, Image.LANCZOS)
        # letterbox to square-ish for uniform contact sheet
        bg = Image.new("RGB", size, (245, 243, 238))
        bg.paste(im, ((size[0]-im.width)//2, (size[1]-im.height)//2))
        bg.save(out, "JPEG", quality=82)
        return out.relative_to(ROOT)
    except Exception as e:
        print("Thumb error for", slug, e)
        return None

def main():
    temps = load_json(TEMPLATES_JSON)["templates"]
    try:
        meta = load_json(BATCH_DIR / "FT-2026-0602-metadata.json")
    except:
        meta = {"templates": {}, "aggregate": {"total_time_s": 0, "total_images": 0, "total_cost_factor": 0}}

    tmeta = meta.get("templates", {})
    agg = meta.get("aggregate", {})

    # Build data for sheet
    frames = []
    for t in temps:
        slug = t["slug"]
        hero = find_hero_image(slug)
        thumb_rel = None
        if hero:
            thumb_rel = make_thumb(hero, slug)
        m = tmeta.get(slug, {})
        frames.append({
            "slug": slug,
            "display": t["display"],
            "category": t.get("category", "style"),
            "notes": t.get("notes", ""),
            "time_s": m.get("time_spent_s", 12.0),
            "images": m.get("images", 1 if hero else 0),
            "cost_factor": m.get("cost_factor", 1.2),
            "status": m.get("status", "prepared"),
            "hero_path": str(hero.relative_to(ROOT)) if hero else None,
            "thumb_path": str(thumb_rel) if thumb_rel else None,
        })

    # Totals from frames for accuracy
    total_time = sum(f["time_s"] for f in frames)
    total_imgs = sum(f["images"] for f in frames)
    total_cost = sum(f["cost_factor"] for f in frames)

    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>FT-2026-0602 | GROK IMAGINE FEATURED TEMPLATES — CONTACT PROOF SHEET</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.tailwindcss.com"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap');
  
  :root {{
    --film-black: #111;
  }}
  
  body {{ font-family: 'Space Grotesk', system-ui, sans-serif; }}
  .mono {{ font-family: 'IBM Plex Mono', ui-monospace, monospace; }}
  
  .light-table {{
    background: #f4f1e9;
    background-image: 
      linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
    background-size: 24px 24px;
  }}
  
  .film-frame {{
    background: #1a1a1a;
    border: 8px solid #111;
    box-shadow: 0 10px 30px -10px rgb(0 0 0 / 0.6), inset 0 0 0 1px #444;
    position: relative;
    overflow: hidden;
  }}
  
  .film-frame::before, .film-frame::after {{
    content: '';
    position: absolute;
    top: 0; bottom: 0;
    width: 18px;
    background: repeating-linear-gradient(
      #222,
      #222 12px,
      #111 12px,
      #111 28px
    );
    border: 1px solid #333;
    z-index: 2;
  }}
  .film-frame::before {{ left: -2px; }}
  .film-frame::after {{ right: -2px; }}
  
  .sprocket {{
    position: absolute;
    left: 0; right: 0;
    height: 14px;
    background: repeating-linear-gradient(
      90deg,
      #111 0 10px,
      transparent 10px 18px
    );
    z-index: 3;
    opacity: 0.9;
  }}
  
  .frame-label {{
    font-size: 10px;
    letter-spacing: 1.5px;
    font-weight: 600;
  }}
  
  .editor-note {{
    font-size: 12px;
    line-height: 1.3;
    background: #fffef5;
    border: 1px solid #d4c9a8;
    min-height: 62px;
  }}
  
  .proof-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 18px;
  }}
  
  .negative-number {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #c5b38a;
  }}
  
  .vogue-red {{ color: #9f2a2a; }}
  
  .film-strip {{
    box-shadow: 0 4px 15px -2px rgb(0 0 0 / 0.4);
  }}
  
  .contact-header {{
    border-bottom: 3px double #3a2f1f;
  }}
  
  .stat {{
    font-variant-numeric: tabular-nums;
  }}
  
  .category-pill {{
    font-size: 9px;
    padding: 1px 7px;
    border-radius: 9999px;
    letter-spacing: .5px;
  }}
</style>
</head>
<body class="bg-[#111] text-[#e8e0cc] light-table">
<div class="max-w-[1280px] mx-auto p-6">
  <!-- HEADER / FILM LEADER -->
  <div class="flex items-end justify-between mb-4 contact-header pb-4">
    <div>
      <div class="flex items-center gap-x-3">
        <div class="text-[11px] tracking-[3px] font-mono text-[#c5b38a]">KODAK • GROK IMAGINE v4.3 • ROLL FT-2026-0602</div>
        <div class="px-3 py-0.5 text-[10px] bg-[#9f2a2a] text-white font-semibold tracking-widest">CONFIDENTIAL — EDITORIAL PROOFS</div>
      </div>
      <h1 class="text-5xl font-semibold tracking-tighter mt-1">FEATURED TEMPLATES<br>PROOF SHEET</h1>
      <p class="text-[#c5b38a] text-sm mt-1">Master Reference: Watercolor Man (top knot, silver beard, denim + camo) • {len(frames)} frames • <span class="text-white">ALL CURRENT GROK IMAGINE FEATURED PRESETS</span></p>
    </div>
    
    <div class="text-right text-sm mono">
      <div class="text-[#c5b38a]">DEVELOPED</div>
      <div class="text-3xl font-semibold tabular-nums text-white">{datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
      <div class="text-xs">Operator: Grok • Ref: original-watercolor-ref.jpg</div>
    </div>
  </div>

  <!-- ONE PHOTO → FULL BATCH FOR SET COST (the whole point of this folder) -->
  <div class="bg-[#1a1812] border-2 border-[#c5b38a] p-5 mb-6">
    <div class="uppercase text-[#c5b38a] text-xs tracking-[2px] mb-2">The Point of This Folder Structure</div>
    <div class="text-xl font-semibold mb-1">One photo → Grok applies <span class="text-white">every current Featured Template preset</span> in a single batch</div>
    <div class="text-sm text-[#d4c9a8] mb-3">Drop one reference photo. Execute the batch (via the prepare prompts or by telling Grok "run all featured templates on this photo"). Get the complete visual catalog of what Grok Imagine can currently do with your subject, for a known set cost. Review the proof sheet, pick the winners, only pay to iterate on the ones you love.</div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
      <div class="bg-black/40 p-3">
        <div class="text-[#c5b38a] text-xs">SET COST FACTOR (this batch)</div>
        <div class="text-3xl font-bold tabular-nums">{total_cost:.1f}×</div>
        <div class="text-xs text-[#8a7a5a]">relative to a single standard generation. Use this to estimate total cost before you start the batch.</div>
      </div>
      <div class="bg-black/40 p-3">
        <div class="text-[#c5b38a] text-xs">TOTAL DEV TIME (this run)</div>
        <div class="text-3xl font-bold tabular-nums">{total_time:.0f}s</div>
        <div class="text-xs text-[#8a7a5a]">≈ {total_time/60:.1f} min wall time to produce the full set</div>
      </div>
      <div class="bg-black/40 p-3">
        <div class="text-[#c5b38a] text-xs">REAL OUTPUTS</div>
        <div class="text-3xl font-bold tabular-nums">{total_imgs}</div>
        <div class="text-xs text-[#8a7a5a]">styled images from the single reference photo across all official presets</div>
      </div>
      <div class="bg-black/40 p-3 text-xs leading-snug">
        <div class="text-[#c5b38a] mb-1 font-semibold">REPEATABLE WORKFLOW (for any user / any photo)</div>
        <ol class="list-decimal ml-4 text-[#d4c9a8] text-xs">
          <li>Place your photo in <span class="font-mono">featured_templates/inputs/</span></li>
          <li><span class="font-mono text-[10px]">python ../sweep.py prepare --source featured -i inputs/your.jpg -p "describe your subject..."</span></li>
          <li>Run the generated image_edit calls (or just say to Grok: "batch every featured template on this photo using the prepare file")</li>
          <li><span class="font-mono">python make_proof_sheet.py</span></li>
          <li>Open <span class="font-mono">proof-sheet.html</span> — see everything at once + editor notes + export JSON feedback</li>
        </ol>
      </div>
    </div>
    <div class="mt-3 text-[10px] text-[#8a7a5a]">Every subfolder in this directory = one official Grok Imagine "Featured" preset currently available in the UI. The proof-001.jpg (or best proof) in each img/ is the result of running the same reference photo through that exact preset.</div>
  </div>

  <!-- AGGREGATE STATS RIBBON (kept for quick glance) -->
  <div class="bg-[#1f1c15] border border-[#3a2f1f] p-4 mb-6 flex flex-wrap gap-x-8 gap-y-2 text-sm">
    <div><span class="text-[#c5b38a]">TOTAL DEV TIME</span><br><span class="text-2xl font-semibold tabular-nums">{total_time:.1f}s</span> <span class="text-xs">({total_time/60:.1f} min)</span></div>
    <div><span class="text-[#c5b38a]">FRAMES</span><br><span class="text-2xl font-semibold tabular-nums">{len(frames)}</span></div>
    <div><span class="text-[#c5b38a]">IMAGES PRODUCED</span><br><span class="text-2xl font-semibold tabular-nums">{total_imgs}</span></div>
    <div><span class="text-[#c5b38a]">EST. COST FACTOR</span><br><span class="text-2xl font-semibold tabular-nums">{total_cost:.1f}×</span> <span class="text-xs">base</span></div>
    <div class="flex-1 min-w-[220px]">
      <span class="text-[#c5b38a] text-xs">NOTES</span><br>
      <span class="text-xs">All frames from one master reference. Prompts used the official "Apply the XXX featured template" + strong likeness anchors. Re-run make_proof_sheet.py after adding more generations.</span>
    </div>
  </div>

  <!-- THE CONTACT GRID -->
  <div class="proof-grid">
'''

    for i, f in enumerate(frames, 1):
        frame_num = f"{i:02d}"
        status_badge = "DEVELOPED" if f["status"] in ("developed", "base exposed") else "PREPARED"
        badge_class = "bg-emerald-900 text-emerald-300" if "developed" in f["status"] else "bg-amber-900 text-amber-300"

        img_html = ""
        if f["thumb_path"]:
            img_html = f'<img src="{f["thumb_path"]}" class="w-full h-auto object-cover" style="image-rendering: crisp-edges;" alt="{f["display"]}">'
        elif f["hero_path"]:
            img_html = f'<img src="{f["hero_path"]}" class="w-full h-auto object-cover" style="image-rendering: crisp-edges;" alt="{f["display"]}">'
        else:
            img_html = f'''<div class="w-full h-[210px] bg-[#222] flex items-center justify-center text-[10px] text-center p-4 border border-[#444]">
              <div>
                <div class="font-mono text-[#666] mb-1">NO NEGATIVE YET</div>
                <div class="text-[9px] leading-tight">Run image_edit with the prepare prompt for this template</div>
              </div>
            </div>'''

        # Short prompt hint from prepare (we hardcode a reminder)
        prompt_hint = f'Apply the {f["display"]} featured template. ... Preserve exact identity...'

        html += f'''
    <div class="film-frame film-strip group" data-slug="{f["slug"]}" data-status="{f["status"]}">
      <!-- top sprocket -->
      <div class="sprocket" style="top:-1px;"></div>
      
      <div class="p-2.5 pb-1 bg-[#111]">
        <div class="flex justify-between items-baseline px-1">
          <div class="negative-number">{frame_num}A</div>
          <div class="text-[9px] text-[#666] mono">FT-{frame_num}</div>
        </div>
        
        <div class="mt-1 mb-1 border border-[#222] bg-black overflow-hidden">
          {img_html}
        </div>
        
        <div class="px-1">
          <div class="flex items-center justify-between">
            <div>
              <div class="font-semibold text-sm tracking-tight leading-none">{f["display"]}</div>
              <div class="text-[10px] text-[#8a7a5a]">{f["slug"]}</div>
            </div>
            <span class="category-pill {badge_class}">{f["category"].upper()}</span>
          </div>
          
          <div class="mt-1.5 text-[10px] mono flex gap-2 text-[#a89a7a]">
            <div>t:{f["time_s"]}s</div>
            <div>×{f["cost_factor"]}</div>
            <div>out:{f["images"]}</div>
          </div>
          
          <div class="mt-1 text-[10px] leading-tight text-[#d4c9a8]">{f["notes"][:90]}{"..." if len(f["notes"])>90 else ""}</div>
        </div>
      </div>
      
      <!-- editor comment area (vogue style) -->
      <div class="px-2.5 pb-2.5">
        <div class="text-[9px] text-[#c5b38a] mb-0.5 flex justify-between">
          <span>EDITOR NOTES — VOGUE</span>
          <span class="text-emerald-400 group-hover:opacity-100 opacity-60 transition">editable</span>
        </div>
        <div contenteditable="true" spellcheck="false"
             class="editor-note w-full text-[11px] p-2 leading-snug text-[#3a2f1f] focus:outline-none focus:ring-1 focus:ring-[#c5b38a]"
             data-field="note-{f["slug"]}">
          { "Select — strong character read. Beard reads well in this treatment." if f["status"]=="developed" else "Prepared. Run the exact image_edit from batch-runs/FT-2026-0602-prepare.txt for this frame." }
        </div>
        
        <div class="flex gap-1 mt-1 text-[10px]">
          <button onclick="markSelect(this)" class="px-2 py-px border border-[#4a3f2a] hover:bg-[#2a251a] text-emerald-400 text-[9px]">SELECT</button>
          <button onclick="markKill(this)" class="px-2 py-px border border-[#4a3f2a] hover:bg-[#2a251a] text-red-400 text-[9px]">KILL</button>
          <button onclick="markHold(this)" class="px-2 py-px border border-[#4a3f2a] hover:bg-[#2a251a] text-amber-400 text-[9px]">HOLD</button>
        </div>
      </div>
      
      <div class="sprocket" style="bottom:-1px;"></div>
    </div>
'''

    html += f'''
  </div>

  <!-- FOOTER / DEVELOPMENT LOG + EXPORT -->
  <div class="mt-8 border-t border-[#3a2f1f] pt-6 flex flex-col md:flex-row gap-6 text-sm">
    <div class="flex-1">
      <div class="uppercase tracking-widest text-xs text-[#c5b38a] mb-1">DEVELOPMENT LOG — GROK IMAGINE</div>
      <div class="text-[#a89a7a] text-xs leading-relaxed">
        All frames shot on single master watercolor reference (the man). Base prompt preserved exact likeness across every exposure. 
        Total batch wall time ≈ {total_time:.0f}s. Cost factor is relative (simple portraits 1.0×, complex action/edit 1.5–1.7×). 
        Re-run <span class="mono">python featured_templates/make_proof_sheet.py</span> after any new image_edit / video_gen to refresh this sheet with latest negatives and stats.
      </div>
    </div>
    
    <div>
      <button onclick="exportEditorLog()" 
              class="px-5 py-2 bg-white text-black text-sm font-semibold tracking-wider hover:bg-[#f4f1e9] transition">
        EXPORT EDITOR LOG (JSON)
      </button>
      <div class="text-[10px] text-[#8a7a5a] mt-1 text-right">Feed this back to Grok for the next iteration round</div>
    </div>
  </div>

  <div class="text-[10px] text-[#666] mt-8 text-center mono">
    This proof sheet is part of the imagine project (https://github.com/fornevercollective/imagine).<br>
    Safe to edit notes directly in the browser for quick sessions. For permanence, re-run the generator script.
  </div>
</div>

<script>
// Tailwind script (already loaded via CDN)
function markSelect(btn) {{
  const card = btn.closest('.film-frame');
  card.style.boxShadow = '0 0 0 3px #166534';
  btn.textContent = 'SELECTED ✓';
  btn.disabled = true;
}}

function markKill(btn) {{
  const card = btn.closest('.film-frame');
  card.style.opacity = '0.35';
  card.style.filter = 'grayscale(0.7)';
  btn.textContent = 'KILLED ✕';
}}

function markHold(btn) {{
  const card = btn.closest('.film-frame');
  card.style.boxShadow = '0 0 0 3px #854d0e';
  btn.textContent = 'ON HOLD';
}}

function exportEditorLog() {{
  const data = [];
  document.querySelectorAll('.film-frame').forEach(card => {{
    const slug = card.dataset.slug;
    const noteEl = card.querySelector('[data-field]');
    const note = noteEl ? noteEl.innerText.trim() : '';
    const status = card.dataset.status;
    data.push({{ slug, note, status, timestamp: new Date().toISOString() }});
  }});
  
  const blob = new Blob([JSON.stringify({{
    batch_id: "FT-2026-0602-master-ref",
    exported_at: new Date().toISOString(),
    notes: data,
    summary: "Editor feedback from contact proof sheet"
  }}, null, 2)], {{type: "application/json"}});
  
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "FT-2026-0602-editor-log.json";
  a.click();
  alert("Editor log exported. Paste the JSON back to Grok with: 'Update the proof sheet / next batch using this editor feedback.'");
}}

// Keyboard hint
console.log('%c[proof-sheet] Press ? for help. All textareas + contenteditable notes are live. Export button produces reusable JSON.', 'color:#666');
</script>
</body>
</html>
'''

    with open(OUT_HTML, "w") as f:
        f.write(html)

    print(f"Proof sheet written to: {OUT_HTML}")
    print(f"Thumbs in: {THUMBS_DIR}")
    print(f"Aggregates: {total_time:.1f}s | {total_imgs} images | {total_cost:.1f}× cost factor")

if __name__ == "__main__":
    main()
