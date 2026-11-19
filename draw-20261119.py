#!/usr/bin/env python3
"""Front page for Thursday 19 November 2026 world news (1024x1024).

Same proven v2 layout as the 18 Nov entry (dev rate 975976): masthead,
3 photo panels for stories 1-3, summaries for topics 1-10, headlines
11-35 only, world map with numbered dots for stories 1-10, by-the-numbers.

All 35 stories verified by web search on 19 Nov 2026 (see sources.md):
GTA VI rollout, Iran-Gulf escalation, Shenzhen trilateral, Jeffries,
Cyclone Akvan, Fed minutes, Peltola, Pew, Voyager 1, Nvidia H200, plus
25 more headlines. Photos are original PIL drawings, not photographs.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 22, 30)
NAVY = (16, 28, 54)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
RULE = (120, 110, 95)
GREY = (70, 66, 58)

FD = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(FD + name, size)

F_KICK = font("NotoSans-Bold.ttf", 15)
F_DATE = font("NotoSans-ExtraBold.ttf", 46)
F_SUB = font("NotoSans-Regular.ttf", 14)
F_CAP = font("NotoSans-Bold.ttf", 11)
F_TAG = font("NotoSans-Bold.ttf", 12)
F_H1 = font("NotoSans-Bold.ttf", 18)
F_B1 = font("NotoSans-Regular.ttf", 12)
F_H2 = font("NotoSans-Bold.ttf", 15)
F_B2 = font("NotoSans-Regular.ttf", 11)
F_H3 = font("NotoSans-Bold.ttf", 16)
F_B3 = font("NotoSans-Regular.ttf", 12)
F_LIST = font("NotoSans-Regular.ttf", 12)
F_LEAD = font("NotoSans-Bold.ttf", 12)
F_SEC = font("NotoSans-Bold.ttf", 13)
F_NUM = font("NotoSans-ExtraBold.ttf", 16)
F_FOOT = font("NotoSans-Regular.ttf", 11)
F_DOT = font("NotoSans-Bold.ttf", 9)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap_px(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def counter(x, y, n, r=11):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    t = str(n)
    d.text((x + r, y + r), t, font=F_DOT, fill=(255, 255, 255), anchor="mm")

# ---------- masthead (0-104) ----------
d.rectangle([0, 0, W, 104], fill=NAVY)
d.text((24, 12), "THE DAY IN WORLD NEWS", font=F_KICK, fill=GOLD)
d.text((1000, 12), "35 STORIES  ·  6 CONTINENTS  ·  ONE PAGE",
       font=F_KICK, fill=GOLD, anchor="ra")
d.text((24, 30), "Thursday 19 November 2026", font=F_DATE, fill=(255, 255, 255))
d.text((24, 84), "Every story on this page happened, or was first reported, on this day.",
       font=F_SUB, fill=(200, 205, 220))
d.line([(0, 104), (W, 104)], fill=GOLD, width=3)

# ---------- picture panels, stories 1-3 (y 112-236) ----------
PX = [24, 353, 682]
PW = 317
PY, PH = 112, 124

def panel_caption(x, text):
    d.rectangle([x, PY + PH - 22, x + PW, PY + PH], fill=(0, 0, 0))
    d.text((x + PW // 2, PY + PH - 11), text, font=F_CAP,
           fill=(255, 255, 255), anchor="mm")

# 1 - Vice City at dusk: pink-orange sky, sun, palms, neon skyline
x = PX[0]
for yy in range(PH):
    t = yy / PH
    r = int(255 - 60 * t); g = int(120 + 60 * t); b = int(150 + 40 * t)
    d.line([(x, PY + yy), (x + PW, PY + yy)], fill=(r, g, b))
d.ellipse([x + 130, PY + 14, x + 186, PY + 70], fill=(255, 214, 120))
# skyline
for bx, bw, bh in ((0, 40, 52), (46, 30, 70), (82, 44, 46), (132, 34, 62),
                   (172, 38, 48), (216, 30, 66), (252, 34, 54), (292, 25, 60)):
    d.rectangle([x + bx, PY + PH - bh, x + bx + bw, PY + PH], fill=(38, 20, 52))
    for wy in range(PY + PH - bh + 6, PY + PH - 4, 12):
        for wx in range(bx + 6, bx + bw - 4, 10):
            d.rectangle([x + wx, wy, x + wx + 4, wy + 5], fill=(255, 220, 90))
# palm silhouettes, left and right
for px, ph in ((18, 58), (296, 48)):
    d.line([(x + px, PY + PH), (x + px, PY + PH - ph)], fill=(20, 40, 24), width=4)
    for ang in range(-70, 71, 35):
        import math
        ex = px + int(22 * math.sin(math.radians(ang)))
        ey = PY + PH - ph - int(14 * abs(math.cos(math.radians(ang))))
        d.line([(x + px, PY + PH - ph), (x + ex, ey)], fill=(20, 40, 24), width=3)
panel_caption(x, "VICE CITY  ·  LEONIDA")

# 2 - Gulf night: radar, drone, moon, sea (story 2: Kuwait / Bahrain)
x = PX[1]
d.rectangle([x, PY, x + PW, PY + PH], fill=(13, 27, 62))
for sx, sy in ((30, 18), (90, 30), (150, 14), (210, 26), (260, 12), (120, 40)):
    d.ellipse([x + sx - 1, PY + sy - 1, x + sx + 1, PY + sy + 1], fill=(255, 255, 255))
d.ellipse([x + 268, PY + 16, x + 296, PY + 44], fill=(232, 228, 200))
d.rectangle([x, PY + 88, x + PW, PY + PH], fill=(18, 60, 70))
d.line([(x, PY + 88), (x + PW, PY + 88)], fill=(120, 180, 190), width=2)
d.line([(x + 52, PY + 88), (x + 52, PY + 56)], fill=(180, 190, 200), width=4)
d.polygon([(x + 36, PY + 62), (x + 54, PY + 36), (x + 70, PY + 58)],
          fill=(180, 190, 200))
cx, cy = x + 160, PY + 52
for dx, dy in ((-22, -14), (22, -14), (-22, 14), (22, 14)):
    d.line([(cx, cy), (cx + dx, cy + dy)], fill=(230, 230, 230), width=3)
    d.ellipse([cx + dx - 9, cy + dy - 3, cx + dx + 9, cy + dy + 3], fill=(230, 230, 230))
d.rounded_rectangle([cx - 14, cy - 8, cx + 14, cy + 8], radius=5, fill=(230, 230, 230))
d.line([(x + 225, PY + 30), (x + 285, PY + 62)], fill=(240, 140, 60), width=4)
d.ellipse([x + 282, PY + 59, x + 290, PY + 67], fill=(240, 140, 60))
panel_caption(x, "ALI AL SALEM  ·  KUWAIT")

# 3 - Cyclone Akvan: spiral bands over the Bay of Bengal
x = PX[2]
d.rectangle([x, PY, x + PW, PY + PH], fill=(24, 78, 110))
d.rectangle([x, PY + 96, x + PW, PY + PH], fill=(16, 52, 76))
import math
ccx, ccy = x + 158, PY + 62
for k in range(4):
    r0 = 12 + k * 14
    d.arc([ccx - r0, ccy - r0, ccx + r0, ccy + r0],
          start=40 + k * 55, end=300 + k * 55, fill=(235, 240, 245), width=7)
d.ellipse([ccx - 8, ccy - 8, ccx + 8, ccy + 8], fill=(235, 240, 245))
# rain streaks
for sx in range(0, PW, 26):
    d.line([(x + sx, PY + 8), (x + sx - 6, PY + 26)], fill=(190, 210, 225), width=2)
panel_caption(x, "BAY OF BENGAL  ·  AKVAN")

# ---------- topics 1-3 text (y 242-356) ----------
TOP3 = [
    ("ENTERTAINMENT · GAMING", "GTA VI rolls out worldwide after 13 years",
     "Midnight launches began in New Zealand and Sydney; critics give it 99 "
     "on Metacritic. Pre-orders top $1.65bn."),
    ("MIDDLE EAST · CONFLICT", "Iran widens attacks to Kuwait and Bahrain",
     "Tehran hit a US air base in Kuwait and sites in Bahrain, days after US "
     "jets struck Qeshm. Gulf states say they intercepted the fire."),
    ("ASIA · DIPLOMACY", "Trump, Xi and Putin to meet in Shenzhen",
     "The first trilateral of the three leaders is set for Thursday at APEC. "
     "Ukraine, Iran, trade and nuclear arms are on the table."),
]
TY = 242
for i, (tag, head, body) in enumerate(TOP3):
    x = PX[i]
    counter(x, TY, i + 1)
    d.text((x + 28, TY + 2), tag, font=F_TAG, fill=RED)
    lines = wrap_px(head, F_H1, PW)
    assert len(lines) <= 2, (head, lines)
    hy = TY + 26
    for ln in lines:
        d.text((x, hy), ln, font=F_H1, fill=INK)
        hy += 22
    blines = wrap_px(body, F_B1, PW)
    assert len(blines) <= 3, (head, blines)
    by = hy + 4
    for ln in blines:
        d.text((x, by), ln, font=F_B1, fill=(52, 50, 46))
        by += 15

d.line([(24, 366), (1000, 366)], fill=INK, width=2)

# ---------- topics 4-7 (4 cols, y 374-488) ----------
TOP47 = [
    ("UNITED STATES · POLITICS", "Jeffries nominated Speaker, 251–11",
     "House Democrats pick the New Yorker to lead the next Congress. If "
     "elected in January, he is the first Black Speaker."),
    ("SOUTH ASIA · WEATHER", "Cyclone Akvan turns severe off India",
     "Landfall is due Friday near Machilipatnam, with gusts to 145 km/h. "
     "Odisha is moving 200,000 people from the coast."),
    ("UNITED STATES · ECONOMY", "Fed minutes point to more rate hikes",
     "Almost all officials expect further rises to tame inflation. Rates "
     "held at 3.75–4% in a 10–2 vote."),
    ("UNITED STATES · POLITICS", "Peltola wins Alaska; Democrats 56–44",
     "The first Alaska Native senator takes the last midterm seat. Democrats "
     "hold their biggest majority since 2009."),
]
CX4 = [24, 271, 518, 765]
CW4 = 235
for i, (tag, head, body) in enumerate(TOP47):
    x = CX4[i]
    n = i + 4
    counter(x, 374, n, r=10)
    d.text((x + 26, 375), tag, font=font("NotoSans-Bold.ttf", 10), fill=RED)
    lines = wrap_px(head, F_H2, CW4)
    assert len(lines) <= 3, (head, lines)
    hy = 396
    for ln in lines:
        d.text((x, hy), ln, font=F_H2, fill=INK)
        hy += 19
    blines = wrap_px(body, F_B2, CW4)
    assert len(blines) <= 3, (head, blines)
    by = hy + 3
    for ln in blines:
        d.text((x, by), ln, font=F_B2, fill=(52, 50, 46))
        by += 14

# ---------- topics 8-10 (3 cols, y 496-610) ----------
TOP810 = [
    ("WORLD · RELIGION", "Pew: Islam to be largest faith by 2035",
     "Muslims, 2.57bn, would pass Christians, 2.52bn, driven by higher "
     "fertility. Both faiths keep growing."),
    ("SPACE · NASA", "Voyager 1 reaches one light-day out",
     "The 1977 probe is 16bn miles away; a radio signal now takes a day. "
     "NASA confirms the milestone on Thursday."),
    ("TECH · CHIPS", "Nvidia halts H200 shipments to China",
     "Acting chief Colette Kress says no more licensed Hopper chips will "
     "ship. The $2.4bn quarter is the last."),
]
for i, (tag, head, body) in enumerate(TOP810):
    x = PX[i]
    n = i + 8
    counter(x, 496, n)
    d.text((x + 28, 498), tag, font=F_TAG, fill=RED)
    lines = wrap_px(head, F_H3, PW)
    assert len(lines) <= 2, (head, lines)
    hy = 522
    for ln in lines:
        d.text((x, hy), ln, font=F_H3, fill=INK)
        hy += 20
    blines = wrap_px(body, F_B3, PW)
    assert len(blines) <= 3, (head, blines)
    by = hy + 4
    for ln in blines:
        d.text((x, by), ln, font=F_B3, fill=(52, 50, 46))
        by += 15

d.line([(24, 620), (1000, 620)], fill=INK, width=2)

# ---------- bottom: world map (left) + stories 11-35 (right) ----------
LAND = {
    1: [(9, 12), (18, 20)],
    2: [(3, 6), (9, 15), (18, 20), (33, 36), (39, 57)],
    3: [(3, 7), (9, 16), (30, 31), (33, 37), (38, 57)],
    4: [(4, 8), (10, 16), (31, 37), (38, 56)],
    5: [(5, 9), (11, 16), (31, 36), (39, 55), (55, 57)],
    6: [(6, 10), (12, 16), (30, 32), (32, 36), (40, 54), (55, 56)],
    7: [(7, 11), (13, 16), (30, 32), (33, 36), (41, 53)],
    8: [(8, 12), (14, 16), (34, 36), (42, 52)],
    9: [(9, 12), (14, 15), (30, 37), (38, 42), (43, 51)],
    10: [(10, 13), (30, 37), (38, 42), (43, 50)],
    11: [(11, 13), (30, 37), (39, 42), (44, 49)],
    12: [(12, 13), (14, 18), (31, 37), (44, 46), (49, 53)],
    13: [(13, 18), (31, 37), (50, 53)],
    14: [(13, 19), (31, 37)],
    15: [(14, 19), (32, 37)],
    16: [(14, 19), (32, 36), (39, 40)],
    17: [(15, 19), (32, 36), (39, 40)],
    18: [(15, 18), (33, 35), (51, 57)],
    19: [(16, 18), (33, 35), (51, 57)],
    20: [(16, 18), (52, 56)],
    21: [(17, 18), (52, 56), (58, 59)],
    22: [(17, 18)],
}
MAP_X, MAP_Y = 24, 660
DOT = (96, 116, 96)
for r, spans in LAND.items():
    for c0, c1 in spans:
        for c in range(c0, c1 + 1):
            cx = MAP_X + c * 5 + 2
            cy = MAP_Y + r * 5 + 2
            d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=DOT)
# numbered dots for stories 1-10: (lon, lat)
DOTS = [(151, -33.9), (48, 29.3), (114.1, 22.5), (-77, 38.9), (85.4, 12.9),
        (-77, 38.9), (-150, 64), (-77, 38.9), (-118.2, 34.2), (114.1, 22.5)]
NUDGE = [(0, 0), (0, 0), (6, 6), (-10, -8), (0, 0),
         (10, 8), (0, 0), (-2, 10), (0, 0), (-6, -6)]
for i, (lon, lat) in enumerate(DOTS):
    c = int((lon + 180) / 6)
    r = int((78 - lat) / 5)
    cx = MAP_X + c * 5 + 2 + NUDGE[i][0]
    cy = MAP_Y + r * 5 + 2 + NUDGE[i][1]
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    d.text((cx, cy), str(i + 1), font=F_DOT, fill=(255, 255, 255), anchor="mm")

d.text((24, 630), "WHERE THE NEWS HAPPENED", font=F_SEC, fill=INK)
d.text((24, 792), "Numbered dots mark stories 1–10.", font=F_FOOT, fill=GREY)
d.line([(24, 812), (330, 812)], fill=RULE, width=1)
d.text((24, 820), "BY THE NUMBERS", font=F_SEC, fill=RED)
NUMBERS = [
    ("99", "GTA VI's Metacritic score, a record"),
    ("$1.65bn", "GTA VI pre-orders and early sales"),
    ("251–11", "Jeffries' vote for Speaker nominee"),
    ("200,000", "people Odisha is moving from the coast"),
]
ny = 842
for num, lab in NUMBERS:
    d.text((24, ny), num, font=F_NUM, fill=NAVY)
    d.text((24, ny + 20), lab, font=F_FOOT, fill=GREY)
    ny += 34

# stories 11-35, two columns, headline only, one line each
MORE = [
    (11, "India-Japan 2+2", "defence talks open in Tokyo"),
    (12, "Modi meets royals", "William and Kate in Delhi"),
    (13, "Somalia vs UAE", "secret bases alleged"),
    (14, "Deutsche Bank", "$582m Epstein-linked deals"),
    (15, "NSA network down", "classified system hit"),
    (16, "Green cards", "US proposes tougher rules"),
    (17, "Tanker attacked", "hit off Bulgaria"),
    (18, "Gaza warning", "Board of Peace fears collapse"),
    (19, "EU Ukraine loan", "€45bn plan proposed"),
    (20, "Canada-China", "Carney rethinks ties, eyes US deal"),
    (21, "AI cyber threat", "senators say defences lag"),
    (22, "Saudi all-clear", "danger passed in 3 cities"),
    (23, "Libya seizure", "cocaine, millions of pills"),
    (24, "Mélenchon rise", "could win French presidency"),
    (25, "Lost billion years", "Earth gap explained"),
    (26, "Duckett 133", "England on top in 3rd ODI"),
    (27, "AI 171 probe", "report at 'fag end'"),
    (28, "50 pupils ill", "tar-plant pollution scare"),
    (29, "Sports leagues", "India forms 14-member panel"),
    (30, "Microsoft", "AI services talks with ByteDance"),
    (31, "Oil slides", "Gulf risk, risk aversion rise"),
    (32, "Trump on Vance", "'unhappy' over Iran war stance"),
    (33, "Liu Yunping", "first Taiwanese American chair"),
    (34, "Taiwan bill", "transnational repression crime"),
    (35, "GTA VI verdict", "'may mark end of an era'"),
]
d.text((342, 630), "ALSO ON THURSDAY 19 NOVEMBER — 25 MORE STORIES",
       font=F_SEC, fill=RED)
d.line([(342, 652), (1000, 652)], fill=RED, width=2)
COL_X = [342, 673]
COL_W = 323
for j, (n, lead, rest) in enumerate(MORE):
    col = j // 13
    row = j % 13
    x = COL_X[col]
    y = 662 + row * 24
    d.text((x, y), f"{n}.", font=F_LEAD, fill=RED)
    lx = x + 26
    d.text((lx, y), lead, font=F_LEAD, fill=INK)
    lw = d.textlength(lead, font=F_LEAD)
    txt = " — " + rest
    assert d.textlength(txt, font=F_LIST) <= COL_W - 26 - lw, (n, lead, rest)
    d.text((lx + lw, y), txt, font=F_LIST, fill=(52, 50, 46))

# ---------- footer ----------
d.line([(24, 988), (1000, 988)], fill=RULE, width=1)
d.text((512, 996),
       "All stories happened or were first reported on Thursday 19 November 2026.  "
       "Sources: Reuters, AP, BBC, CNN, FT, IMD, NASA, Pew, The Hindu, PTI.  Original drawings.",
       font=F_FOOT, fill=GREY, anchor="ma")

img.save("/home/hatch/workspace/makefun/news-image-20261119/entry.png",
         optimize=True)
print("saved entry.png")
