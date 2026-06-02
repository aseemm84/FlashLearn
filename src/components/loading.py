# filepath: src/components/loading.py
"""
Screen 3 - Loading Screen
Calls the Groq API, shows animated spinner, handles errors gracefully.
"""

import time
import threading
import streamlit as st
from src.api.groq_client import generate_flashcards, DEPTH_CARD_COUNT


_LOADING_TIPS = [
    "🧠  Analysing your learning profile...",
    "📐  Structuring cards in pedagogical order...",
    "✍️   Writing concise, personalised answers...",
    "🎨  Polishing your custom deck...",
    "⚡  Almost there — finalising cards...",
]


def render_loading_screen() -> None:
    """Calls the API and transitions to the flashcard screen (or shows an error)."""

    topic = st.session_state.topic
    depth = st.session_state.depth_level
    card_count = DEPTH_CARD_COUNT.get(depth, 15)

    # ── Animated loading UI ───────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="fl-loader-wrap">
          <div class="fl-loader-orbit"></div>
          <div>
            <div class="fl-hero-title" style="font-size:1.8rem; margin-bottom:0.5rem;">
              Crafting Your Deck
            </div>
            <div class="fl-subtitle">
              Generating <strong style="color:#A78BFA">{card_count} flashcards</strong>
              on <em>{topic}</em>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tip_placeholder = st.empty()

    def _show_tip(i: int):
        tip = _LOADING_TIPS[i % len(_LOADING_TIPS)]
        tip_placeholder.markdown(
            f'<div class="fl-loader-text" style="text-align:center">{tip}</div>',
            unsafe_allow_html=True,
        )

    _show_tip(0)

    # ── API Call ──────────────────────────────────────────────────────────────
    api_key = st.session_state.get("groq_api_key", "")

    # Rotate tips while waiting
    tip_index = [1]
    stop_flag = [False]

    def _tip_rotator():
        while not stop_flag[0]:
            time.sleep(2)
            if not stop_flag[0]:
                _show_tip(tip_index[0])
                tip_index[0] += 1

    t = threading.Thread(target=_tip_rotator, daemon=True)
    t.start()

    try:
        cards = generate_flashcards(
            api_key=api_key,
            name=st.session_state.user_name,
            age=st.session_state.user_age,
            profession=st.session_state.user_profession,
            sub_profession=st.session_state.user_sub_profession,
            topic=topic,
            depth_level=depth,
        )
        stop_flag[0] = True
        st.session_state.flashcards = cards
        st.session_state.current_card = 0
        st.session_state.flipped = False
        st.session_state.screen = "flashcards"
        st.rerun()

    except RuntimeError as e:
        stop_flag[0] = True
        st.session_state.error_message = str(e)
        st.session_state.screen = "topic"
        st.rerun()

    except Exception as e:
        stop_flag[0] = True
        st.session_state.error_message = f"Unexpected error: {e}"
        st.session_state.screen = "topic"
        st.rerun()
