# filepath: src/export/image_export.py
"""
Pillow-based PNG Export
Creates a styled 900x520 card image with gradient background,
rounded corners, and clear Q/A typography.
All resources are free/open-source (Pillow).
"""

import io
import math
from PIL import Image, ImageDraw, ImageFont


# ── Colour palette ─────────────────────────────────────────────────────────────
_BG_TOP   = (15,  10,  30)
_BG_BOT   = (10,  18,  35)
_ACCENT1  = (124, 58,  237)   # purple
_ACCENT2  = (6,   182, 212)   # cyan
_TEXT_PRI = (241, 245, 249)
_TEXT_SEC = (148, 163, 184)
_TEXT_MUT = (71,  85,  105)
_CARD_BG  = (20,  15,  42,  210)   # RGBA
_BORDER   = (124, 58,  237, 70)    # RGBA

# ── Canvas size ───────────────────────────────────────────────────────────────
_W, _H = 900, 520
_PAD    = 52
_RADIUS = 28


def _make_gradient(w: int, h: int) -> Image.Image:
    """Creates a two-colour diagonal gradient background."""
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    for y in range(h):
        ratio = y / h
        r = int(_BG_TOP[0] + (_BG_BOT[0] - _BG_TOP[0]) * ratio)
        g = int(_BG_TOP[1] + (_BG_BOT[1] - _BG_TOP[1]) * ratio)
        b = int(_BG_TOP[2] + (_BG_BOT[2] - _BG_TOP[2]) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return base


def _rounded_rect(draw, xy, radius: int, fill, outline=None, outline_width=1):
    """Draws a rounded rectangle."""
    try:
        draw.rounded_rectangle(xy, radius=radius, fill=fill,
                               outline=outline, width=outline_width)
    except AttributeError:
        x0, y0, x1, y1 = xy
        draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
        draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
        for cx, cy in [(x0+radius, y0+radius), (x1-radius, y0+radius),
                       (x0+radius, y1-radius), (x1-radius, y1-radius)]:
            draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=fill)


def _get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Tries to load a system font; falls back to default."""
    candidates_bold = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:\\Windows\\Fonts\\arialbd.ttf",
    ]
    candidates_reg = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for path in (candidates_bold if bold else candidates_reg):
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def _wrap_text(text: str, font, max_width: int) -> list[str]:
    """Wraps text to fit within max_width pixels."""
    words = text.split()
    lines: list[str] = []
    current = ""
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for word in words:
        test = f"{current} {word}".strip()
        bbox = dummy.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _accent_strip(img: Image.Image) -> None:
    """Draws a thin gradient accent line at the top of the card."""
    draw = ImageDraw.Draw(img)
    for x in range(_W):
        ratio = x / _W
        r = int(_ACCENT1[0] + (_ACCENT2[0] - _ACCENT1[0]) * ratio)
        g = int(_ACCENT1[1] + (_ACCENT2[1] - _ACCENT1[1]) * ratio)
        b = int(_ACCENT1[2] + (_ACCENT2[2] - _ACCENT1[2]) * ratio)
        draw.line([(x, 0), (x, 4)], fill=(r, g, b))


def card_to_png_bytes(
    question: str,
    answer: str,
    topic: str,
    card_num: int,
    total: int,
    user_name: str,
) -> bytes:
    """
    Renders a styled flashcard as a PNG and returns raw bytes.

    Args:
        question:  The card question text.
        answer:    The card answer text.
        topic:     The deck topic (shown in header).
        card_num:  1-based card index.
        total:     Total cards in deck.
        user_name: Learner's name (shown in footer).

    Returns:
        PNG image as bytes.
    """
    # ── Canvas ────────────────────────────────────────────────────────────────
    img = _make_gradient(_W, _H)
    draw = ImageDraw.Draw(img, "RGBA")

    # ── Decorative glow circles ───────────────────────────────────────────────
    draw.ellipse([-120, -120, 200, 200], fill=(*_ACCENT1, 22))
    draw.ellipse([_W - 180, _H - 180, _W + 120, _H + 120], fill=(*_ACCENT2, 18))

    # ── Card body ─────────────────────────────────────────────────────────────
    card_x0, card_y0 = _PAD, _PAD
    card_x1, card_y1 = _W - _PAD, _H - _PAD
    _rounded_rect(
        draw,
        [card_x0, card_y0, card_x1, card_y1],
        radius=_RADIUS,
        fill=(20, 15, 40, 200),
        outline=(*_ACCENT1, 70),
        outline_width=1,
    )

    # Accent strip
    _accent_strip(img)

    # ── Fonts ─────────────────────────────────────────────────────────────────
    font_topic  = _get_font(14, bold=True)
    font_label  = _get_font(12, bold=True)
    font_q      = _get_font(22, bold=True)
    font_a      = _get_font(18, bold=False)
    font_footer = _get_font(12, bold=False)

    # ── Header ────────────────────────────────────────────────────────────────
    topic_text   = topic.upper()[:50]
    counter_text = f"{card_num} / {total}"

    draw.text((_PAD + 20, _PAD + 18), topic_text, font=font_topic, fill=(*_ACCENT2, 220))
    ctr_bbox = draw.textbbox((0, 0), counter_text, font=font_topic)
    ctr_w = ctr_bbox[2] - ctr_bbox[0]
    draw.text((_W - _PAD - 20 - ctr_w, _PAD + 18), counter_text,
              font=font_topic, fill=_TEXT_SEC)

    # Divider line under header
    div_y = _PAD + 44
    for x in range(_PAD + 16, _W - _PAD - 16):
        ratio = (x - _PAD) / (_W - 2 * _PAD)
        alpha = int(80 + 60 * math.sin(ratio * math.pi))
        draw.point((x, div_y), fill=(*_TEXT_MUT, alpha))

    # ── Question section ──────────────────────────────────────────────────────
    q_label_y = div_y + 18
    draw.text((_PAD + 20, q_label_y), "QUESTION", font=font_label, fill=(*_ACCENT1, 255))

    q_text_y = q_label_y + 26
    max_w = _W - 2 * (_PAD + 20)
    q_lines = _wrap_text(question, font_q, max_w)
    for line in q_lines[:3]:
        draw.text((_PAD + 20, q_text_y), line, font=font_q, fill=_TEXT_PRI)
        q_text_y += 32

    # ── Separator ─────────────────────────────────────────────────────────────
    sep_y = q_text_y + 12
    draw.line([(_PAD + 20, sep_y), (_W - _PAD - 20, sep_y)],
              fill=(*_ACCENT1, 50), width=1)

    # ── Answer section ────────────────────────────────────────────────────────
    a_label_y = sep_y + 14
    draw.text((_PAD + 20, a_label_y), "ANSWER", font=font_label, fill=(*_ACCENT2, 255))

    a_text_y = a_label_y + 26
    a_lines = _wrap_text(answer, font_a, max_w)
    for line in a_lines[:4]:
        draw.text((_PAD + 20, a_text_y), line, font=font_a, fill=_TEXT_SEC)
        a_text_y += 26

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_y = card_y1 - 32
    draw.text((_PAD + 20, footer_y),
              f"FlashLearn AI  ·  {user_name}", font=font_footer, fill=_TEXT_MUT)
    brand_text = "flashlearn.ai"
    br_bbox = draw.textbbox((0, 0), brand_text, font=font_footer)
    br_w = br_bbox[2] - br_bbox[0]
    draw.text((_W - _PAD - 20 - br_w, footer_y), brand_text,
              font=font_footer, fill=_TEXT_MUT)

    # ── Convert to PNG bytes ──────────────────────────────────────────────────
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf.read()
