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
_BG       = colors.HexColor("#0A0A0F")
_BG2      = colors.HexColor("#12121A")
_CARD_BG  = colors.HexColor("#16162A")
_ACCENT_P = colors.HexColor("#7C3AED")
_ACCENT_C = colors.HexColor("#06B6D4")
_ACCENT_PK= colors.HexColor("#EC4899")
_TEXT_PRI = colors.HexColor("#F1F5F9")
_TEXT_SEC = colors.HexColor("#94A3B8")
_TEXT_MUT = colors.HexColor("#475569")
_BORDER   = colors.HexColor("#1E1E30")
_WHITE    = colors.white

W, H = A4  # 210 x 297 mm


# ── Custom canvas with background + header/footer ──────────────────────────────
class _ThemedCanvas(rl_canvas.Canvas):
    def __init__(self, *args, meta: dict | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta = meta or {}
        self._page_num = 0

    def showPage(self):
        self._page_num += 1
        self._draw_page_bg()
        self._draw_footer()
        super().showPage()

    def save(self):
        self._page_num += 1
        self._draw_page_bg()
        self._draw_footer()
        super().save()

    def _draw_page_bg(self):
        self.setFillColor(_BG)
        self.rect(0, 0, W, H, fill=1, stroke=0)

        # Subtle gradient simulation
        self.setFillColorRGB(0.09, 0.04, 0.22, alpha=0.35)
        self.ellipse(-30 * mm, H - 60 * mm, 80 * mm, H + 20 * mm, fill=1, stroke=0)

        self.setFillColorRGB(0.02, 0.35, 0.52, alpha=0.20)
        self.ellipse(W - 70 * mm, -20 * mm, W + 20 * mm, 60 * mm, fill=1, stroke=0)

    def _draw_footer(self):
        topic = self._meta.get("topic", "")
        user  = self._meta.get("user_name", "")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(_TEXT_MUT)
        self.drawString(15 * mm, 8 * mm, f"FlashLearn AI  ·  {user}  ·  {topic}")
        pg_str = f"Page {self._page_num}"
        self.drawRightString(W - 15 * mm, 8 * mm, pg_str)
        # Footer accent line
        self.setStrokeColor(_ACCENT_P)
        self.setLineWidth(0.4)
        self.line(15 * mm, 13 * mm, W - 15 * mm, 13 * mm)


# ── Paragraph styles ───────────────────────────────────────────────────────────
def _styles() -> dict:
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Helvetica-Bold",
            fontSize=32,
            textColor=_TEXT_PRI,
            alignment=TA_CENTER,
            leading=38,
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
        "card_num": ParagraphStyle(
            "card_num",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=_ACCENT_P,
            alignment=TA_LEFT,
            leading=10,
            spaceAfter=2,
        ),
        "card_label_q": ParagraphStyle(
            "card_label_q",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            textColor=_ACCENT_C,
            alignment=TA_LEFT,
            leading=10,
            spaceAfter=3,
        ),
        "card_label_a": ParagraphStyle(
            "card_label_a",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            textColor=_ACCENT_PK,
            alignment=TA_LEFT,
            leading=10,
            spaceAfter=3,
        ),
        "card_q": ParagraphStyle(
            "card_q",
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=_TEXT_PRI,
            alignment=TA_LEFT,
            leading=17,
            spaceAfter=6,
        ),
        "card_a": ParagraphStyle(
            "card_a",
            fontName="Helvetica",
            fontSize=10.5,
            textColor=_TEXT_SEC,
            alignment=TA_LEFT,
            leading=15,
        ),
        "section_head": ParagraphStyle(
            "section_head",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=_ACCENT_P,
            alignment=TA_LEFT,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
        ),
    }


# ── Cover page ─────────────────────────────────────────────────────────────────
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
    elems = [
        Spacer(1, 40 * mm),
        Paragraph("FlashLearn AI", ParagraphStyle(
            "brand", fontName="Helvetica-Bold",
            fontSize=14, textColor=_ACCENT_C,
            alignment=TA_CENTER, leading=18)),
        Spacer(1, 4 * mm),
        Paragraph(topic, styles["cover_title"]),
        Spacer(1, 4 * mm),
        HRFlowable(width="60%", thickness=1, color=_ACCENT_P, hAlign="CENTER"),
        Spacer(1, 6 * mm),
        Paragraph(f"{depth_level} Deck  ·  {total_cards} Flashcards", styles["cover_sub"]),
        Spacer(1, 3 * mm),
        Paragraph(
            f"Prepared for <b>{user_name}</b>  ·  {user_profession} ({user_sub})",
            styles["cover_meta"],
        ),
        Paragraph(f"Generated on {date_str}", styles["cover_meta"]),
        PageBreak(),
    ]
    return elems


# ── Two-cards-per-row layout ────────────────────────────────────────────────────
def _build_card_table(cards: list[dict], styles: dict) -> list:
    """Lays out cards in a 2-column grid using ReportLab Tables."""
    elements = []
    col_w = (W - 30 * mm) / 2 - 4 * mm
    row_h = 52 * mm

    pairs = [cards[i:i+2] for i in range(0, len(cards), 2)]

    for pair_idx, pair in enumerate(pairs):
        row_data = []
        for ci, card in enumerate(pair):
            card_content = [
                Paragraph(f"CARD {pair_idx * 2 + ci + 1}", styles["card_num"]),
                Paragraph("Q:", styles["card_label_q"]),
                Paragraph(card["question"], styles["card_q"]),
                Spacer(1, 2 * mm),
                Paragraph("A:", styles["card_label_a"]),
                Paragraph(card["answer"], styles["card_a"]),
            ]
            frame = KeepInFrame(
                col_w - 8 * mm,
                row_h - 6 * mm,
                card_content,
                mode="shrink",
            )
            row_data.append(frame)

        while len(row_data) < 2:
            row_data.append(Paragraph("", styles["card_a"]))

        tbl = Table([row_data], colWidths=[col_w, col_w], rowHeights=[row_h])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, 0), _CARD_BG),
            ("BACKGROUND",    (1, 0), (1, 0), _CARD_BG),
            ("BOX",           (0, 0), (0, 0), 0.5, _BORDER),
            ("BOX",           (1, 0), (1, 0), 0.5, _BORDER),
            ("TOPPADDING",    (0, 0), (-1, -1), 5 * mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5 * mm),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4 * mm),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 4 * mm),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(tbl)
        elements.append(Spacer(1, 3 * mm))

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
    Generates a styled multi-page PDF of the full flashcard deck.

    Args:
        cards:               List of {"question": str, "answer": str}.
        topic:               Deck topic.
        depth_level:         Basic / Intermediate / Advanced / Deep Dive.
        user_name:           Learner name for cover and footer.
        user_profession:     Profession category.
        user_sub_profession: Specialisation / role.

    Returns:
        PDF file as bytes.
    """
    buf = io.BytesIO()
    meta = {
        "topic": topic,
        "user_name": user_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"FlashLearn AI - {topic}",
        author="FlashLearn AI",
        subject=f"{depth_level} flashcard deck for {user_name}",
    )

    st = _styles()
    elements: list = []

    # Cover
    elements.extend(
        _cover_elements(
            topic, depth_level, user_name,
            user_profession, user_sub_profession,
            len(cards), st,
        )
    )

    # Section header
    elements.append(
        Paragraph(
            f"  {depth_level} Flashcard Deck  ·  {len(cards)} Cards",
            st["section_head"]
        )
    )
    elements.append(HRFlowable(width="100%", thickness=0.5, color=_ACCENT_P))
    elements.append(Spacer(1, 4 * mm))

    # Cards grid
    elements.extend(_build_card_table(cards, st))

    def _canvas_maker(filename, **kwargs):
        return _ThemedCanvas(filename, meta=meta, **kwargs)

    doc.build(elements, canvasmaker=_canvas_maker)
    buf.seek(0)
    return buf.read()
