# filepath: src/components/welcome.py
"""
Screen 1 - Welcome Screen
Collects: Name, Age, Profession (dropdown) + dependent sub-profession dropdown.
Also auto-loads GROQ_API_KEY from st.secrets if available (for cloud deployment).
"""

import streamlit as st

# ── Creator branding constants ─────────────────────────────────────────────────
_CREATOR_NAME     = "Aseem Mehrotra"
_CREATOR_TITLE    = "Data & AI Builder · Ex-ADNOC · FinTech & Data Science"
_CREATOR_LINKEDIN = "https://www.linkedin.com/in/aseem-mehrotra/"
_CREATOR_GITHUB   = "https://github.com/aseemm84"
_CREATOR_LOCATION = "Abu Dhabi, UAE"

# ── Shared footer injected on every screen ─────────────────────────────────────
_FOOTER_HTML = f"""
<style>
  /* ── Creator footer ── */
  .fl-creator-footer {{
    margin-top: 3rem;
    padding: 1.4rem 2rem;
    border-top: 1px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.8rem;
  }}
  .fl-creator-left {{
    display: flex;
    align-items: center;
    gap: 0.9rem;
  }}
  .fl-creator-avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7C3AED, #06B6D4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
    letter-spacing: -0.5px;
  }}
  .fl-creator-info {{
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
  }}
  .fl-creator-byline {{
    font-size: 0.72rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
  }}
  .fl-creator-name {{
    font-size: 0.92rem;
    font-weight: 700;
    color: #CBD5E1;
  }}
  .fl-creator-role {{
    font-size: 0.76rem;
    color: #475569;
  }}
  .fl-creator-links {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }}
  .fl-social-btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.38rem 0.85rem;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 600;
    text-decoration: none !important;
    transition: all 0.2s ease;
    border: 1px solid;
  }}
  .fl-social-btn.linkedin {{
    background: rgba(10, 102, 194, 0.12);
    border-color: rgba(10, 102, 194, 0.35);
    color: #60A5FA !important;
  }}
  .fl-social-btn.linkedin:hover {{
    background: rgba(10, 102, 194, 0.25);
    border-color: rgba(10, 102, 194, 0.65);
    transform: translateY(-1px);
  }}
  .fl-social-btn.github {{
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.12);
    color: #94A3B8 !important;
  }}
  .fl-social-btn.github:hover {{
    background: rgba(255,255,255,0.10);
    border-color: rgba(255,255,255,0.25);
    color: #F1F5F9 !important;
    transform: translateY(-1px);
  }}
  /* ── Sidebar creator card ── */
  .fl-sidebar-creator {{
    margin-top: 0.5rem;
    padding: 1rem 0.8rem;
    background: rgba(124,58,237,0.06);
    border: 1px solid rgba(124,58,237,0.18);
    border-radius: 12px;
  }}
  .fl-sidebar-creator-name {{
    font-size: 0.88rem;
    font-weight: 700;
    color: #CBD5E1;
    margin-bottom: 0.15rem;
  }}
  .fl-sidebar-creator-role {{
    font-size: 0.73rem;
    color: #64748B;
    line-height: 1.4;
    margin-bottom: 0.7rem;
  }}
  .fl-sidebar-links {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }}
  .fl-sidebar-link {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.28rem 0.7rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    text-decoration: none !important;
    border: 1px solid;
  }}
  .fl-sidebar-link.li {{
    background: rgba(10,102,194,0.10);
    border-color: rgba(10,102,194,0.30);
    color: #60A5FA !important;
  }}
  .fl-sidebar-link.gh {{
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.12);
    color: #94A3B8 !important;
  }}
  .fl-sidebar-link:hover {{
    filter: brightness(1.2);
    transform: translateY(-1px);
  }}
</style>

<div class="fl-creator-footer">
  <div class="fl-creator-left">
    <div class="fl-creator-avatar">AM</div>
    <div class="fl-creator-info">
      <span class="fl-creator-byline">Built by</span>
      <span class="fl-creator-name">{_CREATOR_NAME}</span>
      <span class="fl-creator-role">{_CREATOR_TITLE}</span>
    </div>
  </div>
  <div class="fl-creator-links">
    <a href="{_CREATOR_LINKEDIN}" target="_blank" class="fl-social-btn linkedin">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
      </svg>
      LinkedIn
    </a>
    <a href="{_CREATOR_GITHUB}" target="_blank" class="fl-social-btn github">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
      </svg>
      GitHub
    </a>
  </div>
</div>
"""

# ── Sidebar creator card HTML ──────────────────────────────────────────────────
_SIDEBAR_CREATOR_HTML = f"""
<div class="fl-sidebar-creator">
  <div class="fl-sidebar-creator-name">👨‍💻 {_CREATOR_NAME}</div>
  <div class="fl-sidebar-creator-role">{_CREATOR_TITLE}<br>{_CREATOR_LOCATION}</div>
  <div class="fl-sidebar-links">
    <a href="{_CREATOR_LINKEDIN}" target="_blank" class="fl-sidebar-link li">
      <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor">
        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
      </svg>
      LinkedIn
    </a>
    <a href="{_CREATOR_GITHUB}" target="_blank" class="fl-sidebar-link gh">
      <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
      </svg>
      GitHub
    </a>
  </div>
</div>
"""


def render_creator_footer() -> None:
    """Renders the persistent creator branding footer. Call at the end of every screen."""
    st.markdown(_FOOTER_HTML, unsafe_allow_html=True)

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
    # Subtle creator credit directly under the hero tagline
    st.markdown(
        f"""
        <p style="text-align:center; font-size:0.78rem; color:#334155;
                  margin-top:0.5rem; margin-bottom:0;">
          Crafted by
          <a href="{_CREATOR_LINKEDIN}" target="_blank"
             style="color:#7C3AED; text-decoration:none; font-weight:600;">
            {_CREATOR_NAME}
          </a>
          &nbsp;·&nbsp;
          <a href="{_CREATOR_GITHUB}" target="_blank"
             style="color:#475569; text-decoration:none;">
            View on GitHub ↗
          </a>
        </p>
        """,
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
        # ── Creator card in sidebar ───────────────────────────────────────────
        st.markdown("### 👨‍💻 About the Creator")
        st.markdown(_SIDEBAR_CREATOR_HTML, unsafe_allow_html=True)
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

    # ── Creator footer ────────────────────────────────────────────────────────
    render_creator_footer()


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
