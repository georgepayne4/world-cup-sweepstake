"""Generate the World Cup Sweepstake announcement PDF.

Trionda stadium-night brand: dark hero with spotlight and swooping
tri-color curves, real Trionda ball, grass-textured footer.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from brand import (
    RED, BLUE, GREEN, GOLD, INK, GREY_DARK, NIGHT, CREAM, WHITE,
    ACCENT_CYCLE,
    fill_rgba, stroke_rgba,
    draw_night_hero, draw_swoosh_curves, draw_ball_with_glow,
    draw_tri_underline, draw_grass,
)

OUT = "World_Cup_Sweepstake_Announcement.pdf"

# Event details
DRAW_DATE = "MONDAY 8 JUNE 2026"
DRAW_TIME = "8:30PM"
BUY_IN = 15
N_PLAYERS = 12
POT_TOTAL = BUY_IN * N_PLAYERS  # £180

PRIZES = [
    ("Tournament Winner",       0.60),
    ("Runner-up",               0.20),
    ("Most Cards (Y=1, R=3)",   0.05),
    ("First Red Card",          0.05),
    ("Fastest Goal",            0.05),
    ("Highest-Scoring Match",   0.05),
]


def build():
    w, h = A4
    c = canvas.Canvas(OUT, pagesize=A4)

    grass_h = 2.6 * cm
    hero_top = h
    hero_bottom = h - 14.2 * cm

    # Cream base + dark hero + swoosh curves
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, stroke=0, fill=1)
    draw_night_hero(c, w, hero_top, hero_bottom, centre_frac=0.30)

    curves = [
        (RED,   0.22, [(-2*cm, h - 8.5*cm), (5*cm, h - 5*cm),
                       (w*0.45, h - 2.5*cm), (w + 2*cm, h - 4*cm)]),
        (BLUE,  0.20, [(-2*cm, h - 4*cm), (w*0.30, h - 6.5*cm),
                       (w*0.65, h - 9*cm), (w + 2*cm, h - 6.5*cm)]),
        (GREEN, 0.24, [(-2*cm, h - 12.5*cm), (w*0.30, h - 9.5*cm),
                       (w*0.70, h - 11*cm), (w + 2*cm, h - 9*cm)]),
    ]
    draw_swoosh_curves(c, w, h, curves)

    # Title (white on dark)
    title_y = h - 2.0 * cm
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(w / 2, title_y, "FIFA WORLD CUP 2026")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(w / 2, title_y - 1.8 * cm, "SWEEPSTAKE")
    draw_tri_underline(c, w / 2, title_y - 2.5 * cm, 6.5 * cm)

    # Ball (moved up so it sits in the spotlight)
    ball_size = 7.0 * cm
    ball_cy = h - 9.0 * cm
    draw_ball_with_glow(c, w / 2, ball_cy, ball_size)

    # Boundary lines
    fill_rgba(c, "#000000", 0.18)
    c.rect(0, hero_bottom - 0.06 * cm, w, 0.06 * cm, stroke=0, fill=1)
    fill_rgba(c, "#FFFFFF", 0.15)
    c.rect(0, hero_bottom, w, 0.04 * cm, stroke=0, fill=1)

    # Date / time pill straddling the boundary
    pill_w, pill_h = 14.0 * cm, 1.9 * cm
    pill_x = (w - pill_w) / 2
    pill_y = hero_bottom - pill_h / 2 + 0.2 * cm
    c.setFillColor(GOLD)
    c.roundRect(pill_x, pill_y, pill_w, pill_h, 0.4 * cm, stroke=0, fill=1)
    inner_pad = 0.18 * cm
    c.setFillColor(NIGHT)
    c.roundRect(pill_x + inner_pad, pill_y + inner_pad,
                pill_w - inner_pad * 2, pill_h - inner_pad * 2,
                0.28 * cm, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(w / 2, pill_y + pill_h - 0.65 * cm, "DRAW NIGHT")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(w / 2, pill_y + 0.45 * cm, f"{DRAW_DATE}  ·  {DRAW_TIME}")

    # Money line
    money_y = hero_bottom - 2.0 * cm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, money_y, f"£{BUY_IN} BUY-IN     ·     £{POT_TOTAL} POT     ·     {N_PLAYERS} PLAYERS")

    # Prizes
    prizes_top = money_y - 1.2 * cm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w / 2, prizes_top, "PRIZES")
    draw_tri_underline(c, w / 2, prizes_top - 0.28 * cm, 3.5 * cm, h_=0.08*cm)

    rows_top = prizes_top - 1.05 * cm
    row_h = 0.78 * cm
    left = 4.0 * cm
    right = w - 4.0 * cm

    for i, (name, pct) in enumerate(PRIZES):
        y = rows_top - i * row_h
        amount = int(round(POT_TOTAL * pct))
        c.setFillColor(INK)
        c.setFont("Helvetica", 13)
        c.drawString(left, y, name)

        name_w = c.stringWidth(name, "Helvetica", 13)
        amt_text = f"£{amount}"
        amt_w = c.stringWidth(amt_text, "Helvetica-Bold", 14)
        leader_x1 = left + name_w + 0.3 * cm
        leader_x2 = right - amt_w - 0.3 * cm
        if leader_x2 > leader_x1:
            stroke_rgba(c, "#888888", 0.5)
            c.setLineWidth(0.7)
            c.setDash(0.5, 2.5)
            c.line(leader_x1, y + 0.12 * cm, leader_x2, y + 0.12 * cm)
            c.setDash()

        c.setFillColor(ACCENT_CYCLE[i % 3])
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(right, y, amt_text)

    # Grass footer
    draw_grass(c, w, grass_h, 0)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.85))
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(w / 2, 0.55 * cm,
        "12 PLAYERS  ·  4 TEAMS EACH  ·  6 WAYS TO WIN  ·  GOOD LUCK")

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
