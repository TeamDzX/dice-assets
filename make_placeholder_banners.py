#!/usr/bin/env python3
"""Generate 800x400 placeholder banners (soft glowing blobs on a themed
gradient — house style, no text) until the ComfyUI/FLUX server is back up.

Once the server is available, regenerate the real banners with the prompts in
GALLERY_HANDOVER.md §Banners and overwrite these files (then bump `updated`
in packs.json; banner URLs are stable so no version bump is needed).
"""
from PIL import Image, ImageDraw, ImageFilter
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 800, 400

# slug: (top colour, bottom colour, [glow colours])
THEMES = {
    "sakura-set":     ((46, 24, 34),  (94, 42, 66),   [(246, 204, 216), (197, 179, 230), (168, 198, 134)]),
    "metal-works":    ((24, 26, 30),  (58, 64, 74),   [(217, 219, 222), (227, 169, 143), (180, 101, 63)]),
    "gemstones":      ((16, 14, 26),  (38, 34, 66),   [(79, 161, 115), (31, 60, 136), (140, 31, 53)]),
    "neon-glow":      ((8, 6, 14),    (22, 12, 34),   [(255, 46, 147), (34, 211, 238), (163, 230, 53)]),
    "tatami-room":    ((42, 43, 28),  (84, 85, 54),   [(143, 143, 94), (188, 186, 140), (110, 111, 74)]),
    "casino-night":   ((26, 8, 10),   (58, 13, 18),   [(122, 22, 34), (27, 44, 92), (212, 175, 55)]),
    "party-night":    ((30, 12, 8),   (70, 28, 14),   [(255, 140, 50), (255, 46, 100), (255, 214, 90)]),
    "tavern-classics":((22, 14, 8),   (52, 34, 18),   [(214, 158, 78), (140, 90, 40), (240, 220, 180)]),
}

os.makedirs(os.path.join(ROOT, "banners"), exist_ok=True)

for slug, (top, bottom, glows) in THEMES.items():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    glow_layer = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(glow_layer)
    spots = [(160, 210, 150), (420, 130, 120), (650, 260, 170)]
    for (cx, cy, rad), colour in zip(spots, glows):
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=colour)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(80))

    from PIL import ImageChops
    img = ImageChops.screen(img, glow_layer.point(lambda v: int(v * 0.55)))

    out = os.path.join(ROOT, "banners", f"{slug}.jpg")
    img.save(out, "JPEG", quality=88)
    print("banner:", out)

print("done — placeholders only; regenerate with FLUX when the server is back")
