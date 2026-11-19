#!/usr/bin/env python3
"""Front page: world news of Thursday 19 November 2026.

Draws a 1024x1024 newspaper front page with PIL only. All artwork is
drawn programmatically (no external images): a Vice City sunset skyline,
a Gulf night sea, a cyclone spiral, and a dotted world map.
Stories and facts come from sources.md in this folder.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

INK = (24, 24, 30)
NAVY = (13, 27, 62)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
CREAM = (247, 243, 232)
GREY = (90, 88, 82)
RULE = (40, 40, 48)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, max_w, leading, fill=INK, max_lines=None):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    lines = wrap(d, text, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def num_badge(d, cx, cy, n, r=11):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    t = str(n)
    f = font(SANS_B, 12)
    d.text((cx - d.textlength(t, font=f) / 2, cy - 8), t,
           font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- data
# (headline, kicker, summary, date, place, source) for the top ten.
TOP = [
    ("GTA VI rolls out worldwide after 13 years", "ENTERTAINMENT \u00b7 GAMING",
     "Midnight launches in New Zealand and Sydney; 99 on Metacritic; "
     "$1.65bn in pre-orders.",
     "19 Nov", "Sydney / New Zealand", "Reuters"),
    ("Iran widens attacks to Kuwait and Bahrain", "MIDDLE EAST \u00b7 CONFLICT",
     "Ali Al Salem air base in Kuwait and sites in Bahrain hit, in "
     "retaliation for the US strike on Qeshm.",
     "18 Nov, reported 19 Nov", "Kuwait / Bahrain", "AP / Reuters"),
    ("Trump, Xi and Putin to meet in Shenzhen", "ASIA \u00b7 DIPLOMACY",
     "First trilateral meeting of the three leaders, held on the APEC "
     "sidelines.",
     "19 Nov", "Shenzhen", "Reuters"),
    ("Jeffries nominated Speaker, 251\u201311", "UNITED STATES \u00b7 POLITICS",
     "House Democrats pick the New Yorker to lead the next Congress.",
     "18 Nov, reported 19 Nov", "Washington", "AP / Reuters"),
    ("Cyclone Akvan turns severe off India", "SOUTH ASIA \u00b7 WEATHER",
     "Landfall due 20 Nov near Machilipatnam; gusts of 145 km/h; "
     "200,000 evacuated.",
     "19 Nov", "Bay of Bengal", "IMD / The Hindu"),
    ("Fed minutes point to more rate hikes", "UNITED STATES \u00b7 ECONOMY",
     "Minutes of 27\u201328 Oct; rates held at 3.75\u20134% on a 10\u20132 vote.",
     "18 Nov, reported 19 Nov", "Washington", "Reuters"),
    ("Peltola wins Alaska; Democrats 56\u201344", "UNITED STATES \u00b7 POLITICS",
     "First Alaska Native senator; largest Democratic Senate majority "
     "since 2009.",
     "17\u201318 Nov, reported 19 Nov", "Alaska", "Reuters"),
    ("Pew: Islam to be largest faith by 2035", "WORLD \u00b7 RELIGION",
     "2.57bn Muslims vs 2.52bn Christians by 2035.",
     "18 Nov, reported 19 Nov", "Washington", "Pew Research Center"),
    ("Voyager 1 reaches one light-day out", "SPACE \u00b7 NASA",
     "16bn miles from Earth; its signal now takes a day; NASA briefing "
     "on 19 Nov.",
     "18\u201319 Nov", "NASA / JPL", "NASA / Reuters"),
    ("Nvidia halts H200 shipments to China", "TECH \u00b7 CHIPS",
     "Acting CEO Colette Kress; $2.4bn licensed Hopper quarter.",
     "18 Nov, reported 19 Nov", "Shenzhen", "Reuters"),
]

# (headline, date, place, source) for stories 11-35. Place "" = no place given.
MORE = [
    ("India\u2013Japan 2+2 defence talks open in Tokyo", "19 Nov", "Tokyo", "The Hindu / MEA"),
    ("Modi meets Prince and Princess of Wales", "19 Nov", "New Delhi", "The Hindu"),
    ("Somalia accuses UAE of secret bases", "17\u201318 Nov, reported 19 Nov", "Mogadishu", "Middle East Eye"),
    ("Deutsche Bank handled $582m Epstein-linked deals", "18 Nov", "London", "Financial Times"),
    ("NSA classified network suffers outage", "18 Nov", "Washington", "CNN"),
    ("US proposes tougher green-card rules", "19 Nov", "Washington", "Reuters"),
    ("LPG tanker hit by projectiles off Bulgaria", "19 Nov", "Black Sea", "Reuters"),
    ("Gaza Board of Peace fears collapse", "18 Nov", "Gaza", "Al Jazeera"),
    ("EU proposes \u20ac45bn loan for Ukraine", "18 Nov", "Brussels", "Financial Times / Reuters"),
    ("Canada rethinks China ties, Carney eyes US deal", "19 Nov", "Ottawa", "Reuters"),
    ("US senators: AI cyber threats outpacing defences", "19 Nov", "Washington", "Reuters"),
    ("Saudi Arabia says danger passed in three cities", "19 Nov", "Riyadh", "Reuters"),
    ("Cocaine and millions of pills seized in Libya", "19 Nov", "eastern Libya", "Reuters"),
    ("M\u00e9lenchon could win French presidency, minister says", "19 Nov", "Paris", "Reuters"),
    ("Earth's missing billion years of history explained", "19 Nov", "", "Space.com"),
    ("Duckett's 133 puts England on top in 3rd ODI", "19 Nov", "Australia", "Reuters"),
    ("AI 171 crash probe report at 'fag end'", "19 Nov", "New Delhi", "PTI"),
    ("50 pupils hospitalised in tar-plant pollution scare", "19 Nov", "India", "PTI"),
    ("India forms 14-member panel for sports leagues", "19 Nov", "New Delhi", "PTI"),
    ("Microsoft in talks to sell AI services to ByteDance", "19 Nov", "", "Reuters"),
    ("Oil slides as Gulf risk and risk aversion rise", "19 Nov", "", "Reuters"),
    ("Trump 'unhappy' Vance did not back Iran war", "19 Nov", "Washington", "Reuters"),
    ("Liu Yunping first Taiwanese American caucus chair", "19 Nov", "Washington", "AP"),
    ("Taiwan adds transnational repression crime", "19 Nov", "Taipei", "CNA"),
    ("GTA VI 'may mark end of an era'", "19 Nov", "", "The Economist"),
]

# ---------------------------------------------------------------- photos
def photo_skyline(d, x0, y0, w, h):
    """Vice City at sunset: pink sky, low sun, lit towers, one palm."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(244, 130, 170))
    d.rectangle([x0, y0 + h * 0.55, x0 + w, y0 + h], fill=(248, 183, 110))
    d.ellipse([x0 + w * 0.60, y0 + 12, x0 + w * 0.60 + 52, y0 + 64],
              fill=(255, 214, 120))
    rnd = random.Random(7)
    bx = x0 + 4
    while bx < x0 + w - 18:
        bw = rnd.randint(26, 44)
        bh = rnd.randint(38, 82)
        by = y0 + h - bh
        d.rectangle([bx, by, bx + bw, y0 + h], fill=(38, 24, 58))
        for wy in range(by + 8, y0 + h - 6, 12):
            for wx in range(bx + 5, bx + bw - 5, 10):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 110))
        bx += bw + 3
    px, py = x0 + 14, y0 + h - 6
    d.line([px, py, px + 4, py - 42], fill=(30, 18, 40), width=3)
    for ang in (-70, -40, -12, 18, 48):
        rad = math.radians(ang)
        d.line([px + 4, py - 42,
                px + 4 + 26 * math.cos(rad), py - 42 + 14 * math.sin(rad)],
               fill=(30, 18, 40), width=3)
    d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(20, 20, 20))
    lab = "VICE CITY \u00b7 LEONIDA"
    lf = font(SANS_B, 10)
    d.text((x0 + w / 2 - d.textlength(lab, font=lf) / 2, y0 + h - 14),
           lab, font=lf, fill=(255, 255, 255))


def photo_gulf(d, x0, y0, w, h):
    """Night sea in the Gulf: stars, moon, a tanker, a missile streak."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(10, 18, 54))
    rnd = random.Random(11)
    for _ in range(46):
        sx = x0 + rnd.randint(4, w - 4)
        sy = y0 + rnd.randint(4, int(h * 0.5))
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    d.ellipse([x0 + w - 58, y0 + 12, x0 + w - 22, y0 + 48],
              fill=(238, 232, 200))
    d.rectangle([x0, y0 + int(h * 0.58), x0 + w, y0 + h], fill=(16, 68, 96))
    for i in range(5):
        yy = y0 + int(h * 0.62) + i * 9
        d.line([x0 + 8, yy, x0 + w - 8, yy], fill=(90, 160, 190), width=1)
    tx, ty = x0 + w * 0.30, y0 + int(h * 0.52)
    d.rectangle([tx, ty, tx + 120, ty + 18], fill=(12, 12, 16))
    d.rectangle([tx + 88, ty - 16, tx + 104, ty], fill=(12, 12, 16))
    d.rectangle([tx + 10, ty - 8, tx + 30, ty], fill=(12, 12, 16))
    for wx in range(int(tx) + 6, int(tx) + 112, 12):
        d.rectangle([wx, ty + 5, wx + 4, ty + 9], fill=(255, 200, 90))
    d.line([x0 + w - 30, y0 + 18, x0 + w - 96, y0 + 62],
           fill=(255, 140, 60), width=3)
    d.ellipse([x0 + w - 102, y0 + 56, x0 + w - 90, y0 + 68],
              fill=(255, 180, 80))
    d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(20, 20, 20))
    lab = "ALI AL SALEM \u00b7 KUWAIT"
    lf = font(SANS_B, 10)
    d.text((x0 + w / 2 - d.textlength(lab, font=lf) / 2, y0 + h - 14),
           lab, font=lf, fill=(255, 255, 255))


def photo_cyclone(d, x0, y0, w, h):
    """Cyclone Akvan: teal sea, white spiral arms, driving rain."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(14, 74, 96))
    cx, cy = x0 + w * 0.52, y0 + h * 0.48
    for arm in range(3):
        pts = []
        for t in range(0, 190, 4):
            a = math.radians(t + arm * 120)
            r = 4 + t * 0.42
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.82))
        d.line(pts, fill=(235, 245, 250), width=7, joint="curve")
    d.ellipse([cx - 13, cy - 11, cx + 13, cy + 11], fill=(20, 40, 60))
    d.ellipse([cx - 7, cy - 6, cx + 7, cy + 6], fill=(235, 245, 250))
    rnd = random.Random(19)
    for _ in range(26):
        rx = x0 + rnd.randint(4, w - 10)
        ry = y0 + rnd.randint(4, h - 24)
        d.line([rx, ry, rx - 6, ry + 12], fill=(190, 220, 235), width=2)
    d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(20, 20, 20))
    lab = "BAY OF BENGAL \u00b7 AKVAN"
    lf = font(SANS_B, 10)
    d.text((x0 + w / 2 - d.textlength(lab, font=lf) / 2, y0 + h - 14),
           lab, font=lf, fill=(255, 255, 255))


# ---------------------------------------------------------------- map
# Rough landmass blocks in map coordinates (x, y, w, h), hand-placed.
LAND = [
    (18, 22, 62, 52),    # North America
    (52, 74, 30, 26),    # Central America
    (78, 96, 34, 32),    # South America (kept inside the map box)
    (148, 18, 26, 34),   # Europe
    (142, 52, 34, 40),   # Africa
    (178, 12, 78, 44),   # Asia
    (196, 58, 44, 34),   # SE Asia / India area
    (238, 96, 34, 22),   # Australia
]
# Numbered story dots (story no, map x, map y) inside the map box.
DOTS = [(1, 262, 106), (2, 190, 38), (3, 236, 42), (4, 38, 32),
        (5, 208, 68), (6, 58, 44), (7, 20, 24), (8, 28, 54),
        (9, 50, 62), (10, 222, 60)]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(233, 228, 210))
    step = 7
    for bx, by, bw, bh in LAND:
        for gx in range(bx, bx + bw, step):
            for gy in range(by, min(by + bh, h), step):
                d.ellipse([x0 + gx - 1, y0 + gy - 1, x0 + gx + 1, y0 + gy + 1],
                          fill=(74, 110, 74))
    for n, dx, dy in DOTS:
        num_badge(d, x0 + dx, y0 + dy, n, r=9)


# ---------------------------------------------------------------- page
def top_story(d, x, y, w, idx, head_f, body_f, meta_f, kick_f):
    head, kick, summ, date, place, src = TOP[idx]
    n = idx + 1
    num_badge(d, x + 11, y + 11, n)
    d.text((x + 28, y + 3), kick, font=kick_f, fill=RED)
    yy = para(d, x, y + 22, head, head_f, w, 19, max_lines=2)
    yy = para(d, x, yy + 3, summ, body_f, w, 14, max_lines=2)
    meta = f"{date} \u00b7 {place} \u00b7 {src}"
    para(d, x, yy + 3, meta, meta_f, w, 12, fill=GREY, max_lines=1)
    return yy


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    f_title = font(SERIF_B, 46)
    f_sub = font(SANS, 15)
    f_eyebrow = font(SANS_B, 13)
    f_head = font(SERIF_B, 18)
    f_head_sm = font(SERIF_B, 16)
    f_body = font(SANS, 11)
    f_meta = font(SANS, 9)
    f_kick = font(SANS_B, 10)
    f_sec = font(SANS_B, 13)
    f_more_head = font(SANS_B, 10)
    f_more_meta = font(SANS, 8)

    # ---- masthead
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.text((24, 12), "THE DAY IN WORLD NEWS", font=f_eyebrow, fill=GOLD)
    right = "35 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE"
    d.text((W - 24 - d.textlength(right, font=f_eyebrow), 12), right,
           font=f_eyebrow, fill=GOLD)
    d.text((24, 34), "Thursday 19 November 2026", font=f_title,
           fill=(255, 255, 255))
    d.text((24, 88), "Top stories of 19 November 2026 \u2014 coverage as of "
           "the morning of 19 November 2026.", font=f_sub,
           fill=(220, 225, 240))
    d.rectangle([0, 112, W, 116], fill=GOLD)

    # ---- photo row
    pw, ph, gap = 318, 100, 11
    px = 24
    photo_skyline(d, px, 126, pw, ph)
    photo_gulf(d, px + pw + gap, 126, pw, ph)
    photo_cyclone(d, px + 2 * (pw + gap), 126, pw, ph)

    # ---- top stories, rows of 3 / 4 / 3
    col_w3 = (W - 48 - 2 * 20) / 3
    col_w4 = (W - 48 - 3 * 16) / 4
    y = 238
    for i in range(3):
        top_story(d, 24 + i * (col_w3 + 20), y, col_w3, i,
                  f_head, f_body, f_meta, f_kick)
    d.line([24, 346, W - 24, 346], fill=(200, 195, 180), width=1)
    y = 356
    for j, i in enumerate(range(3, 7)):
        top_story(d, 24 + j * (col_w4 + 16), y, col_w4, i,
                  f_head_sm, f_body, f_meta, f_kick)
    d.line([24, 464, W - 24, 464], fill=(200, 195, 180), width=1)
    y = 474
    for i in range(7, 10):
        top_story(d, 24 + (i - 7) * (col_w3 + 20), y, col_w3, i,
                  f_head, f_body, f_meta, f_kick)

    # ---- lower band
    d.line([24, 584, W - 24, 584], fill=RULE, width=2)
    d.text((24, 594), "WHERE THE NEWS HAPPENED", font=f_sec, fill=INK)
    d.text((336, 594), "ALSO ON THURSDAY 19 NOVEMBER \u2014 25 MORE STORIES",
           font=f_sec, fill=RED)
    d.line([336, 616, W - 24, 616], fill=RED, width=1)

    draw_map(d, 24, 622, 296, 128)
    d.text((24, 758), "Numbered dots mark stories 1\u201310.",
           font=f_meta, fill=GREY)

    # by the numbers
    d.line([24, 782, 320, 782], fill=(200, 195, 180), width=1)
    d.text((24, 790), "BY THE NUMBERS", font=f_sec, fill=RED)
    stats = [("99", "GTA VI's Metacritic score, a record"),
             ("$1.65bn", "GTA VI pre-orders and early sales"),
             ("251\u201311", "Jeffries' vote for Speaker nominee"),
             ("200,000", "people Odisha is moving from the coast")]
    yy = 812
    for big, small in stats:
        d.text((24, yy), big, font=font(SERIF_B, 15), fill=INK)
        d.text((24, yy + 19), small, font=f_meta, fill=GREY)
        yy += 32

    # ---- headlines 11-35, two columns
    col_x = [336, 672]
    col_w = 316
    per_col = 13
    for ci in range(2):
        yy = 626
        for k in range(per_col):
            idx = ci * per_col + k
            if idx >= len(MORE):
                break
            head, date, place, src = MORE[idx]
            num = str(11 + idx)
            d.text((col_x[ci], yy), num + ".", font=f_more_head, fill=RED)
            nx = col_x[ci] + 26
            yy = para(d, nx, yy, head, f_more_head, col_w - 26, 12,
                      max_lines=2)
            meta = f"{date} \u00b7 {place} \u00b7 {src}" if place \
                else f"{date} \u00b7 {src}"
            yy = para(d, nx, yy + 1, meta, f_more_meta, col_w - 26, 10,
                      fill=GREY, max_lines=1)
            yy += 2

    # ---- footer
    d.line([24, 992, W - 24, 992], fill=RULE, width=1)
    foot = ("Top stories of 19 November 2026 (some first reported late "
            "18 November). Sources: Reuters, AP, BBC, CNN, FT, IMD, NASA, "
            "Pew, The Hindu, PTI. Original drawings.")
    fw = d.textlength(foot, font=f_meta)
    d.text(((W - fw) / 2, 1000), foot, font=f_meta, fill=GREY)

    img.save(OUT)
    print(f"saved {OUT} {img.size}")


if __name__ == "__main__":
    main()
