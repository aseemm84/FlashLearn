# filepath: src/styles/theme.py
"""
Global CSS Injection
Glassmorphism dark theme with Google Fonts (Outfit + Space Grotesk).
Includes card flip animation, button hover effects, and gradient backgrounds.
"""

import streamlit as st

_CSS = """
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* ── CSS Variables ────────────────────────────────────────────────────────── */
:root {
  --bg-primary:      #0A0A0F;
  --bg-secondary:    #12121A;
  --bg-card:         rgba(255,255,255,0.04);
  --bg-card-hover:   rgba(255,255,255,0.08);
  --border-glass:    rgba(255,255,255,0.10);
  --border-glow:     rgba(124,58,237,0.50);
  --accent-purple:   #7C3AED;
  --accent-violet:   #9333EA;
  --accent-cyan:     #06B6D4;
  --accent-pink:     #EC4899;
  --text-primary:    #F1F5F9;
  --text-secondary:  #94A3B8;
  --text-muted:      #475569;
  --gradient-main:   linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%);
  --gradient-card:   linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(6,182,212,0.10) 100%);
  --shadow-glow:     0 0 40px rgba(124,58,237,0.25);
  --shadow-card:     0 8px 32px rgba(0,0,0,0.40);
  --radius-lg:       16px;
  --radius-xl:       24px;
  --transition:      all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --font-main:       'Outfit', sans-serif;
  --font-display:    'Space Grotesk', sans-serif;
}

/* ── Reset & Base ─────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
  background: var(--bg-primary) !important;
  font-family: var(--font-main) !important;
  color: var(--text-primary) !important;
  min-height: 100vh;
}

/* ── Animated Mesh Background ─────────────────────────────────────────────── */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 40%, rgba(124,58,237,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 70%, rgba(6,182,212,0.09) 0%, transparent 55%),
    radial-gradient(ellipse 50% 60% at 50% 10%, rgba(236,72,153,0.06) 0%, transparent 50%);
  animation: meshPulse 10s ease-in-out infinite alternate;
  pointer-events: none;
  z-index: 0;
}

@keyframes meshPulse {
  0%   { opacity: 0.7; transform: scale(1); }
  100% { opacity: 1.0; transform: scale(1.05); }
}

/* ── Hide Streamlit Chrome ────────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
  padding-top: 2rem !important;
  padding-bottom: 3rem !important;
  max-width: 960px !important;
  position: relative;
  z-index: 1;
}

/* ── Typography ───────────────────────────────────────────────────────────── */
h1, h2, h3, h4 { font-family: var(--font-display) !important; }

.fl-hero-title {
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 6vw, 4rem);
  font-weight: 800;
  background: var(--gradient-main);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.15;
  letter-spacing: -0.02em;
  text-align: center;
}

.fl-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  text-align: center;
  margin-top: 0.5rem;
  font-weight: 400;
}

.fl-section-title {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.fl-badge {
  display: inline-block;
  padding: 0.25rem 0.85rem;
  border-radius: 99px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: rgba(124,58,237,0.18);
  color: #A78BFA;
  border: 1px solid rgba(124,58,237,0.35);
  margin-bottom: 1.2rem;
}

/* ── Glass Card ───────────────────────────────────────────────────────────── */
.fl-glass-card {
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-xl);
  padding: 2rem 2.2rem;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: var(--shadow-card);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.fl-glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-card);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.fl-glass-card:hover::before { opacity: 1; }
.fl-glass-card:hover {
  border-color: var(--border-glow);
  box-shadow: var(--shadow-glow), var(--shadow-card);
  transform: translateY(-2px);
}

/* ── Streamlit Input Overrides ────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
  font-family: var(--font-main) !important;
  font-size: 0.95rem !important;
  transition: var(--transition) !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--accent-purple) !important;
  box-shadow: 0 0 0 3px rgba(124,58,237,0.20) !important;
}

.stTextInput label,
.stSelectbox label,
.stNumberInput label,
.stRadio label,
.stSlider label {
  color: var(--text-secondary) !important;
  font-family: var(--font-main) !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.03em !important;
  text-transform: uppercase !important;
  margin-bottom: 0.4rem !important;
}

/* ── Buttons ──────────────────────────────────────────────────────────────── */
.stButton > button {
  background: var(--gradient-main) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: var(--font-display) !important;
  font-size: 0.95rem !important;
  font-weight: 600 !important;
  padding: 0.6rem 1.6rem !important;
  cursor: pointer !important;
  transition: var(--transition) !important;
  letter-spacing: 0.02em !important;
  box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
  position: relative !important;
  overflow: hidden !important;
  width: 100% !important;
}

.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(124,58,237,0.55) !important;
  filter: brightness(1.1) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
}

/* ── Download Button ──────────────────────────────────────────────────────── */
.stDownloadButton > button {
  background: rgba(6,182,212,0.15) !important;
  color: var(--accent-cyan) !important;
  border: 1px solid rgba(6,182,212,0.40) !important;
  border-radius: 12px !important;
  font-family: var(--font-display) !important;
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  padding: 0.5rem 1.2rem !important;
  transition: var(--transition) !important;
  width: 100% !important;
}

.stDownloadButton > button:hover {
  background: rgba(6,182,212,0.28) !important;
  border-color: var(--accent-cyan) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 24px rgba(6,182,212,0.30) !important;
}

/* ── Progress Bar ─────────────────────────────────────────────────────────── */
.stProgress > div > div > div > div {
  background: var(--gradient-main) !important;
  border-radius: 99px !important;
}
.stProgress > div > div {
  background: rgba(255,255,255,0.08) !important;
  border-radius: 99px !important;
  height: 6px !important;
}

/* ── Radio Buttons ────────────────────────────────────────────────────────── */
.stRadio > div {
  display: flex !important;
  gap: 0.6rem !important;
  flex-wrap: wrap !important;
}
.stRadio > div > label {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid var(--border-glass) !important;
  border-radius: 10px !important;
  padding: 0.5rem 1rem !important;
  cursor: pointer !important;
  transition: var(--transition) !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  color: var(--text-secondary) !important;
  font-size: 0.9rem !important;
}
.stRadio > div > label:hover {
  border-color: var(--accent-purple) !important;
  color: var(--text-primary) !important;
}

/* ── Divider ──────────────────────────────────────────────────────────────── */
hr {
  border: none !important;
  border-top: 1px solid var(--border-glass) !important;
  margin: 1.5rem 0 !important;
}

/* ── Spinner ──────────────────────────────────────────────────────────────── */
.stSpinner > div {
  border-top-color: var(--accent-purple) !important;
}

/* ── 3-D Flip Card ────────────────────────────────────────────────────────── */
.flip-card-scene {
  width: 100%;
  min-height: 260px;
  perspective: 1200px;
  cursor: pointer;
  user-select: none;
  margin: 1rem 0;
}

.flip-card {
  width: 100%;
  height: 100%;
  min-height: 260px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.65s cubic-bezier(0.4, 0.2, 0.2, 1);
}

.flip-card.is-flipped {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: var(--radius-xl);
  padding: 2rem 2.4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  border: 1px solid var(--border-glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: var(--shadow-card);
}

.flip-card-front {
  background: linear-gradient(135deg,
    rgba(124,58,237,0.18) 0%,
    rgba(12,12,22,0.85) 50%,
    rgba(6,182,212,0.12) 100%);
}

.flip-card-back {
  background: linear-gradient(135deg,
    rgba(6,182,212,0.18) 0%,
    rgba(12,12,22,0.85) 50%,
    rgba(236,72,153,0.12) 100%);
  transform: rotateY(180deg);
}

.flip-card-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 1.1rem;
  padding: 0.25rem 0.9rem;
  border-radius: 99px;
}

.flip-card-front .flip-card-label {
  background: rgba(124,58,237,0.25);
  color: #A78BFA;
  border: 1px solid rgba(124,58,237,0.40);
}

.flip-card-back .flip-card-label {
  background: rgba(6,182,212,0.20);
  color: #67E8F9;
  border: 1px solid rgba(6,182,212,0.40);
}

.flip-card-text {
  font-family: var(--font-display);
  font-size: clamp(1rem, 2.2vw, 1.25rem);
  font-weight: 500;
  line-height: 1.55;
  color: var(--text-primary);
}

.flip-hint {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

/* ── Card Counter ─────────────────────────────────────────────────────────── */
.card-counter {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.card-counter-num {
  font-family: var(--font-display);
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 600;
}
.card-counter-sep {
  color: var(--text-muted);
}

/* ── Nav Dots ─────────────────────────────────────────────────────────────── */
.nav-dots {
  display: flex;
  justify-content: center;
  gap: 0.45rem;
  margin: 0.8rem 0;
  flex-wrap: wrap;
}
.nav-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--text-muted);
  display: inline-block;
  transition: var(--transition);
}
.nav-dot.active {
  background: var(--accent-purple);
  box-shadow: 0 0 8px var(--accent-purple);
  transform: scale(1.35);
}
.nav-dot.visited {
  background: rgba(124,58,237,0.45);
}

/* ── Loading Screen ───────────────────────────────────────────────────────── */
.fl-loader-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 1.5rem;
}

.fl-loader-orbit {
  width: 80px; height: 80px;
  border-radius: 50%;
  border: 3px solid transparent;
  border-top-color: var(--accent-purple);
  border-right-color: var(--accent-cyan);
  animation: orbit 1.1s linear infinite;
  position: relative;
}

.fl-loader-orbit::after {
  content: '⚡';
  font-size: 1.6rem;
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}

@keyframes orbit {
  to { transform: rotate(360deg); }
}

.fl-loader-text {
  font-family: var(--font-display);
  font-size: 1.05rem;
  color: var(--text-secondary);
  animation: loadingPulse 1.8s ease-in-out infinite;
}

@keyframes loadingPulse {
  0%, 100% { opacity: 0.5; }
  50%       { opacity: 1.0; }
}

/* ── Stat Chips ───────────────────────────────────────────────────────────── */
.stat-row {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin: 1rem 0;
}
.stat-chip {
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border-glass);
  border-radius: 10px;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.stat-chip strong {
  color: var(--text-primary);
  font-weight: 600;
}

/* ── Error Box ────────────────────────────────────────────────────────────── */
.fl-error-box {
  background: rgba(239,68,68,0.12);
  border: 1px solid rgba(239,68,68,0.35);
  border-radius: var(--radius-lg);
  padding: 1.2rem 1.6rem;
  color: #FCA5A5;
  font-size: 0.95rem;
  line-height: 1.55;
}

/* ── Success Box ──────────────────────────────────────────────────────────── */
.fl-success-box {
  background: rgba(16,185,129,0.12);
  border: 1px solid rgba(16,185,129,0.35);
  border-radius: var(--radius-lg);
  padding: 1rem 1.4rem;
  color: #6EE7B7;
  font-size: 0.9rem;
}

/* ── Scrollbar ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb {
  background: rgba(124,58,237,0.45);
  border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent-purple); }

/* ── Responsive ───────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
  .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
  .fl-glass-card { padding: 1.4rem 1.2rem; }
  .flip-card-text { font-size: 0.95rem; }
}
"""


def inject_global_css() -> None:
    """Injects the global CSS stylesheet into the Streamlit app."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
