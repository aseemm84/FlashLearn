# filepath: src/components/topic.py
"""
Screen 2 - Topic & Depth Selection
Lets the user choose what to learn and at what depth.
"""

import streamlit as st
from src.components.welcome import render_creator_footer

DEPTH_CONFIG = {
    "Basic":        {"cards": 15, "icon": "🌱", "desc": "Core concepts, perfect starting point"},
    "Intermediate": {"cards": 20, "icon": "🔥", "desc": "Builds on fundamentals, adds nuance"},
    "Advanced":     {"cards": 25, "icon": "⚡", "desc": "In-depth coverage, practical details"},
    "Deep Dive":    {"cards": 30, "icon": "🚀", "desc": "Comprehensive mastery-level deck"},
}

TOPIC_SUGGESTIONS = [
    "Quantum Computing", "Machine Learning Basics", "The Human Brain",
    "Climate Change", "Blockchain & Web3", "Ancient Roman History",
    "Personal Finance", "CRISPR Gene Editing", "Stoic Philosophy",
    "The Big Bang Theory", "Prompt Engineering", "Sleep Science",
]


def render_topic_screen() -> None:
    """Renders the Topic & Depth selection screen."""

    # ── Back nav ──────────────────────────────────────────────────────────────
    if st.button("← Back", key="topic_back"):
        st.session_state.screen = "welcome"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Greeting ──────────────────────────────────────────────────────────────
    name = st.session_state.user_name
    profession = st.session_state.user_profession
    sub = st.session_state.user_sub_profession
    age = st.session_state.user_age

    st.markdown('<div class="fl-badge">✦ Step 2 of 2</div>', unsafe_allow_html=True)
    st.markdown(
        f'<h1 class="fl-hero-title">What shall we learn,<br>{name}?</h1>',
        unsafe_allow_html=True,
    )

    # Stat chips
    st.markdown(
        f"""
        <div class="stat-row">
          <div class="stat-chip">👤 <strong>{name}</strong></div>
          <div class="stat-chip">🎂 <strong>Age {age}</strong></div>
          <div class="stat-chip">💼 <strong>{profession}</strong> · {sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Topic Input ───────────────────────────────────────────────────────────
    st.markdown('<div class="fl-glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="fl-section-title">📚 Learning Topic</p>', unsafe_allow_html=True)

    topic = st.text_input(
        "Enter any topic you want to master",
        placeholder="e.g. Quantum Computing, Stoic Philosophy, Neural Networks...",
        value=st.session_state.get("topic", ""),
        label_visibility="collapsed",
    )

    # Quick-pick suggestions
    st.markdown(
        "<small style='color:#64748B; font-size:0.8rem;'>✦ Quick picks:</small>",
        unsafe_allow_html=True,
    )
    suggestion_cols = st.columns(4)
    for idx, suggestion in enumerate(TOPIC_SUGGESTIONS):
        with suggestion_cols[idx % 4]:
            if st.button(
                suggestion,
                key=f"sugg_{idx}",
                use_container_width=True,
            ):
                st.session_state.topic = suggestion
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Depth Level ───────────────────────────────────────────────────────────
    st.markdown('<div class="fl-glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="fl-section-title">🎯 Depth Level</p>', unsafe_allow_html=True)
    st.markdown(
        "<small style='color:#94A3B8'>How deep should we go?</small>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    depth_keys = list(DEPTH_CONFIG.keys())
    prev_depth = st.session_state.get("depth_level", "Basic")
    prev_idx = depth_keys.index(prev_depth) if prev_depth in depth_keys else 0

    depth_level = st.radio(
        "Depth",
        options=depth_keys,
        index=prev_idx,
        label_visibility="collapsed",
        horizontal=True,
    )

    # Show description for selected level
    cfg = DEPTH_CONFIG[depth_level]
    st.markdown(
        f"""
        <div style="margin-top:0.8rem; padding:0.75rem 1rem;
                    background:rgba(124,58,237,0.10);
                    border:1px solid rgba(124,58,237,0.25);
                    border-radius:10px; display:flex; gap:0.6rem;
                    align-items:center;">
          <span style="font-size:1.3rem">{cfg['icon']}</span>
          <span>
            <strong style="color:var(--text-primary)">{depth_level}</strong>
            <span style="color:var(--text-secondary); font-size:0.88rem">
              · {cfg['cards']} cards · {cfg['desc']}
            </span>
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Generate CTA ──────────────────────────────────────────────────────────
    actual_topic = topic.strip() or st.session_state.get("topic", "").strip()
    cta_col, _ = st.columns([1, 2])
    with cta_col:
        if st.button(
            f"⚡ Generate {cfg['cards']} Flashcards",
            disabled=not actual_topic,
            use_container_width=True,
            key="generate_cta",
        ):
            st.session_state.topic = actual_topic
            st.session_state.depth_level = depth_level
            st.session_state.screen = "loading"
            st.session_state.flashcards = []
            st.session_state.current_card = 0
            st.session_state.flipped = False
            st.session_state.error_message = ""
            st.rerun()

    if not actual_topic:
        st.markdown(
            "<small style='color:#64748B'>↑ Enter a topic to unlock generation</small>",
            unsafe_allow_html=True,
        )

    # ── Creator footer ────────────────────────────────────────────────────────
    render_creator_footer()
