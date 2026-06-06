"""Generate the World Cup Sweepstake announcement PDF.

Trionda Tri-Color brand: red / blue / green panel header, modern clean
sans-serif typography, lots of breathing room, tri-color ball illustration.
Designed to be saved as an image.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

OUT = "World_Cup_Sweepstake_Announcement.pdf"
BALL_SVG = "assets/ball.svg"

# Event details
DRAW_DATE = "MONDAY 8 JUNE 2026"
DRAW_TIME = "8:30PM"
BUY_IN = 15
N_PLAYERS = 12
POT_TOTAL = BUY_IN * N_PLAYERS  # £180

# Trionda Tri-Color palette
RED = colors.HexColor("#E1342B")
BLUE = colors.HexColor("#1B5BB0")
GREEN = colors.HexColor("#2EA663")
INK = colors.HexColor("#111111")
GREY_DARK = colors.HexColor("#444444")
GREY = colors.HexColor("#888888")
GREY_LIGHT = colors.HexColor("#E8E8E8")
WHITE = colors.HexColor("#FFFFFF")
OFF_WHITE = colors.HexColor("#FAFAFA")

PRIZES = [
    ("Tournament Winner",       0.60),
    ("Runner-up",               0.20),
    ("Most Cards (Y=1, R=3)",   0.05),
    ("First Red Card",          0.05),
    ("Fastest Goal",            0.05),
    ("Highest-Scoring Match",   0.05),
]


def draw_tri_color_band(c, w, h, y, band_h):
    """Three solid color blocks side by side."""
    third = w / 3
    c.setFillColor(RED);   c.rect(0,           y, third, band_h, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(third,       y, third, band_h, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(third * 2,   y, third, band_h, stroke=0, fill=1)


def draw_wave_footer(c, w, y, h):
    """Wavy line at the bottom."""
    # Three short colored wave segments
    c.setStrokeColor(RED)
    c.setLineWidth(2.5)
    pts = 60
    import math
    third = w / 3
    for k, color in enumerate([RED, BLUE, GREEN]):
        c.setStrokeColor(color)
        p = c.beginPath()
        x0 = k * third
        for i in range(pts + 1):
            x = x0 + (i / pts) * third
            yy = y + math.sin((i / pts) * math.pi * 3) * 0.18 * cm
            if i == 0:
                p.moveTo(x, yy)
            else:
                p.lineTo(x, yy)
        c.drawPath(p, stroke=1, fill=0)


def draw_ball(c, w, h, cx, cy, size):
    """Render the SVG ball centred at (cx, cy) with overall size in cm."""
    drawing = svg2rlg(BALL_SVG)
    # svglib drawing dimensions
    sw = drawing.width
    sh = drawing.height
    scale = (size) / max(sw, sh)
    drawing.width = sw * scale
    drawing.height = sh * scale
    drawing.scale(scale, scale)
    renderPDF.draw(drawing, c, cx - drawing.width / 2, cy - drawing.height / 2)


def build():
    w, h = A4
    c = canvas.Canvas(OUT, pagesize=A4)

    # White background
    c.setFillColor(WHITE)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # === Tri-color header band ===
    band_h = 2.0 * cm
    draw_tri_color_band(c, w, h, h - band_h, band_h)

    # === Title block ===
    title_top = h - band_h - 1.8 * cm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w / 2, title_top, "FIFA WORLD CUP 2026")
    c.setFillColor(GREY_DARK)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(w / 2, title_top - 1.6 * cm, "SWEEPSTAKE")

    # Decorative tri-color rule under title
    rule_y = title_top - 2.4 * cm
    rule_third = 3.0 * cm
    c.setFillColor(RED);   c.rect(w / 2 - rule_third * 1.5, rule_y, rule_third, 0.12 * cm, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(w / 2 - rule_third * 0.5, rule_y, rule_third, 0.12 * cm, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(w / 2 + rule_third * 0.5, rule_y, rule_third, 0.12 * cm, stroke=0, fill=1)

    # === Ball ===
    ball_size = 6.5 * cm
    ball_cy = h - 11.5 * cm
    draw_ball(c, w, h, w / 2, ball_cy, ball_size)

    # === Date / time line ===
    dt_y = h - 16.0 * cm
    c.setFillColor(GREY_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w / 2, dt_y + 0.5 * cm, "·  DRAW NIGHT  ·")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(w / 2, dt_y - 0.4 * cm, f"{DRAW_DATE}  ·  {DRAW_TIME}")

    # === Money line ===
    money_y = dt_y - 2.0 * cm
    c.setFillColor(GREY_DARK)
    c.setFont("Helvetica-Bold", 14)
    line = f"£{BUY_IN} BUY-IN     ·     £{POT_TOTAL} POT     ·     {N_PLAYERS} PLAYERS"
    c.drawCentredString(w / 2, money_y, line)

    # === Prizes ===
    prizes_top = money_y - 1.6 * cm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w / 2, prizes_top, "PRIZES")
    # tri-color underline
    ul_w = 1.4 * cm
    c.setFillColor(RED);   c.rect(w / 2 - ul_w * 1.5, prizes_top - 0.25 * cm, ul_w, 0.08 * cm, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(w / 2 - ul_w * 0.5, prizes_top - 0.25 * cm, ul_w, 0.08 * cm, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(w / 2 + ul_w * 0.5, prizes_top - 0.25 * cm, ul_w, 0.08 * cm, stroke=0, fill=1)

    rows_top = prizes_top - 1.1 * cm
    row_h = 0.85 * cm
    left = 4.0 * cm
    right = w - 4.0 * cm

    for i, (name, pct) in enumerate(PRIZES):
        y = rows_top - i * row_h
        amount = int(round(POT_TOTAL * pct))

        # Name (left-aligned)
        c.setFillColor(INK)
        c.setFont("Helvetica", 13)
        c.drawString(left, y, name)

        # Dotted leader between name and amount
        name_w = c.stringWidth(name, "Helvetica", 13)
        amt_text = f"£{amount}"
        amt_w = c.stringWidth(amt_text, "Helvetica-Bold", 14)
        leader_x1 = left + name_w + 0.3 * cm
        leader_x2 = right - amt_w - 0.3 * cm
        if leader_x2 > leader_x1:
            c.setStrokeColor(GREY_LIGHT)
            c.setLineWidth(0.7)
            c.setDash(0.5, 2.5)
            c.line(leader_x1, y + 0.12 * cm, leader_x2, y + 0.12 * cm)
            c.setDash()

        # Amount (right-aligned, bold)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(right, y, amt_text)

    # === Bottom decorative wave ===
    draw_wave_footer(c, w, 1.4 * cm, h)
    # Small footer text
    c.setFillColor(GREY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, 0.7 * cm,
        "12 PLAYERS  ·  4 TEAMS EACH  ·  6 WAYS TO WIN  ·  GOOD LUCK")

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
