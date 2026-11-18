#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed text, fixed palette, seeded star field, no timestamps.
Requires Pillow only for the build; main.py (the graded entrypoint) is
stdlib-only and just copies the finished image to /output/entry.png.

News sources cross-checked for 18 Nov 2026: AP, Reuters, BBC, DW,
The Indian Express, Jagran Josh, Education Times, The Knowledge Library.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
GREY = (90, 86, 76)
RED = (185, 28, 28)
RULE = (60, 56, 48)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, spacing=4):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def star_field(draw, box, seed=7, count=70):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(count):
        x = rnd.randint(x0 + 4, x1 - 4)
        y = rnd.randint(y0 + 4, y1 - 30)
        r = rnd.choice([1, 1, 2])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(220, 228, 240))


def draw_bridge_scene(draw, box):
    """Night illustration: the Crimea (Kerch) bridge, one span broken,
    explosion over the gap, reflections on the water."""
    x0, y0, x1, y1 = box
    # solid night sky
    draw.rectangle([x0, y0, x1, y0 + 190], fill=(13, 28, 50))
    star_field(draw, (x0, y0, x1, y0 + 150))
    # moon
    draw.ellipse([x1 - 72, y0 + 22, x1 - 30, y0 + 64], fill=(232, 230, 210))
    draw.ellipse([x1 - 64, y0 + 30, x1 - 48, y0 + 46], fill=(210, 208, 188))
    # water
    draw.rectangle([x0, y0 + 190, x1, y1], fill=(8, 20, 32))
    for yy in range(y0 + 198, y1 - 6, 14):
        draw.line([(x0 + 12, yy), (x1 - 12, yy)], fill=(16, 36, 54))
    # bridge deck: full width, clear gap in the middle
    deck_y = y0 + 150
    cx = (x0 + x1) // 2 + 10
    draw.rectangle([x0 + 8, deck_y, cx - 52, deck_y + 9], fill=(226, 230, 236))
    draw.rectangle([cx + 52, deck_y, x1 - 8, deck_y + 9], fill=(226, 230, 236))
    # fallen segment, tilted down into the gap
    draw.line([(cx - 52, deck_y + 9), (cx - 14, deck_y + 44)], fill=(226, 230, 236), width=7)
    draw.line([(cx - 14, deck_y + 44), (cx + 22, deck_y + 52)], fill=(190, 194, 200), width=7)
    # towers
    for tx in (x0 + 66, x1 - 78):
        draw.rectangle([tx, deck_y - 96, tx + 12, deck_y], fill=(226, 230, 236))
        draw.rectangle([tx - 6, deck_y - 96, tx + 18, deck_y - 88], fill=(226, 230, 236))
    # cables from tower tops to the deck ends
    for tx in (x0 + 72, x1 - 72):
        draw.line([(tx + 6, deck_y - 92), (cx - 56, deck_y)], fill=(160, 166, 174), width=2)
        draw.line([(tx + 6, deck_y - 92), (cx + 56, deck_y)], fill=(160, 166, 174), width=2)
        draw.line([(tx + 6, deck_y - 92), (x0 + 14, deck_y)], fill=(160, 166, 174), width=2)
        draw.line([(tx + 6, deck_y - 92), (x1 - 14, deck_y)], fill=(160, 166, 174), width=2)
    # explosion: compact burst over the gap
    ex, ey = cx, deck_y - 34
    for r, col in ((40, (255, 140, 40)), (28, (255, 176, 66)), (16, (255, 214, 120))):
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    pts = []
    for k in range(12):
        ang = math.pi * 2 * k / 12
        rr = 40 if k % 2 == 0 else 18
        pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
    draw.polygon(pts, fill=(255, 200, 90))
    draw.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=(255, 240, 200))
    # smoke puffs
    for sx, sy, sr in ((ex - 46, ey - 40, 15), (ex + 36, ey - 50, 18),
                       (ex + 56, ey - 24, 12), (ex - 58, ey - 16, 11)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(74, 78, 86))
    # reflection streaks under the blast
    for i, ww in enumerate((96, 66, 40)):
        draw.line([(ex - ww // 2, y0 + 204 + i * 13),
                   (ex + ww // 2, y0 + 204 + i * 13)],
                  fill=(255, 150, 50), width=3)
    # caption
    draw.text((x0 + 12, y1 - 26), "ILLUSTRATION: THE CRIMEA BRIDGE AFTER THE STRIKE",
              font=font(SANS_B, 13), fill=(210, 214, 220))


def icon_globe(draw, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=col, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=col, width=2)


def icon_waves(draw, box, col):
    x0, y0, x1, y1 = box
    for i, yy in enumerate((y0 + 10, y0 + 22, y0 + 34)):
        draw.arc([x0, yy, x1, yy + 16], 180, 360, fill=col, width=3)


def icon_arrows(draw, box, col):
    x0, y0, x1, y1 = box
    my = (y0 + y1) // 2
    draw.line([(x0 + 4, y0 + 12), (x1 - 10, y0 + 12)], fill=col, width=3)
    draw.polygon([(x1 - 10, y0 + 6), (x1 - 2, y0 + 12), (x1 - 10, y0 + 18)], fill=col)
    draw.line([(x1 - 4, y1 - 12), (x0 + 10, y1 - 12)], fill=col, width=3)
    draw.polygon([(x0 + 10, y1 - 18), (x0 + 2, y1 - 12), (x0 + 10, y1 - 6)], fill=col)


def icon_ban(draw, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    draw.line([(cx - r * 0.7, cy + r * 0.7), (cx + r * 0.7, cy - r * 0.7)],
              fill=col, width=3)


def icon_cyclone(draw, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r in (18, 12, 6):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 30, 300, fill=col, width=3)


def icon_cricket(draw, box, col):
    x0, y0, x1, y1 = box
    # bat: flat blade upper right, handle down to lower left
    draw.polygon([(x1 - 16, y0 + 4), (x1 - 4, y0 + 10), (x0 + 16, y1 - 16),
                  (x0 + 8, y1 - 22)], fill=col)
    draw.line([(x0 + 12, y1 - 18), (x0 + 4, y1 - 6)], fill=col, width=5)
    # ball with seam
    draw.ellipse([x0 + 26, y0 + 26, x0 + 42, y0 + 42], fill=col)
    draw.arc([x0 + 28, y0 + 28, x0 + 40, y0 + 40], 200, 340, fill=PAPER, width=2)


ICONS = {
    "globe": icon_globe,
    "waves": icon_waves,
    "arrows": icon_arrows,
    "ban": icon_ban,
    "cyclone": icon_cyclone,
    "cricket": icon_cricket,
}

STORIES = [
    ("ASIA", (192, 86, 33), "globe",
     "TRUMP LANDS IN MANILA FOR QUAD TALKS",
     "The US president opens his Asia tour ahead of a China visit, as ASEAN leaders meet."),
    ("THE GULF", (14, 116, 144), "waves",
     "IRAN HITS US RADAR IN BAHRAIN",
     "Drone attack deepens the Gulf exchange; a tanker is hit in the Strait of Hormuz."),
    ("TRADE", (21, 128, 61), "arrows",
     "CANADA AND CHINA EXTEND TRADE DEALS",
     "Xi meets Carney ahead of the APEC summit as Ottawa and Beijing ease tensions."),
    ("MIDDLE EAST", (109, 40, 217), "ban",
     "BRITAIN SANCTIONS SETTLEMENT FIRMS",
     "London targets firms in the occupied West Bank to protect a two-state solution."),
    ("WEATHER", (29, 78, 216), "cyclone",
     "CYCLONE AKVAN BEARS DOWN",
     "The Bay of Bengal storm strengthens; India's east coast is put on alert."),
    ("SPORT", (190, 18, 60), "cricket",
     "DHONI CALLS TIME ON IPL CAREER",
     "The Chennai legend retires as a player and becomes Super Kings mentor."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # margin
    # outer hairline
    d.rectangle([M - 8, M - 8, W - M + 8, H - M + 8], outline=RULE, width=2)

    # ---- masthead ----
    title_f = font(SERIF_B, 78)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 30), title, font=title_f, fill=INK)
    y = 30 + 78 + 10
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    d.line([(M, y + 6), (W - M, y + 6)], fill=INK, width=1)
    y += 16
    date_f = font(SANS_B, 27)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, y), date, font=date_f, fill=RED)
    y += 27 + 10
    tag_f = font(SANS, 16)
    tag = "ONE DAY  ·  ONE IMAGE  —  THE WORLD IN A SINGLE FRAME"
    tw2 = d.textlength(tag, font=tag_f)
    d.text(((W - tw2) / 2, y), tag, font=tag_f, fill=GREY)
    y += 16 + 14

    # ---- lead story ----
    lead_top, lead_h = y, 302
    d.rectangle([M, lead_top, W - M, lead_top + lead_h], outline=INK, width=2)
    pic = (M + 2, lead_top + 2, M + 482, lead_top + lead_h - 2)
    draw_bridge_scene(d, pic)
    tx = M + 482 + 26
    tw_ = W - M - 26 - tx
    yy = lead_top + 24
    d.text((tx, yy), "WAR IN UKRAINE", font=font(SANS_B, 17), fill=RED)
    yy += 17 + 12
    head_f = font(SANS_B, 37)
    lines = wrap(d, "UKRAINE HITS THE CRIMEA BRIDGE AGAIN", head_f, tw_)
    yy = draw_lines(d, lines, tx, yy, head_f, INK, spacing=6)
    yy += 10
    d.line([(tx, yy), (tx + 64, yy)], fill=RED, width=4)
    yy += 18
    deck_f = font(SANS, 18)
    deck = ("Kyiv strikes the Kerch crossing for a second straight day — "
            "as Russian missiles pound two bridges in the capital.")
    draw_lines(d, wrap(d, deck, deck_f, tw_), tx, yy, deck_f, (52, 50, 44), spacing=6)
    yy = lead_top + lead_h + 16

    # ---- grid of six stories ----
    cols, rows = 3, 2
    gap = 15
    cell_w = (W - 2 * M - (cols - 1) * gap) // cols
    cell_h = 188
    grid_top = yy
    for i, (kicker, col, icon, headline, deck) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x = M + c * (cell_w + gap)
        y0 = grid_top + r * (cell_h + gap)
        d.rectangle([x, y0, x + cell_w, y0 + cell_h], outline=(150, 144, 128), width=1)
        d.rectangle([x, y0, x + cell_w, y0 + 5], fill=col)
        ix = x + cell_w - 52
        ICONS[icon](d, (ix, y0 + 16, ix + 44, y0 + 60), col)
        cx = x + 16
        cy = y0 + 16
        d.text((cx, cy), kicker, font=font(SANS_B, 14), fill=col)
        cy += 14 + 8
        hf = font(SANS_B, 20)
        lines = wrap(d, headline, hf, cell_w - 32 - 52)
        cy = draw_lines(d, lines, cx, cy, hf, INK, spacing=3)
        cy += 6
        df = font(SANS, 15)
        draw_lines(d, wrap(d, deck, df, cell_w - 32), cx, cy, df, (52, 50, 44), spacing=4)

    # ---- footer ----
    fy = grid_top + rows * cell_h + (rows - 1) * gap + 16
    d.line([(M, fy), (W - M, fy)], fill=INK, width=2)
    fy += 12
    tick_f = font(SANS_B, 15)
    tick = ("ALSO TODAY:   Baidu chief warns of an AI bubble  ·  Modi rallies the "
            "Indo-Pacific at the East Asia Summit  ·  Thailand fire kills 11  ·  "
            "Pope Leo struck by a rosary in Peru")
    draw_lines(d, wrap(d, tick, tick_f, W - 2 * M), M, fy, tick_f, INK, spacing=4)
    fy += 15 * 2 + 4 + 10
    src_f = font(SANS, 13)
    src = "Sources: AP  ·  Reuters  ·  BBC  ·  DW  ·  The Indian Express  —  18 November 2026"
    d.text((M, fy), src, font=src_f, fill=GREY)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
