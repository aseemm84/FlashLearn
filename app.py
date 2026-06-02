# filepath: app.py
"""
FlashLearn AI - Main Entry Point
Orchestrates screen routing via Streamlit session state.
"""

import streamlit as st
from src.styles.theme import inject_global_css
from src.components.welcome import render_welcome_screen
from src.components.topic import render_topic_screen
from src.components.loading import render_loading_screen
from src.components.flashcards import render_flashcard_screen

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FlashLearn AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject global CSS / theme ──────────────────────────────────────────────────
inject_global_css()

# ── Session-state bootstrap ────────────────────────────────────────────────────
DEFAULTS = {
    "screen": "welcome",        # welcome | topic | loading | flashcards
    "user_name": "",
    "user_age": 18,
    "user_profession": "",
    "user_sub_profession": "",
    "topic": "",
    "depth_level": "Basic",
    "flashcards": [],           # list of {"question": ..., "answer": ...}
    "current_card": 0,
    "flipped": False,
    "error_message": "",
}

for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Router ─────────────────────────────────────────────────────────────────────
screen = st.session_state.screen

if screen == "welcome":
    render_welcome_screen()
elif screen == "topic":
    render_topic_screen()
elif screen == "loading":
    render_loading_screen()
elif screen == "flashcards":
    render_flashcard_screen()
