# RAG//CORE — Local Setup

Hybrid RAG pipeline: TF-IDF + Knowledge Graph + RRF Fusion + Claude Sonnet streaming.

## Folder Structure

```
rag-app/
├── server/          ← Express backend (proxies Anthropic API)
│   ├── index.js
│   ├── package.json
│   └── .env         ← PUT YOUR API KEY HERE
└── client/          ← React + Vite frontend
    ├── src/App.jsx
    ├── vite.config.js
    └── package.json
```

## Setup (one time)

### 1. Install dependencies

```bash
# Install server deps
cd server
npm install

# Install client deps
cd ../client
npm install
```

### 2. Add your Anthropic API key

Edit `server/.env`:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

Get your key at: https://console.anthropic.com/

## Run

You need **two terminals** open simultaneously:

**Terminal 1 — Start the backend server:**
```bash
cd server
npm run dev
```
You should see: `🚀 RAG//CORE server running at http://localhost:3001`

**Terminal 2 — Start the frontend:**
```bash
cd client
npm run dev
```
You should see: `Local: http://localhost:5173`

## Open in browser

Go to: **http://localhost:5173**

## How it works

1. You type a query in the UI
2. The frontend runs TF-IDF vector search + KG traversal locally in the browser
3. Results are fused via Reciprocal Rank Fusion (RRF)
4. The fused context is sent to `localhost:3001/api/chat`
5. The Express server forwards it to the Anthropic API with your key
6. Claude Sonnet streams the answer back token by token

## Troubleshooting

| Problem | Fix |
|---|---|
| `ANTHROPIC_API_KEY not set` | Add your key to `server/.env` |
| `Failed to fetch` in browser | Make sure server is running on port 3001 |
| Port 5173 in use | Change port in `client/vite.config.js` |
| Port 3001 in use | Change PORT in `server/index.js` and update vite proxy |
