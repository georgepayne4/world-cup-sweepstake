"""Shared Trionda Tri-Color brand primitives for both sweepstake PDFs.

Provides: palette, alpha helpers, and the drawing pieces used in the
hero (night background, swoosh curves, ball with halo) and footer (grass).
"""
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

BALL_PNG = "assets/trionda_clean_medium.png"

# ── Palette ──────────────────────────────────────────────────────────
RED               = colors.HexColor("#E1342B")
BLUE              = colors.HexColor("#1B5BB0")
GREEN             = colors.HexColor("#2EA663")
GREEN_BRIGHT      = colors.HexColor("#3EBA72")
GREEN_PITCH       = colors.HexColor("#1F7A3A")
GREEN_PITCH_DARK  = colors.HexColor("#0E4520")
NIGHT             = colors.HexColor("#06120D")
NIGHT_GREEN       = colors.HexColor("#0B2A1E")
NIGHT_GREEN_MID   = colors.HexColor("#143527")
GOLD              = colors.HexColor("#E5C56F")
INK               = colors.HexColor("#0D0D0D")
GREY_DARK         = colors.HexColor("#444444")
GREY              = colors.HexColor("#888888")
GREY_LIGHT        = colors.HexColor("#E0E0E0")
OFF_WHITE         = colors.HexColor("#FAFAFA")
CREAM             = colors.HexColor("#F5F1E6")
WHITE             = colors.white

ACCENT_CYCLE = [RED, BLUE, GREEN]


# ── Alpha helpers ────────────────────────────────────────────────────
def fill_rgba(c, hex_color, alpha):
    cc = colors.HexColor(hex_color) if isinstance(hex_color, str) else hex_color
    c.setFillColor(colors.Color(cc.red, cc.green, cc.blue, alpha=alpha))


def stroke_rgba(c, hex_color, alpha):
    cc = colors.HexColor(hex_color) if isinstance(hex_color, str) else hex_color
    c.setStrokeColor(colors.Color(cc.red, cc.green, cc.blue, alpha=alpha))


# ── Hero pieces ──────────────────────────────────────────────────────
def draw_night_hero(c, w, hero_top, hero_bottom, centre_frac=0.30):
    """Stadium-night background: smooth deep-green→black with a brighter
    spot near the top centre."""
    c.setFillColor(NIGHT)
    c.rect(0, hero_bottom, w, hero_top - hero_bottom, stroke=0, fill=1)
    bands = 90
    band_h = (hero_top - hero_bottom) / bands
    for i in range(bands):
        d = abs(i / bands - centre_frac) / 0.8
        d = min(1.0, d)
        r = NIGHT_GREEN_MID.red   * (1 - d) + NIGHT.red   * d
        g = NIGHT_GREEN_MID.green * (1 - d) + NIGHT.green * d
        b = NIGHT_GREEN_MID.blue  * (1 - d) + NIGHT.blue  * d
        fill_rgba(c, colors.Color(r, g, b), 0.30)
        y = hero_bottom + i * band_h
        c.rect(0, y, w, band_h + 0.05, stroke=0, fill=1)


def draw_swoosh_curves(c, w, h, curves):
    """Draw a list of (color, alpha, points-of-cubic-bezier) sweeping
    arcs across the hero. `points` is [start, c1, c2, end] in points."""
    for color, alpha, pts in curves:
        stroke_rgba(c, color, alpha)
        c.setLineWidth(0.55 * cm)
        c.setLineCap(1)
        p = c.beginPath()
        p.moveTo(*pts[0])
        p.curveTo(*pts[1], *pts[2], *pts[3])
        c.drawPath(p, stroke=1, fill=0)
        # Thin brighter accent
        stroke_rgba(c, color, alpha + 0.18)
        c.setLineWidth(0.10 * cm)
        p2 = c.beginPath()
        p2.moveTo(*pts[0])
        p2.curveTo(*pts[1], *pts[2], *pts[3])
        c.drawPath(p2, stroke=1, fill=0)


def draw_ball_with_glow(c, cx, cy, size, halo=True, shadow=True):
    """Draw the Trionda ball at (cx, cy) with optional halo + shadow."""
    if halo:
        fill_rgba(c, "#E8F4DE", 0.14)
        c.circle(cx, cy, size * 0.62, stroke=0, fill=1)
    # CRITICAL: reset graphics-state alpha so the image renders fully opaque.
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
    if shadow:
        fill_rgba(c, "#000000", 0.45)
        c.ellipse(cx - bw * 0.45, cy - bh * 0.58,
                  cx + bw * 0.45, cy - bh * 0.51, stroke=0, fill=1)


def draw_tri_underline(c, cx, y, total_w, h_=0.10*cm):
    seg = total_w / 3
    c.setFillColor(RED);   c.rect(cx - seg * 1.5, y, seg, h_, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(cx - seg * 0.5, y, seg, h_, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(cx + seg * 0.5, y, seg, h_, stroke=0, fill=1)


def draw_tri_left_underline(c, x, y, total_w, h_=0.08*cm):
    """Tri-color underline starting from x (for left-aligned section headers)."""
    seg = total_w / 3
    c.setFillColor(RED);   c.rect(x,             y, seg, h_, stroke=0, fill=1)
    c.setFillColor(BLUE);  c.rect(x + seg,       y, seg, h_, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(x + seg * 2,   y, seg, h_, stroke=0, fill=1)


# ── Grass footer ─────────────────────────────────────────────────────
def draw_grass(c, w, grass_top, grass_bottom):
    """Pitch grass strip — vertical gradient + dense randomised blades."""
    bands = 30
    band_h = (grass_top - grass_bottom) / bands
    for i in range(bands):
        t = i / (bands - 1)  # 0 at bottom → 1 at top
        r = GREEN_PITCH_DARK.red   * (1 - t) + GREEN_PITCH.red   * t
        g = GREEN_PITCH_DARK.green * (1 - t) + GREEN_PITCH.green * t
        b = GREEN_PITCH_DARK.blue  * (1 - t) + GREEN_PITCH.blue  * t
        c.setFillColor(colors.Color(r, g, b))
        y = grass_bottom + i * band_h
        c.rect(0, y, w, band_h + 0.05, stroke=0, fill=1)

    import random
    rng = random.Random(7)
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
