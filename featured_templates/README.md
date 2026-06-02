# Grok Imagine Featured Templates

Folders for all current **Featured Templates** from [grok.com/imagine](https://grok.com/imagine).

Use this to quickly iterate one photo + prompt across **all styles**, collecting outputs into per-template `img/` and `vid/` subfolders.

## Structure

```
featured_templates/
├── inputs/                 # Drop your source photo(s) here (e.g. photo.jpg)
├── <template-name>/        # One folder per featured template
│   ├── img/                # Generated stills / edited images for this style
│   └── vid/                # Generated videos / animations for this style
├── README.md
└── templates.json          # Machine-readable list of all templates
```

## Current Featured Templates (23)

1. chibi
2. professional-headshot
3. logo-editor
4. 70s-street-style
5. quality-enhancer
6. comic-book
7. object-remover
8. product-showcase
9. glossy-product-shot
10. 80s-anime
11. watercolor-portrait
12. video-game
13. 3d-animation
14. spaghetti-western
15. haze-portrait
16. funky-dance
17. future-past
18. roman-empire
19. ad-astra
20. add-girlfriend
21. future-family
22. laser-fight
23. sunny-morning

## How to quickly iterate one photo across all styles

1. Put your source image in `inputs/` (e.g. `inputs/my_photo.jpg`).
2. Decide on a **base prompt** describing the desired transformation or scene (the template will supply the style).
3. Ask Grok (in this CLI or on grok.com) to generate for each template, e.g.:
   - "Using the photo at inputs/my_photo.jpg, apply the Chibi template style. Save the image output to chibi/img/ and if it produces video also to chibi/vid/. Base prompt: <your prompt here>"
   - Repeat for other templates (or ask me to batch a few at a time).
4. For video-focused: many templates animate the photo; request video output explicitly.

### Using me (Grok in this session) to generate

I have direct access to Imagine via tools:
- `image_gen` (text-to-image)
- `image_edit` (image-to-image with reference photo + prompt; perfect for templates)
- `video_gen` (text-to-video; for img2vid you may describe the input or use follow-up edits)

Example request:
"Take the photo in inputs/photo.jpg and generate a version in 'Funky Dance' style using image_edit. Place the result in funky-dance/img/. Then generate a matching short video into funky-dance/vid/."

I can do multiple in parallel by calling tools together, then move the generated files (from session caches) into the target subfolders for you.

### Manual workflow (grok.com / app)

- Go to grok.com/imagine (or the Imagine tab).
- Select a Featured Template (Chibi, Funky Dance, etc.).
- Upload your photo from `inputs/`.
- Enter an optional additional prompt / instruction.
- Generate image(s) and/or video.
- Download and drop the results into the matching `<template>/img/` or `/vid/`.

## Tips for good results with one photo + style sweep

- Keep the **subject / composition** description consistent across runs.
- Let the template name drive the **style** (e.g. don't over-specify "in chibi style" if using the Chibi template).
- For video: start with image-to-video via the template, or add motion instructions like "gentle camera push in, subtle head movement".
- Use `inputs/` variants (different crops, lighting refs) for A/B testing a prompt.
- After a batch, review in `*/img/` and `*/vid/`, then refine the shared prompt and re-run only the weak ones.

## Updating the list

If new Featured Templates appear on grok.com/imagine, add matching folders + update this README + templates.json.

Run `ls -d */ | grep -v inputs` to see current template folders.

## templates.json

See templates.json for a scriptable list (name + display name + suggested category hints).

Happy style-sweeping! 🚀
