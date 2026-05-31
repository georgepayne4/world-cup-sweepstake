"""Generate the World Cup Sweepstake one-page comprehensive PDF.

Single A4 page with: header, prize categories, draw rules, full 48-team pool
sorted into 4 ranking-based tiers.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas

OUT = "World_Cup_Sweepstake.pdf"

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
    ("Tournament Winner",            "60%", "Team that lifts the trophy.",                                        GOLD),
    ("Runner-up",                    "20%", "Team that loses the final.",                                         GREEN_LIGHT),
    ("Most Cards (points)",          "5%",  "Highest team card points across the tournament. Y=1pt, R=3pt.",      RED),
    ("First Red Card",               "5%",  "First red shown in any match of the tournament.",                    BLUE),
    ("Fastest Goal",                 "5%",  "Earliest goal of the tournament by match clock.",                    PURPLE),
    ("Highest-Scoring Match",        "5%",  "Higher scorer in the match with most combined goals (pens excl.).",  ORANGE),
]

POTS = [
    ("Pot 1 — Top Seeds",  ["France","Spain","Argentina","England","Portugal","Brazil","Netherlands","Morocco","Belgium","Germany","Croatia","Colombia"],                GOLD),
    ("Pot 2 — Strong",     ["Senegal","Mexico","USA","Uruguay","Japan","Switzerland","Iran","Türkiye","Ecuador","Austria","South Korea","Australia"],                   GREEN_LIGHT),
    ("Pot 3 — Mid",        ["Algeria","Egypt","Canada","Norway","Panama","Ivory Coast","Sweden","Paraguay","Czechia","Scotland","Tunisia","DR Congo"],                  BLUE),
    ("Pot 4 — Outsiders",  ["Uzbekistan","Qatar","Iraq","South Africa","Saudi Arabia","Jordan","Bosnia & Herzegovina","Cape Verde","Ghana","Curaçao","Haiti","New Zealand"], PURPLE),
]


def draw_background(c, w, h):
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, stroke=0, fill=1)


def draw_header(c, w, h):
    band_h = 3.0 * cm
    # Solid green band
    c.setFillColor(GREEN_DARK)
    c.rect(0, h - band_h, w, band_h, stroke=0, fill=1)
    # Decorative diagonal stripes
    c.saveState()
    c.setFillColor(GREEN_PITCH)
    for i in range(-2, 30):
        c.beginPath()
        p = c.beginPath()
        x = i * 0.8 * cm
        p.moveTo(x, h - band_h)
        p.lineTo(x + 0.4 * cm, h - band_h)
        p.lineTo(x + 0.4 * cm + 1.0 * cm, h)
        p.lineTo(x + 1.0 * cm, h)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
    c.restoreState()
    # Gold rule below
    c.setFillColor(GOLD)
    c.rect(0, h - band_h - 0.15 * cm, w, 0.15 * cm, stroke=0, fill=1)

    # Title
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(w / 2, h - 1.4 * cm, "FIFA WORLD CUP 2026 SWEEPSTAKE")
    c.setFillColor(GOLD_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w / 2, h - 2.25 * cm, "12 PLAYERS  ·  4 TEAMS EACH  ·  6 WAYS TO WIN")


def draw_prizes(c, w, h, top_y):
    # Section title
    c.setFillColor(GREEN_DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(1.5 * cm, top_y, "PRIZES")
    c.setFillColor(GOLD)
    c.rect(1.5 * cm, top_y - 0.15 * cm, 2.0 * cm, 0.08 * cm, stroke=0, fill=1)

    row_h = 1.05 * cm
    pad_top = 0.5 * cm
    table_top = top_y - pad_top
    left = 1.5 * cm
    right = w - 1.5 * cm
    badge_w = 2.0 * cm

    for i, (name, pct, desc, color) in enumerate(PRIZES):
        y = table_top - i * row_h
        # Row background
        c.setFillColor(colors.HexColor("#FFFFFF") if i % 2 == 0 else colors.HexColor("#F4EFE0"))
        c.roundRect(left, y - row_h + 0.15 * cm, right - left, row_h - 0.2 * cm,
                    0.15 * cm, stroke=0, fill=1)
        # Color stripe
        c.setFillColor(color)
        c.rect(left, y - row_h + 0.15 * cm, 0.22 * cm, row_h - 0.2 * cm, stroke=0, fill=1)

        # Name
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(left + 0.6 * cm, y - 0.35 * cm, name)
        # Description
        c.setFillColor(colors.HexColor("#3A4A40"))
        c.setFont("Helvetica", 9)
        c.drawString(left + 0.6 * cm, y - 0.78 * cm, desc)

        # Pct badge
        bx = right - badge_w - 0.1 * cm
        by = y - row_h + 0.27 * cm
        c.setFillColor(color)
        c.roundRect(bx, by, badge_w, row_h - 0.45 * cm, 0.15 * cm, stroke=0, fill=1)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 15)
        c.drawCentredString(bx + badge_w / 2, by + 0.28 * cm, pct)

    return table_top - len(PRIZES) * row_h


def draw_rules(c, w, h, top_y):
    c.setFillColor(GREEN_DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(1.5 * cm, top_y, "HOW THE DRAW WORKS")
    c.setFillColor(GOLD)
    c.rect(1.5 * cm, top_y - 0.15 * cm, 5.4 * cm, 0.08 * cm, stroke=0, fill=1)

    items = [
        ("1", "Randomise the 12 players into a draft order."),
        ("2", "4 pots of 12 teams, tiered by FIFA ranking."),
        ("3", "Each player draws one team from each pot."),
        ("4", "Shared draw URL — everyone watches together."),
    ]
    block_top = top_y - 0.75 * cm
    col_w = (w - 3.0 * cm) / 4
    circle_r = 0.36 * cm

    for i, (num, text) in enumerate(items):
        x = 1.5 * cm + i * col_w
        cx = x + col_w / 2
        # Circle centered at top of cell
        c.setFillColor(GREEN_PITCH)
        c.circle(cx, block_top, circle_r, stroke=0, fill=1)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(cx, block_top - 0.16 * cm, num)

        # Wrap text into lines that fit the column width (with margin)
        c.setFillColor(INK)
        c.setFont("Helvetica", 9.5)
        max_text_w = col_w - 0.6 * cm
        words = text.split()
        lines, cur = [], ""
        for word in words:
            test = (cur + " " + word).strip()
            if c.stringWidth(test, "Helvetica", 9.5) > max_text_w and cur:
                lines.append(cur); cur = word
            else:
                cur = test
        if cur: lines.append(cur)
        # Draw lines centered below circle
        text_top = block_top - circle_r - 0.4 * cm
        for li, line in enumerate(lines):
            c.drawCentredString(cx, text_top - li * 0.34 * cm, line)

    return block_top - circle_r - 0.4 * cm - 3 * 0.34 * cm


def draw_teams(c, w, h, top_y):
    c.setFillColor(GREEN_DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(1.5 * cm, top_y, "TEAM POOL  ·  TIERED BY FIFA WORLD RANKING")
    c.setFillColor(GOLD)
    c.rect(1.5 * cm, top_y - 0.15 * cm, 9.5 * cm, 0.08 * cm, stroke=0, fill=1)

    left = 1.5 * cm
    right = w - 1.5 * cm
    n_pots = 4
    gap = 0.3 * cm
    col_w = (right - left - gap * (n_pots - 1)) / n_pots

    col_top = top_y - 0.65 * cm
    header_h = 0.85 * cm
    row_h = 0.62 * cm
    col_h = header_h + 12 * row_h + 0.3 * cm

    for i, (label, teams, color) in enumerate(POTS):
        x = left + i * (col_w + gap)
        # Card background
        c.setFillColor(colors.white)
        c.roundRect(x, col_top - col_h, col_w, col_h, 0.2 * cm, stroke=0, fill=1)
        # Header
        c.setFillColor(color)
        c.roundRect(x, col_top - header_h, col_w, header_h, 0.2 * cm, stroke=0, fill=1)
        # Cover bottom corners to make header a top-only rounded rect
        c.rect(x, col_top - header_h, col_w, 0.2 * cm, stroke=0, fill=1)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + col_w / 2, col_top - 0.35 * cm, label.split("—")[0].strip())
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#F8E9C8"))
        c.drawCentredString(x + col_w / 2, col_top - 0.65 * cm, label.split("—")[1].strip().upper())

        # Teams list
        c.setFont("Helvetica", 9.2)
        for j, team in enumerate(teams):
            ty = col_top - header_h - 0.4 * cm - j * row_h
            # Alternating row tint
            if j % 2 == 1:
                c.setFillColor(colors.HexColor("#F4EFE0"))
                c.rect(x + 0.1 * cm, ty - 0.18 * cm, col_w - 0.2 * cm, row_h - 0.05 * cm, stroke=0, fill=1)
            # Bullet
            c.setFillColor(color)
            c.circle(x + 0.4 * cm, ty - 0.02 * cm, 0.08 * cm, stroke=0, fill=1)
            # Name
            c.setFillColor(INK)
            c.drawString(x + 0.65 * cm, ty - 0.07 * cm, team)
        # Card border
        c.setStrokeColor(colors.HexColor("#E0D8BF"))
        c.setLineWidth(0.4)
        c.roundRect(x, col_top - col_h, col_w, col_h, 0.2 * cm, stroke=1, fill=0)

    return col_top - col_h - 0.4 * cm


def draw_footer(c, w, h):
    band_h = 0.9 * cm
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, w, band_h, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, band_h, w, 0.08 * cm, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(w / 2, band_h / 2 - 0.1 * cm,
        "GROUP STAGE  ·  ROUND OF 32  ·  ROUND OF 16  ·  QUARTERS  ·  SEMIS  ·  FINAL    ·    GOOD LUCK!")


def build():
    w, h = A4
    c = canvas.Canvas(OUT, pagesize=A4)

    draw_background(c, w, h)
    draw_header(c, w, h)

    # Prizes block starts below header
    y = h - 3.7 * cm
    y = draw_prizes(c, w, h, y - 0.4 * cm)
    y = draw_rules(c, w, h, y - 0.6 * cm)
    y = draw_teams(c, w, h, y - 0.4 * cm)

    draw_footer(c, w, h)

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
