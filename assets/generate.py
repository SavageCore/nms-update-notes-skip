#!/usr/bin/env python3
"""Regenerate the Nexus page images from the source artwork.

  assets/header-1300x372.jpg   (artwork band + title overlay, banner)
  assets/gallery-1920x1080.jpg (artwork with red X, gallery)

The header source is the game's own update-notes background texture
(textures/ui/frontend/backgrounds/patchnotesbg.dds), converted to
assets/src/header-notes.jpg - clean artwork with no dialog text behind the
title. The gallery source is a Steam screenshot of the actual update
notes page (assets/src/gallery-notes.jpg), crossed out.

Usage: python3 assets/generate.py   (or: make assets)
Requires: Pillow (pip install Pillow). Typeface is vendored (see FONT).
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HDR_SRC = os.path.join(HERE, "src", "header-notes.jpg")
SRC = os.path.join(HERE, "src", "gallery-notes.jpg")
HDR = os.path.join(HERE, "header-1300x372.jpg")
GALLERY = os.path.join(HERE, "gallery-1920x1080.jpg")

# In-game heading typeface, vendored (SIL OFL 1.1):
# https://github.com/NMSCD/No-Mans-Sky-Universal-Font
FONT = os.path.join(HERE, "fonts", "GeosansLight-NMS.ttf")

TITLE = ["UPDATE NOTES SKIP"]
SUBTITLE = "SKIPS THE UPDATE NOTES PAGE ON STARTUP"

# Header crop, in source pixels: full-width band around the upper-middle
# of the artwork, keeping the faces and the red planet in frame and the
# dark panel top-left clear for the title.
HDR_X = 0
HDR_Y = 500
HDR_W = 3840

# Header size in output pixels.
HDR_OUT_W = 1300
HDR_OUT_H = 372

# Title placement in the header.
TITLE_X = 48
TITLE_Y = 48
TITLE_SIZE = 50
TITLE_GAP = 62
SUBTITLE_SIZE = 30

X_RED = (255, 57, 0)


def text_shadowed(d, xy, s, font, fill):
    x, y = xy
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)):
        d.text((x + dx, y + dy), s, font=font, fill=(0, 0, 0))
    d.text((x, y), s, font=font, fill=fill)


def header():
    img = Image.open(HDR_SRC).convert("RGB")
    assert img.size[0] * 9 == img.size[1] * 16, f"source is not 16:9: {img.size}"
    assert img.size[0] >= HDR_X + HDR_W, f"crop too wide for source: {img.size}"

    band_h = int(HDR_W * HDR_OUT_H / HDR_OUT_W)
    band = img.crop((HDR_X, HDR_Y, HDR_X + HDR_W, HDR_Y + band_h))
    band = band.resize((HDR_OUT_W, HDR_OUT_H), Image.LANCZOS)
    d = ImageDraw.Draw(band, "RGBA")
    # left-weighted gradient: title sits on the left
    for x in range(HDR_OUT_W):
        a = int(205 * max(0.0, 1 - x / (HDR_OUT_W * 0.62)) ** 1.5)
        d.rectangle([x, 0, x + 1, HDR_OUT_H], fill=(0, 0, 0, a))
    band = band.convert("RGB")
    d = ImageDraw.Draw(band)
    fb = ImageFont.truetype(FONT, TITLE_SIZE)
    fs = ImageFont.truetype(FONT, SUBTITLE_SIZE)

    for i, line in enumerate(TITLE):
        text_shadowed(d, (TITLE_X, TITLE_Y + i * TITLE_GAP), line, fb, (255, 255, 255))
    text_shadowed(
        d,
        (TITLE_X + 2, TITLE_Y + len(TITLE) * TITLE_GAP + 8),
        SUBTITLE,
        fs,
        (255, 205, 130),
    )
    band.save(HDR, quality=92)
    print(f"wrote {HDR}")


def gallery():
    w, h = 1920, 1080
    src = Image.open(SRC).convert("RGB")
    scale = max(w / src.width, h / src.height)
    img = src.resize(
        (round(src.width * scale), round(src.height * scale)), Image.LANCZOS
    )
    left = (img.width - w) // 2
    top = (img.height - h) // 2
    img = img.crop((left, top, left + w, top + h))
    d = ImageDraw.Draw(img)
    d.line([(0, 0), (w, h)], fill=(0, 0, 0), width=30)
    d.line([(w, 0), (0, h)], fill=(0, 0, 0), width=30)
    d.line([(0, 0), (w, h)], fill=X_RED, width=22)
    d.line([(w, 0), (0, h)], fill=X_RED, width=22)
    img.save(GALLERY, quality=92)
    print(f"wrote {GALLERY}")


if __name__ == "__main__":
    header()
    gallery()
