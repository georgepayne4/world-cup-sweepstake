"""Generate the comprehensive sweepstake reference PDF.

Same Trionda stadium-night brand as the announcement: dark hero with
swooping tri-color curves and a small ball, content sections in
prize rules / draw mechanics / 48-team pool, grass footer.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from brand import (
    RED, BLUE, GREEN, GOLD, INK, GREY_DARK, GREY, GREY_LIGHT,
    OFF_WHITE, CREAM, WHITE,
    fill_rgba, stroke_rgba,
    draw_night_hero, draw_swoosh_curves, draw_ball_with_glow,
    draw_tri_underline, draw_tri_left_underline, draw_grass,
)

OUT = "World_Cup_Sweepstake_Reference.pdf"

PRIZES = [
    ("Tournament Winner",       "60%",  "Team that lifts the trophy.",                                          RED),
    ("Runner-up",               "20%",  "Team that loses the final.",                                           BLUE),
    ("Most Cards (points)",     "5%",   "Highest team card points across the tournament. Y = 1, R = 3.",        GREEN),
    ("First Red Card",          "5%",   "Earliest tournament round with any red; within that round the lowest match-clock minute wins.", RED),
    ("Fastest Goal",            "5%",   "Earliest goal of the tournament by match clock.",                      BLUE),
    ("Highest-Scoring Match",   "5%",   "Higher scorer in the match with most combined goals (pens excluded).", GREEN),
]

POTS = [
    ("Pot 1",  RED,       ["France","Spain","Argentina","England","Portugal","Brazil","Netherlands","Morocco","Belgium","Germany","Croatia","Colombia"]),
    ("Pot 2",  BLUE,      ["Senegal","Mexico","USA","Uruguay","Japan","Switzerland","Iran","Türkiye","Ecuador","Austria","South Korea","Australia"]),
    ("Pot 3",  GREEN,     ["Algeria","Egypt","Canada","Norway","Panama","Ivory Coast","Sweden","Paraguay","Czechia","Scotland","Tunisia","DR Congo"]),
    ("Pot 4",  GREY_DARK, ["Uzbekistan","Qatar","Iraq","South Africa","Saudi Arabia","Jordan","Bosnia & Herzegovina","Cape Verde","Ghana","Curaçao","Haiti","New Zealand"]),
]

DRAW_STEPS = [
    ("1", "Randomise the 12 players into a draft order."),
    ("2", "4 pots of 12 teams, tiered by FIFA ranking."),
    ("3", "Each player draws one team from each pot."),
    ("4", "Shared draw URL — everyone watches together."),
]


def draw_hero(c, w, h, hero_bottom):
    hero_top = h
    draw_night_hero(c, w, hero_top, hero_bottom, centre_frac=0.40)

    # Swooping tri-color curves across the hero
    curves = [
        (RED,   0.22, [(-2*cm, h - 5.2*cm), (4*cm, h - 3.5*cm),
                      (w*0.55, h - 1.5*cm), (w + 2*cm, h - 2.8*cm)]),
        (BLUE,  0.20, [(-2*cm, h - 2.8*cm), (w*0.30, h - 4.2*cm),
                      (w*0.65, h - 5.5*cm), (w + 2*cm, h - 4.4*cm)]),
        (GREEN, 0.24, [(-2*cm, h - 6.3*cm), (w*0.30, h - 5.5*cm),
                      (w*0.70, h - 6.5*cm), (w + 2*cm, h - 5.5*cm)]),
    ]
    draw_swoosh_curves(c, w, h, curves)

    # Title (left-aligned, makes room for the ball on the right)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(2.0 * cm, h - 2.0 * cm, "FIFA WORLD CUP 2026")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(2.0 * cm, h - 3.7 * cm, "SWEEPSTAKE")
    draw_tri_left_underline(c, 2.0 * cm, h - 4.3 * cm, 7.0 * cm, h_=0.10*cm)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.75))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.0 * cm, h - 5.4 * cm, "REFERENCE  ·  PRIZES  ·  DRAW  ·  TEAMS")

    # Ball on the right
    ball_size = 4.5 * cm
    draw_ball_with_glow(c, w - 3.8 * cm, h - 3.5 * cm, ball_size, halo=True, shadow=False)


def draw_section_header(c, w, y, text):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2.0 * cm, y, text)
    rule_w = c.stringWidth(text, "Helvetica-Bold", 13)
    draw_tri_left_underline(c, 2.0 * cm, y - 0.22 * cm, rule_w, h_=0.08*cm)


def draw_prizes(c, w, top_y):
    draw_section_header(c, w, top_y, "PRIZES")
    rows_top = top_y - 0.95 * cm
    row_h = 0.80 * cm
    left = 2.0 * cm
    right = w - 2.0 * cm

    for i, (name, pct, desc, color) in enumerate(PRIZES):
        y = rows_top - i * row_h

        # Color tag
        c.setFillColor(color)
        c.rect(left, y - 0.04 * cm, 0.20 * cm, 0.48 * cm, stroke=0, fill=1)

        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(left + 0.55 * cm, y + 0.20 * cm, name)
        c.setFillColor(GREY_DARK)
        c.setFont("Helvetica", 9)
        c.drawString(left + 0.55 * cm, y - 0.22 * cm, desc)

        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 15)
        c.drawRightString(right, y + 0.05 * cm, pct)

    return rows_top - len(PRIZES) * row_h


def draw_draw_section(c, w, top_y):
    draw_section_header(c, w, top_y, "HOW THE DRAW WORKS")
    y = top_y - 1.0 * cm
    col_w = (w - 4.0 * cm) / 4
    step_colors = [RED, BLUE, GREEN, GREY_DARK]
    for i, (num, text) in enumerate(DRAW_STEPS):
        x = 2.0 * cm + i * col_w
        cx = x + col_w / 2

        # Numbered circle, tri-colour
        c.setFillColor(step_colors[i])
        c.circle(cx, y, 0.42 * cm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(cx, y - 0.15 * cm, num)

        c.setFillColor(INK)
        c.setFont("Helvetica", 9.5)
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
            c.drawCentredString(cx, y - 1.05 * cm - li * 0.34 * cm, line)

    return y - 1.05 * cm - 3 * 0.34 * cm


def draw_pots(c, w, top_y):
    draw_section_header(c, w, top_y, "TEAM POOL  ·  TIERED BY FIFA WORLD RANKING")

    left = 2.0 * cm
    right = w - 2.0 * cm
    gap = 0.3 * cm
    n = 4
    col_w = (right - left - gap * (n - 1)) / n

    col_top = top_y - 1.0 * cm
    header_h = 1.0 * cm
    row_h = 0.52 * cm
    col_h = header_h + 12 * row_h + 0.3 * cm

    for i, (label, color, teams) in enumerate(POTS):
        x = left + i * (col_w + gap)
        # Card background
        c.setFillColor(OFF_WHITE)
        c.roundRect(x, col_top - col_h, col_w, col_h, 0.18 * cm, stroke=0, fill=1)
        # Header strip top (color band)
        c.setFillColor(color)
        c.rect(x, col_top - 0.22 * cm, col_w, 0.22 * cm, stroke=0, fill=1)
        # Pot label
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(x + col_w / 2, col_top - 0.85 * cm, label)

        c.setFillColor(INK)
        c.setFont("Helvetica", 9.2)
        for j, team in enumerate(teams):
            ty = col_top - header_h - 0.3 * cm - j * row_h
            c.setFillColor(color)
            c.circle(x + 0.42 * cm, ty - 0.02 * cm, 0.07 * cm, stroke=0, fill=1)
            c.setFillColor(INK)
            c.drawString(x + 0.62 * cm, ty - 0.06 * cm, team)

        c.setStrokeColor(GREY_LIGHT)
        c.setLineWidth(0.5)
        c.roundRect(x, col_top - col_h, col_w, col_h, 0.18 * cm, stroke=1, fill=0)

    return col_top - col_h


def build():
    w, h = A4
    c = canvas.Canvas(OUT, pagesize=A4)

    # Cream page base
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # Dark hero — top 6.2cm
    hero_bottom = h - 6.2 * cm
    draw_hero(c, w, h, hero_bottom)

    # Soft transition rule under hero
    fill_rgba(c, "#000000", 0.18)
    c.rect(0, hero_bottom - 0.06 * cm, w, 0.06 * cm, stroke=0, fill=1)
    fill_rgba(c, "#FFFFFF", 0.10)
    c.rect(0, hero_bottom, w, 0.04 * cm, stroke=0, fill=1)

    # Content sections
    y = hero_bottom - 1.2 * cm
    y = draw_prizes(c, w, y) - 0.5 * cm
    y = draw_draw_section(c, w, y) - 0.4 * cm
    y = draw_pots(c, w, y)

    # Grass footer
    draw_grass(c, w, 2.0 * cm, 0)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.85))
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(w / 2, 0.5 * cm,
        "12 PLAYERS  ·  4 TEAMS EACH  ·  6 WAYS TO WIN  ·  GOOD LUCK")

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
