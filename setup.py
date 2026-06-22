# -*- coding: utf-8 -*-
import os
import subprocess
import sys

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    # Force UTF-8 to prevent Windows encoding issues
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print(r"""
  ____  _                   ____ _                 _ _____  
 / ___| | __ _ _ __   __ _/ ___| | __ _ _ __   __| |___ \ 
 \___ \| |/ _` | '_ \ / _` \___ \ | |/ _` | '_ \ / _` | __) |
  ___) | | (_| | | | | (_| |___) | | (_| | | | | (_| | __/ 
 |____/|_|\__,_|_| |_|\__, |____/|_|\__,_|_| |_|\__,_|_____|
                      |___/                                 
        [ Your Local AI Security Bodyguard ]
                      by: s3x0s
                 First Version (1.0.0)
    """)
    
    print("🚀 Initializing ShadowGuard AI Project (100% Local, No API Required)...")
    print("="*60)

    # 1. Root Files
    write_file('.gitignore', "node_modules/\nextension/dist/\ndashboard/dist/\n__pycache__/\n*.pyc\nbackend/data/*.db\n.env\n.DS_Store\n")

    write_file('README.md', """# 🛡️ ShadowGuard AI\n\n**Your AI Security Bodyguard.**\n\nShadowGuard AI is a Chrome extension that detects sensitive data (passwords, API keys, SSNs, credit cards) the instant you type or paste it into any AI chat tool, and blocks it before it's sent — **entirely on-device, zero data ever leaves the browser for detection.**\n\n## 🌟 Features\n\n### Phase 1: 100% Local Detection Engine\n- **Zero-Trust Architecture:** All PII/secret detection runs via regex/heuristics directly in the browser content script.\n- **Comprehensive Pattern Matching:** Detects AWS keys, GitHub tokens, OpenAI/Anthropic API keys, JWTs, Credit Cards (with Luhn validation), US SSNs, and password contexts.\n- **Synchronous Paste Blocking:** Intercepts paste events in the capture phase, preventing the secret from ever reaching the DOM.\n- **Visual Feedback:** Instant red overlay warning on the input field.\n\n### Phase 2: Backend & Dashboard\n- **FastAPI Backend:** Receives masked detection metadata via WebSocket for a live threat feed.\n- **Extension Risk Scanner:** Flags dangerous permission combinations in your installed Chrome extensions.\n- **React Dashboard:** Real-time UI showing live threats, extension risks, and historical charts.\n\n## 🚀 Quick Start\n\n### 1. Start Backend & Dashboard\n```bash\ndocker compose up --build -d\n```\n- Backend: `http://localhost:8000`\n- Dashboard: `http://localhost:3000`\n\n### 2. Build & Load the Chrome Extension\n```bash\ncd extension\nnpm install\nnpm run build\n```\n**Load into Chrome:**\n1. Go to `chrome://extensions/`.\n2. Enable **Developer mode**.\n3. Click **Load unpacked** and select the `extension/dist` folder.\n\n## 🎤 Demo Script\n1. Open `http://localhost:3000` (Dashboard).\n2. Open the ShadowGuard popup on `claude.ai` (See 🟢 Recognized AI).\n3. Paste a fake AWS key (`AKIAIOSFODNN7EXAMPLE`) into the chat.\n4. Watch the paste get blocked instantly with a red overlay.\n5. Check the Dashboard to see the live WebSocket alert!\n\n## 🛠️ Tech Stack\n- **Extension:** React, TypeScript, Vite, Manifest V3\n- **Backend:** Python, FastAPI, SQLAlchemy, SQLite\n- **Dashboard:** React, Recharts, Nginx\n- **DevOps:** Docker, Docker Compose\n""")

    write_file('docker-compose.yml', """version: '3.8'\nservices:\n  backend:\n    build: {context: ., dockerfile: backend/Dockerfile}\n    ports: ["8000:8000"]\n    volumes: ["./backend:/app/backend", "backend_data:/app/data"]\n  dashboard:\n    build: {context: ., dockerfile: dashboard/Dockerfile}\n    ports: ["3000:80"]\n    depends_on: [backend]\nvolumes:\n  backend_data:\n""")

    # 2. Backend Files
    write_file('backend/Dockerfile', """FROM python:3.11-slim\nWORKDIR /app\nCOPY backend/requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY backend/ /app/backend/\nRUN touch /app/backend/__init__.py /app/backend/routers/__init__.py\nRUN mkdir -p /app/data\nCMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]\n""")
    write_file('backend/requirements.txt', "fastapi==0.111.0\nuvicorn==0.30.1\nsqlalchemy==2.0.30\npydantic==2.7.1\n")
    write_file('backend/main.py', """from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\nfrom contextlib import asynccontextmanager\nfrom .database import engine, Base\nfrom .routers import alerts, extensions\n\n@asynccontextmanager\nasync def lifespan(app: FastAPI):\n    Base.metadata.create_all(bind=engine)\n    yield\n\napp = FastAPI(lifespan=lifespan)\napp.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])\napp.include_router(alerts.router, prefix="/api")\napp.include_router(extensions.router, prefix="/api")\n\n@app.get("/")\ndef read_root():\n    return {"status": "ShadowGuard Backend Running"}\n""")
    write_file('backend/database.py', """from sqlalchemy import create_engine\nfrom sqlalchemy.orm import declarative_base, sessionmaker\nSQLALCHEMY_DATABASE_URL = "sqlite:////app/data/shadowguard.db"\nengine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})\nSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\nBase = declarative_base()\n""")
    write_file('backend/models.py', """from sqlalchemy import Column, Integer, String, Float, DateTime\nfrom sqlalchemy.sql import func\nfrom .database import Base\n\nclass Detection(Base):\n    __tablename__ = "detections"\n    id = Column(Integer, primary_key=True, index=True)\n    type = Column(String, index=True)\n    masked_value = Column(String)\n    risk_score = Column(Float)\n    source_url = Column(String)\n    timestamp = Column(DateTime(timezone=True), server_default=func.now())\n\nclass ExtensionRisk(Base):\n    __tablename__ = "extension_risks"\n    id = Column(Integer, primary_key=True, index=True)\n    extension_id = Column(String, unique=True, index=True)\n    name = Column(String)\n    permissions = Column(String)\n    risk_score = Column(Float)\n    risk_reasons = Column(String)\n    last_updated = Column(DateTime(timezone=True), server_default=func.now())\n""")
    write_file('backend/schemas.py', """from pydantic import BaseModel\nfrom typing import List\nfrom datetime import datetime\n\nclass DetectionCreate(BaseModel):\n    type: str; masked_value: str; risk_score: float; source_url: str; timestamp: datetime\n\nclass ExtensionData(BaseModel):\n    id: str; name: str; permissions: List[str]\n\nclass ExtensionRiskResponse(BaseModel):\n    extension_id: str; name: str; permissions: List[str]; risk_score: float; risk_reasons: List[str]\n""")
    write_file('backend/routers/alerts.py', """from fastapi import APIRouter, WebSocket, WebSocketDisconnect\nfrom ..database import SessionLocal\nfrom ..models import Detection\nfrom ..schemas import DetectionCreate\n\nrouter = APIRouter()\nclass ConnectionManager:\n    def __init__(self): self.active_connections = []\n    async def connect(self, ws): await ws.accept(); self.active_connections.append(ws)\n    def disconnect(self, ws): \n        if ws in self.active_connections: self.active_connections.remove(ws)\n    async def broadcast(self, msg):\n        for c in self.active_connections:\n            try: await c.send_json(msg)\n            except: pass\n\nmanager = ConnectionManager()\n\n@router.websocket("/ws/alerts")\nasync def ws_endpoint(ws: WebSocket):\n    await manager.connect(ws)\n    try:\n        while True: await ws.receive_text()\n    except WebSocketDisconnect: manager.disconnect(ws)\n\n@router.post("/detections")\nasync def create_detection(d: DetectionCreate):\n    db = SessionLocal()\n    obj = Detection(type=d.type, masked_value=d.masked_value, risk_score=d.risk_score, source_url=d.source_url, timestamp=d.timestamp)\n    db.add(obj); db.commit(); db.refresh(obj)\n    await manager.broadcast({"id": obj.id, "type": obj.type, "masked_value": obj.masked_value, "risk_score": obj.risk_score, "source_url": obj.source_url, "timestamp": obj.timestamp.isoformat()})\n    db.close()\n    return {"status": "success"}\n\n@router.get("/detections")\ndef get_detections():\n    db = SessionLocal()\n    res = [{"id": d.id, "type": d.type, "masked_value": d.masked_value, "risk_score": d.risk_score, "source_url": d.source_url, "timestamp": d.timestamp.isoformat()} for d in db.query(Detection).order_by(Detection.timestamp.desc()).limit(50).all()]\n    db.close()\n    return res\n""")
    write_file('backend/routers/extensions.py', """from fastapi import APIRouter\nfrom ..database import SessionLocal\nfrom ..models import ExtensionRisk\nfrom ..schemas import ExtensionData, ExtensionRiskResponse\nimport json\nfrom typing import List\n\nrouter = APIRouter()\nDANGEROUS = {"clipboardRead": 20, "webRequest": 30, "cookies": 40, "<all_urls>": 50, "history": 30, "tabs": 20}\n\n@router.post("/extensions")\nasync def update_extensions(ext_list: List[ExtensionData]):\n    db = SessionLocal()\n    for ext in ext_list:\n        score, reasons = 0, []\n        for p in ext.permissions:\n            if p in DANGEROUS: score += DANGEROUS[p]; reasons.append(f"Has '{p}'")\n        existing = db.query(ExtensionRisk).filter(ExtensionRisk.extension_id == ext.id).first()\n        if existing:\n            existing.name, existing.permissions, existing.risk_score, existing.risk_reasons = ext.name, json.dumps(ext.permissions), min(score, 100), json.dumps(reasons)\n        else:\n            db.add(ExtensionRisk(extension_id=ext.id, name=ext.name, permissions=json.dumps(ext.permissions), risk_score=min(score, 100), risk_reasons=json.dumps(reasons)))\n    db.commit(); db.close()\n    return {"status": "success"}\n\n@router.get("/extensions", response_model=List[ExtensionRiskResponse])\ndef get_extensions():\n    db = SessionLocal()\n    res = [ExtensionRiskResponse(extension_id=e.extension_id, name=e.name, permissions=json.loads(e.permissions), risk_score=e.risk_score, risk_reasons=json.loads(e.risk_reasons)) for e in db.query(ExtensionRisk).all()]\n    db.close()\n    return res\n""")

    # 3. Dashboard Files
    write_file('dashboard/Dockerfile', """FROM node:18-alpine as build\nWORKDIR /app\nCOPY dashboard/package.json ./\nRUN npm install\nCOPY dashboard/ .\nRUN npm run build\nFROM nginx:alpine\nCOPY dashboard/nginx.conf /etc/nginx/conf.d/default.conf\nCOPY --from=build /app/dist /usr/share/nginx/html\nEXPOSE 80\nCMD ["nginx", "-g", "daemon off;"]\n""")
    write_file('dashboard/nginx.conf', """server { listen 80; server_name localhost; root /usr/share/nginx/html; index index.html; location / { try_files $uri $uri/ /index.html; } }""")
    write_file('dashboard/package.json', """{"name": "shadowguard-dashboard", "private": true, "version": "0.0.0", "type": "module", "scripts": {"dev": "vite", "build": "tsc && vite build"}, "dependencies": {"react": "^18.2.0", "react-dom": "^18.2.0", "react-router-dom": "^6.23.1", "recharts": "^2.12.7"}, "devDependencies": {"@types/react": "^18.2.66", "@types/react-dom": "^18.2.22", "@vitejs/plugin-react": "^4.2.1", "typescript": "^5.2.2", "vite": "^5.2.0"}}""")
    write_file('dashboard/vite.config.ts', """import { defineConfig } from 'vite'\nimport react from '@vitejs/plugin-react'\nexport default defineConfig({ plugins: [react()], server: { host: '0.0.0.0', port: 5173 } })""")
    tsconfig = """{"compilerOptions": {"target": "ES2020", "useDefineForClassFields": true, "lib": ["ES2020", "DOM", "DOM.Iterable"], "module": "ESNext", "skipLibCheck": true, "moduleResolution": "bundler", "allowImportingTsExtensions": true, "resolveJsonModule": true, "isolatedModules": true, "noEmit": true, "jsx": "react-jsx", "strict": true, "noUnusedLocals": false, "noUnusedParameters": false}, "include": ["src"], "references": [{"path": "./tsconfig.node.json"}]}"""
    tsconfig_node = """{"compilerOptions": {"composite": true, "skipLibCheck": true, "module": "ESNext", "moduleResolution": "bundler", "allowSyntheticDefaultImports": true}, "include": ["vite.config.ts"]}"""
    write_file('dashboard/tsconfig.json', tsconfig)
    write_file('dashboard/tsconfig.node.json', tsconfig_node)
    write_file('dashboard/index.html', """<!doctype html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>ShadowGuard</title></head><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>""")
    write_file('dashboard/src/main.tsx', """import React from 'react'\nimport ReactDOM from 'react-dom/client'\nimport App from './App.tsx'\nReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>)""")
    write_file('dashboard/src/App.css', """body{margin:0;font-family:system-ui;background:#0f172a;color:#f8fafc}.app-container{display:flex;height:100vh}.sidebar{width:250px;background:#1e293b;padding:20px;border-right:1px solid #334155}.sidebar h2{margin-top:0;color:#38bdf8}.sidebar ul{list-style:none;padding:0}.sidebar li{margin:20px 0}.sidebar a{color:#cbd5e1;text-decoration:none;font-weight:500}.sidebar a:hover{color:#38bdf8}.content{flex:1;padding:40px;overflow-y:auto}h1{margin-top:0;border-bottom:2px solid #334155;padding-bottom:10px}.card{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:20px;margin-bottom:20px}.alert-item{display:flex;justify-content:space-between;padding:15px;background:#0f172a;border-radius:6px;margin-bottom:10px;border-left:4px solid #ef4444}""")
    write_file('dashboard/src/App.tsx', """import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'\nimport Home from './pages/index'\nimport Extensions from './pages/extensions'\nimport History from './pages/history'\nimport './App.css'\nfunction App() { return (<BrowserRouter><div className="app-container"><nav className="sidebar"><h2>🛡️ ShadowGuard</h2><ul><li><Link to="/">Live Feed</Link></li><li><Link to="/extensions">Extensions</Link></li><li><Link to="/history">History</Link></li></ul></nav><main className="content"><Routes><Route path="/" element={<Home />} /><Route path="/extensions" element={<Extensions />} /><Route path="/history" element={<History />} /></Routes></main></div></BrowserRouter>) }\nexport default App""")
    write_file('dashboard/src/pages/index.tsx', """import { useEffect, useState } from 'react'\ninterface D { id: number; type: string; masked_value: string; risk_score: number; source_url: string; timestamp: string; }\nexport default function Home() {\n  const [a, s] = useState<D[]>([])\n  useEffect(() => {\n    fetch('http://localhost:8000/api/detections').then(r=>r.json()).then(s)\n    const ws = new WebSocket('ws://localhost:8000/api/ws/alerts')\n    ws.onmessage = (e) => s(p => [JSON.parse(e.data), ...p].slice(0,50))\n    return () => ws.close()\n  }, [])\n  return (<div><h1>Live Threat Feed</h1><div className="card">{a.length===0?<p>Waiting...</p>:a.map(x=><div key={x.id} className="alert-item"><div><strong>{x.type}</strong><div style={{fontFamily:'monospace',color:'#94a3b8'}}>{x.masked_value}</div></div><div style={{textAlign:'right'}}><div style={{fontSize:24,fontWeight:'bold',color:'#f87171'}}>{x.risk_score}</div></div></div>)}</div></div>)\n}""")
    write_file('dashboard/src/pages/extensions.tsx', """import { useEffect, useState } from 'react'\ninterface E { extension_id: string; name: string; risk_score: number; risk_reasons: string[]; }\nexport default function Ext() {\n  const [e, s] = useState<E[]>([])\n  useEffect(() => { fetch('http://localhost:8000/api/extensions').then(r=>r.json()).then(s) }, [])\n  return (<div><h1>Extension Scanner</h1><div className="card">{e.length===0?<p>Waiting for extension to sync...</p>:e.map(x=><div key={x.extension_id} className="alert-item" style={{borderLeftColor:x.risk_score>50?'#ef4444':'#10b981'}}><div><strong>{x.name}</strong>{x.risk_reasons.map((r,i)=><div key={i} style={{color:'#f59e0b',fontSize:12}}>⚠️ {r}</div>)}</div><div style={{fontSize:24,fontWeight:'bold',color:x.risk_score>50?'#f87171':'#34d399'}}>{x.risk_score}</div></div>)}</div></div>)\n}""")
    write_file('dashboard/src/pages/history.tsx', """import { useEffect, useState } from 'react'\nimport { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'\ninterface D { id: number; type: string; masked_value: string; source_url: string; timestamp: string; }\nexport default function Hist() {\n  const [h, sH] = useState<D[]>([]); const [c, sC] = useState<any[]>([])\n  useEffect(() => { fetch('http://localhost:8000/api/detections').then(r=>r.json()).then(d => { sH(d); const m:Record<string,number>={}; d.forEach((x:D)=>m[x.type]=(m[x.type]||0)+1); sC(Object.keys(m).map(k=>({type:k,count:m[k]}))) }) }, [])\n  return (<div><h1>History</h1><div className="card"><ResponsiveContainer width="100%" height={300}><BarChart data={c}><XAxis dataKey="type" stroke="#94a3b8"/><YAxis stroke="#94a3b8"/><Tooltip/><Bar dataKey="count" fill="#38bdf8"/></BarChart></ResponsiveContainer></div></div>)\n}""")

    # 4. Extension Files
    write_file('extension/manifest.json', """{"manifest_version":3,"name":"ShadowGuard AI","version":"0.1.0","permissions":["storage","management","activeTab"],"host_permissions":["<all_urls>"],"background":{"service_worker":"src/background/background.ts","type":"module"},"content_scripts":[{"matches":["<all_urls>"],"js":["src/content-scripts/inputMonitor.ts"],"css":["src/content-scripts/overlay.css"],"run_at":"document_idle","all_frames":true}],"action":{"default_popup":"src/popup/index.html"},"content_security_policy":{"extension_pages":"script-src 'self'; object-src 'self';"}}""")
    write_file('extension/package.json', """{"name":"shadowguard-ext","version":"0.1.0","type":"module","scripts":{"build":"tsc && vite build"},"dependencies":{"react":"^18.2.0","react-dom":"^18.2.0"},"devDependencies":{"@crxjs/vite-plugin":"^2.0.0-beta.25","@types/react":"^18.2.0","@types/react-dom":"^18.2.0","@types/chrome":"^0.0.268","@vitejs/plugin-react":"^4.3.1","typescript":"^5.2.2","vite":"^5.3.1"}}""")
    write_file('extension/vite.config.ts', """import { defineConfig } from 'vite';\nimport react from '@vitejs/plugin-react';\nimport { crx } from '@crxjs/vite-plugin';\nimport manifest from './manifest.json';\nexport default defineConfig({ plugins: [react(), crx({ manifest })], build: { minify: false } });""")
    write_file('extension/tsconfig.json', tsconfig)
    write_file('extension/tsconfig.node.json', tsconfig_node)
    
    write_file('extension/src/detection/patterns.ts', """export type DetectionType = "aws_access_key" | "aws_secret_key" | "github_token" | "openai_key" | "anthropic_key" | "jwt" | "credit_card" | "ssn" | "password_context" | "generic_api_key";
export interface Detection { type: DetectionType; match: string; maskedValue: string; index: number; severity: number; label: string; }
interface PatternRule { type: DetectionType; label: string; severity: number; regex: RegExp; validate?: (m: string) => boolean; }
const RULES: PatternRule[] = [
  { type: "aws_access_key", label: "AWS Access Key", severity: 95, regex: /AKIA[0-9A-Z]{16}/ },
  { type: "aws_secret_key", label: "AWS Secret Key", severity: 95, regex: /(?:aws|secret)[_-]?(?:access)?[_-]?key\\s*[:=]\\s*['"]?[A-Za-z0-9/+=]{40}['"]?/i },
  { type: "github_token", label: "GitHub Token", severity: 90, regex: /gh[pousr]_[A-Za-z0-9]{36,255}/ },
  { type: "openai_key", label: "OpenAI API Key", severity: 90, regex: /sk-[A-Za-z0-9]{20,}T3BlbkFJ[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{20,}/ },
  { type: "anthropic_key", label: "Anthropic API Key", severity: 90, regex: /sk-ant-[A-Za-z0-9_-]{20,}/ },
  { type: "generic_api_key", label: "Generic API Key", severity: 60, regex: /api[_-]?key\\s*[:=]\\s*['"]?[A-Za-z0-9_-]{20,}['"]?/i },
  { type: "jwt", label: "JWT Token", severity: 80, regex: /eyJ[A-Za-z0-9_-]+\\.eyJ[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+/ },
  { type: "ssn", label: "US SSN", severity: 95, regex: /\\b\\d{3}-\\d{2}-\\d{4}\\b/ },
  { type: "credit_card", label: "Credit Card", severity: 90, regex: /\\b(?:\\d[ -]?){13,19}\\b/, validate: (m) => luhn(m.replace(/[ -]/g, "")) },
  { type: "password_context", label: "Password", severity: 70, regex: /(?:password|pwd|passwd)\\s*[:=]\\s*['"]?\\S{4,}['"]?/i }
];
function luhn(d: string): boolean { if (!/^\\d{13,19}$/.test(d)) return false; let s=0, db=false; for(let i=d.length-1;i>=0;i--){ let x=parseInt(d[i],10); if(db){x*=2;if(x>9)x-=9;} s+=x; db=!db; } return s%10===0; }
export function maskValue(v: string, t: DetectionType): string { const c=v.trim(); if(t==="credit_card") return `****-****-****-${c.replace(/[ -]/g,"").slice(-4)}`; if(t==="ssn") return `***-**-${c.slice(-4)}`; if(c.length<=8) return "*".repeat(c.length); return `${c.slice(0,4)}${"*".repeat(Math.max(c.length-8,4))}${c.slice(-4)}`; }
export function scanText(text: string): Detection[] { if(!text) return []; const res: Detection[] = []; for(const r of RULES){ const g=new RegExp(r.regex,"g"); let m; while((m=g.exec(text))!==null){ if(r.validate && !r.validate(m[0])) continue; res.push({type:r.type,match:m[0],maskedValue:maskValue(m[0],r.type),index:m.index,severity:r.severity,label:r.label}); if(m.index===g.lastIndex)g.lastIndex++; } } return res; }
export function computeRiskScore(d: Detection[]): number { if(d.length===0) return 0; return Math.min(Math.max(...d.map(x=>x.severity)) + Math.min((d.length-1)*5, 20), 100); }
""")
    write_file('extension/src/content-scripts/overlay.css', """.shadowguard-overlay{position:fixed;background:rgba(255,0,0,0.05);border:2px solid #ff0000;border-radius:6px;pointer-events:none;z-index:2147483647;display:flex;align-items:center;justify-content:center;font-family:system-ui;font-weight:600;color:#dc2626;font-size:14px;box-shadow:0 0 20px rgba(255,0,0,0.4);backdrop-filter:blur(2px)}.shadowguard-overlay-text{background:white;padding:6px 14px;border-radius:6px;pointer-events:auto;box-shadow:0 4px 12px rgba(0,0,0,0.15)}""")
    write_file('extension/src/content-scripts/inputMonitor.ts', """import { scanText, computeRiskScore, Detection } from '../detection/patterns';
function isMon(el: EventTarget | null): el is HTMLElement { if(!el||!(el instanceof HTMLElement)) return false; const t=el.tagName.toLowerCase(); return t==='textarea'||t==='input'||el.isContentEditable; }
function getTxt(el: HTMLElement): string { return el.isContentEditable ? el.innerText : (el as HTMLInputElement).value; }
function showOverlay(el: HTMLElement, d: Detection[]) { document.querySelectorAll('.shadowguard-overlay').forEach(o=>o.remove()); const r=el.getBoundingClientRect(); const o=document.createElement('div'); o.className='shadowguard-overlay'; o.style.top=`${r.top}px`; o.style.left=`${r.left}px`; o.style.width=`${r.width}px`; o.style.height=`${r.height}px`; const t=document.createElement('div'); t.className='shadowguard-overlay-text'; t.innerText=`🛑 ShadowGuard: ${d[0].label} blocked!`; o.appendChild(t); document.body.appendChild(o); setTimeout(()=>o.remove(), 3000); }
function report(d: Detection[]) { chrome.runtime.sendMessage({type:'DETECTIONS_FOUND', payload:{detections:d.map(x=>({type:x.type,maskedValue:x.maskedValue,label:x.label,severity:x.severity})), riskScore:computeRiskScore(d), timestamp:new Date().toISOString(), url:window.location.href}}).catch(()=>{}); }
document.addEventListener('paste', (e) => { const t=e.target; if(isMon(t)){ const txt=e.clipboardData?.getData('text')||''; if(txt){ const d=scanText(txt); if(d.length>0){ e.preventDefault(); e.stopPropagation(); showOverlay(t as HTMLElement, d); report(d); } } } }, true);
let timer: number; document.addEventListener('input', (e) => { const t=e.target; if(isMon(t)){ clearTimeout(timer); timer=window.setTimeout(()=>{ const d=scanText(getTxt(t as HTMLElement)); if(d.length>0){ showOverlay(t as HTMLElement, d); report(d); } }, 300); } }, true);
""")
    write_file('extension/src/background/background.ts', """const API = 'http://localhost:8000/api';
interface E { detections: any[]; riskScore: number; timestamp: string; url: string; }
async function sendExt() { try { const e = await chrome.management.getAll(); await fetch(`${API}/extensions`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(e.filter(x=>x.enabled&&x.type==='extension').map(x=>({id:x.id,name:x.name,permissions:x.permissions||[]})))}); } catch(e){} }
async function sendDet(ev: E) { try { const p = ev.detections.reduce((a,b)=>a.severity>b.severity?a:b); await fetch(`${API}/detections`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({type:p.type,masked_value:p.maskedValue,risk_score:ev.riskScore,source_url:ev.url,timestamp:ev.timestamp})}); } catch(e){} }
chrome.runtime.onInstalled.addListener(() => { chrome.storage.local.get(['h'], r => { if(!r.h) chrome.storage.local.set({h:[{detections:[{type:'aws_access_key',maskedValue:'AKIA****FAKE',label:'AWS Key',severity:95}],riskScore:95,timestamp:new Date(Date.now()-3600000).toISOString(),url:'https://chat.openai.com'}], rs:95}); }); sendExt(); });
chrome.runtime.onStartup.addListener(sendExt);
chrome.runtime.onMessage.addListener((m, s, res) => {
  if(m.type==='DETECTIONS_FOUND') { chrome.storage.local.get(['h'], r => { const h=r.h||[]; h.unshift(m.payload); if(h.length>50)h.pop(); chrome.storage.local.set({h, rs:Math.max(...h.slice(0,10).map((x:E)=>x.riskScore),0)}); }); sendDet(m.payload); res({ok:1}); }
  if(m.type==='GET_STATE') { chrome.storage.local.get(['h','rs'], r => res({history:r.h||[], riskScore:r.rs||0})); return true; }
});
""")
    write_file('extension/src/popup/index.html', """<!DOCTYPE html><html><head><meta charset="UTF-8"/><style>body{margin:0;padding:0;width:380px;}</style></head><body><div id="root"></div><script type="module" src="./main.tsx"></script></body></html>""")
    write_file('extension/src/popup/main.tsx', """import React from 'react';\nimport ReactDOM from 'react-dom/client';\nimport App from './App';\nReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);""")
    write_file('extension/src/popup/App.tsx', """import React, { useEffect, useState } from 'react';
interface DI { type: string; maskedValue: string; label: string; severity: number; }
interface DE { detections: DI[]; riskScore: number; timestamp: string; url: string; }
const AI = ['chat.openai.com','claude.ai','gemini.google.com','copilot.microsoft.com'];
function App() {
  const [h, sH] = useState<DE[]>([]); const [rs, sRS] = useState(0); const [url, sUrl] = useState('');
  useEffect(() => {
    chrome.runtime.sendMessage({type:'GET_STATE'}, r => { if(r){ sH(r.history||[]); sRS(r.riskScore||0); } });
    chrome.tabs.query({active:true, currentWindow:true}, t => { if(t&&t[0]?.url) sUrl(t[0].url); });
  }, []);
  const host = (u:string) => { try{return new URL(u).hostname}catch{return u} };
  const isAI = AI.some(d => host(url).endsWith(d));
  const col = (s:number) => s>=80?'#ef4444':s>=50?'#f59e0b':'#10b981';
  return (<div style={{padding:20,fontFamily:'system-ui',background:'#0f172a',color:'#f8fafc',minHeight:450}}>
    <div style={{display:'flex',justifyContent:'space-between',marginBottom:12}}><h1 style={{margin:0,fontSize:22}}>🛡️ ShadowGuard</h1><div style={{background:col(rs),padding:'6px 14px',borderRadius:99,fontWeight:'bold'}}>{rs}</div></div>
    {url && !url.startsWith('chrome') && <div style={{padding:8,borderRadius:8,marginBottom:16,fontSize:12,fontWeight:600,background:isAI?'#064e3b':'#78350f',color:isAI?'#6ee7b7':'#fcd34d',textAlign:'center'}}>{isAI?'🟢 Recognized AI':'🟡 Unrecognized Domain'}</div>}
    <h2 style={{fontSize:14,borderTop:'1px solid #334155',paddingTop:20}}>Recent Detections</h2>
    {h.map((ev,i) => (<div key={i} style={{background:'#1e293b',padding:14,borderRadius:10,marginBottom:12}}>
      <div style={{display:'flex',justifyContent:'space-between'}}><span style={{color:'#f87171',fontWeight:700}}>{ev.detections[0]?.label}</span><span style={{fontSize:11,color:'#64748b'}}>{new Date(ev.timestamp).toLocaleTimeString()}</span></div>
      <div style={{fontFamily:'monospace',background:'#0f172a',padding:6,borderRadius:6,margin:'8px 0',fontSize:13}}>{ev.detections[0]?.maskedValue}</div>
      <div style={{fontSize:11,color:'#64748b'}}>📍 {host(ev.url)}</div>
    </div>))}
  </div>);
}
export default App;
""")

    print("\n🐳 Starting Backend & Dashboard (Docker)...")
    try:
        subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["docker-compose", "up", "-d", "--build"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Error: Docker is not installed or not running. Please install Docker Desktop and start it.")
            return
    
        print("\n🧩 Building Chrome Extension...")
    try:
        # FIX: shell=True is required on Windows because npm is a .cmd file, not an .exe
        subprocess.run("npm install", cwd="extension", check=True, shell=True)
        subprocess.run("npm run build", cwd="extension", check=True, shell=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: Node.js/npm is not installed or not in your System PATH.")
        print("Please install Node.js from https://nodejs.org/ and restart PyCharm.")
        return

    print("\n" + "="*60)
    print("✅ SHADOWGUARD AI IS READY!")
    print("="*60)
    print("👉 NEXT STEP: Load the extension into Chrome:")
    print("   1. Open Chrome and go to: chrome://extensions/")
    print("   2. Enable 'Developer mode' (top right).")
    print("   3. Click 'Load unpacked' and select the 'extension/dist' folder.")
    print("\n🌐 Dashboard is running at: http://localhost:3000")
    print("🚀 Go paste a fake AWS key (AKIAIOSFODNN7EXAMPLE) into ChatGPT to test!")

if __name__ == "__main__":
    main()