"""Generate the comprehensive sweepstake reference PDF.

Single page: prize rules + draw mechanics + full 48-team pool, in the
same Trionda Tri-Color brand language as the announcement.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

OUT = "World_Cup_Sweepstake_Reference.pdf"
BALL_PNG = "assets/trionda_clean_medium.png"

# Palette
RED = colors.HexColor("#E1342B")
BLUE = colors.HexColor("#1B5BB0")
GREEN = colors.HexColor("#2EA663")
INK = colors.HexColor("#111111")
GREY_DARK = colors.HexColor("#444444")
GREY = colors.HexColor("#888888")
GREY_LIGHT = colors.HexColor("#E8E8E8")
OFF_WHITE = colors.HexColor("#FAFAFA")

PRIZES = [
    ("Tournament Winner",       "60%",  "Team that lifts the trophy.",                                            RED),
    ("Runner-up",               "20%",  "Team that loses the final.",                                             BLUE),
    ("Most Cards (points)",     "5%",   "Highest team card points across the tournament. Y = 1, R = 3.",          GREEN),
    ("First Red Card",          "5%",   "First red shown in any match of the tournament.",                        RED),
    ("Fastest Goal",            "5%",   "Earliest goal of the tournament by match clock.",                        BLUE),
    ("Highest-Scoring Match",   "5%",   "Higher scorer in the match with most combined goals (pens excluded).",   GREEN),
]

POTS = [
    ("Pot 1",  RED,   ["France","Spain","Argentina","England","Portugal","Brazil","Netherlands","Morocco","Belgium","Germany","Croatia","Colombia"]),
    ("Pot 2",  BLUE,  ["Senegal","Mexico","USA","Uruguay","Japan","Switzerland","Iran","Türkiye","Ecuador","Austria","South Korea","Australia"]),
    ("Pot 3",  GREEN, ["Algeria","Egypt","Canada","Norway","Panama","Ivory Coast","Sweden","Paraguay","Czechia","Scotland","Tunisia","DR Congo"]),
    ("Pot 4",  GREY_DARK, ["Uzbekistan","Qatar","Iraq","South Africa","Saudi Arabia","Jordan","Bosnia & Herzegovina","Cape Verde","Ghana","Curaçao","Haiti","New Zealand"]),
]

DRAW_STEPS = [
    ("1", "Randomise the 12 players into a draft order."),
    ("2", "4 pots of 12 teams, tiered by FIFA ranking."),
    ("3", "Each player draws one team from each pot."),
    ("4", "Shared draw URL — everyone watches together."),
]


def draw_tri_color_band(c, w, y, band_h):
    third = w / 3
    c.setFillColor(RED);   c.rect(0,         y, third, band_h, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(third,     y, third, band_h, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(third * 2, y, third, band_h, stroke=0, fill=1)


def draw_tri_underline(c, cx, y, total_w, h_=0.08*cm):
    """Tri-color underline centred at cx, total width total_w."""
    seg = total_w / 3
    c.setFillColor(RED);   c.rect(cx - seg * 1.5, y, seg, h_, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(cx - seg * 0.5, y, seg, h_, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(cx + seg * 0.5, y, seg, h_, stroke=0, fill=1)


def draw_ball(c, cx, cy, size):
    img = ImageReader(BALL_PNG)
    iw, ih = img.getSize()
    aspect = ih / iw
    bw = size
    bh = size * aspect
    c.drawImage(img, cx - bw / 2, cy - bh / 2, width=bw, height=bh, mask='auto')


def draw_wave(c, w, y):
    import math
    third = w / 3
    pts = 60
    for k, color in enumerate([RED, BLUE, GREEN]):
        c.setStrokeColor(color)
        c.setLineWidth(2)
        p = c.beginPath()
        x0 = k * third
        for i in range(pts + 1):
            x = x0 + (i / pts) * third
            yy = y + math.sin((i / pts) * math.pi * 3) * 0.16 * cm
            if i == 0:
                p.moveTo(x, yy)
            else:
                p.lineTo(x, yy)
        c.drawPath(p, stroke=1, fill=0)


def draw_section_header(c, w, y, text):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2.0 * cm, y, text)
    # Tri-color rule under header
    rule_w = c.stringWidth(text, "Helvetica-Bold", 12)
    seg = rule_w / 3
    c.setFillColor(RED);   c.rect(2.0 * cm,                  y - 0.18 * cm, seg, 0.08 * cm, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(2.0 * cm + seg,            y - 0.18 * cm, seg, 0.08 * cm, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(2.0 * cm + seg * 2,        y - 0.18 * cm, seg, 0.08 * cm, stroke=0, fill=1)


def draw_prizes(c, w, top_y):
    draw_section_header(c, w, top_y, "PRIZES")
    rows_top = top_y - 0.85 * cm
    row_h = 0.78 * cm
    left = 2.0 * cm
    right = w - 2.0 * cm

    for i, (name, pct, desc, color) in enumerate(PRIZES):
        y = rows_top - i * row_h

        # Color tag (small square at far left)
        c.setFillColor(color)
        c.rect(left, y - 0.04 * cm, 0.18 * cm, 0.45 * cm, stroke=0, fill=1)

        # Name (bold)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left + 0.5 * cm, y + 0.18 * cm, name)
        # Description (grey, smaller)
        c.setFillColor(GREY_DARK)
        c.setFont("Helvetica", 9)
        c.drawString(left + 0.5 * cm, y - 0.22 * cm, desc)

        # Pct (right-aligned bold, colored)
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(right, y + 0.05 * cm, pct)

    return rows_top - len(PRIZES) * row_h


def draw_draw_section(c, w, top_y):
    draw_section_header(c, w, top_y, "HOW THE DRAW WORKS")
    y = top_y - 1.0 * cm
    col_w = (w - 4.0 * cm) / 4
    circle_colors = [RED, BLUE, GREEN, INK]
    for i, (num, text) in enumerate(DRAW_STEPS):
        x = 2.0 * cm + i * col_w
        cx = x + col_w / 2
        # Numbered circle in tri-color
        c.setFillColor(circle_colors[i])
        c.circle(cx, y, 0.4 * cm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(cx, y - 0.15 * cm, num)

        # Text wrapped
        c.setFillColor(INK)
        c.setFont("Helvetica", 9.5)
        # Simple wrapping
        words = text.split()
        lines, cur = [], ""
        for word in words:
            test = (cur + " " + word).strip()
            if c.stringWidth(test, "Helvetica", 9.5) > col_w - 0.4 * cm and cur:
                lines.append(cur); cur = word
            else:
                cur = test
        if cur: lines.append(cur)
        for li, line in enumerate(lines):
            c.drawCentredString(cx, y - 1.0 * cm - li * 0.32 * cm, line)

    return y - 1.0 * cm - 3 * 0.32 * cm


def draw_pots(c, w, top_y):
    draw_section_header(c, w, top_y, "TEAM POOL  ·  TIERED BY FIFA WORLD RANKING")

    left = 2.0 * cm
    right = w - 2.0 * cm
    gap = 0.3 * cm
    n = 4
    col_w = (right - left - gap * (n - 1)) / n

    col_top = top_y - 0.9 * cm
    header_h = 0.85 * cm
    row_h = 0.5 * cm
    col_h = header_h + 12 * row_h + 0.25 * cm

    for i, (label, color, teams) in enumerate(POTS):
        x = left + i * (col_w + gap)
        # Card
        c.setFillColor(OFF_WHITE)
        c.roundRect(x, col_top - col_h, col_w, col_h, 0.15 * cm, stroke=0, fill=1)
        # Header strip
        c.setFillColor(color)
        c.rect(x, col_top - 0.18 * cm, col_w, 0.18 * cm, stroke=0, fill=1)
        # Pot label
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + col_w / 2, col_top - 0.7 * cm, label)

        c.setFillColor(INK)
        c.setFont("Helvetica", 9.2)
        for j, team in enumerate(teams):
            ty = col_top - header_h - 0.3 * cm - j * row_h
            # Small color dot
            c.setFillColor(color)
            c.circle(x + 0.4 * cm, ty - 0.02 * cm, 0.06 * cm, stroke=0, fill=1)
            c.setFillColor(INK)
            c.drawString(x + 0.6 * cm, ty - 0.06 * cm, team)

        # Subtle border
        c.setStrokeColor(GREY_LIGHT)
        c.setLineWidth(0.5)
        c.roundRect(x, col_top - col_h, col_w, col_h, 0.15 * cm, stroke=1, fill=0)

    return col_top - col_h


def build():
    w, h = A4
    c = canvas.Canvas(OUT, pagesize=A4)

    # Background
    c.setFillColor(colors.white)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # Tri-color header band
    band_h = 1.6 * cm
    draw_tri_color_band(c, w, h - band_h, band_h)

    # Title block
    title_y = h - band_h - 1.3 * cm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(w / 2, title_y, "FIFA WORLD CUP 2026")
    c.setFillColor(GREY_DARK)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w / 2, title_y - 1.1 * cm, "SWEEPSTAKE")

    # Tri-color underline + small ball on the right
    draw_tri_underline(c, w / 2, title_y - 1.6 * cm, 6.0 * cm)
    draw_ball(c, w - 2.8 * cm, h - band_h - 1.4 * cm, 2.4 * cm)

    # Sections
    y = title_y - 2.4 * cm
    y = draw_prizes(c, w, y) - 0.6 * cm
    y = draw_draw_section(c, w, y) - 0.6 * cm
    y = draw_pots(c, w, y)

    # Bottom wave + footer
    draw_wave(c, w, 1.4 * cm)
    c.setFillColor(GREY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, 0.7 * cm,
        "12 PLAYERS  ·  4 TEAMS EACH  ·  6 WAYS TO WIN  ·  GOOD LUCK")

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
