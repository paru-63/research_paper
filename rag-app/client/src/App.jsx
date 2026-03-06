import { useState, useEffect, useRef, useCallback } from "react";

// ═══════════════════════════════════════════════════════════════
// KNOWLEDGE GRAPH DATA
// ═══════════════════════════════════════════════════════════════
const KG = {
  P01: { id:"P01", title:"Revolutionizing Research Writing and Publishing by using AI-Powered Tools and Technique", year:2024, authors:["Mandira Bairagi","Dr. Shalini R. Lihitkar"], journal:"IEEE Access", keywords:["Artificial intelligence","AI Tools","Research communication","Scholarly publication"], domains:["Artificial Intelligence Tools"], citations:[{title:"Revolutionizing Research Writing using AI-Powered Tools",year:2023,count:8}], shares_topic:[] },
  P02: { id:"P02", title:"SmartNews: AI-Powered News Summarize", year:2025, authors:["Mrs. Abha Pathak","Trupti Pawar","Yogeshwari Pawar","Shreya Pawar"], journal:"Int. Journal on Advanced Computer Theory and Engineering", keywords:["NLP","evaluate summarization models using Python"], domains:["Natural Language Processing (NLP)"], citations:[{title:"SmartNews: AI-Powered News Summarizer",year:2025,count:0}], shares_topic:[{pid:"P05",kw:"NLP"}] },
  P03: { id:"P03", title:"Automatic Text Summarization Methods: A Comprehensive Review", year:2024, authors:["Divakar Yadav","Jalpa Desai","Arun Kumar Yadav"], journal:"IEEE Access", keywords:["Automatic text summarization","Natural Language Processing","Categorization of text summarization"], domains:["NLP"], citations:[{title:"Automatic Text Summarization: A Comprehensive Review",year:2023,count:25}], shares_topic:[] },
  P04: { id:"P04", title:"Automatic text summarization of scientific articles using transformers", year:2024, authors:["Seema Aswani","Kabita Choudhary","Sujala Shetty","Nasheen Nur"], journal:"Journal of Autonomous Intelligence", keywords:["NLP","long document summarization","transformers","multi-headed attention","scientific article summarization"], domains:["Natural Language Processing","CNN"], citations:[{title:"Automatic text summarization using transformers — review",year:2024,count:2}], shares_topic:[] },
  P05: { id:"P05", title:"Text Summarization Using Natural Language Processing", year:2024, authors:["Sanjivani C. Kachare","Manali U. Sawant","Manasi S. Yadav","Ms. Priyanka R. Jadhav"], journal:"IJCRT", keywords:["NLP","Text Summarization","Text Rank","OCR","Open AI"], domains:["NLP","Open AI"], citations:[{title:"Text Summarization Using NLP",year:2024,count:3}], shares_topic:[{pid:"P02",kw:"NLP"},{pid:"P06",kw:"Text Summarization"}] },
  P06: { id:"P06", title:"Text Summarization Using NLP and Google Text To Speech API", year:2020, authors:["Subash Voleti","Chaitan Raju","Teja Rani","Mugada Swetha"], journal:"IRJET", keywords:["Text Summarization","Text Rank Algorithm","NLTK","GTTS API","Extractive Text Summarization"], domains:["GTTS(Google Text To Speech) API"], citations:[{title:"Text Summarization using NLP and GTTS",year:2020,count:10}], shares_topic:[{pid:"P05",kw:"Text Summarization"}] },
  P07: { id:"P07", title:"A Survey of Text Summarization Using NLP", year:2025, authors:["Bhuvan Shingade","Yash Matha","Ved Kolambkar","Suyash Kasar","Prof. Rohini Palve"], journal:"SIRJANA JOURNAL", keywords:["Machine Learning","Natural Language Processing","LSTM","Abstractive Summarization","Extractive Summarization"], domains:["Machine Learning","LSTM","NLP"], citations:[{title:"A Survey of Text Summarization Using NLP",year:2023,count:2}], shares_topic:[] },
  P08: { id:"P08", title:"A Survey of Automatic Text Summarization", year:2014, authors:["Niharika Verma","Prof. Ashish Tiwari"], journal:"IJERT", keywords:["abstraction-predicated summary","automatic text summarization","extraction summary","feature extraction","text reduction"], domains:["Automatic Text Summarization"], citations:[{title:"A Survey of Automatic Text Summarization",year:2014,count:15}], shares_topic:[] },
  P09: { id:"P09", title:"Research Paper Summarizer Using AI", year:2024, authors:["G. Santhoshi","M. Jyothi","Kovvuri Ramya Sri","G. Hasika","G. Varsha","R. Snigdha"], journal:"IRAEM", keywords:["Natural Language Processing","Highlighting Keywords","Read Aloud","Plagiarism","Images","Research"], domains:["Natural Language Toolkit (NLTK)"], citations:[], shares_topic:[] },
};

const PAPERS = Object.values(KG);

// ═══════════════════════════════════════════════════════════════
// TF-IDF + KG RETRIEVAL ENGINE
// ═══════════════════════════════════════════════════════════════
function tokenize(text) {
  return (text.toLowerCase().match(/[a-z0-9]+/g) || []).filter(w => w.length > 2);
}

function buildCorpus() {
  return PAPERS.map(p => ({
    id: p.id,
    text: `${p.title} ${p.authors.join(" ")} ${p.keywords.join(" ")} ${p.domains.join(" ")} ${p.journal}`,
  }));
}

function tfidfSearch(query, topK = 5) {
  const corpus = buildCorpus();
  const N = corpus.length;
  const df = {};
  const tfDocs = corpus.map(doc => {
    const tokens = tokenize(doc.text);
    const tf = {};
    tokens.forEach(t => tf[t] = (tf[t] || 0) + 1 / tokens.length);
    Object.keys(tf).forEach(w => df[w] = (df[w] || 0) + 1);
    return { id: doc.id, tf };
  });
  const idf = {};
  Object.keys(df).forEach(w => idf[w] = Math.log((N + 1) / (df[w] + 1)) + 1);

  const qTokens = tokenize(query);
  const qVec = {};
  qTokens.forEach(t => { if (idf[t]) qVec[t] = (1 / qTokens.length) * idf[t]; });

  const scores = tfDocs.map(doc => {
    const dVec = {};
    Object.keys(doc.tf).forEach(w => { if (idf[w]) dVec[w] = doc.tf[w] * idf[w]; });
    const dot = Object.keys(qVec).reduce((s, w) => s + (qVec[w] || 0) * (dVec[w] || 0), 0);
    const na = Math.sqrt(Object.values(qVec).reduce((s, v) => s + v * v, 0)) || 1e-9;
    const nb = Math.sqrt(Object.values(dVec).reduce((s, v) => s + v * v, 0)) || 1e-9;
    return { id: doc.id, score: dot / (na * nb) };
  });
  scores.sort((a, b) => b.score - a.score);
  return scores.slice(0, topK).filter(x => x.score > 0);
}

function kgSearch(query, topK = 5) {
  const ql = query.toLowerCase();
  const qWords = ql.split(/\s+/).filter(w => w.length > 2);
  const scores = {};
  PAPERS.forEach(p => {
    let score = 0;
    p.keywords.forEach(kw => {
      const kl = kw.toLowerCase();
      if (qWords.some(w => kl.includes(w) || w.includes(kl.slice(0,8)))) score += 2;
    });
    p.domains.forEach(dm => {
      if (qWords.some(w => dm.toLowerCase().includes(w))) score += 1.5;
    });
    if (qWords.some(w => p.title.toLowerCase().includes(w))) score += 1;
    p.authors.forEach(a => {
      if (qWords.some(w => a.toLowerCase().includes(w))) score += 0.5;
    });
    if (score > 0) scores[p.id] = score;
  });
  return Object.entries(scores).sort((a, b) => b[1] - a[1]).slice(0, topK)
    .map(([id, s]) => ({ id, score: s }));
}

function hybridRetrieve(query, topK = 5) {
  const vec = tfidfSearch(query, topK);
  const kg = kgSearch(query, topK);
  const rrf = {};
  vec.forEach((r, i) => rrf[r.id] = (rrf[r.id] || 0) + 0.6 / (i + 1));
  kg.forEach((r, i) => rrf[r.id] = (rrf[r.id] || 0) + 0.4 / (i + 1));
  return Object.entries(rrf).sort((a, b) => b[1] - a[1]).slice(0, topK)
    .map(([id, score]) => ({ paper: KG[id], score: +score.toFixed(4), vecRank: vec.findIndex(r => r.id === id) + 1, kgRank: kg.findIndex(r => r.id === id) + 1 }))
    .filter(r => r.paper);
}

// ═══════════════════════════════════════════════════════════════
// PROMPT BUILDER
// ═══════════════════════════════════════════════════════════════
function buildPrompt(query, retrieved) {
  const ctx = retrieved.map((r, i) => {
    const p = r.paper;
    return `[Paper ${i+1} — Fusion Score: ${r.score}]
Title: ${p.title}
Authors: ${p.authors.join(", ")}
Year: ${p.year} | Journal: ${p.journal}
Keywords: ${p.keywords.join(", ")}
Domains: ${p.domains.join(", ")}
Citations: ${p.citations.map(c => `"${c.title}" (${c.year}, cited ${c.count}×)`).join("; ") || "None"}
KG Relations: ${p.shares_topic.map(r => `shares topic "${r.kw}" with ${r.pid}`).join("; ") || "None"}`;
  }).join("\n\n");

  return `You are an expert NLP research analyst with deep knowledge of text summarization systems.

A user has queried a Hybrid RAG (Retrieval-Augmented Generation) research knowledge base.

USER QUERY: "${query}"

RETRIEVED PAPERS (via TF-IDF Vector Search 60% + Knowledge Graph Traversal 40%, fused with Reciprocal Rank Fusion):
${ctx}

INSTRUCTIONS:
Based on these retrieved papers and your knowledge, provide a comprehensive, well-structured answer to the user's query. Your response must:
1. Directly answer the query with concrete insights from the retrieved papers
2. Cite specific papers by their titles and authors
3. Compare and contrast different approaches found across papers
4. Highlight key findings, methodologies, and contributions relevant to the query
5. Note any knowledge gaps or areas for further research
6. Be written in clear academic prose (not bullet points)

Format your response with these sections:
**Direct Answer**
**Key Findings from Retrieved Papers**
**Methodology Comparison**
**Research Landscape**
**Key Takeaways**

Be specific, cite authors and years, and synthesize insights across all retrieved papers.`;
}

// ═══════════════════════════════════════════════════════════════
// PARTICLE SYSTEM (Canvas)
// ═══════════════════════════════════════════════════════════════
function useParticles(canvasRef) {
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let raf, particles = [];
    const resize = () => { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; };
    resize();
    window.addEventListener("resize", resize);
    for (let i = 0; i < 60; i++) particles.push({
      x: Math.random() * canvas.width, y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.4, vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 1.5 + 0.3,
      col: ["#00ffaa","#0080ff","#aa44ff","#ff6b35","#ffd60a"][Math.floor(Math.random() * 5)],
      opacity: Math.random() * 0.6 + 0.1,
    });
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x, dy = particles[i].y - particles[j].y;
          const d = Math.sqrt(dx*dx + dy*dy);
          if (d < 130) { ctx.beginPath(); ctx.strokeStyle = `rgba(0,255,170,${0.05*(1-d/130)})`; ctx.lineWidth=0.5; ctx.moveTo(particles[i].x,particles[i].y); ctx.lineTo(particles[j].x,particles[j].y); ctx.stroke(); }
        }
      }
      particles.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0) p.x = canvas.width; if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height; if (p.y > canvas.height) p.y = 0;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
        ctx.fillStyle = p.col; ctx.globalAlpha = p.opacity; ctx.fill(); ctx.globalAlpha = 1;
      });
      raf = requestAnimationFrame(draw);
    };
    draw();
    return () => { cancelAnimationFrame(raf); window.removeEventListener("resize", resize); };
  }, []);
}

// ═══════════════════════════════════════════════════════════════
// COMPONENTS
// ═══════════════════════════════════════════════════════════════
function Tag({ children, color = "#00ffaa" }) {
  return (
    <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, padding: "2px 8px", borderRadius: 99, border: `1px solid ${color}40`, background: `${color}12`, color, display: "inline-block", margin: "2px" }}>{children}</span>
  );
}

function PipelineStep({ label, sub, color, active, done, index }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 0" }}>
      <div style={{ width: 32, height: 32, borderRadius: "50%", flexShrink: 0, background: done ? color : active ? `${color}25` : "rgba(255,255,255,0.04)", border: `2px solid ${active || done ? color : "rgba(255,255,255,0.08)"}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, color: done ? "#000" : active ? color : "rgba(255,255,255,0.3)", boxShadow: active ? `0 0 20px ${color}60` : done ? `0 0 12px ${color}40` : "none", transition: "all 0.4s ease", fontFamily: "'JetBrains Mono', monospace" }}>
        {done ? "✓" : index + 1}
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 12, fontWeight: 600, color: active ? color : done ? "#e8edf5" : "rgba(232,237,245,0.4)", fontFamily: "'Unbounded', sans-serif", transition: "color 0.3s" }}>{label}</div>
        {sub && <div style={{ fontSize: 10, color: "rgba(113,128,150,0.8)", fontFamily: "'JetBrains Mono', monospace", marginTop: 2 }}>{sub}</div>}
      </div>
      {active && (
        <div style={{ display: "flex", gap: 3 }}>
          {[0,1,2].map(i => <div key={i} style={{ width: 4, height: 4, borderRadius: "50%", background: color, animation: `bounce 1s ease ${i*0.2}s infinite` }} />)}
        </div>
      )}
    </div>
  );
}

function MetricBadge({ label, value, color }) {
  return (
    <div style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 8, padding: "10px 12px", textAlign: "center" }}>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 18, fontWeight: 700, color, marginBottom: 2 }}>{value}</div>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568", textTransform: "uppercase", letterSpacing: 1 }}>{label}</div>
    </div>
  );
}

function RetrievedCard({ result, index }) {
  const p = result.paper;
  const colors = ["#00ffaa","#0080ff","#aa44ff","#ff6b35","#ffd60a"];
  const c = colors[index % colors.length];
  return (
    <div style={{ background: "rgba(255,255,255,0.02)", border: `1px solid ${c}30`, borderRadius: 10, padding: 14, position: "relative", overflow: "hidden" }}>
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 2, background: `linear-gradient(90deg, ${c}, transparent)` }} />
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: c, border: `1px solid ${c}40`, padding: "1px 7px", borderRadius: 99 }}>{p.id}</span>
        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568" }}>{p.year}</span>
        <span style={{ marginLeft: "auto", fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: c }}>RRF: {result.score}</span>
        {result.vecRank > 0 && <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#0080ff" }}>V#{result.vecRank}</span>}
        {result.kgRank > 0 && <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#aa44ff" }}>KG#{result.kgRank}</span>}
      </div>
      <div style={{ fontSize: 12, fontWeight: 600, lineHeight: 1.35, marginBottom: 6, fontFamily: "'Unbounded', sans-serif" }}>{p.title}</div>
      <div style={{ fontSize: 10, color: "#718096", marginBottom: 8 }}>{p.authors.slice(0,2).join(", ")}{p.authors.length > 2 ? ` +${p.authors.length-2}` : ""} · {p.journal}</div>
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        {p.keywords.slice(0,3).map(k => <Tag key={k} color="#00eeff">{k}</Tag>)}
        {p.domains.slice(0,1).map(d => <Tag key={d} color="#ff6b35">{d}</Tag>)}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════════════════════
const SUGGESTED = [
  "What are the main approaches to automatic text summarization?",
  "How do transformer models improve NLP summarization?",
  "Compare extractive and abstractive summarization methods",
  "What role does NLP play in AI-powered research tools?",
  "How is LSTM used in text summarization?",
  "What evaluation metrics are used for summarization systems?",
];

const PIPELINE_STEPS = [
  { label: "Query Analysis", sub: "Tokenize & extract intent", color: "#00ffaa" },
  { label: "TF-IDF Vector Search", sub: "Semantic similarity (60%)", color: "#0080ff" },
  { label: "KG Graph Traversal", sub: "Structural retrieval (40%)", color: "#aa44ff" },
  { label: "RRF Fusion", sub: "Reciprocal rank merging", color: "#ff6b35" },
  { label: "Prompt Engineering", sub: "KG context injection", color: "#ffd60a" },
  { label: "Claude Sonnet", sub: "Streaming answer...", color: "#00eeff" },
];

export default function App() {
  const canvasRef = useRef(null);
  useParticles(canvasRef);

  const [query, setQuery] = useState("");
  const [phase, setPhase] = useState("idle");
  const [activeStep, setActiveStep] = useState(-1);
  const [doneSteps, setDoneSteps] = useState([]);
  const [retrieved, setRetrieved] = useState([]);
  const [answer, setAnswer] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState("query");
  const [logLines, setLogLines] = useState([]);

  const answerRef = useRef(null);

  useEffect(() => {
    if (answerRef.current) answerRef.current.scrollTop = answerRef.current.scrollHeight;
  }, [answer]);

  const addLog = useCallback((msg, color = "#718096") => {
    setLogLines(prev => [...prev.slice(-30), { msg, color, ts: Date.now() }]);
  }, []);

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  const runPipeline = useCallback(async (q) => {
    if (!q.trim() || phase === "running") return;
    const finalQuery = q.trim();
    setPhase("running");
    setActiveStep(0);
    setDoneSteps([]);
    setRetrieved([]);
    setAnswer("");
    setStreaming(false);
    setMetrics(null);
    setLogLines([]);

    addLog(`[QUERY] "${finalQuery}"`, "#00ffaa");
    await sleep(600);

    setDoneSteps([0]); setActiveStep(1);
    addLog("[VEC] Building TF-IDF query vector...", "#0080ff");
    await sleep(500);

    const vecResults = tfidfSearch(finalQuery, 5);
    addLog(`[VEC] ${vecResults.length} results — top score: ${vecResults[0]?.score.toFixed(4)}`, "#0080ff");
    await sleep(400);

    setDoneSteps([0,1]); setActiveStep(2);
    addLog("[KG] Traversing keyword & domain nodes...", "#aa44ff");
    await sleep(500);

    const kgResults = kgSearch(finalQuery, 5);
    addLog(`[KG] ${kgResults.length} results — top score: ${kgResults[0]?.score.toFixed(2)}`, "#aa44ff");
    await sleep(400);

    setDoneSteps([0,1,2]); setActiveStep(3);
    addLog("[RRF] Fusing: 0.6×VEC + 0.4×KG", "#ff6b35");
    await sleep(500);

    const fused = hybridRetrieve(finalQuery, 5);
    setRetrieved(fused);
    addLog(`[RRF] Fused ${fused.length} results — top: ${fused[0]?.paper.id} (${fused[0]?.score})`, "#ff6b35");
    await sleep(400);

    setDoneSteps([0,1,2,3]); setActiveStep(4);
    const prompt = buildPrompt(finalQuery, fused);
    const promptWords = prompt.split(" ").length;
    addLog(`[PROMPT] Built: ~${promptWords} words, ${fused.length} papers injected`, "#ffd60a");
    await sleep(600);

    // Step 5 — LLM streaming call to local server
    setDoneSteps([0,1,2,3,4]); setActiveStep(5);
    addLog("[LLM] Connecting to Claude Sonnet via local server...", "#00eeff");
    setStreaming(true);
    setActiveTab("answer");

    const t0 = performance.now();
    let fullText = "";

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || `Server error ${res.status}`);
      }

      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop();
        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const data = line.slice(6).trim();
          if (!data || data === "[DONE]") continue;
          try {
            const evt = JSON.parse(data);
            if (evt.error) throw new Error(evt.error);
            if (evt.text) {
              fullText += evt.text;
              setAnswer(fullText);
            }
          } catch (e) {
            if (e.message !== "Unexpected end of JSON input") throw e;
          }
        }
      }
    } catch (err) {
      addLog(`[ERROR] ${err.message}`, "#ff3366");
      setPhase("error");
      setStreaming(false);
      return;
    }

    const elapsed = ((performance.now() - t0) / 1000).toFixed(1);
    const outTokens = Math.round(fullText.split(" ").length * 1.3);
    setStreaming(false);
    setDoneSteps([0,1,2,3,4,5]);
    setActiveStep(-1);
    setPhase("done");
    addLog(`[LLM] Stream complete: ~${outTokens} tokens | ${elapsed}s`, "#00ffaa");

    const kwCov = fused[0] ? fused[0].paper.keywords.filter(k => fullText.toLowerCase().includes(k.toLowerCase().slice(0,8))).length / Math.max(fused[0].paper.keywords.length, 1) : 0;
    const sections = ["Direct Answer","Key Findings","Methodology","Research Landscape","Key Takeaways"].filter(s => fullText.includes(s)).length / 5;
    const m = { retrieved: fused.length, vecHits: vecResults.length, kgHits: kgResults.length, promptTokens: Math.round(prompt.split(" ").length * 1.3), outTokens, latency: elapsed, kwCov: +kwCov.toFixed(3), secComp: +sections.toFixed(2), topPaper: fused[0]?.paper.id, topScore: fused[0]?.score };
    setMetrics(m);
    setHistory(prev => [{ query: finalQuery, answer: fullText, retrieved: fused, metrics: { outTokens, latency: elapsed, kwCov: +kwCov.toFixed(3) }, ts: new Date().toLocaleTimeString() }, ...prev.slice(0, 9)]);
  }, [phase, addLog]);

  const handleSubmit = (q) => {
    const finalQ = q || query;
    if (!finalQ.trim()) return;
    setQuery(finalQ);
    runPipeline(finalQ);
  };

  return (
    <div style={{ minHeight: "100vh", background: "#02040a", color: "#e8edf5", fontFamily: "'Outfit', sans-serif", position: "relative", overflow: "hidden" }}>
      <canvas ref={canvasRef} style={{ position: "fixed", inset: 0, zIndex: 0, opacity: 0.5, width: "100%", height: "100%" }} />
      <div style={{ position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none", backgroundImage: "linear-gradient(rgba(0,255,170,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,170,0.02) 1px, transparent 1px)", backgroundSize: "40px 40px" }} />
      <div style={{ position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none" }}>
        <div style={{ position: "absolute", width: 600, height: 600, top: -200, left: -150, borderRadius: "50%", background: "radial-gradient(circle, rgba(0,255,170,0.1) 0%, transparent 70%)", filter: "blur(80px)", animation: "drift1 20s ease infinite" }} />
        <div style={{ position: "absolute", width: 500, height: 500, top: "30%", right: -100, borderRadius: "50%", background: "radial-gradient(circle, rgba(0,128,255,0.1) 0%, transparent 70%)", filter: "blur(80px)", animation: "drift2 25s ease infinite" }} />
        <div style={{ position: "absolute", width: 400, height: 400, bottom: -100, left: "40%", borderRadius: "50%", background: "radial-gradient(circle, rgba(170,68,255,0.09) 0%, transparent 70%)", filter: "blur(80px)", animation: "drift3 18s ease infinite" }} />
      </div>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Unbounded:wght@400;600;700;900&family=Outfit:wght@300;400;500;600&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(0,255,170,0.3); border-radius: 99px; }
        @keyframes drift1 { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(80px,-60px) scale(1.1)} }
        @keyframes drift2 { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(-60px,40px) scale(0.9)} }
        @keyframes drift3 { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(40px,-30px) scale(1.15)} }
        @keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
        @keyframes slideIn { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
        @keyframes fadeIn { from{opacity:0} to{opacity:1} }
        textarea:focus { outline: none; }
        .suggestion:hover { border-color: rgba(0,255,170,0.4) !important; background: rgba(0,255,170,0.05) !important; cursor: pointer; }
        .hist-item:hover { border-color: rgba(0,255,170,0.3) !important; cursor: pointer; }
        .answer-text strong { color: #00ffaa; }
      `}</style>

      {/* TOP BAR */}
      <div style={{ position: "sticky", top: 0, zIndex: 100, background: "rgba(2,4,10,0.9)", backdropFilter: "blur(20px)", borderBottom: "1px solid rgba(255,255,255,0.06)", padding: "0 28px", height: 52, display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{ fontFamily: "'Unbounded', sans-serif", fontSize: 16, fontWeight: 900, color: "#00ffaa", letterSpacing: 1, textShadow: "0 0 20px rgba(0,255,170,0.5)", flexShrink: 0 }}>RAG//CORE</div>
        <div style={{ width: 1, height: 24, background: "rgba(255,255,255,0.08)" }} />
        <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 9, fontFamily: "'JetBrains Mono', monospace", color: "#00ffaa", flexShrink: 0 }}>
          <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#00ffaa", animation: "bounce 2s ease infinite" }} />
          SYSTEM ONLINE
        </div>
        <div style={{ flex: 1, overflow: "hidden", fontSize: 9, fontFamily: "'JetBrains Mono', monospace", color: "#4a5568" }}>
          ◈ 9 PAPERS · 34 AUTHORS · 801 TRIPLES · CLAUDE SONNET · LOCAL SERVER :3001
        </div>
        {["query","pipeline","papers","history"].map(tab => (
          <button key={tab} onClick={() => setActiveTab(tab)} style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, letterSpacing: 1.5, textTransform: "uppercase", background: "transparent", border: "none", borderBottom: `2px solid ${activeTab === tab ? "#00ffaa" : "transparent"}`, color: activeTab === tab ? "#e8edf5" : "#4a5568", padding: "0 12px", height: "100%", cursor: "pointer", transition: "all 0.2s", flexShrink: 0 }}>{tab}</button>
        ))}
      </div>

      <div style={{ position: "relative", zIndex: 2, maxWidth: 1400, margin: "0 auto", padding: "24px 24px" }}>

        {/* ═══ QUERY TAB ═══ */}
        {activeTab === "query" && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            <div style={{ textAlign: "center", marginBottom: 36 }}>
              <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: "#00ffaa", letterSpacing: 3, border: "1px solid rgba(0,255,170,0.3)", background: "rgba(0,255,170,0.06)", padding: "4px 16px", borderRadius: 99, display: "inline-flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
                <div style={{ width: 5, height: 5, borderRadius: "50%", background: "#00ffaa", animation: "bounce 1.5s ease infinite" }} />
                HYBRID RAG PIPELINE — LOCAL DEPLOYMENT
              </div>
              <h1 style={{ fontFamily: "'Unbounded', sans-serif", fontSize: "clamp(28px,5vw,56px)", fontWeight: 900, lineHeight: 1, letterSpacing: -2, background: "linear-gradient(135deg, #00ffaa, #00eeff, #0080ff, #aa44ff)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text", marginBottom: 12 }}>
                Query Your<br />Research KG
              </h1>
              <p style={{ color: "#718096", fontSize: 14, fontWeight: 300, maxWidth: 480, margin: "0 auto" }}>
                Hybrid RAG pipeline powered by Claude Sonnet. Retrieves papers via TF-IDF + KG traversal, fuses with RRF, and streams answers.
              </p>
            </div>

            {/* Search Box */}
            <div style={{ maxWidth: 760, margin: "0 auto 32px" }}>
              <div style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(0,255,170,0.2)", borderRadius: 16, overflow: "hidden", boxShadow: "0 0 40px rgba(0,255,170,0.07)" }}>
                <textarea value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSubmit(); } }} placeholder="Ask about text summarization methods, NLP approaches, transformer models..." rows={3} style={{ width: "100%", background: "transparent", border: "none", padding: "18px 20px 10px", fontSize: 14, color: "#e8edf5", fontFamily: "'Outfit', sans-serif", resize: "none", lineHeight: 1.6 }} />
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "10px 16px", borderTop: "1px solid rgba(255,255,255,0.05)" }}>
                  <span style={{ fontSize: 10, fontFamily: "'JetBrains Mono', monospace", color: "#4a5568" }}>KG: 9 papers · Enter to send · Shift+Enter for newline</span>
                  <button onClick={() => handleSubmit()} disabled={!query.trim() || phase === "running"} style={{ background: phase === "running" ? "rgba(0,255,170,0.1)" : "linear-gradient(135deg, #00ffaa, #0080ff)", border: "none", borderRadius: 8, padding: "9px 22px", fontFamily: "'JetBrains Mono', monospace", fontSize: 11, fontWeight: 700, color: phase === "running" ? "#00ffaa" : "#000", cursor: phase === "running" ? "default" : "pointer", letterSpacing: 1, opacity: !query.trim() ? 0.4 : 1, transition: "all 0.2s", display: "flex", alignItems: "center", gap: 8 }}>
                    {phase === "running" ? <><div style={{ width: 10, height: 10, border: "2px solid #00ffaa", borderTopColor: "transparent", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />PROCESSING</> : "▶ RUN PIPELINE"}
                  </button>
                </div>
              </div>
            </div>

            {/* Suggestions */}
            <div style={{ maxWidth: 760, margin: "0 auto 40px" }}>
              <div style={{ fontSize: 9, fontFamily: "'JetBrains Mono', monospace", color: "#4a5568", letterSpacing: 2, marginBottom: 12, textTransform: "uppercase" }}>Suggested Queries</div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(230px, 1fr))", gap: 8 }}>
                {SUGGESTED.map((s, i) => (
                  <button key={i} className="suggestion" onClick={() => { setQuery(s); handleSubmit(s); }} style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 8, padding: "10px 12px", textAlign: "left", fontFamily: "'Outfit', sans-serif", fontSize: 12, color: "#718096", cursor: "pointer", transition: "all 0.2s", lineHeight: 1.4 }}>{s}</button>
                ))}
              </div>
            </div>

            {/* RESULTS */}
            {phase !== "idle" && (
              <div style={{ maxWidth: 1200, margin: "0 auto", display: "grid", gridTemplateColumns: "300px 1fr", gap: 20 }}>
                {/* Left panel */}
                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                  <div style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 18 }}>
                    <div style={{ fontSize: 9, fontFamily: "'JetBrains Mono', monospace", color: "#4a5568", letterSpacing: 2, marginBottom: 14, textTransform: "uppercase" }}>Pipeline Execution</div>
                    {PIPELINE_STEPS.map((s, i) => <PipelineStep key={i} {...s} active={activeStep === i} done={doneSteps.includes(i)} index={i} />)}
                  </div>

                  {metrics && (
                    <div style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(0,255,170,0.15)", borderRadius: 14, padding: 18 }}>
                      <div style={{ fontSize: 9, fontFamily: "'JetBrains Mono', monospace", color: "#4a5568", letterSpacing: 2, marginBottom: 14, textTransform: "uppercase" }}>Run Metrics</div>
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                        <MetricBadge label="Retrieved" value={metrics.retrieved} color="#00ffaa" />
                        <MetricBadge label="Vec Hits" value={metrics.vecHits} color="#0080ff" />
                        <MetricBadge label="KG Hits" value={metrics.kgHits} color="#aa44ff" />
                        <MetricBadge label="Latency" value={`${metrics.latency}s`} color="#ff6b35" />
                        <MetricBadge label="~Tokens" value={metrics.outTokens} color="#ffd60a" />
                        <MetricBadge label="Kw Cov" value={metrics.kwCov} color="#00eeff" />
                        <MetricBadge label="Sec Comp" value={metrics.secComp} color="#00ffaa" />
                        <MetricBadge label="Top Paper" value={metrics.topPaper} color="#aa44ff" />
                      </div>
                    </div>
                  )}

                  {retrieved.length > 0 && (
                    <div style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 18 }}>
                      <div style={{ fontSize: 9, fontFamily: "'JetBrains Mono', monospace", color: "#4a5568", letterSpacing: 2, marginBottom: 14, textTransform: "uppercase" }}>Retrieved Papers</div>
                      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                        {retrieved.map((r, i) => <RetrievedCard key={r.paper.id} result={r} index={i} />)}
                      </div>
                    </div>
                  )}
                </div>

                {/* Right panel */}
                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                  {/* Log */}
                  <div style={{ background: "rgba(6,9,18,0.9)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, overflow: "hidden" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 14px", background: "rgba(255,255,255,0.03)", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
                      {["#ff5f57","#febc2e","#28c840"].map(c => <div key={c} style={{ width: 10, height: 10, borderRadius: "50%", background: c }} />)}
                      <span style={{ flex: 1, textAlign: "center", fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568", letterSpacing: 2 }}>PIPELINE LOG</span>
                    </div>
                    <div style={{ padding: 14, maxHeight: 150, overflowY: "auto", fontFamily: "'JetBrains Mono', monospace", fontSize: 11, lineHeight: 1.8 }}>
                      {logLines.map((l, i) => <div key={i} style={{ color: l.color }}>{l.msg}</div>)}
                      {phase === "running" && <span style={{ display: "inline-block", width: 8, height: 13, background: "#00ffaa", animation: "blink 1s step-end infinite", verticalAlign: "middle" }} />}
                    </div>
                  </div>

                  {/* Answer */}
                  {(answer || streaming) && (
                    <div style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(0,255,170,0.2)", borderRadius: 14, overflow: "hidden", flex: 1 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "14px 18px", background: "rgba(0,255,170,0.04)", borderBottom: "1px solid rgba(0,255,170,0.12)" }}>
                        <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#00ffaa", animation: streaming ? "bounce 1s ease infinite" : "none" }} />
                        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: "#00ffaa", letterSpacing: 1, textTransform: "uppercase" }}>
                          {streaming ? "Claude is streaming..." : "Answer Ready"}
                        </span>
                        {!streaming && metrics && <span style={{ marginLeft: "auto", fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568" }}>{metrics.outTokens} tokens · {metrics.latency}s</span>}
                      </div>
                      <div ref={answerRef} className="answer-text" style={{ padding: "20px 22px", maxHeight: 560, overflowY: "auto", fontSize: 13, lineHeight: 1.8, color: "#c8d5e8", whiteSpace: "pre-wrap" }}>
                        {answer}
                        {streaming && <span style={{ display: "inline-block", width: 8, height: 14, background: "#00ffaa", animation: "blink 1s step-end infinite", verticalAlign: "middle", marginLeft: 2 }} />}
                      </div>
                    </div>
                  )}

                  {phase === "error" && (
                    <div style={{ background: "rgba(255,51,102,0.08)", border: "1px solid rgba(255,51,102,0.3)", borderRadius: 10, padding: "14px 18px", fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: "#ff3366" }}>
                      ⚠ Pipeline error — check that the server is running at localhost:3001 and your ANTHROPIC_API_KEY is set in server/.env
                    </div>
                  )}

                  {phase === "done" && (
                    <button onClick={() => { setPhase("idle"); setQuery(""); setAnswer(""); setRetrieved([]); setMetrics(null); setLogLines([]); }} style={{ background: "transparent", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 8, padding: "11px 0", fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: "#718096", cursor: "pointer", letterSpacing: 1, textTransform: "uppercase" }}>
                      ↺ New Query
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ═══ PIPELINE TAB ═══ */}
        {activeTab === "pipeline" && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            <div style={{ marginBottom: 28 }}>
              <div style={{ fontFamily: "'Unbounded', sans-serif", fontSize: 22, fontWeight: 700, letterSpacing: -0.5, marginBottom: 6 }}>Pipeline Architecture</div>
              <div style={{ color: "#718096", fontSize: 13 }}>Hybrid RAG — TF-IDF Vector Search × Knowledge Graph Traversal × RRF Fusion × Claude Sonnet Streaming</div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 24 }}>
              <div style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 22 }}>
                <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568", letterSpacing: 2, marginBottom: 18, textTransform: "uppercase" }}>Fusion Formula</div>
                <div style={{ background: "rgba(6,9,18,0.9)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 10, padding: 16, fontFamily: "'JetBrains Mono', monospace", fontSize: 13, color: "#00ffaa", lineHeight: 2.2 }}>
                  score<span style={{ color: "#4a5568" }}>_RRF</span>(d) =<br/>
                  &nbsp;<span style={{ color: "#0080ff" }}>0.6</span> / (rank<span style={{ color: "#4a5568" }}>_vec</span> + 1)<br/>
                  + <span style={{ color: "#aa44ff" }}>0.4</span> / (rank<span style={{ color: "#4a5568" }}>_kg</span> + 1)
                </div>
                {[{ label: "TF-IDF Vector Store", pct: 60, color: "#0080ff" }, { label: "KG Graph Traversal", pct: 40, color: "#aa44ff" }].map(b => (
                  <div key={b.label} style={{ marginTop: 14 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#718096", marginBottom: 5 }}><span>{b.label}</span><span style={{ color: b.color, fontFamily: "'JetBrains Mono', monospace" }}>{b.pct}%</span></div>
                    <div style={{ height: 5, background: "rgba(255,255,255,0.05)", borderRadius: 99, overflow: "hidden" }}>
                      <div style={{ height: "100%", width: b.pct + "%", background: b.color, borderRadius: 99 }} />
                    </div>
                  </div>
                ))}
              </div>
              <div style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 14, padding: 22 }}>
                <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568", letterSpacing: 2, marginBottom: 18, textTransform: "uppercase" }}>Relationship Distribution</div>
                {[{n:"COLLABORATED_WITH",c:54,col:"#00ffaa"},{n:"AFFILIATED_WITH",c:49,col:"#0080ff"},{n:"HAS_KEYWORD",c:36,col:"#aa44ff"},{n:"AUTHORED",c:34,col:"#ff6b35"},{n:"BELONGS_TO_DOMAIN",c:13,col:"#ffd60a"},{n:"PUBLISHED_IN",c:9,col:"#00eeff"},{n:"CITES",c:9,col:"#00ffaa"},{n:"SHARES_TOPIC",c:2,col:"#ff3366"}].map(r => (
                  <div key={r.n} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 9 }}>
                    <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: r.col, width: 170, flexShrink: 0 }}>{r.n}</span>
                    <div style={{ flex: 1, height: 4, background: "rgba(255,255,255,0.04)", borderRadius: 99, overflow: "hidden" }}>
                      <div style={{ height: "100%", width: (r.c/54*100)+"%", background: r.col, borderRadius: 99 }} />
                    </div>
                    <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#718096", width: 20, textAlign: "right" }}>{r.c}</span>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))", gap: 10 }}>
              {[["Papers","9","#00ffaa"],["Authors","34","#0080ff"],["KG Triples","801","#aa44ff"],["Relationships","207","#ff6b35"],["Institutions","10","#ffd60a"],["Journals","8","#00eeff"],["Keywords","34","#00ffaa"],["Domains","12","#ff3366"],["References","9","#aa44ff"]].map(([l,v,c]) => (
                <div key={l} style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: 10, padding: "14px 12px", textAlign: "center" }}>
                  <div style={{ fontFamily: "'Unbounded', sans-serif", fontSize: 28, fontWeight: 700, color: c, letterSpacing: -2 }}>{v}</div>
                  <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 8, color: "#4a5568", textTransform: "uppercase", letterSpacing: 1.5 }}>{l}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ═══ PAPERS TAB ═══ */}
        {activeTab === "papers" && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            <div style={{ marginBottom: 24 }}>
              <div style={{ fontFamily: "'Unbounded', sans-serif", fontSize: 22, fontWeight: 700, letterSpacing: -0.5, marginBottom: 6 }}>Research Papers</div>
              <div style={{ color: "#718096", fontSize: 13 }}>9 papers in the knowledge graph — click any to run a query</div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: 14 }}>
              {PAPERS.map((p, i) => {
                const colors = ["#00ffaa","#0080ff","#aa44ff","#ff6b35","#ffd60a","#00eeff","#ff3366","#00ffaa","#0080ff"];
                const c = colors[i];
                return (
                  <div key={p.id} onClick={() => { setQuery(`Summarize and analyze: ${p.title}`); setActiveTab("query"); handleSubmit(`Summarize and analyze: ${p.title}`); }}
                    style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12, padding: 18, cursor: "pointer", position: "relative", overflow: "hidden", transition: "all 0.25s" }}
                    onMouseEnter={e => { e.currentTarget.style.borderColor = c; e.currentTarget.style.transform = "translateY(-4px)"; }}
                    onMouseLeave={e => { e.currentTarget.style.borderColor = "rgba(255,255,255,0.07)"; e.currentTarget.style.transform = ""; }}>
                    <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 2, background: `linear-gradient(90deg, ${c}, transparent)` }} />
                    <div style={{ display: "flex", gap: 8, marginBottom: 8, alignItems: "center" }}>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: c, border: `1px solid ${c}40`, padding: "1px 8px", borderRadius: 99 }}>{p.id}</span>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568" }}>{p.year}</span>
                      {p.shares_topic.length > 0 && <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#ff6b35", border: "1px solid rgba(255,107,53,0.3)", padding: "1px 7px", borderRadius: 99 }}>LINKED</span>}
                    </div>
                    <div style={{ fontFamily: "'Unbounded', sans-serif", fontSize: 13, fontWeight: 600, lineHeight: 1.35, marginBottom: 8 }}>{p.title}</div>
                    <div style={{ fontSize: 11, color: "#718096", marginBottom: 6 }}>{p.authors.slice(0,2).join(", ")}{p.authors.length > 2 ? ` +${p.authors.length-2}` : ""}</div>
                    <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568", marginBottom: 10 }}>{p.journal}</div>
                    <div style={{ display: "flex", flexWrap: "wrap" }}>
                      {p.keywords.slice(0,3).map(k => <Tag key={k} color="#00eeff">{k}</Tag>)}
                      {p.domains.slice(0,1).map(d => <Tag key={d} color="#ff6b35">{d}</Tag>)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ═══ HISTORY TAB ═══ */}
        {activeTab === "history" && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            <div style={{ marginBottom: 24 }}>
              <div style={{ fontFamily: "'Unbounded', sans-serif", fontSize: 22, fontWeight: 700, letterSpacing: -0.5, marginBottom: 6 }}>Query History</div>
              <div style={{ color: "#718096", fontSize: 13 }}>{history.length} queries this session</div>
            </div>
            {history.length === 0 ? (
              <div style={{ textAlign: "center", padding: 80, color: "#4a5568" }}>
                <div style={{ fontSize: 36, marginBottom: 12 }}>⬡</div>
                <div>No queries yet. Run a query to see history here.</div>
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {history.map((h, i) => (
                  <div key={i} className="hist-item" style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 12, overflow: "hidden", transition: "border-color 0.2s" }}
                    onClick={() => { setQuery(h.query); setAnswer(h.answer); setRetrieved(h.retrieved); setMetrics(h.metrics); setPhase("done"); setActiveTab("query"); }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "12px 18px", borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#00ffaa" }}>#{history.length - i}</span>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568" }}>{h.ts}</span>
                      <span style={{ flex: 1, fontSize: 12, color: "#e8edf5", fontWeight: 500, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{h.query}</span>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#00ffaa" }}>KwCov: {h.metrics?.kwCov}</span>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#0080ff" }}>{h.metrics?.outTokens}t</span>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#4a5568" }}>{h.metrics?.latency}s</span>
                    </div>
                    <div style={{ padding: "12px 18px", fontSize: 12, color: "#718096", lineHeight: 1.6, maxHeight: 80, overflow: "hidden", position: "relative" }}>
                      {h.answer.slice(0, 200)}…
                      <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 30, background: "linear-gradient(transparent, rgba(10,14,26,0.9))" }} />
                    </div>
                    <div style={{ padding: "8px 18px", display: "flex", gap: 6, borderTop: "1px solid rgba(255,255,255,0.04)" }}>
                      {h.retrieved.slice(0,3).map(r => <span key={r.paper.id} style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "#aa44ff", border: "1px solid rgba(170,68,255,0.3)", padding: "1px 8px", borderRadius: 99 }}>{r.paper.id}</span>)}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
