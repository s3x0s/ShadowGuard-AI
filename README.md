```markdown
# 🛡️ ShadowGuard AI

**Your 100% Local, Zero-Trust AI Security Bodyguard.**

[![Hackathon](https://img.shields.io/badge/Hackathon-UC%20Berkeley%20AI%20Hackathon-blue)]()
[![Version](https://img.shields.io/badge/Version-1.0.0-green)]()
[![API Required](https://img.shields.io/badge/API%20Required-None-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

ShadowGuard AI is a Chrome extension that detects sensitive data (passwords, API keys, SSNs, credit cards) the instant you type or paste it into any AI chat tool, and blocks it before it's sent — **entirely on-device. Zero data ever leaves the browser for detection.**

---

## 🌟 Inspiration
Developers and users constantly copy-paste code, logs, and environment variables into AI chatbots (ChatGPT, Claude, Gemini) for debugging. One accidental paste of an AWS key or credit card can lead to a catastrophic breach. Existing Data Loss Prevention (DLP) tools are enterprise-heavy and ironically require sending your data to a third-party cloud server to check if it's sensitive. 

**ShadowGuard AI flips this model:** 100% of the detection logic runs locally in the browser via synchronous JavaScript. Raw secrets never leave the user's device.

## 🚀 Features

### Phase 1: 100% Local Detection Engine
- **Zero-Trust Architecture:** All PII/secret detection runs via regex and heuristics directly in the browser content script. No network calls.
- **Comprehensive Pattern Matching:** Detects AWS keys, GitHub tokens, OpenAI/Anthropic API keys, JWTs, US SSNs, and password contexts.
- **Mathematical Credit Card Validation:** Implements a synchronous **Luhn algorithm check** in the browser to prevent false positives (e.g., ignoring 16-digit order IDs).
- **Synchronous Paste Blocking:** Intercepts paste events in the capture phase, preventing the secret from ever reaching the DOM.
- **Visual Feedback:** Instant red overlay warning on the input field.

### Phase 2: Backend & Dashboard
- **FastAPI Backend:** Receives masked detection metadata via WebSocket for a live threat feed.
- **Extension Risk Scanner:** Flags dangerous permission combinations in your installed Chrome extensions.
- **React Dashboard:** Real-time UI showing live threats, extension risks, and historical charts using Recharts.
- **Zero-Trust Telemetry:** Even when the backend receives data, it *only* receives heavily masked metadata (e.g., `AKIA****MPLE`). The raw secret is never transmitted.

---

## 🛠️ Tech Stack
- **Extension:** React, TypeScript, Vite, Chrome Manifest V3
- **Backend:** Python, FastAPI, SQLAlchemy, SQLite, WebSockets
- **Dashboard:** React, Recharts, Nginx
- **DevOps:** Docker, Docker Compose

---

## 🏃 Quick Start (No API Keys Required!)

This project is designed to run completely offline without any external API dependencies.

### 1. Start Backend & Dashboard
Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
docker compose up --build -d
```
Backend API: http://localhost:8000
Dashboard UI: http://localhost:3000

2. Build & Load the Chrome Extension
Open a new terminal and run:
```Bash
cd extension
npm install
npm run build
```
Load into Chrome:
Open Chrome and navigate to chrome://extensions/.
Enable Developer mode (toggle in the top right corner).
Click Load unpacked (top left).
Select the extension/dist folder you just built.
Pin the 🛡️ ShadowGuard icon to your toolbar for easy access.

🎤 3-Minute Demo Script
Want to see it in action? Follow these exact steps:
Open the Dashboard: Go to http://localhost:3000 and click on the Live Threat Feed.
Go to an AI Chat: Open a new tab and go to https://claude.ai or https://chat.openai.com.
The "Leak" Attempt: Copy this fake AWS key and try to paste it into the AI chat box:
<img width="981" height="102" alt="image" src="https://github.com/user-attachments/assets/e2c16349-737f-4b50-95fd-0ef2349fc569" />

The Block:
The text will not paste into the box.
A sleek red overlay flashes over the input: "🛑 ShadowGuard: AWS Access Key blocked!"
Open the ShadowGuard popup. The Risk Score jumps to 95, and the masked key (AKIA****MPLE) is logged.
The Proof: Look at the Dashboard. The alert appears instantly via WebSocket. Open Chrome DevTools (Network Tab) to prove that the backend only received the masked value, never the raw secret.

📂 Project Structure
```text
shadowguard-ai/
├── backend/            # FastAPI server, SQLite DB, WebSocket alerts
├── dashboard/          # React + Recharts live threat visualization
├── extension/          # Chrome Extension (Manifest V3, React, TS)
│   ├── src/
│   │   ├── detection/  # 100% local regex & Luhn validation engine
│   │   ├── content-scripts/ # DOM interception & overlay UI
│   │   ├── background/ # Service worker & backend communication
│   │   └── popup/      # Extension popup UI
├── docker-compose.yml  # One-command infrastructure setup
└── README.md           # You are here!
```
🧠 Ethical Considerations & Privacy
We addressed privacy and security at the absolute core of our architecture. Traditional AI security tools often require routing user data through third-party cloud servers to analyze it, creating a single point of failure. ShadowGuard AI ensures that using an AI security tool never becomes the very vector that compromises the user's data. Furthermore, by running entirely locally, we eliminate the carbon footprint associated with sending every keystroke to a cloud-based NLP model.

🏆 Credits & Hackathon Info
Author: s3x0s
Version: 1.0.0 (First Release)
Built for: UC Berkeley AI Hackathon (Cal Hacks)
Tracks: Best Technical Implementation, Best Creativity and Originality, Best UI/UX

📜 License
This project is open-source and available under the MIT License.


### 💡 Final Tips for your GitHub Repo:
1. **Add a `.gitignore`:** Make sure your `.gitignore` file (which the `setup.py` created) includes `node_modules/` and `extension/dist/` so you don't upload massive, unnecessary folders to GitHub.
2. **Pushing to GitHub:** If you haven't already, run these commands in your PyCharm terminal:
   ```bash
   git init
   git add .
   git commit -m "🚀 Initial Release: ShadowGuard AI v1.0.0 by s3x0s"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/shadowguard-ai.git
   git push -u origin main
