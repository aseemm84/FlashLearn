# filepath: src/components/welcome.py
"""
Screen 1 - Welcome Screen
Collects: Name, Age, Profession (dropdown) + dependent sub-profession dropdown.
Also auto-loads GROQ_API_KEY from st.secrets if available (for cloud deployment).
"""

import streamlit as st

# ── Profession → Sub-profession map ───────────────────────────────────────────
PROFESSION_MAP: dict[str, list[str]] = {
    "Student": [
        "Grade 1-5 (Primary)", "Grade 6-8 (Middle School)",
        "Grade 9-10 (High School Freshman/Sophomore)",
        "Grade 11-12 (High School Junior/Senior)",
        "Undergraduate (Year 1-2)", "Undergraduate (Year 3-4)",
        "Master's Student", "PhD / Doctoral Researcher",
    ],
    "Professional": [
        "Software Engineer / Developer", "Data Scientist / ML Engineer",
        "Product Manager", "UX / UI Designer", "DevOps / Cloud Engineer",
        "Cybersecurity Analyst", "Finance / Banking", "Marketing / Growth",
        "HR / People Operations", "Legal / Compliance",
        "Healthcare / Medicine", "Sales / Business Development",
        "Operations / Supply Chain", "Research Scientist",
    ],
    "Entrepreneur": [
        "Pre-Idea / Exploring", "Ideation Stage",
        "Early-Stage Startup (Seed)", "Growth-Stage Startup (Series A/B)",
        "SME Owner (Established Business)", "Social Entrepreneur",
        "Freelancer / Solopreneur",
    ],
    "Creative": [
        "Graphic Designer", "Video / Film Producer", "Writer / Author",
        "Musician / Audio Producer", "Animator / Motion Designer",
        "Photographer", "Game Designer", "Architect / Interior Designer",
    ],
    "Educator": [
        "Primary School Teacher", "Secondary School Teacher",
        "College / University Lecturer", "Corporate Trainer",
        "Curriculum Developer", "Online Course Creator",
        "Special Needs Educator",
    ],
    "Healthcare": [
        "Medical Doctor (General Practice)", "Specialist Physician",
        "Nurse / Midwife", "Pharmacist", "Dentist",
        "Physiotherapist / Occupational Therapist",
        "Mental Health Professional", "Nutritionist / Dietitian",
        "Medical Researcher",
    ],
    "Other": [
        "Retired", "Job Seeker", "Homemaker", "Hobbyist / Self-Learner",
        "Military / Defence", "Government / Public Sector",
        "Non-Profit / NGO", "Sports / Athletics", "Other",
    ],
}


def _load_api_key_from_secrets() -> str:
    """Attempt to load the Groq API key from Streamlit secrets (cloud deployment)."""
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        return key or ""
    except Exception:
        return ""


def render_welcome_screen() -> None:
    """Renders the Welcome / Profile collection screen."""

    # Auto-load key from secrets if not already set
    if not st.session_state.get("groq_api_key"):
        secret_key = _load_api_key_from_secrets()
        if secret_key:
            st.session_state["groq_api_key"] = secret_key

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="fl-badge">✦ AI-Powered Learning</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="fl-hero-title">Welcome to FlashLearn AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="fl-subtitle">Adaptive flashcards, tailored to <em>you</em>.</p>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── API Key sidebar ───────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        st.markdown(
            "<small style='color:#94A3B8'>Get a free key at "
            "<a href='https://console.groq.com' target='_blank' "
            "style='color:#A78BFA'>console.groq.com</a></small>",
            unsafe_allow_html=True,
        )
        current_key = st.session_state.get("groq_api_key", "")
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            value=current_key,
            help="Stored only in this browser session. Never logged or shared.",
        )
        if api_key:
            st.session_state["groq_api_key"] = api_key
            st.success("✓ Key saved for this session")
        elif _load_api_key_from_secrets():
            st.info("✓ Using key from app secrets")

        st.markdown("---")
        st.markdown("### 📖 About")
        st.markdown(
            "<small style='color:#94A3B8'>FlashLearn AI uses <strong>Llama 4 Scout</strong> "
            "via Groq to generate custom flashcard decks tailored to your age and background. "
            "100% free and open source.</small>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown(
            "<small style='color:#475569'>Built with Streamlit, Groq, "
            "ReportLab & Pillow.</small>",
            unsafe_allow_html=True,
        )

    # ── Profile Form ──────────────────────────────────────────────────────────
    st.markdown('<div class="fl-glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="fl-section-title">👤 Your Learning Profile</p>', unsafe_allow_html=True)
    st.markdown(
        "<small style='color:#94A3B8'>Help us personalise every flashcard just for you.</small>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(
            "Your Name",
            placeholder="e.g. Alex Rivera",
            value=st.session_state.get("user_name", ""),
        )
    with col2:
        age = st.number_input(
            "Age",
            min_value=6,
            max_value=100,
            step=1,
            value=int(st.session_state.get("user_age", 18)),
        )

    professions = list(PROFESSION_MAP.keys())
    prev_profession = st.session_state.get("user_profession", "")
    default_prof_idx = professions.index(prev_profession) if prev_profession in professions else 0

    profession = st.selectbox(
        "Profession Category",
        options=professions,
        index=default_prof_idx,
    )

    sub_options = PROFESSION_MAP[profession]
    prev_sub = st.session_state.get("user_sub_profession", "")
    default_sub_idx = sub_options.index(prev_sub) if prev_sub in sub_options else 0

    sub_profession = st.selectbox(
        "Specialisation / Role",
        options=sub_options,
        index=default_sub_idx,
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Validation + CTA ──────────────────────────────────────────────────────
    groq_key_set = bool(st.session_state.get("groq_api_key", "").strip())

    if not groq_key_set:
        st.markdown(
            '<div class="fl-error-box">⚠️ Please enter your free Groq API key '
            'in the sidebar to continue. '
            '<a href="https://console.groq.com" target="_blank" '
            'style="color:#FCA5A5; text-decoration:underline;">Get one free →</a>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

    # Error message from a previous failed generation
    if st.session_state.get("error_message"):
        st.markdown(
            f'<div class="fl-error-box">{st.session_state.error_message}</div>',
            unsafe_allow_html=True,
        )
        st.session_state.error_message = ""
        st.markdown("<br>", unsafe_allow_html=True)

    btn_col, _ = st.columns([1, 2])
    with btn_col:
        if st.button(
            "Continue →",
            disabled=not groq_key_set,
            use_container_width=True,
            key="welcome_cta",
        ):
            if not name.strip():
                st.error("Please enter your name to continue.")
            else:
                st.session_state.user_name = name.strip()
                st.session_state.user_age = int(age)
                st.session_state.user_profession = profession
                st.session_state.user_sub_profession = sub_profession
                st.session_state.screen = "topic"
                st.rerun()

    # ── Feature Highlights ────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    _feature_card(c1, "🧠", "Age-Adaptive AI", "Content difficulty tuned to your age and background.")
    _feature_card(c2, "⚡", "Instant Generation", "30 flashcards in under 10 seconds with Llama 4.")
    _feature_card(c3, "📤", "Export Anywhere", "Save cards as PNG images or download the full PDF deck.")


def _feature_card(col, icon: str, title: str, desc: str) -> None:
    col.markdown(
        f"""
        <div class="fl-glass-card" style="text-align:center; padding:1.4rem 1rem;">
          <div style="font-size:2rem; margin-bottom:0.6rem;">{icon}</div>
          <div style="font-family:var(--font-display); font-weight:600;
                      font-size:0.95rem; color:var(--text-primary);
                      margin-bottom:0.35rem;">{title}</div>
          <div style="font-size:0.82rem; color:var(--text-secondary);
                      line-height:1.5;">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
