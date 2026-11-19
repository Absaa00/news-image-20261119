#!/usr/bin/env python3
"""Generate entry.png for news-image-20261119 (offline, PIL, deterministic).

Six-panel newspaper front page, 1024x1024, summing up Thursday
19 November 2026's world news. Run: python3 gen_image.py
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (245, 240, 228)      # paper
INK = (20, 20, 20)
RED = (178, 34, 34)
MUTED = (70, 70, 70)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(img, x, y, w, h, kicker, headline, sub, draw_scene):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3, fill=(250, 247, 238))
    ih = 112  # illustration height
    draw_scene(img, x + 3, y + 3, w - 6, ih)
    d.line([x, y + ih + 3, x + w, y + ih + 3], fill=INK, width=2)
    tx = x + 14
    ty = y + ih + 12
    d.text((tx, ty), kicker, font=font(SANS_B, 17), fill=RED)
    ty += 26
    for ln in wrap(d, headline, font(SERIF_B, 26), w - 28):
        d.text((tx, ty), ln, font=font(SERIF_B, 26), fill=INK)
        ty += 31
    ty += 4
    for ln in wrap(d, sub, font(SANS, 17), w - 28):
        d.text((tx, ty), ln, font=font(SANS, 17), fill=MUTED)
        ty += 22


def skyline(d, x, y, w, h, base, tops, col):
    d.rectangle([x, y, x + w, y + h], fill=base)
    import random
    rnd = random.Random(19)
    bx = x + 8
    while bx < x + w - 30:
        bw = rnd.randint(28, 52)
        bh = rnd.randint(35, tops)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=col)
        for wy in range(y + h - bh + 8, y + h - 6, 14):
            d.rectangle([bx + 5, wy, bx + bw - 5, wy + 6], fill=(255, 214, 90))
        bx += bw + 6


def scene_gta(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(255, 122, 26))  # sunset orange
    d.ellipse([x + w - 95, y + 8, x + w - 25, y + 78], fill=(255, 235, 120))
    # neon sign
    d.text((x + 14, y + 10), "VICE CITY", font=font(SANS_B, 30),
           fill=(255, 60, 200))
    d.text((x + 16, y + 46), "WELCOME BACK", font=font(SANS_B, 16),
           fill=(255, 255, 255))
    # city strip at bottom
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(38, 28, 52))
    for bx in range(x + 8, x + w - 20, 42):
        bh = 14 + ((bx * 7) % 20)
        d.rectangle([bx, y + h - bh, bx + 30, y + h], fill=(20, 14, 30))
        d.rectangle([bx + 6, y + h - bh + 4, bx + 24, y + h - bh + 9],
                    fill=(255, 80, 200))


def scene_gulf(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))  # night
    for sx in range(x + 20, x + w - 10, 47):
        d.ellipse([sx, y + 12 + (sx % 23), sx + 3, y + 15 + (sx % 23)],
                  fill=(255, 255, 255))
    # radar dish
    cx, cy = x + 110, y + 88
    d.line([cx, cy, cx - 26, y + h - 6], fill=(200, 200, 200), width=5)
    d.pieslice([cx - 42, cy - 42, cx + 42, cy + 42], 180, 360,
               fill=(120, 200, 120))
    # missile arcs
    for mx, my, col in ((x + 300, y + 30, (255, 90, 60)),
                        (x + 360, y + 55, (255, 160, 60))):
        d.arc([mx - 70, my - 40, mx + 70, my + 60], 200, 330, fill=col, width=5)
        d.ellipse([mx + 52, my + 18, mx + 64, my + 30], fill=col)
    # sea
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(30, 70, 110))


def scene_nvidia(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(18, 90, 40))  # nvidia green
    # chip
    cx, cy = x + w // 2, y + h // 2
    for i in range(-2, 3):
        d.line([cx - 52, cy + i * 20, cx - 68, cy + i * 20], fill=(190, 230, 190),
               width=4)
        d.line([cx + 52, cy + i * 20, cx + 68, cy + i * 20], fill=(190, 230, 190),
               width=4)
    d.rectangle([cx - 52, cy - 44, cx + 52, cy + 44], fill=(10, 40, 18),
                outline=(220, 240, 220), width=3)
    f = font(SANS_B, 30)
    d.text((cx - 22, cy - 18), "AI", font=f, fill=(140, 255, 140))
    d.text((x + 14, y + 8), "H-SERIES", font=font(SANS_B, 15),
           fill=(200, 240, 200))
    d.text((x + w - 172, y + h - 26), "SHIPMENTS HALTED",
           font=font(SANS_B, 15), fill=(255, 220, 120))


def scene_voyager(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 34))
    for sx in range(x + 14, x + w - 8, 38):
        d.ellipse([sx, y + 10 + (sx * 13 % 40), sx + 3, y + 13 + (sx * 13 % 40)],
                  fill=(255, 255, 255))
    # sun
    d.ellipse([x + 18, y + h - 52, x + 62, y + h - 8], fill=(255, 214, 90))
    # probe: gold dish + body + antenna
    cx, cy = x + w - 130, y + 40
    d.pieslice([cx - 48, cy - 26, cx + 48, cy + 26], 0, 180,
               fill=(212, 175, 55), outline=(150, 110, 20))
    d.rectangle([cx - 10, cy + 26, cx + 10, cy + 46], fill=(200, 200, 200))
    d.line([cx + 10, cy + 36, cx + 40, cy + 56], fill=(200, 200, 200), width=4)
    d.text((x + 14, y + 8), "1 LIGHT-DAY FROM EARTH",
           font=font(SANS_B, 16), fill=(180, 220, 255))
    d.text((x + w - 210, y + h - 28), "LAUNCHED 1977",
           font=font(SANS_B, 15), fill=(180, 220, 255))


def scene_eu(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))  # EU blue
    import math
    cx, cy = x + 110, y + h // 2
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx, sy = cx + 52 * math.cos(a), cy + 38 * math.sin(a)
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 204, 0))
    f = font(SERIF_B, 44)
    d.text((x + 210, y + 28), "€45 bn", font=f, fill=(255, 255, 255))
    d.text((x + 210, y + 78), "loan for Kyiv",
           font=font(SANS, 20), fill=(200, 220, 255))


def scene_cyclone(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(122, 178, 214))
    cx, cy = x + w // 2, y + h // 2 - 4
    for r in range(52, 8, -9):
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8],
              20 + r * 3, 300 + r * 3, fill=(255, 255, 255), width=6)
    d.ellipse([cx - 10, cy - 8, cx + 10, cy + 8], fill=(255, 255, 255))
    # waves
    for wy in (y + h - 22, y + h - 10):
        for wx in range(x + 6, x + w - 10, 34):
            d.arc([wx, wy, wx + 30, wy + 14], 180, 360,
                  fill=(255, 255, 255), width=3)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((W // 2, 12), "THE WORLD IN ONE PAGE",
           font=font(SERIF_B, 62), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 82), "THURSDAY 19 NOVEMBER 2026  •  SIX STORIES THAT SHAPED THE DAY",
           font=font(SANS, 20), fill=(200, 200, 200), anchor="ma")
    d.line([0, 122, W, 122], fill=INK, width=3)

    pw, ph = 494, 262
    ox, oy = 12, 132
    gap = 12
    panels = [
        ("CULTURE", "GTA VI begins global rollout",
         "After a 13-year wait, players flood into Vice City as Rockstar's "
         "sequel launches worldwide.", scene_gta),
        ("GULF TENSIONS", "US and Iran exchange fire again",
         "US strikes a missile site on Qeshm Island; Iran widens attacks to "
         "bases in Kuwait and Bahrain.", scene_gulf),
        ("TECH", "Nvidia's new era after Huang",
         "Acting CEO Kress promises earlier pay raises; the chipmaker halts "
         "H-series shipments to China.", scene_nvidia),
        ("SPACE", "Voyager 1 reaches a light-day",
         "After nearly 50 years in space, NASA's probe is one light-day from "
         "Earth — a record distance.", scene_voyager),
        ("EUROPE", "EU proposes €45bn Ukraine loan",
         "Brussels seeks funds to keep Kyiv afloat, to be repaid after Russia "
         "pays war reparations.", scene_eu),
        ("WEATHER", "Cyclone Akvan nears India",
         "The severe storm in the Bay of Bengal is forecast to cross the coast "
         "between Machilipatnam and Puri.", scene_cyclone),
    ]
    for i, (k, head, sub, scene) in enumerate(panels):
        px = ox + (i % 2) * (pw + gap)
        py = oy + (i // 2) * (ph + gap)
        panel(img, px, py, pw, ph, k, head, sub, scene)

    # ticker strip
    ty = oy + 3 * ph + 2 * gap + 6
    d.line([0, ty, W, ty], fill=INK, width=3)
    d.text((12, ty + 10),
           "ALSO: Jeffries set to be first Black US Speaker  •  Trump, Xi, Putin to meet "
           "at APEC  •  Fed signals more hikes",
           font=font(SANS, 16), fill=MUTED)
    d.text((12, H - 26), "Sources: AP, Reuters, BBC, NASA, IMD  •  Drawn programmatically, no photos",
           font=font(SANS, 15), fill=MUTED)

    img.save("entry.png", optimize=True)
    data = open("entry.png", "rb").read()
    print(f"entry.png {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
    assert len(data) <= 1024 * 1024, "over 1 MiB"


if __name__ == "__main__":
    main()
