# ⚡ FlashLearn AI

> **AI-powered adaptive flashcards — $0 budget, production-grade quality.**

FlashLearn AI generates personalised flashcard decks using **Llama 4 Scout via the free Groq API**.
Cards are tailored to your **age, profession, and chosen depth level**.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🧠 Adaptive AI | Cards adapt to age (6–100) and profession |
| 📐 4 Depth Levels | Basic (15) → Deep Dive (30 cards) |
| 🎴 3-D Flip Cards | Pure-CSS perspective flip animation |
| 🖼 PNG Export | Save any card as a styled image (Pillow) |
| 📄 PDF Export | Full deck as a themed PDF (ReportLab) |
| 🎨 Glassmorphism UI | Dark theme, Space Grotesk / Outfit fonts |
| 💸 $0 Cost | Groq free tier + Streamlit Community Cloud |

---

## 🗂 Project Structure

```
flashlearn-ai/
├── app.py                    # Entry point + router
├── requirements.txt
├── .streamlit/
│   └── config.toml           # Dark theme config
└── src/
    ├── api/
    │   └── groq_client.py    # Groq API + rate-limit handling
    ├── components/
    │   ├── welcome.py        # Screen 1 – Profile collection
    │   ├── topic.py          # Screen 2 – Topic + depth
    │   ├── loading.py        # Screen 3 – Animated loader
    │   └── flashcards.py     # Screen 4 – Flip cards + export
    ├── export/
    │   ├── image_export.py   # Pillow PNG card export
    │   └── pdf_export.py     # ReportLab PDF deck export
    └── styles/
        └── theme.py          # Global CSS / glassmorphism
```

---

## ⚡ Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Free Groq API Key

1. Visit https://console.groq.com
2. Sign up (free, no credit card needed)
3. Create API Key (starts with `gsk_...`)

### 3. Run

```bash
streamlit run app.py
```

Enter your API key in the sidebar when the app opens.

---

## 🌐 Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to https://share.streamlit.io → New app
3. Select your repo → `app.py`
4. Add `GROQ_API_KEY` as a Secret in app settings

---

## 🛠 Tech Stack

| Layer | Technology | Cost |
|---|---|---|
| Frontend | Streamlit | Free |
| LLM | Llama 4 Scout via Groq | Free tier |
| PDF | ReportLab | Open source |
| Images | Pillow | Open source |
| Fonts | Google Fonts (CDN) | Free |
| Hosting | Streamlit Community Cloud | Free |

---

## 📝 License

MIT — free to use, modify, and deploy.
