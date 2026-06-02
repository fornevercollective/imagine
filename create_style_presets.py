#!/usr/bin/env python3
"""
Create extended style_presets/ for imagine project.
Covers VSCO / film emulations, Pinterest aesthetics, cinematic genre LUTs.
Each preset gets: prompt.txt (style descriptor for Imagine), meta.json, img/, vid/ with .gitkeep.
Also generates style_presets/styles.json manifest.
Run from project root: python create_style_presets.py
"""

from pathlib import Path
import json
import os

ROOT = Path(__file__).parent
PRESETS_DIR = ROOT / "style_presets"
INPUTS_DIR = ROOT / "inputs"

# Master list of extended presets. Slugs are fs-safe.
# Add more over time. prompt = the "LUT + aesthetic" text to append to base prompt.
PRESETS = [
    # === Film Emulations (VSCO / analog stocks) ===
    {
        "slug": "kodak-portra-400",
        "display": "Kodak Portra 400",
        "category": "film_emulation",
        "tags": ["kodak", "vsco", "portrait", "natural", "warm", "film"],
        "prompt": "shot on Kodak Portra 400 film stock, natural accurate skin tones, soft pleasing contrast, delicate film grain, creamy highlights, subtle warm color shift, fine detail, analog photography, slight halation in bright areas",
        "best_for": "portraits, people, soft natural light, lifestyle",
        "notes": "Classic VSCO favorite. Flattering, low contrast, creamy."
    },
    {
        "slug": "kodak-ektar-100",
        "display": "Kodak Ektar 100",
        "category": "film_emulation",
        "tags": ["kodak", "vsco", "saturated", "vibrant", "landscape"],
        "prompt": "shot on Kodak Ektar 100 film, highly saturated vibrant colors, punchy contrast, fine grain, rich reds and blues, sharp detail, cinematic film look, slight warmth",
        "best_for": "landscapes, color pop, product, fashion",
        "notes": "Punchier, more saturated than Portra."
    },
    {
        "slug": "kodak-gold-200",
        "display": "Kodak Gold 200",
        "category": "film_emulation",
        "tags": ["kodak", "vsco", "vintage", "warm", "90s"],
        "prompt": "shot on Kodak Gold 200 film, warm vintage color palette, golden yellows and oranges, moderate contrast, visible grain, nostalgic 90s snapshot aesthetic, soft skin",
        "best_for": "vintage, summer, candid, family photos",
        "notes": "Iconic warm consumer film look."
    },
    {
        "slug": "kodak-ultramax-400",
        "display": "Kodak Ultramax 400",
        "category": "film_emulation",
        "tags": ["kodak", "vsco", "everyday", "grainy"],
        "prompt": "shot on Kodak Ultramax 400, everyday film look, balanced warm tones, medium grain, good skin rendition, slightly soft focus, versatile snapshot film photography",
        "best_for": "street, travel, all purpose",
        "notes": "Modern everyday Kodak stock."
    },
    {
        "slug": "kodak-tri-x-400-bw",
        "display": "Kodak Tri-X 400 (B&W)",
        "category": "film_emulation",
        "tags": ["kodak", "bw", "vsco", "grain", "classic"],
        "prompt": "shot on Kodak Tri-X 400 black and white film, classic high contrast B&W, prominent grain, deep blacks, bright whites, documentary photojournalism aesthetic, strong tonality",
        "best_for": "dramatic portraits, street, documentary",
        "notes": "The classic B&W film grain king."
    },
    {
        "slug": "fuji-velvia-50",
        "display": "Fuji Velvia 50",
        "category": "film_emulation",
        "tags": ["fuji", "vsco", "saturated", "landscape", "vivid"],
        "prompt": "shot on Fuji Velvia 50 slide film, extremely saturated vivid colors, high contrast, rich greens and reds, fine grain, landscape and nature film look, almost hyper real",
        "best_for": "nature, travel, bold color, scenery",
        "notes": "Most saturated film stock. Great for epic landscapes."
    },
    {
        "slug": "fuji-superia-400",
        "display": "Fuji Superia 400",
        "category": "film_emulation",
        "tags": ["fuji", "vsco", "90s", "consumer", "grain"],
        "prompt": "shot on Fuji Superia 400 film, 90s consumer film colors, slightly cool greens, natural skin with film shift, visible grain, everyday nostalgic look",
        "best_for": "90s nostalgia, street, candid",
        "notes": "Popular 90s point-and-shoot film."
    },
    {
        "slug": "fuji-pro-400h",
        "display": "Fuji Pro 400H",
        "category": "film_emulation",
        "tags": ["fuji", "vsco", "portrait", "professional", "soft"],
        "prompt": "shot on Fuji Pro 400H professional film, beautiful skin tones with slight green bias, soft contrast, smooth gradation, fine grain, wedding and portrait film classic",
        "best_for": "weddings, portraits, soft beauty",
        "notes": "Beloved by wedding photographers."
    },
    {
        "slug": "fuji-acros-100-bw",
        "display": "Fuji Acros 100 (B&W)",
        "category": "film_emulation",
        "tags": ["fuji", "bw", "vsco", "fine-grain", "portrait"],
        "prompt": "shot on Fuji Acros 100 black & white, extremely fine grain, excellent tonality and shadow detail, smooth creamy B&W, subtle warmth in highlights, architectural and portrait classic",
        "best_for": "fine art, architecture, delicate portraits",
        "notes": "One of the finest grain B&W films."
    },
    {
        "slug": "fuji-eterna-500",
        "display": "Fuji Eterna 500",
        "category": "film_emulation",
        "tags": ["fuji", "cinematic", "movie", "low-contrast"],
        "prompt": "shot on Fuji Eterna 500 motion picture film, low contrast cinematic look, soft colors, beautiful skin, designed for movies, subtle grain, telecine film look",
        "best_for": "cinematic video stills, narrative, low contrast beauty",
        "notes": "Real movie film stock. Perfect base for video too."
    },
    {
        "slug": "cinestill-50d",
        "display": "Cinestill 50D",
        "category": "film_emulation",
        "tags": ["cinestill", "cinematic", "halations", "daylight"],
        "prompt": "shot on Cinestill 50D (Kodak Vision3 50D motion picture film, remjet removed), cinematic halation glow in highlights, vibrant yet natural colors, fine grain, beautiful for daylight and golden hour, red halation around bright lights",
        "best_for": "cinematic portraits, golden hour, night lights with glow",
        "notes": "Popular 'movie film' look with signature halation."
    },
    {
        "slug": "cinestill-800t",
        "display": "Cinestill 800T",
        "category": "film_emulation",
        "tags": ["cinestill", "cinematic", "night", "tungsten", "halations"],
        "prompt": "shot on Cinestill 800T tungsten balanced motion picture film (remjet removed), strong red/orange halation around practical lights and neons, cinematic night look, pushed grain, teal shadows, very filmic and atmospheric",
        "best_for": "night scenes, neon, urban, moody cinematic",
        "notes": "The go-to for cinematic night + neon glows."
    },
    {
        "slug": "ilford-hp5-400-bw",
        "display": "Ilford HP5 Plus 400 (B&W)",
        "category": "film_emulation",
        "tags": ["ilford", "bw", "vsco", "versatile", "grain"],
        "prompt": "shot on Ilford HP5 Plus 400 black and white, versatile high speed B&W, pronounced but pleasing grain, good shadow detail, classic documentary and street photography look, can be pushed for more contrast/grain",
        "best_for": "street photography, documentary, dramatic B&W",
        "notes": "Workhorse B&W film."
    },
    {
        "slug": "kodachrome-64",
        "display": "Kodachrome 64",
        "category": "film_emulation",
        "tags": ["kodak", "slide", "vintage", "saturated", "iconic"],
        "prompt": "shot on Kodachrome 64 slide film, legendary vibrant yet natural colors, famous for reds and skin, high sharpness, fine grain, iconic National Geographic and 70s-80s photojournalism look, warm slide film rendering",
        "best_for": "iconic vintage color, travel, documentary",
        "notes": "The most famous slide film ever."
    },

    # === Pinterest / Core Aesthetics ===
    {
        "slug": "cottagecore",
        "display": "Cottagecore",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "cozy", "rural", "soft", "pastel"],
        "prompt": "cottagecore aesthetic, romantic rural fantasy, soft pastels, floral details, natural light through lace curtains, handwritten letters vibe, overgrown gardens, cozy cardigans, dreamy filmic soft focus, warm gentle color grade, Pinterest cozy countryside",
        "best_for": "portraits in nature, feminine, cozy scenes",
        "notes": "Romanticizing simple rural life."
    },
    {
        "slug": "dark-academia",
        "display": "Dark Academia",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "moody", "academic", "browns", "library"],
        "prompt": "dark academia aesthetic, moody university library, rich browns, deep forest greens, burgundy, tweed textures, leather books, dramatic window light, chiaroscuro lighting, vintage scholarly atmosphere, filmic desaturated color grade, subtle dust motes and grain, Pinterest intellectual dark mood",
        "best_for": "portraits, indoor, fall/winter, intellectual vibe",
        "notes": "Classic Pinterest dark moody academia."
    },
    {
        "slug": "light-academia",
        "display": "Light Academia",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "soft", "academic", "cream", "sunny"],
        "prompt": "light academia aesthetic, bright sunlit libraries and old universities, cream, beige, soft golds, linen and wool textures, gentle natural window light, romantic scholarly, light and airy film look, warm soft contrast, delicate grain",
        "best_for": "soft portraits, study scenes, spring/summer academia",
        "notes": "The lighter, more optimistic academia cousin."
    },
    {
        "slug": "fairycore",
        "display": "Fairycore",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "ethereal", "fantasy", "pastel", "nature"],
        "prompt": "fairycore aesthetic, whimsical fairy forest, soft glowing light, pastel pinks blues lavenders, delicate flowers and wings details, ethereal bokeh, dreamy soft focus, magical woodland, very soft filmic pastel color grade, sparkles and light leaks, Pinterest fantasy soft",
        "best_for": "ethereal portraits, nature fantasy, feminine magic",
        "notes": "Whimsical fairy / enchanted forest."
    },
    {
        "slug": "old-money-aesthetic",
        "display": "Old Money Aesthetic",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "luxury", "quiet", "neutral", "heritage"],
        "prompt": "old money aesthetic / quiet luxury, timeless elegant wealth, neutral palette of cream, navy, beige, camel, heritage tailoring, cashmere, pearls, old European estates, soft natural light, sophisticated filmic color, minimal grain, high end editorial photography look, Pinterest refined wealth",
        "best_for": "fashion portraits, luxury lifestyle, elegant",
        "notes": "Subtle inherited wealth vibes (not flashy)."
    },
    {
        "slug": "clean-girl",
        "display": "Clean Girl Aesthetic",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "minimal", "glowy", "modern", "skin"],
        "prompt": "clean girl aesthetic, dewy glowing skin, slicked back hair, minimal makeup, all beige/cream/white/neutral modern wardrobe, clean minimalist backgrounds, bright even studio or natural light, glossy skin, fresh healthy look, high key soft film photography, subtle grain, Pinterest clean modern beauty",
        "best_for": "beauty portraits, skincare, modern minimal fashion",
        "notes": "The glowy no-makeup makeup Pinterest trend."
    },
    {
        "slug": "y2k-aesthetic",
        "display": "Y2K Aesthetic",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "2000s", "chrome", "pink", "futuristic"],
        "prompt": "Y2K aesthetic, early 2000s, metallic chrome, baby pink and blue, low rise, butterflies, glitter, holographic, flash photography, pink digital camera look, glossy lips, playful futuristic, heavy film grain + flash, polaroid + digital mix, Pinterest 2000s nostalgia",
        "best_for": "fun fashion, party, nostalgic 00s portraits",
        "notes": "McBling / early 2000s internet + pop culture."
    },
    {
        "slug": "cybercore",
        "display": "Cybercore",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "cyber", "tech", "neon", "futuristic"],
        "prompt": "cybercore / techwear aesthetic, cyberpunk fashion without the full dystopia, black tech fabrics, reflective details, LED accents, cool blue and purple lighting, futuristic clean, high contrast cinematic, subtle matrix code feel, sharp modern film look",
        "best_for": "fashion tech, futuristic portraits, night urban",
        "notes": "More fashion focused than full cyberpunk."
    },
    {
        "slug": "grunge-90s",
        "display": "Grunge 90s",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "90s", "grunge", "flannel", "moody"],
        "prompt": "90s grunge aesthetic, flannel, band tees, ripped jeans, Doc Martens, dark moody lighting, Seattle overcast, high contrast B&W or desaturated color, heavy film grain, raw documentary feel, Kurt Cobain / Hole / Nirvana vibe, anti-glamour, Pinterest 90s grunge revival",
        "best_for": "edgy portraits, music, alternative fashion",
        "notes": "Raw 90s alternative."
    },
    {
        "slug": "barbiecore",
        "display": "Barbiecore",
        "category": "pinterest_aesthetic",
        "tags": ["pinterest", "pink", "barbie", "playful", "saturated"],
        "prompt": "barbiecore aesthetic, hot pink everything, playful hyper feminine, glossy, plastic fantastic, bright saturated pink dominant palette, fun lighting, Barbie movie inspired, high gloss, bold makeup, cheerful and campy film look, strong pink color grade, Pinterest pink maximalism",
        "best_for": "fun bold fashion, playful portraits, color statements",
        "notes": "The 2023+ pink explosion aesthetic."
    },

    # === Cinematic Genre LUTs ===
    {
        "slug": "film-noir",
        "display": "Film Noir",
        "category": "cinematic_genre",
        "tags": ["cinematic", "bw", "noir", "dramatic", "shadows"],
        "prompt": "classic film noir cinematic style, high contrast black and white, deep impenetrable shadows, bright specular highlights, venetian blind shadows on face, cigarette smoke, rain on window, 1940s-50s hardboiled detective mood, heavy grain, dramatic low key lighting, chiaroscuro, vintage movie still",
        "best_for": "dramatic B&W portraits, mystery, shadows",
        "notes": "The original cinematic B&W look."
    },
    {
        "slug": "neo-noir",
        "display": "Neo-Noir",
        "category": "cinematic_genre",
        "tags": ["cinematic", "noir", "color", "rain", "urban"],
        "prompt": "neo-noir cinematic, modern color noir, desaturated palette with pops of red or neon, rain soaked streets, reflections, trench coat, moody underlit face, high contrast, anamorphic lens flares, dark urban atmosphere, film grain, Taxi Driver / Blade Runner influence, cinematic color grade",
        "best_for": "moody urban portraits, night rain, thriller",
        "notes": "Color evolution of classic noir."
    },
    {
        "slug": "cyberpunk-neon",
        "display": "Cyberpunk Neon",
        "category": "cinematic_genre",
        "tags": ["cinematic", "cyberpunk", "neon", "night", "future"],
        "prompt": "cyberpunk cinematic, dense neon magenta cyan and electric blue signs, heavy rain, wet reflective streets and puddles, high contrast, strong backlight, holographic elements, futuristic dystopian Tokyo night, anamorphic flares and glows, heavy film grain + digital noise mix, Blade Runner 2049 / Ghost in the Shell vibe",
        "best_for": "night futuristic, neon portraits, sci-fi action",
        "notes": "The ultimate neon rain cyber look."
    },
    {
        "slug": "teal-orange-blockbuster",
        "display": "Teal Orange Blockbuster",
        "category": "cinematic_genre",
        "tags": ["cinematic", "teal-orange", "hollywood", "action"],
        "prompt": "modern Hollywood blockbuster cinematic LUT, classic teal and orange color grade, cool teal shadows, warm orange skin highlights, high contrast, crushed blacks, lifted shadows slightly, anamorphic lens characteristics, epic widescreen, Michael Bay / Nolan / modern action movie look, polished filmic",
        "best_for": "epic portraits, action, commercial cinematic",
        "notes": "The most overused (but effective) modern cinematic grade."
    },
    {
        "slug": "western-sepia",
        "display": "Western Sepia / Dusty",
        "category": "cinematic_genre",
        "tags": ["cinematic", "western", "sepia", "dusty", "vintage"],
        "prompt": "spaghetti western / classic western cinematic, warm sepia and tobacco tones, dusty hazy atmosphere, harsh midday sun, deep shadows, golden hour backlight, leather and denim textures, high contrast with crushed blacks, heavy grain, 35mm or 70mm film western look, Clint Eastwood / Sergio Leone aesthetic",
        "best_for": "western, desert, rugged portraits, period",
        "notes": "Ties into existing Spaghetti Western featured template."
    },
    {
        "slug": "horror-grain",
        "display": "Horror / Desaturated Grain",
        "category": "cinematic_genre",
        "tags": ["cinematic", "horror", "grain", "desaturated", "eerie"],
        "prompt": "horror movie cinematic, desaturated color almost monochrome with sickly green or blue push in shadows, high grain, heavy vignette, deep blacks, low key lighting, unsettling atmosphere, found footage or 70s horror film look, subtle film weave, The VVitch / Hereditary / classic horror color grade",
        "best_for": "eerie portraits, dark scenes, tension",
        "notes": "Creepy, skin looks unhealthy, dread inducing."
    },
    {
        "slug": "dune-sci-fi",
        "display": "Dune Sci-Fi Epic",
        "category": "cinematic_genre",
        "tags": ["cinematic", "sci-fi", "desert", "epic", "denis"],
        "prompt": "Dune / epic sci-fi cinematic, vast desert scale, orange and teal but more muted and sandy than blockbuster, extreme contrast between bright sun and deep shadow, practical lens flares, IMAX scale, dry dusty air, monumental architecture, Villeneuve style color science, rich yet desaturated, 70mm film epic look",
        "best_for": "epic wide shots, sci-fi portraits, grand scale",
        "notes": "Modern epic sci-fi reference (Dune 2021/24)."
    },
    {
        "slug": "golden-hour-romance",
        "display": "Golden Hour Romance",
        "category": "cinematic_genre",
        "tags": ["cinematic", "romance", "warm", "golden", "soft"],
        "prompt": "romantic golden hour cinematic, warm honey and amber tones, soft glowing backlight, lens flare, bokeh, shallow depth of field, skin beautifully wrapped in golden light, dreamy soft focus, pastel peach and cream palette, high end romantic drama or period romance film look, gentle grain, very flattering",
        "best_for": "romance, couples, beauty in warm light",
        "notes": "The most flattering cinematic for people."
    },
    {
        "slug": "vhs-80s",
        "display": "VHS 80s / Lo-fi",
        "category": "cinematic_genre",
        "tags": ["cinematic", "vhs", "80s", "lofi", "analog"],
        "prompt": "80s VHS / lo-fi analog video look, heavy tracking lines, color bleed, chroma noise, low resolution feel, warm browns and yellows or garish 80s video colors, scan lines, tape wear, home video or straight-to-VHS movie aesthetic, very grainy and imperfect, nostalgic degraded media",
        "best_for": "80s nostalgia, retro video, lo-fi music video",
        "notes": "Analog video degradation as aesthetic."
    },
    {
        "slug": "anamorphic-cinematic",
        "display": "Anamorphic Cinematic",
        "category": "cinematic_genre",
        "tags": ["cinematic", "anamorphic", "lens", "flares", "widescreen"],
        "prompt": "shot on anamorphic lenses (2.39:1 or 2.35), characteristic blue or amber horizontal lens flares, oval bokeh, slight edge softness and breathing, widescreen epic framing, high end cinema camera look, subtle barrel distortion on edges, very filmic and expensive looking, used in most modern blockbusters",
        "best_for": "any cinematic, adds instant production value",
        "notes": "Lens characteristics more than color grade. Combine with others."
    },
    {
        "slug": "ethereal-fantasy",
        "display": "Ethereal Fantasy",
        "category": "cinematic_genre",
        "tags": ["cinematic", "fantasy", "ethereal", "glow", "soft"],
        "prompt": "ethereal high fantasy cinematic, soft glowing rim light, magical god rays, pastel and iridescent highlights, high key with lifted shadows, skin luminous, floating particles, dreamy shallow depth, Lord of the Rings / Studio Ghibli live action meets cinema color grade, very soft and magical film look",
        "best_for": "fantasy portraits, magical scenes, beauty",
        "notes": "Soft magical glow fantasy."
    },
    {
        "slug": "gritty-documentary",
        "display": "Gritty Documentary",
        "category": "cinematic_genre",
        "tags": ["cinematic", "documentary", "gritty", "natural", "handheld"],
        "prompt": "gritty documentary cinematic, available light only, slightly under exposed, natural skin with imperfections, subtle teal push in shadows, handheld camera feel, 16mm or Super 16 film grain + digital noise, journalistic, raw, no glamour, The Social Dilemma / modern docs or 70s cinema verite look",
        "best_for": "realism, street, interview style, authentic",
        "notes": "Anti-glamour, truth seeking look."
    },
    {
        "slug": "vintage-35mm",
        "display": "Vintage 35mm Film Fade",
        "category": "cinematic_genre",
        "tags": ["cinematic", "vintage", "35mm", "fade", "grain"],
        "prompt": "vintage 35mm film print look, faded colors, yellowing in highlights, heavy but organic grain, slight gate weave, dirt and scratches, 70s-80s movie print degradation, warm faded palette, beautiful for period or nostalgic, The Godfather or Taxi Driver aged film print aesthetic",
        "best_for": "period pieces, nostalgia, emotional memory",
        "notes": "Aged film print degradation."
    },
    {
        "slug": "moody-teal-drama",
        "display": "Moody Teal Drama",
        "category": "cinematic_genre",
        "tags": ["cinematic", "teal", "moody", "drama", "netflix"],
        "prompt": "moody modern drama / Netflix cinematic, dominant teal and cyan in shadows, warm but controlled skin, high contrast, deep blacks, lifted midtones in a controlled way, very current prestige TV / limited series look, subtle grain, clean yet atmospheric, Succession / The Bear / modern dramatic series grade",
        "best_for": "dramatic character portraits, interior scenes",
        "notes": "Current 'prestige' TV color science."
    },
]

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def create_preset(preset: dict):
    slug = preset["slug"]
    d = PRESETS_DIR / slug
    ensure_dir(d)
    ensure_dir(d / "img")
    ensure_dir(d / "vid")

    # prompt.txt - the key thing to append to base prompts
    (d / "prompt.txt").write_text(preset["prompt"].strip() + "\n", encoding="utf-8")

    # meta.json
    meta = {
        "slug": slug,
        "display": preset["display"],
        "category": preset["category"],
        "tags": preset["tags"],
        "best_for": preset.get("best_for", ""),
        "notes": preset.get("notes", ""),
        "source": "extended_preset_for_grok_imagine",
        "version": "1.0"
    }
    (d / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    # .gitkeep for empty dirs
    (d / "img" / ".gitkeep").touch()
    (d / "vid" / ".gitkeep").touch()

    print(f"  created {slug}")

def main():
    print("Creating style_presets structure in", PRESETS_DIR)
    ensure_dir(PRESETS_DIR)
    ensure_dir(INPUTS_DIR)

    for p in PRESETS:
        create_preset(p)

    # Master manifest
    manifest = {
        "meta": {
            "total": len(PRESETS),
            "categories": sorted(set(p["category"] for p in PRESETS)),
            "description": "Extended prompt-based style presets / LUT emulations for Grok Imagine. Use in addition to or instead of the official Featured Templates. Designed for rapid one-photo batch iteration across VSCO film, Pinterest aesthetics, and cinematic genre looks.",
            "usage": "Append the text from prompt.txt to your base subject prompt when using image_edit or text-to-image. Or use the sweep scripts."
        },
        "presets": [
            {
                "slug": p["slug"],
                "display": p["display"],
                "category": p["category"],
                "tags": p["tags"]
            } for p in PRESETS
        ]
    }
    (PRESETS_DIR / "styles.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote styles.json with {len(PRESETS)} presets.")

    # Also write a simple groups helper
    groups = {}
    for p in PRESETS:
        groups.setdefault(p["category"], []).append(p["slug"])
    (PRESETS_DIR / "groups.json").write_text(json.dumps(groups, indent=2) + "\n", encoding="utf-8")
    print("Wrote groups.json for easy batching by category.")

    print("\nDone. Now drop a photo in inputs/ and use sweep or batch scripts.")
    print("Example preset prompt location: style_presets/kodak-portra-400/prompt.txt")

if __name__ == "__main__":
    main()
