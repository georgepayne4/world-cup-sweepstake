"""Generate the World Cup Sweepstake announcement PDF (one-page poster).

Designed to be saved as an image and shared. Hero Trionda ball,
draw night info, £15 buy-in prize breakdown.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

OUT = "World_Cup_Sweepstake_Announcement.pdf"
BALL_IMG = "assets/trionda.jpg"

# Event details
DRAW_DATE = "MONDAY 8 JUNE 2026"
DRAW_TIME = "8:30PM"
BUY_IN = 15
N_PLAYERS = 12
POT_TOTAL = BUY_IN * N_PLAYERS  # £180

# Palette
GREEN_DARK = colors.HexColor("#0B3B2E")
GREEN_PITCH = colors.HexColor("#1B6B43")
GREEN_LIGHT = colors.HexColor("#2E8B57")
GOLD = colors.HexColor("#D4A24C")
GOLD_LIGHT = colors.HexColor("#F2D89A")
CREAM = colors.HexColor("#FBF7EE")
INK = colors.HexColor("#0F1A14")
RED = colors.HexColor("#C03A2B")
BLUE = colors.HexColor("#1F4E8C")
PURPLE = colors.HexColor("#6B3FA0")
ORANGE = colors.HexColor("#E07B27")

PRIZES = [
    ("Tournament Winner",       0.60, GOLD),
    ("Runner-up",               0.20, GREEN_LIGHT),
    ("Most Cards (Y=1, R=3)",   0.05, RED),
    ("First Red Card",          0.05, BLUE),
    ("Fastest Goal",            0.05, PURPLE),
    ("Highest-Scoring Match",   0.05, ORANGE),
]


def draw_background(c, w, h):
    # Cream backdrop
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # Top hero band — solid dark green with diagonal pitch stripes
    band_h = 11.0 * cm
    c.setFillColor(GREEN_DARK)
    c.rect(0, h - band_h, w, band_h, stroke=0, fill=1)
    # Diagonal pitch stripes
    c.setFillColor(GREEN_PITCH)
    for i in range(-2, 30):
        p = c.beginPath()
        x = i * 1.0 * cm
        p.moveTo(x, h - band_h)
        p.lineTo(x + 0.5 * cm, h - band_h)
        p.lineTo(x + 0.5 * cm + 1.6 * cm, h)
        p.lineTo(x + 1.6 * cm, h)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
    # Gold rule under hero
    c.setFillColor(GOLD)
    c.rect(0, h - band_h - 0.15 * cm, w, 0.15 * cm, stroke=0, fill=1)

    # Bottom band
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, w, 1.4 * cm, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, 1.4 * cm, w, 0.1 * cm, stroke=0, fill=1)


def draw_hero(c, w, h):
    # Big title in the hero band
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(w / 2, h - 2.0 * cm, "FIFA WORLD CUP 2026")
    c.setFillColor(GOLD_LIGHT)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(w / 2, h - 3.5 * cm, "SWEEPSTAKE")

    # Sub-banner
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(w / 2, h - 4.55 * cm, "·  DRAW NIGHT  ·")

    # Date / time pill — entirely inside the hero band, above the ball
    pill_w, pill_h = 13.0 * cm, 1.6 * cm
    pill_x = (w - pill_w) / 2
    pill_y = h - 6.45 * cm
    c.setFillColor(GOLD)
    c.roundRect(pill_x, pill_y, pill_w, pill_h, 0.32 * cm, stroke=0, fill=1)
    c.setFillColor(GREEN_DARK)
    c.setFont("Helvetica-Bold", 17)
    c.drawCentredString(w / 2, pill_y + 0.48 * cm, f"{DRAW_DATE}  ·  {DRAW_TIME}")


def draw_ball(c, w, h):
    # Trionda ball straddles the hero/cream boundary (below the date pill)
    ball_size = 6.0 * cm
    cx = w / 2
    cy = h - 11.0 * cm   # centred on the gold rule (band_h = 11)
    ball_x = cx - ball_size / 2
    ball_y = cy - ball_size / 2

    # White circular halo behind ball (with gold ring)
    halo_r = ball_size / 2 + 0.35 * cm
    c.setFillColor(CREAM)
    c.circle(cx, cy, halo_r, stroke=0, fill=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.circle(cx, cy, halo_r, stroke=1, fill=0)

    # Draw the ball image, clipped to a circle so the photo background is hidden
    c.saveState()
    p = c.beginPath()
    p.circle(cx, cy, ball_size / 2)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ImageReader(BALL_IMG), ball_x, ball_y, width=ball_size, height=ball_size,
                preserveAspectRatio=True, mask='auto')
    c.restoreState()


def draw_money_line(c, w, h, y):
    # "£15 BUY-IN · £180 POT · 12 PLAYERS"
    c.setFillColor(GREEN_DARK)
    c.setFont("Helvetica-Bold", 18)
    line = f"£{BUY_IN} BUY-IN     ·     £{POT_TOTAL} POT     ·     {N_PLAYERS} PLAYERS"
    c.drawCentredString(w / 2, y, line)
    # Decorative dividers
    rule_y = y - 0.4 * cm
    c.setFillColor(GOLD)
    c.rect(w / 2 - 5.0 * cm, rule_y, 10.0 * cm, 0.06 * cm, stroke=0, fill=1)
    return y - 1.2 * cm


def draw_prizes(c, w, h, top_y):
    # Section header
    c.setFillColor(GREEN_DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, top_y, "PRIZES")
    c.setFillColor(GOLD)
    c.rect(w / 2 - 1.5 * cm, top_y - 0.2 * cm, 3.0 * cm, 0.08 * cm, stroke=0, fill=1)

    rows_top = top_y - 0.9 * cm
    row_h = 1.05 * cm
    left = 2.0 * cm
    right = w - 2.0 * cm
    badge_w = 2.2 * cm

    for i, (name, pct, color) in enumerate(PRIZES):
        y = rows_top - i * row_h
        amount = int(round(POT_TOTAL * pct))

        # Row background
        c.setFillColor(colors.white if i % 2 == 0 else colors.HexColor("#F4EFE0"))
        c.roundRect(left, y - row_h + 0.18 * cm, right - left, row_h - 0.22 * cm,
                    0.18 * cm, stroke=0, fill=1)
        # Color stripe
        c.setFillColor(color)
        c.rect(left, y - row_h + 0.18 * cm, 0.22 * cm, row_h - 0.22 * cm, stroke=0, fill=1)

        # Prize name
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(left + 0.6 * cm, y - 0.55 * cm, name)

        # £ badge — text colour chosen for contrast with the badge fill
        bx = right - badge_w - 0.1 * cm
        by = y - row_h + 0.32 * cm
        bh = row_h - 0.5 * cm
        c.setFillColor(color)
        c.roundRect(bx, by, badge_w, bh, 0.18 * cm, stroke=0, fill=1)
        text_color = INK if color == GOLD else CREAM
        c.setFillColor(text_color)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(bx + badge_w / 2, by + 0.18 * cm, f"£{amount}")

    return rows_top - len(PRIZES) * row_h


def draw_footer(c, w, h):
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(w / 2, 0.55 * cm,
        "12 PLAYERS  ·  4 TEAMS EACH  ·  6 WAYS TO WIN  ·  GOOD LUCK!")


def build():
    w, h = A4
    c = canvas.Canvas(OUT, pagesize=A4)

    draw_background(c, w, h)
    draw_hero(c, w, h)
    draw_ball(c, w, h)

    # Money line below the ball (ball centre at h-11cm, halo extends ~3.5cm)
    y = h - 15.5 * cm
    y = draw_money_line(c, w, h, y)
    y = draw_prizes(c, w, h, y - 0.7 * cm)

    draw_footer(c, w, h)

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
