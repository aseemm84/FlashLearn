# filepath: src/export/pdf_export.py
"""
ReportLab-based PDF Export
Generates a professional multi-page PDF of the full flashcard deck.
All resources are free/open-source (ReportLab).
"""

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
    KeepInFrame,
)
from reportlab.pdfgen import canvas as rl_canvas


# ── Colour palette ─────────────────────────────────────────────────────────────
_BG       = colors.HexColor("#0D0D1A")   # page background (very dark navy)
_CARD_BG  = colors.HexColor("#1E1B3A")   # card cell – visibly lighter than _BG
_ACCENT_P = colors.HexColor("#7C3AED")   # purple
_ACCENT_C = colors.HexColor("#06B6D4")   # cyan
_ACCENT_PK= colors.HexColor("#EC4899")   # pink
_TEXT_PRI = colors.HexColor("#F1F5F9")   # near-white  ← main body text
_TEXT_SEC = colors.HexColor("#CBD5E1")   # light grey  ← answer text (brighter than before)
_TEXT_MUT = colors.HexColor("#94A3B8")   # muted grey  ← footer / meta
_BORDER   = colors.HexColor("#4C1D95")   # purple border on cards
_WHITE    = colors.white

W, H = A4   # 595.28 x 841.89 pts


# ── Custom canvas ──────────────────────────────────────────────────────────────
class _ThemedCanvas(rl_canvas.Canvas):
    """
    Overrides _startPage() — the correct hook that fires BEFORE ReportLab
    places any flowable content on the page.  The background rectangle is
    therefore always behind text, never on top of it.
    """

    def __init__(self, *args, meta: dict | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta      = meta or {}
        self._page_num  = 0

    # ── Called BEFORE content is painted — correct place for background ────────
    def _startPage(self):
        super()._startPage()
        self._page_num += 1
        self._draw_page_bg()

    # ── Called AFTER content is committed — correct place for overlaid footer ──
    def showPage(self):
        self._draw_footer()   # footer goes on top of content (desired)
        super().showPage()

    # save() must NOT touch page graphics — removed all drawing from here
    def save(self):
        super().save()

    # ── Background: solid dark fill + two soft decorative ellipses ────────────
    def _draw_page_bg(self):
        # Solid dark page fill
        self.setFillColor(_BG)
        self.rect(0, 0, W, H, fill=1, stroke=0)

        # Top-left purple glow (fully opaque, low-contrast blend)
        self.setFillColor(colors.HexColor("#130A2A"))
        self.ellipse(-20 * mm, H - 55 * mm, 75 * mm, H + 15 * mm, fill=1, stroke=0)

        # Bottom-right cyan glow
        self.setFillColor(colors.HexColor("#051820"))
        self.ellipse(W - 65 * mm, -15 * mm, W + 15 * mm, 55 * mm, fill=1, stroke=0)

    # ── Footer: accent line + metadata text ───────────────────────────────────
    def _draw_footer(self):
        topic = self._meta.get("topic", "")
        user  = self._meta.get("user_name", "")

        # Accent line above footer text
        self.setStrokeColor(_ACCENT_P)
        self.setLineWidth(0.5)
        self.line(15 * mm, 14 * mm, W - 15 * mm, 14 * mm)

        # Footer text
        self.setFont("Helvetica", 7.5)
        self.setFillColor(_TEXT_MUT)
        footer_left = f"FlashLearn AI  \u00b7  {user}  \u00b7  {topic}"
        self.drawString(15 * mm, 8 * mm, footer_left)
        self.drawRightString(W - 15 * mm, 8 * mm, f"Page {self._page_num}")


# ── Paragraph styles ───────────────────────────────────────────────────────────
def _styles() -> dict:
    return {
        # ── Cover page ──
        "cover_brand": ParagraphStyle(
            "cover_brand",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=_ACCENT_C,
            alignment=TA_CENTER,
            leading=18,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Helvetica-Bold",
            fontSize=30,
            textColor=_TEXT_PRI,
            alignment=TA_CENTER,
            leading=36,
            spaceAfter=6,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontName="Helvetica",
            fontSize=13,
            textColor=_TEXT_SEC,
            alignment=TA_CENTER,
            leading=18,
            spaceAfter=4,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            fontName="Helvetica",
            fontSize=10,
            textColor=_TEXT_MUT,
            alignment=TA_CENTER,
            leading=16,
        ),
        # ── Section header ──
        "section_head": ParagraphStyle(
            "section_head",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=_ACCENT_P,
            alignment=TA_LEFT,
            leading=15,
            spaceBefore=6,
            spaceAfter=4,
        ),
        # ── Card content ──
        "card_num": ParagraphStyle(
            "card_num",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            textColor=_ACCENT_P,
            alignment=TA_LEFT,
            leading=10,
            spaceAfter=3,
        ),
        "card_label_q": ParagraphStyle(
            "card_label_q",
            fontName="Helvetica-Bold",
            fontSize=7,
            textColor=_ACCENT_C,
            alignment=TA_LEFT,
            leading=9,
            spaceAfter=2,
        ),
        "card_label_a": ParagraphStyle(
            "card_label_a",
            fontName="Helvetica-Bold",
            fontSize=7,
            textColor=_ACCENT_PK,
            alignment=TA_LEFT,
            leading=9,
            spaceAfter=2,
        ),
        "card_q": ParagraphStyle(
            "card_q",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=_TEXT_PRI,      # near-white on dark card bg — readable
            alignment=TA_LEFT,
            leading=15,
            spaceAfter=5,
        ),
        "card_a": ParagraphStyle(
            "card_a",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=_TEXT_SEC,      # light grey on dark card bg — readable
            alignment=TA_LEFT,
            leading=13,
        ),
    }


# ── Cover page elements ────────────────────────────────────────────────────────
def _cover_elements(
    topic: str,
    depth_level: str,
    user_name: str,
    user_profession: str,
    user_sub: str,
    total_cards: int,
    styles: dict,
) -> list:
    date_str = datetime.now().strftime("%B %d, %Y")
    return [
        Spacer(1, 44 * mm),
        Paragraph("FlashLearn AI", styles["cover_brand"]),
        Spacer(1, 5 * mm),
        Paragraph(topic, styles["cover_title"]),
        Spacer(1, 4 * mm),
        HRFlowable(width="55%", thickness=1.2, color=_ACCENT_P, hAlign="CENTER"),
        Spacer(1, 7 * mm),
        Paragraph(f"{depth_level} Deck  \u00b7  {total_cards} Flashcards", styles["cover_sub"]),
        Spacer(1, 4 * mm),
        Paragraph(
            f"Prepared for <b>{user_name}</b>  \u00b7  "
            f"{user_profession} ({user_sub})",
            styles["cover_meta"],
        ),
        Paragraph(f"Generated on {date_str}", styles["cover_meta"]),
        PageBreak(),
    ]


# ── Card grid (2 columns) ──────────────────────────────────────────────────────
def _build_card_table(cards: list[dict], styles: dict) -> list:
    """
    Renders cards in a 2-column grid.
    Each cell has a dark-purple background with light text — fully legible.
    """
    elements  = []
    gap       = 6 * mm
    col_w     = (W - 30 * mm - gap) / 2   # two equal columns
    row_h     = 56 * mm                    # slightly taller for breathing room

    pairs = [cards[i : i + 2] for i in range(0, len(cards), 2)]

    for pair_idx, pair in enumerate(pairs):
        row_cells = []
        for ci, card in enumerate(pair):
            card_num = pair_idx * 2 + ci + 1

            inner = [
                Paragraph(f"CARD {card_num}", styles["card_num"]),
                Paragraph("Q", styles["card_label_q"]),
                Paragraph(card["question"], styles["card_q"]),
                Spacer(1, 1.5 * mm),
                Paragraph("A", styles["card_label_a"]),
                Paragraph(card["answer"], styles["card_a"]),
            ]

            # KeepInFrame shrinks content that would overflow the cell
            row_cells.append(
                KeepInFrame(
                    col_w - 10 * mm,
                    row_h  -  8 * mm,
                    inner,
                    mode="shrink",
                )
            )

        # Pad to always have 2 columns
        while len(row_cells) < 2:
            row_cells.append(Spacer(1, 1))

        tbl = Table(
            [row_cells],
            colWidths  = [col_w, col_w],
            rowHeights = [row_h],
            hAlign     = "LEFT",
        )
        tbl.setStyle(TableStyle([
            # ── Cell backgrounds (dark purple — clearly different from page bg) ──
            ("BACKGROUND",    (0, 0), (0, 0), _CARD_BG),
            ("BACKGROUND",    (1, 0), (1, 0), _CARD_BG),
            # ── Purple border around each card ──
            ("BOX",           (0, 0), (0, 0), 0.8, _BORDER),
            ("BOX",           (1, 0), (1, 0), 0.8, _BORDER),
            # ── Top accent stripe (bright purple line) ──
            ("LINEABOVE",     (0, 0), (0, 0), 2.5, _ACCENT_P),
            ("LINEABOVE",     (1, 0), (1, 0), 2.5, _ACCENT_P),
            # ── Cell padding ──
            ("TOPPADDING",    (0, 0), (-1, -1), 5 * mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4 * mm),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 4 * mm),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            # ── Column gap (transparent spacer column is not used;
            #    instead we rely on table hAlign and the card left margin) ──
        ]))

        elements.append(tbl)
        elements.append(Spacer(1, 4 * mm))

    return elements


# ── Public entry point ─────────────────────────────────────────────────────────
def deck_to_pdf_bytes(
    cards: list[dict],
    topic: str,
    depth_level: str,
    user_name: str,
    user_profession: str,
    user_sub_profession: str,
) -> bytes:
    """
    Generates a styled, readable multi-page PDF of the full flashcard deck.

    Args:
        cards:               List of {"question": str, "answer": str}.
        topic:               Deck topic string.
        depth_level:         "Basic" | "Intermediate" | "Advanced" | "Deep Dive".
        user_name:           Learner's name (cover + footer).
        user_profession:     Profession category.
        user_sub_profession: Specialisation / role.

    Returns:
        Raw PDF bytes ready to stream to the browser.
    """
    buf  = io.BytesIO()
    meta = {"topic": topic, "user_name": user_name}

    doc = SimpleDocTemplate(
        buf,
        pagesize      = A4,
        leftMargin    = 15 * mm,
        rightMargin   = 15 * mm,
        topMargin     = 20 * mm,
        bottomMargin  = 22 * mm,   # room for footer
        title         = f"FlashLearn AI – {topic}",
        author        = "FlashLearn AI",
        subject       = f"{depth_level} deck for {user_name}",
    )

    st       = _styles()
    elements = []

    # Cover page
    elements.extend(
        _cover_elements(
            topic, depth_level, user_name,
            user_profession, user_sub_profession,
            len(cards), st,
        )
    )

    # Section header on card pages
    elements.append(
        Paragraph(
            f"{depth_level} Flashcard Deck  \u00b7  {len(cards)} Cards",
            st["section_head"],
        )
    )
    elements.append(HRFlowable(width="100%", thickness=0.6, color=_ACCENT_P))
    elements.append(Spacer(1, 5 * mm))

    # Card grid
    elements.extend(_build_card_table(cards, st))

    # Build with our themed canvas
    doc.build(
        elements,
        canvasmaker=lambda filename, **kw: _ThemedCanvas(filename, meta=meta, **kw),
    )

    buf.seek(0)
    return buf.read()
