# 🏠 RealEstateAI - AI Marketing Assistant for Realtors

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

> Transform your real estate business with AI-powered marketing automation. Generate reels, listings, virtual staging, and handle leads - all in one platform.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎬 **AI Reel Generator** | Transform property photos into stunning Instagram Reels, YouTube Shorts, and TikToks |
| 📝 **AI Listing Generator** | Generate SEO-optimized MLS descriptions, social media captions, and email campaigns |
| 🪑 **AI Virtual Staging** | Transform empty rooms into beautifully furnished spaces using AI |
| 💬 **AI Lead Bot** | 24/7 chatbot that responds instantly across SMS, WhatsApp, and website |
| 📊 **Market Reports** | Generate professional neighborhood market reports automatically |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key
- (Optional) ElevenLabs API Key for voice generation

### Installation

1. **Clone the repository**
```bash
cd AI-RealEstate-Marketing-System
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application**
```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

## 🔧 Configuration

### Required API Keys (.env)

```env
# OpenAI - Required for AI features
OPENAI_API_KEY=sk-your-openai-api-key
```

## 💰 Pricing

| Plan | Price | Features |
|------|-------|----------|
| Starter | $49/mo | 20 reels, 50 listings |
| Pro | $99/mo | 100 reels, 200 listings, virtual staging |
| Enterprise | $199/mo | Unlimited everything + CRM |

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4, ElevenLabs, Stable Diffusion
- **Video**: MoviePy, FFmpeg
- **Database**: PostgreSQL (Supabase)

## 📁 Project Structure

```
AI-RealEstate-Marketing-System/
├── app/
│   ├── main.py              # Main Streamlit app
│   ├── pages/               # Page modules
│   │   ├── reel_generator.py
│   │   ├── listing_generator.py
│   │   ├── virtual_staging.py
│   │   ├── lead_bot.py
│   │   └── market_report.py
│   └── utils/               # Utility functions
│       ├── openai_client.py
│       ├── image_processor.py
│       └── ElevenLabs_tts.py
├── requirements.txt
├── .env.example
└── README.md
```

## 📝 License

Copyright (c) 2026 Anmol Sharma. All Rights Reserved.

This project is the exclusive property of Anmol Sharma. Unauthorized copying, distribution, or use of this code without explicit permission is strictly prohibited.

---

<p align="center">© 2024 Anmol Sharma - All Rights Reserved</p>


