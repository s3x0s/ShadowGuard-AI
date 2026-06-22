# 🛡️ ShadowGuard AI

**Your AI Security Bodyguard.**

ShadowGuard AI is a Chrome extension that detects sensitive data (passwords, API keys, SSNs, credit cards) the instant you type or paste it into any AI chat tool, and blocks it before it's sent — **entirely on-device, zero data ever leaves the browser for detection.**

## 🌟 Features

### Phase 1: 100% Local Detection Engine
- **Zero-Trust Architecture:** All PII/secret detection runs via regex/heuristics directly in the browser content script.
- **Comprehensive Pattern Matching:** Detects AWS keys, GitHub tokens, OpenAI/Anthropic API keys, JWTs, Credit Cards (with Luhn validation), US SSNs, and password contexts.
- **Synchronous Paste Blocking:** Intercepts paste events in the capture phase, preventing the secret from ever reaching the DOM.
- **Visual Feedback:** Instant red overlay warning on the input field.

### Phase 2: Backend & Dashboard
- **FastAPI Backend:** Receives masked detection metadata via WebSocket for a live threat feed.
- **Extension Risk Scanner:** Flags dangerous permission combinations in your installed Chrome extensions.
- **React Dashboard:** Real-time UI showing live threats, extension risks, and historical charts.

## 🚀 Quick Start

### 1. Start Backend & Dashboard
```bash
docker compose up --build -d
```
- Backend: `http://localhost:8000`
- Dashboard: `http://localhost:3000`

### 2. Build & Load the Chrome Extension
```bash
cd extension
npm install
npm run build
```
**Load into Chrome:**
1. Go to `chrome://extensions/`.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select the `extension/dist` folder.

## 🎤 Demo Script
1. Open `http://localhost:3000` (Dashboard).
2. Open the ShadowGuard popup on `claude.ai` (See 🟢 Recognized AI).
3. Paste a fake AWS key (`AKIAIOSFODNN7EXAMPLE`) into the chat.
4. Watch the paste get blocked instantly with a red overlay.
5. Check the Dashboard to see the live WebSocket alert!

## 🛠️ Tech Stack
- **Extension:** React, TypeScript, Vite, Manifest V3
- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Dashboard:** React, Recharts, Nginx
- **DevOps:** Docker, Docker Compose
