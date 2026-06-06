"""Generate the World Cup Sweepstake announcement PDF.

Dramatic Trionda-inspired aesthetic: dark night hero with spotlight glow,
swooping tri-color curves echoing the ball's panel design, real Trionda
ball, grass-textured footer.
"""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

OUT = "World_Cup_Sweepstake_Announcement.pdf"
BALL_PNG = "assets/trionda_clean_medium.png"

# Event details
DRAW_DATE = "MONDAY 8 JUNE 2026"
DRAW_TIME = "8:30PM"
BUY_IN = 15
N_PLAYERS = 12
POT_TOTAL = BUY_IN * N_PLAYERS  # £180

# Trionda Tri-Color palette + atmospheric darks
RED = colors.HexColor("#E1342B")
BLUE = colors.HexColor("#1B5BB0")
GREEN = colors.HexColor("#2EA663")
GREEN_BRIGHT = colors.HexColor("#3EBA72")
GREEN_PITCH = colors.HexColor("#1F7A3A")
GREEN_PITCH_DARK = colors.HexColor("#0E4520")
NIGHT = colors.HexColor("#06120D")
NIGHT_GREEN = colors.HexColor("#0B2A1E")
NIGHT_GREEN_MID = colors.HexColor("#143527")
GOLD = colors.HexColor("#E5C56F")
INK = colors.HexColor("#0D0D0D")
GREY_DARK = colors.HexColor("#444444")
GREY = colors.HexColor("#888888")
GREY_LIGHT = colors.HexColor("#E0E0E0")
OFF_WHITE = colors.HexColor("#FAFAFA")
CREAM = colors.HexColor("#F5F1E6")
WHITE = colors.white

PRIZES = [
    ("Tournament Winner",       0.60),
    ("Runner-up",               0.20),
    ("Most Cards (Y=1, R=3)",   0.05),
    ("First Red Card",          0.05),
    ("Fastest Goal",            0.05),
    ("Highest-Scoring Match",   0.05),
]


# -------------------------------------------------------------------- helpers

def fill_rgba(c, hex_color, alpha):
    """Set fill to a hex colour with alpha."""
    cc = colors.HexColor(hex_color) if isinstance(hex_color, str) else hex_color
    c.setFillColor(colors.Color(cc.red, cc.green, cc.blue, alpha=alpha))


def stroke_rgba(c, hex_color, alpha):
    cc = colors.HexColor(hex_color) if isinstance(hex_color, str) else hex_color
    c.setStrokeColor(colors.Color(cc.red, cc.green, cc.blue, alpha=alpha))


# -------------------------------------------------------------------- pieces

def draw_night_hero(c, w, h, hero_top, hero_bottom):
    """Stadium-night background: smooth radial dark green→black."""
    # Solid base
    c.setFillColor(NIGHT)
    c.rect(0, hero_bottom, w, hero_top - hero_bottom, stroke=0, fill=1)
    # Smooth vertical falloff via many fine bands
    bands = 90
    band_h = (hero_top - hero_bottom) / bands
    # Centre of the brighter spot, fractional band index
    centre_frac = 0.30
    for i in range(bands):
        d = abs(i / bands - centre_frac) / 0.8
        d = min(1.0, d)
        r = NIGHT_GREEN_MID.red   * (1 - d) + NIGHT.red   * d
        g = NIGHT_GREEN_MID.green * (1 - d) + NIGHT.green * d
        b = NIGHT_GREEN_MID.blue  * (1 - d) + NIGHT.blue  * d
        fill_rgba(c, colors.Color(r, g, b), 0.30)
        y = hero_bottom + i * band_h
        c.rect(0, y, w, band_h + 0.05, stroke=0, fill=1)


def draw_swoosh_curves(c, w, h, hero_top, hero_bottom):
    """Decorative tri-colour swooping curves echoing the ball's panel design."""
    # Three sweeping bezier arcs across the hero, each in one of the three colours.
    swooshes = [
        (RED,   0.22, [(-2*cm, h - 8.5*cm), (5*cm, h - 5*cm),
                       (w*0.45, h - 2.5*cm), (w + 2*cm, h - 4*cm)]),
        (BLUE,  0.20, [(-2*cm, h - 4*cm), (w*0.30, h - 6.5*cm),
                       (w*0.65, h - 9*cm), (w + 2*cm, h - 6.5*cm)]),
        (GREEN, 0.24, [(-2*cm, h - 12.5*cm), (w*0.30, h - 9.5*cm),
                       (w*0.70, h - 11*cm), (w + 2*cm, h - 9*cm)]),
    ]
    for color, alpha, pts in swooshes:
        # Thick translucent stroke
        stroke_rgba(c, color, alpha)
        c.setLineWidth(0.65 * cm)
        c.setLineCap(1)
        p = c.beginPath()
        p.moveTo(*pts[0])
        p.curveTo(*pts[1], *pts[2], *pts[3])
        c.drawPath(p, stroke=1, fill=0)
        # Thin bright accent on top
        stroke_rgba(c, color, alpha + 0.18)
        c.setLineWidth(0.12 * cm)
        p2 = c.beginPath()
        p2.moveTo(*pts[0])
        p2.curveTo(*pts[1], *pts[2], *pts[3])
        c.drawPath(p2, stroke=1, fill=0)


def draw_ball_with_glow(c, cx, cy, size):
    """Ball with a faint halo ring around it."""
    # Outer halo ring — slightly larger than the ball, faint
    fill_rgba(c, "#E8F4DE", 0.14)
    c.circle(cx, cy, size * 0.62, stroke=0, fill=1)

    # CRITICAL: reset the graphics-state alpha to fully opaque before drawing
    # the image, otherwise reportlab's persisted fill-alpha bleeds into the
    # raster and produces a ghost-faded ball.
    c.saveState()
    c.setFillAlpha(1.0)
    c.setStrokeAlpha(1.0)

    img = ImageReader(BALL_PNG)
    iw, ih = img.getSize()
    aspect = ih / iw
    bw = size
    bh = size * aspect
    c.drawImage(img, cx - bw / 2, cy - bh / 2, width=bw, height=bh, mask='auto')
    c.restoreState()

    # Soft cast shadow on the ground
    fill_rgba(c, "#000000", 0.45)
    c.ellipse(cx - bw * 0.45, cy - bh * 0.58,
              cx + bw * 0.45, cy - bh * 0.51, stroke=0, fill=1)


def draw_grass(c, w, grass_top, grass_bottom):
    """Realistic-ish grass strip at the bottom of the page."""
    # Vertical gradient (lighter green at top → deep green at bottom)
    bands = 30
    band_h = (grass_top - grass_bottom) / bands
    for i in range(bands):
        t = i / (bands - 1)  # 0 at bottom, 1 at top
        r = GREEN_PITCH_DARK.red   * (1 - t) + GREEN_PITCH.red   * t
        g = GREEN_PITCH_DARK.green * (1 - t) + GREEN_PITCH.green * t
        b = GREEN_PITCH_DARK.blue  * (1 - t) + GREEN_PITCH.blue  * t
        c.setFillColor(colors.Color(r, g, b))
        y = grass_bottom + i * band_h
        c.rect(0, y, w, band_h + 0.05, stroke=0, fill=1)

    # Blade texture — many short strokes for a denser look
    import random
    rng = random.Random(7)  # deterministic
    for _ in range(1400):
        x = rng.random() * w
        base_y = grass_bottom + rng.random() * (grass_top - grass_bottom)
        depth = (base_y - grass_bottom) / (grass_top - grass_bottom)
        height = (0.08 + rng.random() * (0.18 + depth * 0.18)) * cm
        roll = rng.random()
        if roll < 0.20:
            shade = GREEN_BRIGHT; alpha = 0.35 + depth * 0.35
        elif roll < 0.55:
            shade = GREEN_PITCH; alpha = 0.45
        else:
            shade = GREEN_PITCH_DARK; alpha = 0.55
        stroke_rgba(c, shade, alpha)
        c.setLineWidth(0.04 * cm)
        c.line(x, base_y, x + (rng.random() - 0.5) * 0.08 * cm, base_y + height)


def draw_tri_underline(c, cx, y, total_w, h_=0.10*cm):
    seg = total_w / 3
    c.setFillColor(RED);   c.rect(cx - seg * 1.5, y, seg, h_, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(cx - seg * 0.5, y, seg, h_, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(cx + seg * 0.5, y, seg, h_, stroke=0, fill=1)


# -------------------------------------------------------------------- build

def build():
    w, h = A4
    c = canvas.Canvas(OUT, pagesize=A4)

    # Layout constants
    grass_h = 2.6 * cm
    hero_top = h
    hero_bottom = h - 14.2 * cm   # dark hero takes ~half the page

    # 1) Background: cream page with dark hero on top + grass at the bottom
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    draw_night_hero(c, w, h, hero_top, hero_bottom)
    draw_swoosh_curves(c, w, h, hero_top, hero_bottom)

    # 2) Title (white on dark)
    title_y = h - 2.0 * cm
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(w / 2, title_y, "FIFA WORLD CUP 2026")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(w / 2, title_y - 1.8 * cm, "SWEEPSTAKE")
    draw_tri_underline(c, w / 2, title_y - 2.5 * cm, 6.5 * cm)

    # 3) Ball — moved up; sits in the lower half of the dark hero
    ball_size = 7.0 * cm
    ball_cy = h - 9.0 * cm
    draw_ball_with_glow(c, w / 2, ball_cy, ball_size)

    # 4) Smooth transition / subtle line at the hero/cream boundary
    fill_rgba(c, "#000000", 0.18)
    c.rect(0, hero_bottom - 0.06 * cm, w, 0.06 * cm, stroke=0, fill=1)
    fill_rgba(c, "#FFFFFF", 0.15)
    c.rect(0, hero_bottom, w, 0.04 * cm, stroke=0, fill=1)

    # 5) Date / time pill — straddles the boundary like a chip
    pill_w, pill_h = 14.0 * cm, 1.9 * cm
    pill_x = (w - pill_w) / 2
    pill_y = hero_bottom - pill_h / 2 + 0.2 * cm
    # Pill body with gold gradient feel (single solid gold)
    c.setFillColor(GOLD)
    c.roundRect(pill_x, pill_y, pill_w, pill_h, 0.4 * cm, stroke=0, fill=1)
    # Inner thin tri-color border
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

    # 6) Money line
    money_y = hero_bottom - 2.0 * cm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, money_y, f"£{BUY_IN} BUY-IN     ·     £{POT_TOTAL} POT     ·     {N_PLAYERS} PLAYERS")

    # 7) Prizes section
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

        # £ amount in a tri-color accent block
        color = [RED, BLUE, GREEN][i % 3]
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(right, y, amt_text)

    # 8) Grass at the bottom
    draw_grass(c, w, grass_h, 0)

    # Footer text on grass
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.85))
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(w / 2, 0.55 * cm,
        "12 PLAYERS  ·  4 TEAMS EACH  ·  6 WAYS TO WIN  ·  GOOD LUCK")

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
