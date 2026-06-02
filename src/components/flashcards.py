# filepath: src/components/flashcards.py
"""
Screen 4 - Flashcard Viewer
3-D CSS flip animation, navigation, PNG save, and PDF download.
"""

import streamlit as st
from src.export.image_export import card_to_png_bytes
from src.export.pdf_export import deck_to_pdf_bytes
from src.components.welcome import render_creator_footer


def render_flashcard_screen() -> None:
    """Main flashcard viewer with flip animation and export actions."""

    cards: list[dict] = st.session_state.flashcards
    if not cards:
        st.error("No flashcards found. Please go back and generate a deck.")
        if st.button("← Back to Topics"):
            st.session_state.screen = "topic"
            st.rerun()
        return

    total = len(cards)
    idx: int = st.session_state.current_card
    flipped: bool = st.session_state.flipped
    current = cards[idx]

    # ── Header row ────────────────────────────────────────────────────────────
    col_back, col_title, col_restart = st.columns([1, 4, 1])
    with col_back:
        if st.button("← New Topic", key="fc_back"):
            st.session_state.screen = "topic"
            st.session_state.flipped = False
            st.rerun()
    with col_title:
        st.markdown(
            f"""
            <div style="text-align:center;">
              <div class="fl-badge">⚡ {st.session_state.depth_level} Deck</div>
              <div class="fl-hero-title" style="font-size:1.6rem;">
                {st.session_state.topic}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_restart:
        if st.button("↺ Restart", key="fc_restart"):
            st.session_state.current_card = 0
            st.session_state.flipped = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Progress ──────────────────────────────────────────────────────────────
    st.progress((idx + 1) / total)
    st.markdown(
        f"""
        <div class="card-counter">
          <span class="card-counter-num">Card {idx + 1}</span>
          <span class="card-counter-sep">/</span>
          <span class="card-counter-num" style="color:var(--text-muted)">{total}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Nav Dots ──────────────────────────────────────────────────────────────
    dots_html = '<div class="nav-dots">'
    for i in range(total):
        cls = "active" if i == idx else ("visited" if i < idx else "nav-dot")
        dots_html += f'<span class="nav-dot {cls}"></span>'
    dots_html += "</div>"
    st.markdown(dots_html, unsafe_allow_html=True)

    # ── 3-D Flip Card ─────────────────────────────────────────────────────────
    flipped_class = "is-flipped" if flipped else ""
    q_text = current["question"]
    a_text = current["answer"]

    card_html = f"""
    <div class="flip-card-scene" id="fc-scene" onclick="
      const c = document.getElementById('fc-inner');
      c.classList.toggle('is-flipped');
    ">
      <div class="flip-card {flipped_class}" id="fc-inner">
        <div class="flip-card-front">
          <span class="flip-card-label">Question</span>
          <p class="flip-card-text">{q_text}</p>
          <span class="flip-hint">🖱️ Click to reveal answer</span>
        </div>
        <div class="flip-card-back">
          <span class="flip-card-label">Answer</span>
          <p class="flip-card-text">{a_text}</p>
          <span class="flip-hint">🖱️ Click to see question</span>
        </div>
      </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # Streamlit flip toggle button
    flip_col, _ = st.columns([1, 3])
    with flip_col:
        flip_label = "👁 Show Answer" if not flipped else "🔄 Show Question"
        if st.button(flip_label, key="flip_btn", use_container_width=True):
            st.session_state.flipped = not flipped
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Navigation Buttons ────────────────────────────────────────────────────
    nav_prev, nav_mid, nav_next = st.columns([1, 2, 1])

    with nav_prev:
        if st.button("← Prev", disabled=(idx == 0), key="nav_prev", use_container_width=True):
            st.session_state.current_card = idx - 1
            st.session_state.flipped = False
            st.rerun()

    with nav_mid:
        st.markdown(
            f"<div style='text-align:center; color:var(--text-muted); "
            f"font-size:0.82rem; padding-top:0.6rem;'>"
            f"{idx + 1} of {total} cards</div>",
            unsafe_allow_html=True,
        )

    with nav_next:
        if idx < total - 1:
            if st.button("Next →", key="nav_next", use_container_width=True):
                st.session_state.current_card = idx + 1
                st.session_state.flipped = False
                st.rerun()
        else:
            st.markdown(
                '<div style="text-align:center; font-size:1.5rem; padding-top:0.2rem;">🎉</div>',
                unsafe_allow_html=True,
            )

    # ── End-of-deck celebration ───────────────────────────────────────────────
    if idx == total - 1:
        st.markdown(
            """
            <div class="fl-success-box" style="text-align:center; margin-top:1rem;">
              🎉 <strong>You've completed the entire deck!</strong>
              Hit ↺ Restart to review again, or ← New Topic for a fresh deck.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Export Section ────────────────────────────────────────────────────────
    st.markdown(
        '<p class="fl-section-title" style="margin-bottom:0.8rem;">📤 Export</p>',
        unsafe_allow_html=True,
    )
    exp_col1, exp_col2 = st.columns(2)

    # ── Save Current Card as PNG ──────────────────────────────────────────────
    with exp_col1:
        st.markdown(
            "<small style='color:#94A3B8'>Save this card as a styled image</small>",
            unsafe_allow_html=True,
        )
        try:
            png_bytes = card_to_png_bytes(
                question=current["question"],
                answer=current["answer"],
                topic=st.session_state.topic,
                card_num=idx + 1,
                total=total,
                user_name=st.session_state.user_name,
            )
            safe_topic = st.session_state.topic.replace(" ", "_")[:30]
            st.download_button(
                label="🖼 Save Card as PNG",
                data=png_bytes,
                file_name=f"flashlearn_{safe_topic}_card_{idx+1}.png",
                mime="image/png",
                key=f"png_dl_{idx}",
                use_container_width=True,
            )
        except Exception as e:
            st.markdown(
                f'<div class="fl-error-box">PNG export error: {e}</div>',
                unsafe_allow_html=True,
            )

    # ── Download Full Deck as PDF ─────────────────────────────────────────────
    with exp_col2:
        st.markdown(
            "<small style='color:#94A3B8'>Download the complete deck as PDF</small>",
            unsafe_allow_html=True,
        )
        try:
            pdf_bytes = deck_to_pdf_bytes(
                cards=cards,
                topic=st.session_state.topic,
                depth_level=st.session_state.depth_level,
                user_name=st.session_state.user_name,
                user_profession=st.session_state.user_profession,
                user_sub_profession=st.session_state.user_sub_profession,
            )
            safe_topic = st.session_state.topic.replace(" ", "_")[:30]
            st.download_button(
                label="📄 Download Full Deck (PDF)",
                data=pdf_bytes,
                file_name=f"flashlearn_{safe_topic}_{st.session_state.depth_level}.pdf",
                mime="application/pdf",
                key="pdf_dl",
                use_container_width=True,
            )
        except Exception as e:
            st.markdown(
                f'<div class="fl-error-box">PDF export error: {e}</div>',
                unsafe_allow_html=True,
            )

    # ── Deck Overview ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 View Full Deck Overview", expanded=False):
        for i, card in enumerate(cards):
            active_style = (
                "border-color:rgba(124,58,237,0.55); "
                "background:rgba(124,58,237,0.08);"
                if i == idx else ""
            )
            st.markdown(
                f"""
                <div class="fl-glass-card" style="margin-bottom:0.75rem;
                     padding:1rem 1.3rem; cursor:default; {active_style}">
                  <div style="font-size:0.72rem; font-weight:700; letter-spacing:0.12em;
                               text-transform:uppercase; color:#A78BFA;
                               margin-bottom:0.4rem;">Card {i+1}</div>
                  <div style="font-weight:600; color:var(--text-primary);
                               font-size:0.9rem; margin-bottom:0.3rem;">
                    Q: {card['question']}
                  </div>
                  <div style="color:var(--text-secondary); font-size:0.85rem; line-height:1.5;">
                    A: {card['answer']}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Go to card {i+1}", key=f"goto_{i}"):
                st.session_state.current_card = i
                st.session_state.flipped = False
                st.rerun()

    # ── Creator footer ────────────────────────────────────────────────────────
    render_creator_footer()
