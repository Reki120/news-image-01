#!/usr/bin/env python3
"""Build entry.png: a one-page newspaper front page summing up
Friday 13 November 2026 world news. 1024x1024, PIL only, no AI imagery.
All text drawn programmatically so it stays crisp and correct.
Layout is computed from measured text so nothing overflows."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (0x12, 0x28, 0x4B)
RED = (0xC8, 0x10, 0x2E)
INK = (0x1A, 0x1A, 0x1A)
LIGHT = (0xEE, 0xF1, 0xF5)
GOLD = (0xE8, 0xC8, 0x6A)

FD = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_MAST = font("DejaVuSerif-Bold.ttf", 52)
F_DATE = font("DejaVuSans-Bold.ttf", 23)
F_KICK = font("DejaVuSans-Bold.ttf", 22)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 64)
F_LEAD_SUM = font("DejaVuSans.ttf", 28)
F_HEAD = font("DejaVuSans-Bold.ttf", 32)
F_SUM = font("DejaVuSans.ttf", 22)
F_ALSO = font("DejaVuSans.ttf", 23)
F_ALSO_B = font("DejaVuSans-Bold.ttf", 23)

def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# ---- Masthead band ----
d.rectangle([0, 0, W, 100], fill=NAVY)
d.text((W // 2, 10), "THE WORLD IN ONE DAY", font=F_MAST, fill="white",
       anchor="ma")
d.text((W // 2, 64), "F R I D A Y   1 3   N O V E M B E R   2 0 2 6",
       font=F_DATE, fill=GOLD, anchor="ma")
d.rectangle([0, 100, W, 106], fill=RED)

# ---- Lead story (full width, no kicker line; size marks it as lead) ----
x0, x1 = 36, W - 36
y = 122
d.text((x0, y), "NVIDIA CEO RESIGNS", font=F_LEAD_HEAD, fill=NAVY)
y += 76
lead_sum = ("Jensen Huang steps down after reports of an affair with a woman "
            "alleged to be a Chinese spy; summoned to testify before "
            "Congress; Nvidia shares fall.")
lines = wrap(d, lead_sum, F_LEAD_SUM, x1 - x0)
y = draw_lines(d, lines, x0, y, F_LEAD_SUM, INK, 35)
y += 12
d.line([x0, y, x1, y], fill=(0xBB, 0xBB, 0xBB), width=2)
y += 14

# ---- 2x2 grid, stories 2-5 ----
col_w = (x1 - x0 - 28) // 2
stories = [
    ("MIDDLE EAST", (0x8A, 0x1F, 0x1F), "IRAN CLAIMS RADAR STRIKE",
     "Tehran says it destroyed a U.S. early-warning radar in Bahrain; the "
     "U.S. says it shot down two Iranian drones headed there."),
    ("EUROPE", (0x1F, 0x4E, 0x79), "EUROPE JOINS UKRAINE TALKS",
     "Russia and Ukraine agree Europe joins the next peace round after "
     "U.S. envoys meet Putin; Kyiv fires nearly 1,200 drones at Russia "
     "overnight."),
    ("TECH", (0x2E, 0x6B, 0x3A), "MICROSOFT OUTAGE, DAY 2",
     "Outlook, Teams and Copilot still down in 70+ countries, disrupting "
     "businesses, emergency calls and courts."),
    ("U.S.", (0x7A, 0x4A, 0x12), "U.S. FLIGHTS GROUNDED",
     "An FAA communications failure halts departures nationwide for four "
     "hours; the stop is lifted Friday evening."),
]
# measure each cell's height first
cell_h = []
for kick, color, head, summ in stories:
    hl = wrap(d, head, F_HEAD, col_w)
    sl = wrap(d, summ, F_SUM, col_w)
    cell_h.append(26 + len(hl) * 38 + 4 + len(sl) * 28)
row_h = [max(cell_h[0], cell_h[1]), max(cell_h[2], cell_h[3])]
grid_top = y
for i, (kick, color, head, summ) in enumerate(stories):
    cx = x0 + (i % 2) * (col_w + 28)
    cy = grid_top + (i // 2) * (row_h[0] + 14)
    d.rectangle([cx, cy + 3, cx + 14, cy + 17], fill=color)
    d.text((cx + 24, cy), kick, font=F_KICK, fill=color)
    hl = wrap(d, head, F_HEAD, col_w)
    hy = draw_lines(d, hl, cx, cy + 28, F_HEAD, NAVY, 38)
    sl = wrap(d, summ, F_SUM, col_w)
    draw_lines(d, sl, cx, hy + 4, F_SUM, INK, 28)
    if i % 2 == 0:
        d.line([x0 + col_w + 14, cy + 4, x0 + col_w + 14,
                cy + row_h[i // 2] - 4], fill=(0xDD, 0xDD, 0xDD), width=2)

y = grid_top + row_h[0] + 14 + row_h[1] + 8
d.line([x0, y, x1, y], fill=(0xBB, 0xBB, 0xBB), width=2)
y += 12

# ---- Story 6, full-width bar ----
s6 = ("Taiwan details a large, unannounced Chinese naval exercise across "
      "the western Pacific as intimidation.")
s6l = wrap(d, s6, F_SUM, x1 - x0 - 48)
bar_h = 10 + 26 + 4 + 38 + 4 + len(s6l) * 28 + 10
d.rectangle([x0, y, x1, y + bar_h], fill=LIGHT)
d.rectangle([x0 + 24, y + 13, x0 + 38, y + 27], fill=(0x6B, 0x2E, 0x5A))
d.text((x0 + 48, y + 10), "ASIA", font=F_KICK, fill=(0x6B, 0x2E, 0x5A))
d.text((x0 + 24, y + 40), "CHINA'S PACIFIC DRILLS", font=F_HEAD, fill=NAVY)
draw_lines(d, s6l, x0 + 24, y + 82, F_SUM, INK, 28)
y += bar_h + 12

# ---- ALSO strip ----
also = ("ALSO:  Pope Leo meets abuse survivors in Lima  •  U.S. seizes "
        "$1.2bn in crypto from the Binance hack  •  Brooklyn collapse toll "
        "settles at 8 dead")
al = wrap(d, also, F_ALSO, W - 72)
strip_h = 12 + len(al) * 29 + 12
d.rectangle([0, y, W, y + strip_h], fill=NAVY)
ay = y + 12
for ln in al:
    # gold "ALSO:" on first line only
    if ln.startswith("ALSO:"):
        d.text((36, ay), "ALSO:", font=F_ALSO_B, fill=GOLD)
        rest = ln[len("ALSO:"):]
        d.text((36 + d.textlength("ALSO: ", font=F_ALSO_B), ay), rest,
               font=F_ALSO, fill="white")
    else:
        d.text((36, ay), ln, font=F_ALSO, fill="white")
    ay += 29
y += strip_h
print("final bottom y =", y, "(canvas", H, ")")

img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
print("saved entry.png", img.size)
