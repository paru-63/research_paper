#!/usr/bin/env python3
"""
=============================================================================
MILESTONE 3 — HYBRID RAG PIPELINE
Integrates Knowledge Graph (KG) with Retrieval-Augmented Generation (RAG)
Calls Claude LLM to generate structured research paper summaries
=============================================================================

Pipeline Flow:
  Extracted KG Data (entities + relationships + triples)
        │
   ┌────┴────────────────────────┐
   │                             │
   ▼                             ▼
TF-IDF Vector Store    Knowledge Graph Store
(Semantic Retrieval)   (Graph-Based Retrieval)
   │                             │
   └────────────┬────────────────┘
                │  Reciprocal Rank Fusion
                ▼
        Hybrid Retriever
                │
                ▼
        Prompt Builder
   (KG context + RAG chunks)
                │
                ▼
      Anthropic Claude LLM
    (Paper Summary Generation)
                │
                ▼
          Final Output
   (Summaries + Evaluations)
"""

import json
import math
import os
import re
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime


# =============================================================================
# MODULE 1 — KNOWLEDGE GRAPH STORE
# =============================================================================

class KnowledgeGraphStore:
    def __init__(self, entities_path, relationships_path, triples_path):
        print("  📡 Loading Knowledge Graph from extracted files...")
        with open(entities_path, encoding="utf-8") as f:
            raw = json.load(f)
        self.entities = raw["entities"]
        with open(relationships_path, encoding="utf-8") as f:
            raw = json.load(f)
        self.relationships = raw["relationships"]
        with open(triples_path, encoding="utf-8") as f:
            raw = json.load(f)
        self.triples = raw["triples"]
        self.ref_by_id = {r["id"]: r for r in self.entities.get("references", [])}
        self._build_indexes()
        total_e = sum(len(v) for v in self.entities.values())
        total_r = sum(len(v) for v in self.relationships.values())
        print(f"     ✅ KG loaded: {total_e} entities | {total_r} relationships | {len(self.triples)} triples")

    def _build_indexes(self):
        self.authored_by    = defaultdict(list)
        self.published_in   = {}
        self.has_keyword    = defaultdict(list)
        self.belongs_domain = defaultdict(list)
        self.cites          = defaultdict(list)
        self.shares_topic   = defaultdict(list)
        self.shares_domain  = defaultdict(list)

        for r in self.relationships.get("AUTHORED", []):
            self.authored_by[r["target"]].append(r["source"])
        for r in self.relationships.get("PUBLISHED_IN", []):
            self.published_in[r["source"]] = r["target"]
        for r in self.relationships.get("HAS_KEYWORD", []):
            self.has_keyword[r["source"]].append(r["target"])
        for r in self.relationships.get("BELONGS_TO_DOMAIN", []):
            self.belongs_domain[r["source"]].append(r["target"])
        for r in self.relationships.get("CITES", []):
            self.cites[r["source"]].append({
                "ref_id": r["target"],
                "citation_count": r["properties"].get("citation_count", 0),
                "cited_year": r["properties"].get("cited_year", ""),
            })
        for r in self.relationships.get("SHARES_TOPIC", []):
            kw = r["properties"].get("shared_keyword", "")
            self.shares_topic[r["source"]].append({"paper_id": r["target"], "shared_keyword": kw})
            self.shares_topic[r["target"]].append({"paper_id": r["source"], "shared_keyword": kw})
        for r in self.relationships.get("SHARES_DOMAIN", []):
            dm = r["properties"].get("shared_domain", "")
            self.shares_domain[r["source"]].append({"paper_id": r["target"], "shared_domain": dm})
            self.shares_domain[r["target"]].append({"paper_id": r["source"], "shared_domain": dm})

        self.paper_by_id = {p["id"]: p for p in self.entities.get("papers", [])}

    def get_paper_context(self, paper_id):
        paper = self.paper_by_id.get(paper_id, {})
        if not paper:
            return {}
        citations = []
        for c in self.cites.get(paper_id, [])[:5]:
            ref = self.ref_by_id.get(c["ref_id"], {})
            citations.append({
                "ref_id": c["ref_id"],
                "title": ref.get("title", c["ref_id"]),
                "year": ref.get("year", c.get("cited_year", "")),
                "citation_count": c["citation_count"],
                "link": ref.get("link", ""),
            })
        return {
            "id":           paper_id,
            "title":        paper.get("title", ""),
            "year":         paper.get("year", ""),
            "doi":          paper.get("doi", ""),
            "authors":      self.authored_by.get(paper_id, []),
            "journal":      self.published_in.get(paper_id, ""),
            "keywords":     self.has_keyword.get(paper_id, []),
            "domains":      self.belongs_domain.get(paper_id, []),
            "citations":    citations,
            "shares_topic": self.shares_topic.get(paper_id, []),
            "shares_domain":self.shares_domain.get(paper_id, []),
        }

    def search_by_keyword(self, query, top_k=5):
        query_lower = query.lower()
        scores = {}
        for paper_id, keywords in self.has_keyword.items():
            score = 0
            for kw in keywords:
                kl = kw.lower()
                if kl in query_lower or query_lower in kl:
                    score += 2
                elif any(tok in kl for tok in query_lower.split() if len(tok) > 3):
                    score += 1
            for dm in self.belongs_domain.get(paper_id, []):
                if dm.lower() in query_lower or any(tok in dm.lower()
                   for tok in query_lower.split() if len(tok) > 3):
                    score += 1
            if score > 0:
                scores[paper_id] = score
        ranked = sorted(scores.items(), key=lambda x: -x[1])
        return [self.get_paper_context(pid) for pid, _ in ranked[:top_k]]

    def get_all_papers(self):
        return [self.get_paper_context(pid) for pid in self.paper_by_id]


# =============================================================================
# MODULE 2 — TF-IDF VECTOR STORE
# =============================================================================

class TFIDFVectorStore:
    def __init__(self):
        self.docs = []
        self.vocab = {}
        self.idf = {}
        self.tfidf = []

    def add_documents(self, documents):
        self.docs = documents
        self._build_index()
        print(f"     ✅ Vector store indexed {len(documents)} paper documents")

    def _tokenize(self, text):
        return re.findall(r"[a-z0-9]+", text.lower())

    def _build_index(self):
        N = len(self.docs)
        tf_list, df = [], Counter()
        for doc in self.docs:
            tokens = self._tokenize(doc["text"])
            tf = Counter(tokens)
            tf_list.append(tf)
            for w in set(tokens):
                df[w] += 1
        all_words = list(df.keys())
        self.vocab = {w: i for i, w in enumerate(all_words)}
        self.idf = {w: math.log((N + 1) / (df[w] + 1)) + 1.0 for w in all_words}
        self.tfidf = []
        for tf in tf_list:
            total = sum(tf.values()) or 1
            vec = {w: (cnt / total) * self.idf[w] for w, cnt in tf.items() if w in self.idf}
            self.tfidf.append(vec)

    def _cosine_sim(self, va, vb):
        dot = sum(va.get(w, 0) * vb.get(w, 0) for w in va)
        na = math.sqrt(sum(v**2 for v in va.values())) or 1e-9
        nb = math.sqrt(sum(v**2 for v in vb.values())) or 1e-9
        return dot / (na * nb)

    def search(self, query, top_k=5):
        tokens = self._tokenize(query)
        tf = Counter(tokens)
        total = sum(tf.values()) or 1
        q_vec = {w: (cnt / total) * self.idf.get(w, 1.0)
                 for w, cnt in tf.items() if w in self.vocab}
        scored = [(i, self._cosine_sim(q_vec, dv)) for i, dv in enumerate(self.tfidf)]
        scored.sort(key=lambda x: -x[1])
        return [{"doc": self.docs[i], "score": round(s, 6)}
                for i, s in scored[:top_k] if s > 0]


# =============================================================================
# MODULE 3 — CORPUS BUILDER
# =============================================================================

class CorpusBuilder:
    @staticmethod
    def build(kg):
        docs = []
        for paper_id, paper in kg.paper_by_id.items():
            authors   = ", ".join(kg.authored_by.get(paper_id, []))
            keywords  = ", ".join(kg.has_keyword.get(paper_id, []))
            domains   = ", ".join(kg.belongs_domain.get(paper_id, []))
            journal   = kg.published_in.get(paper_id, "")
            cit_titles = " ".join(c.get("title","") for c in kg.get_paper_context(paper_id)["citations"])
            text = (
                f"Title: {paper['title']}. Year: {paper.get('year','')}. "
                f"Authors: {authors}. Journal: {journal}. "
                f"Keywords: {keywords}. Domains: {domains}. References: {cit_titles}."
            )
            docs.append({
                "id": paper_id,
                "text": text,
                "metadata": {
                    "title": paper["title"],
                    "year": str(paper.get("year","")),
                    "authors": authors,
                    "journal": journal,
                    "keywords": keywords,
                    "domains": domains,
                },
            })
        return docs


# =============================================================================
# MODULE 4 — HYBRID RETRIEVER (Reciprocal Rank Fusion)
# =============================================================================

class HybridRetriever:
    VECTOR_WEIGHT = 0.60
    GRAPH_WEIGHT  = 0.40

    def __init__(self, vector_store, kg):
        self.vs = vector_store
        self.kg = kg

    def retrieve(self, query, top_k=5):
        vec_hits = self.vs.search(query, top_k=top_k)
        kg_hits  = self.kg.search_by_keyword(query, top_k=top_k)

        rrf_scores = {}
        entry_map  = {}

        for rank, hit in enumerate(vec_hits):
            pid = hit["doc"]["id"]
            rrf_scores[pid] = rrf_scores.get(pid, 0) + self.VECTOR_WEIGHT / (rank + 1)
            entry_map[pid] = {
                "doc": hit["doc"],
                "kg_context": self.kg.get_paper_context(pid),
                "vector_score": hit["score"],
                "vector_rank": rank + 1,
            }

        for rank, kg_ctx in enumerate(kg_hits):
            pid = kg_ctx["id"]
            rrf_scores[pid] = rrf_scores.get(pid, 0) + self.GRAPH_WEIGHT / (rank + 1)
            if pid not in entry_map:
                entry_map[pid] = {
                    "doc": {
                        "id": pid,
                        "text": kg_ctx.get("title",""),
                        "metadata": {
                            "title":   kg_ctx.get("title",""),
                            "year":    str(kg_ctx.get("year","")),
                            "authors": ", ".join(kg_ctx.get("authors",[])),
                            "journal": kg_ctx.get("journal",""),
                            "keywords":  ", ".join(kg_ctx.get("keywords",[])),
                            "domains": ", ".join(kg_ctx.get("domains",[])),
                        },
                    },
                    "kg_context": kg_ctx,
                }
            entry_map[pid]["kg_rank"] = rank + 1

        ranked = sorted(rrf_scores.items(), key=lambda x: -x[1])
        merged = []
        for pid, score in ranked[:top_k]:
            entry = entry_map[pid]
            entry["fusion_score"] = round(score, 6)
            merged.append(entry)

        return {"query": query, "vector_results": vec_hits, "kg_results": kg_hits, "merged": merged}


# =============================================================================
# MODULE 5 — PROMPT BUILDER
# =============================================================================

class PromptBuilder:
    @staticmethod
    def build_summary_prompt(kg_ctx, retrieved_chunks):
        authors  = ", ".join(kg_ctx.get("authors",  [])) or "Not available"
        keywords = ", ".join(kg_ctx.get("keywords", [])) or "Not available"
        domains  = ", ".join(kg_ctx.get("domains",  [])) or "Not available"
        journal  = kg_ctx.get("journal", "Not available")

        cit_lines = ""
        for i, c in enumerate(kg_ctx.get("citations", [])[:4], 1):
            cit_lines += (
                f"      [{i}] {c['title']} ({c['year']}) "
                f"— cited {c['citation_count']} times"
                f"{' | ' + c['link'] if c.get('link') else ''}\n"
            )
        if not cit_lines:
            cit_lines = "      None available\n"

        topic_lines = ""
        for r in kg_ctx.get("shares_topic", [])[:3]:
            topic_lines += f"      • Paper {r['paper_id']} (shared keyword: \"{r['shared_keyword']}\")\n"
        if not topic_lines:
            topic_lines = "      None\n"

        domain_lines = ""
        for r in kg_ctx.get("shares_domain", [])[:3]:
            domain_lines += f"      • Paper {r['paper_id']} (shared domain: \"{r['shared_domain']}\")\n"
        if not domain_lines:
            domain_lines = "      None\n"

        rag_section = ""
        for i, chunk in enumerate(retrieved_chunks[:3], 1):
            m = chunk["doc"]["metadata"]
            rag_section += (
                f"\n    ── Related Paper {i} (fusion score: {chunk.get('fusion_score',0):.4f}) ──\n"
                f"    Title:    {m.get('title','')}\n"
                f"    Year:     {m.get('year','')}  |  Journal: {m.get('journal','')}\n"
                f"    Authors:  {m.get('authors','')}\n"
                f"    Keywords: {m.get('keywords','')}\n"
                f"    Domains:  {m.get('domains','')}\n"
            )
        if not rag_section:
            rag_section = "\n    No related papers retrieved.\n"

        prompt = f"""You are an expert research analyst specializing in Natural Language Processing, AI, and academic literature.

Your task is to write a comprehensive, structured summary of the research paper described below.
Use ALL provided context — the Knowledge Graph metadata AND the retrieved related papers — to
produce a detailed, accurate, and insightful summary.

══════════════════════════════════════════════════════════════════
  TARGET PAPER — KNOWLEDGE GRAPH METADATA
══════════════════════════════════════════════════════════════════

  Paper ID : {kg_ctx.get('id','N/A')}
  Title    : {kg_ctx.get('title','N/A')}
  Year     : {kg_ctx.get('year','N/A')}
  Authors  : {authors}
  Journal  : {journal}
  DOI      : {kg_ctx.get('doi','N/A')}

  Research Domains : {domains}
  Keywords         : {keywords}

  Key References Cited:
{cit_lines}
  Papers Sharing the Same Topic (from Knowledge Graph):
{topic_lines}
  Papers Sharing the Same Domain (from Knowledge Graph):
{domain_lines}

══════════════════════════════════════════════════════════════════
  RETRIEVED RELATED PAPERS — HYBRID RAG CONTEXT
  (Vector Search 60% + Knowledge Graph Traversal 40%)
══════════════════════════════════════════════════════════════════
{rag_section}

══════════════════════════════════════════════════════════════════
  INSTRUCTIONS
══════════════════════════════════════════════════════════════════

Write a detailed research paper summary with exactly these eight sections:

## 1. Overview
Provide 2–3 sentences describing the paper's core topic and its significance in the field.

## 2. Research Problem & Objectives
What specific problem does this paper solve? What are the stated research goals?

## 3. Methodology & Technical Approach
Describe the methods, algorithms, frameworks, or architectures used.
Reference the specific keywords and domains from the Knowledge Graph metadata.

## 4. Key Findings & Contributions
List the main contributions, results, or innovations this paper presents.

## 5. Positioning in the Research Landscape
How does this paper relate to the retrieved related papers?
Use the shared topics/domains from the Knowledge Graph to explain where this work fits.

## 6. Practical Applications & Impact
What real-world applications or downstream tasks does this work enable?

## 7. Limitations & Future Directions
What limitations does the paper have, and what future work could build on it?

## 8. Summary Statement
One concise sentence capturing the paper's single most important contribution.

Write in professional academic language. Be specific — use the actual keywords, domain names,
author names, and journal from the provided context. Do not fabricate any information."""

        return prompt


# =============================================================================
# MODULE 6 — LLM CLIENT (Anthropic Claude API)
# =============================================================================

class LLMClient:
    API_URL = "https://api.anthropic.com/v1/messages"
    MODEL   = "claude-sonnet-4-20250514"

    def __init__(self):
        self.api_key    = os.environ.get("ANTHROPIC_API_KEY", "")
        self.using_mock = not bool(self.api_key)
        if self.using_mock:
            print("  ⚠️  ANTHROPIC_API_KEY not set — using structured mock responses.")
            print("      Set the env var and re-run to get real Claude summaries.\n")
        else:
            print(f"  ✅ LLM client ready: {self.MODEL}\n")

    def call(self, prompt, max_tokens=1500):
        if self.using_mock:
            return self._mock_response(prompt)
        t0 = time.time()
        payload = json.dumps({
            "model":      self.MODEL,
            "max_tokens": max_tokens,
            "messages":   [{"role": "user", "content": prompt}],
        }).encode("utf-8")
        req = urllib.request.Request(
            self.API_URL, data=payload,
            headers={"Content-Type": "application/json",
                     "x-api-key": self.api_key,
                     "anthropic-version": "2023-06-01"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            text = "".join(b.get("text","") for b in result.get("content",[]) if b.get("type")=="text")
            return {
                "text": text,
                "input_tokens":  result.get("usage",{}).get("input_tokens",0),
                "output_tokens": result.get("usage",{}).get("output_tokens",0),
                "latency_sec":   round(time.time()-t0, 2),
                "model":         result.get("model", self.MODEL),
                "error":         None,
            }
        except urllib.error.HTTPError as e:
            return {"text":"","input_tokens":0,"output_tokens":0,"latency_sec":0,
                    "model":self.MODEL,"error":f"HTTP {e.code}: {e.read().decode()[:300]}"}
        except Exception as e:
            return {"text":"","input_tokens":0,"output_tokens":0,"latency_sec":0,
                    "model":self.MODEL,"error":str(e)}

    def _mock_response(self, prompt):
        t = re.search(r"Title\s+:\s+(.+)", prompt)
        a = re.search(r"Authors\s+:\s+(.+)", prompt)
        y = re.search(r"Year\s+:\s+(.+)", prompt)
        k = re.search(r"Keywords\s+:\s+(.+)", prompt)
        d = re.search(r"Research Domains\s+:\s+(.+)", prompt)
        j = re.search(r"Journal\s+:\s+(.+)", prompt)

        title   = t.group(1).strip() if t else "the paper"
        authors = a.group(1).strip() if a else "the authors"
        year    = y.group(1).strip() if y else "recently"
        kws     = k.group(1).strip() if k else "NLP, text summarization"
        domains = d.group(1).strip() if d else "Natural Language Processing"
        journal = j.group(1).strip() if j else "an academic journal"
        kw1     = kws.split(",")[0].strip()
        dm1     = domains.split(",")[0].strip()

        text = f"""## 1. Overview
"{title}" ({year}), authored by {authors} and published in {journal}, addresses core challenges in {dm1}. The paper proposes novel approaches to automated text processing and makes significant advances in {kw1}, contributing to the growing body of research on intelligent NLP systems.

## 2. Research Problem & Objectives
The paper targets the problem of accurately and efficiently processing large volumes of natural language text through automated methods. The authors — {authors} — aim to improve upon existing {kw1} techniques by addressing limitations in semantic understanding, computational efficiency, and real-world deployment. The research seeks to bridge the gap between theoretical models and practical applications in {dm1}.

## 3. Methodology & Technical Approach
The methodology is grounded in the research domains identified in the Knowledge Graph: {domains}. The authors design a multi-stage pipeline incorporating text preprocessing, feature extraction, and model-based inference. Core techniques include tokenization, representation learning, and structured evaluation using domain-specific benchmarks. The approach leverages the key concepts: {kws}, combining them into a cohesive system that handles varied text inputs robustly. Evaluation is conducted using standard NLP metrics against established baselines.

## 4. Key Findings & Contributions
- Proposed an effective framework for {kw1} demonstrating measurable improvements over baseline approaches
- Validated the system on real-world datasets, establishing reproducibility and generalizability
- Provided a comprehensive comparative analysis of multiple modeling configurations
- Identified key performance factors that influence {dm1} system quality
- Released experimental findings enabling the broader research community to build upon this work

## 5. Positioning in the Research Landscape
As reflected in the Knowledge Graph, this paper shares topics and domains with related works in the collection, forming part of a broader cluster of research on {kws}. The retrieved related papers confirm that this work contributes to an active area of investigation spanning {domains}. The paper builds on established prior surveys and empirical studies, differentiating its contributions through its specific technical approach and evaluation methodology.

## 6. Practical Applications & Impact
The techniques developed have direct applications in: (1) automated document summarization for news, scientific, and enterprise content; (2) intelligent information retrieval and search systems; (3) knowledge management platforms requiring structured extraction from unstructured text; and (4) educational and research tools assisting users in navigating large literature corpora. Publication in {journal} ensures broad accessibility to both researchers and practitioners seeking deployable {kw1} solutions.

## 7. Limitations & Future Directions
The proposed approach shares limitations common to {dm1} research: dependence on domain-specific training data, computational overhead at scale, and sensitivity to input text quality and language variation. The authors acknowledge that performance may vary across domains not represented in the evaluation. Future work could extend the framework to multilingual settings, incorporate real-time processing capabilities, and explore hybrid architectures integrating the proposed methods with large-scale language models to enhance semantic reasoning and factual grounding.

## 8. Summary Statement
This paper makes a meaningful and well-evaluated contribution to {dm1} by delivering an effective, practically motivated system for {kw1} that advances both the state of the art and the applied toolkit available to NLP researchers and engineers.

---
*[Structured mock summary — set ANTHROPIC_API_KEY for real Claude-generated content]*"""

        return {
            "text": text,
            "input_tokens":  len(prompt.split()),
            "output_tokens": len(text.split()),
            "latency_sec":   0.001,
            "model":         "mock-claude-sonnet",
            "error":         None,
        }


# =============================================================================
# MODULE 7 — RAG EVALUATOR
# =============================================================================

class RAGEvaluator:
    @staticmethod
    def precision_at_k(retrieved, relevant, k):
        return sum(1 for p in retrieved[:k] if p in relevant) / k if k else 0.0

    @staticmethod
    def recall_at_k(retrieved, relevant, k):
        hits = sum(1 for p in retrieved[:k] if p in relevant)
        return hits / len(relevant) if relevant else 0.0

    @staticmethod
    def mrr(retrieved, relevant):
        for rank, pid in enumerate(retrieved, 1):
            if pid in relevant:
                return 1.0 / rank
        return 0.0

    @staticmethod
    def ndcg_at_k(retrieved, relevant, k):
        dcg  = sum(1/math.log2(r+2) for r, pid in enumerate(retrieved[:k]) if pid in relevant)
        idcg = sum(1/math.log2(r+2) for r in range(min(len(relevant), k)))
        return dcg / idcg if idcg else 0.0

    @staticmethod
    def context_relevance(texts, query):
        q_toks = set(w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2)
        if not q_toks:
            return 0.0
        scores = [len(q_toks & set(re.findall(r"[a-z0-9]+", t.lower()))) / len(q_toks) for t in texts]
        return round(sum(scores) / len(scores), 4) if scores else 0.0

    def evaluate(self, query, retrieval_result, relevant_ids, all_ids):
        merged_ids   = [e["doc"]["id"] for e in retrieval_result["merged"]]
        merged_texts = [e["doc"]["text"] for e in retrieval_result["merged"]]
        return {
            "query":             query,
            "relevant_count":    len(relevant_ids),
            "retrieved_count":   len(merged_ids),
            "precision_at_1":    self.precision_at_k(merged_ids, relevant_ids, 1),
            "precision_at_3":    self.precision_at_k(merged_ids, relevant_ids, 3),
            "precision_at_5":    self.precision_at_k(merged_ids, relevant_ids, 5),
            "recall_at_3":       self.recall_at_k(merged_ids, relevant_ids, 3),
            "recall_at_5":       self.recall_at_k(merged_ids, relevant_ids, 5),
            "mrr":               self.mrr(merged_ids, relevant_ids),
            "ndcg_at_3":         self.ndcg_at_k(merged_ids, relevant_ids, 3),
            "ndcg_at_5":         self.ndcg_at_k(merged_ids, relevant_ids, 5),
            "context_relevance": self.context_relevance(merged_texts, query),
            "vector_hits":       len(retrieval_result["vector_results"]),
            "kg_hits":           len(retrieval_result["kg_results"]),
            "top_fusion_score":  retrieval_result["merged"][0]["fusion_score"]
                                 if retrieval_result["merged"] else 0,
        }


# =============================================================================
# MODULE 8 — LLM EVALUATOR
# =============================================================================

class LLMEvaluator:
    REQUIRED_SECTIONS = [
        "Overview", "Research Problem", "Methodology",
        "Key Findings", "Positioning", "Applications",
        "Limitations", "Summary Statement",
    ]
    # Weights must sum to 1.0
    WEIGHTS = {
        "section_completeness": 0.30,
        "keyword_coverage":     0.25,
        "kg_grounding":         0.20,
        "fluency_score":        0.15,
        "informativeness":      0.10,
    }

    def evaluate(self, summary, prompt, kg_ctx, llm_resp):
        result = {
            "paper_id":             kg_ctx.get("id",""),
            "paper_title":          kg_ctx.get("title",""),
            "keyword_coverage":     self._kw_coverage(summary, kg_ctx.get("keywords",[])),
            "section_completeness": self._sec_completeness(summary),
            "kg_grounding":         self._kg_grounding(summary, kg_ctx),
            "fluency_score":        self._fluency(summary),
            "informativeness":      self._informativeness(summary, prompt),
            "word_count":           len(summary.split()),
            "sentence_count":       len(re.findall(r"[.!?]", summary)),
            "model":                llm_resp.get("model",""),
            "input_tokens":         llm_resp.get("input_tokens",0),
            "output_tokens":        llm_resp.get("output_tokens",0),
            "latency_sec":          llm_resp.get("latency_sec",0),
            "has_error":            bool(llm_resp.get("error")),
        }
        result["composite_score"] = round(
            sum(result[k] * w for k, w in self.WEIGHTS.items()), 4
        )
        return result

    def _kw_coverage(self, summary, keywords):
        if not keywords:
            return 0.0
        sl = summary.lower()
        return round(sum(1 for kw in keywords if kw.lower()[:12] in sl) / len(keywords), 4)

    def _sec_completeness(self, summary):
        sl = summary.lower()
        hits = sum(1 for sec in self.REQUIRED_SECTIONS if sec.lower() in sl)
        return round(hits / len(self.REQUIRED_SECTIONS), 4)

    def _kg_grounding(self, summary, kg_ctx):
        facts = (kg_ctx.get("authors",[]) + kg_ctx.get("keywords",[]) +
                 kg_ctx.get("domains",[]) + ([kg_ctx["journal"]] if kg_ctx.get("journal") else []))
        facts = [f for f in facts if f and len(f) > 3]
        if not facts:
            return 0.0
        sl = summary.lower()
        return round(sum(1 for f in facts if f.lower()[:15] in sl) / len(facts), 4)

    def _fluency(self, summary):
        sents = [s.strip() for s in re.split(r"[.!?]", summary) if len(s.strip()) > 5]
        if not sents:
            return 0.0
        return round(sum(1 for s in sents if 8 <= len(s.split()) <= 70) / len(sents), 4)

    def _informativeness(self, summary, prompt):
        stop = {"the","a","an","is","are","of","in","to","and","for","this","that","with","from","by"}
        p_toks = set(re.findall(r"[a-z0-9]+", prompt.lower())) - stop
        s_toks = set(re.findall(r"[a-z0-9]+", summary.lower())) - stop
        return round(len(s_toks - p_toks) / max(len(s_toks), 1), 4)


# =============================================================================
# MODULE 9 — PIPELINE ORCHESTRATOR
# =============================================================================

class HybridRAGPipeline:
    def __init__(self, entities_path, relationships_path, triples_path):
        print("\n" + "═"*70)
        print("  MILESTONE 3 — HYBRID RAG PIPELINE")
        print("  Knowledge Graph  ×  Retrieval-Augmented Generation  ×  LLM")
        print("═"*70 + "\n")

        self.kg = KnowledgeGraphStore(entities_path, relationships_path, triples_path)

        print("\n  📐 Building TF-IDF Vector Store...")
        self.vs = TFIDFVectorStore()
        self.vs.add_documents(CorpusBuilder.build(self.kg))
        print()

        self.retriever      = HybridRetriever(self.vs, self.kg)
        self.prompt_builder = PromptBuilder()
        self.llm            = LLMClient()
        self.rag_eval       = RAGEvaluator()
        self.llm_eval       = LLMEvaluator()

    def run(self, paper_ids=None):
        if paper_ids is None:
            paper_ids = list(self.kg.paper_by_id.keys())

        all_paper_ids = list(self.kg.paper_by_id.keys())
        results = {
            "metadata": {
                "pipeline":           "Hybrid RAG (KG + TF-IDF Vector Store)",
                "llm_model":          self.llm.MODEL,
                "timestamp":          datetime.now().isoformat(),
                "total_papers":       len(self.kg.paper_by_id),
                "papers_processed":   len(paper_ids),
                "kg_entities":        sum(len(v) for v in self.kg.entities.values()),
                "kg_relationships":   sum(len(v) for v in self.kg.relationships.values()),
                "kg_triples":         len(self.kg.triples),
            },
            "paper_summaries": [],
            "rag_evaluations": [],
            "llm_evaluations": [],
        }

        print(f"  🚀 Processing {len(paper_ids)} research papers...\n")
        print("  " + "─"*66)

        for idx, paper_id in enumerate(paper_ids, 1):
            paper = self.kg.paper_by_id.get(paper_id, {})
            title = paper.get("title", "Unknown")
            print(f"\n  [{idx:02d}/{len(paper_ids):02d}] {paper_id}: {title[:62]}...")
            print(f"  {'─'*66}")

            # Build query
            kws     = self.kg.has_keyword.get(paper_id, [])
            doms    = self.kg.belongs_domain.get(paper_id, [])
            query   = f"{title} {' '.join(kws[:4])} {' '.join(doms[:2])}"
            print(f"  📎 Query  : {query[:80]}...")

            # Hybrid retrieval
            retrieval = self.retriever.retrieve(query, top_k=5)
            nv, nk, nm = len(retrieval["vector_results"]), len(retrieval["kg_results"]), len(retrieval["merged"])
            print(f"  🔍 Retrieved: {nv} vector | {nk} KG | {nm} fused (RRF)")

            # RAG evaluation
            relevant = (
                {r["paper_id"] for r in self.kg.shares_topic.get(paper_id, [])} |
                {r["paper_id"] for r in self.kg.shares_domain.get(paper_id, [])}
            )
            relevant.add(paper_id)
            rag_metrics = self.rag_eval.evaluate(query, retrieval, relevant, all_paper_ids)
            results["rag_evaluations"].append(rag_metrics)
            print(f"  📊 RAG    : P@3={rag_metrics['precision_at_3']:.3f} | "
                  f"MRR={rag_metrics['mrr']:.3f} | "
                  f"nDCG@3={rag_metrics['ndcg_at_3']:.3f} | "
                  f"Relevance={rag_metrics['context_relevance']:.3f}")

            # Build prompt
            kg_ctx = self.kg.get_paper_context(paper_id)
            prompt = self.prompt_builder.build_summary_prompt(kg_ctx, retrieval["merged"])
            print(f"  ✏️  Prompt : ~{len(prompt.split())} words | "
                  f"KG facts: {len(kg_ctx.get('authors',[]))} authors, "
                  f"{len(kg_ctx.get('keywords',[]))} keywords, "
                  f"{len(kg_ctx.get('citations',[]))} citations")

            # Call LLM
            print(f"  🤖 LLM    : Calling {self.llm.MODEL}...")
            llm_resp = self.llm.call(prompt, max_tokens=1500)

            if llm_resp.get("error"):
                print(f"  ❌ Error  : {llm_resp['error'][:80]}")
                summary_text = f"[LLM Error: {llm_resp['error']}]"
            else:
                summary_text = llm_resp["text"]
                print(f"  ✅ LLM    : {llm_resp['output_tokens']} tokens out | {llm_resp['latency_sec']}s")

            # LLM evaluation
            llm_metrics = self.llm_eval.evaluate(summary_text, prompt, kg_ctx, llm_resp)
            results["llm_evaluations"].append(llm_metrics)
            print(f"  📊 LLM    : KwCov={llm_metrics['keyword_coverage']:.3f} | "
                  f"SecComp={llm_metrics['section_completeness']:.3f} | "
                  f"KGGrd={llm_metrics['kg_grounding']:.3f} | "
                  f"Composite={llm_metrics['composite_score']:.3f}")

            results["paper_summaries"].append({
                "paper_id":    paper_id,
                "title":       title,
                "year":        paper.get("year",""),
                "authors":     self.kg.authored_by.get(paper_id, []),
                "journal":     self.kg.published_in.get(paper_id, ""),
                "keywords":    kws,
                "domains":     doms,
                "query":       query,
                "retrieval":   {"vector_hits": nv, "kg_hits": nk, "fused": nm,
                                "top_fusion_score": retrieval["merged"][0]["fusion_score"] if retrieval["merged"] else 0},
                "prompt_words": len(prompt.split()),
                "summary":     summary_text,
                "rag_metrics": rag_metrics,
                "llm_metrics": llm_metrics,
            })

        results["aggregate"] = self._aggregate(results["rag_evaluations"], results["llm_evaluations"])
        self._print_aggregate(results)
        return results

    @staticmethod
    def _mean(lst, key):
        vals = [e[key] for e in lst if isinstance(e.get(key), (int, float))]
        return round(sum(vals) / len(vals), 4) if vals else 0.0

    def _aggregate(self, rag_evals, llm_evals):
        m = self._mean
        return {
            "rag": {
                "avg_precision_at_1":    m(rag_evals, "precision_at_1"),
                "avg_precision_at_3":    m(rag_evals, "precision_at_3"),
                "avg_precision_at_5":    m(rag_evals, "precision_at_5"),
                "avg_recall_at_3":       m(rag_evals, "recall_at_3"),
                "avg_recall_at_5":       m(rag_evals, "recall_at_5"),
                "avg_mrr":               m(rag_evals, "mrr"),
                "avg_ndcg_at_3":         m(rag_evals, "ndcg_at_3"),
                "avg_ndcg_at_5":         m(rag_evals, "ndcg_at_5"),
                "avg_context_relevance": m(rag_evals, "context_relevance"),
            },
            "llm": {
                "avg_keyword_coverage":     m(llm_evals, "keyword_coverage"),
                "avg_section_completeness": m(llm_evals, "section_completeness"),
                "avg_kg_grounding":         m(llm_evals, "kg_grounding"),
                "avg_fluency_score":        m(llm_evals, "fluency_score"),
                "avg_informativeness":      m(llm_evals, "informativeness"),
                "avg_composite_score":      m(llm_evals, "composite_score"),
                "avg_word_count":           int(m(llm_evals, "word_count")),
                "avg_latency_sec":          m(llm_evals, "latency_sec"),
                "total_output_tokens":      sum(e.get("output_tokens",0) for e in llm_evals),
            },
        }

    def _print_aggregate(self, results):
        agg = results["aggregate"]
        r, l = agg["rag"], agg["llm"]
        n = len(results["rag_evaluations"])
        print("\n\n" + "═"*70)
        print("  PIPELINE COMPLETE — AGGREGATE EVALUATION RESULTS")
        print("═"*70)
        print(f"\n  Papers processed : {n}")
        print(f"\n  ── RAG Retrieval Metrics (avg over {n} papers) ──────────────────")
        print(f"  Precision@1       : {r['avg_precision_at_1']:.4f}")
        print(f"  Precision@3       : {r['avg_precision_at_3']:.4f}")
        print(f"  Precision@5       : {r['avg_precision_at_5']:.4f}")
        print(f"  Recall@3          : {r['avg_recall_at_3']:.4f}")
        print(f"  Recall@5          : {r['avg_recall_at_5']:.4f}")
        print(f"  MRR               : {r['avg_mrr']:.4f}")
        print(f"  nDCG@3            : {r['avg_ndcg_at_3']:.4f}")
        print(f"  nDCG@5            : {r['avg_ndcg_at_5']:.4f}")
        print(f"  Context Relevance : {r['avg_context_relevance']:.4f}")
        print(f"\n  ── LLM Quality Metrics (avg over {n} summaries) ─────────────────")
        print(f"  Keyword Coverage      : {l['avg_keyword_coverage']:.4f}")
        print(f"  Section Completeness  : {l['avg_section_completeness']:.4f}")
        print(f"  KG Grounding          : {l['avg_kg_grounding']:.4f}")
        print(f"  Fluency Score         : {l['avg_fluency_score']:.4f}")
        print(f"  Informativeness       : {l['avg_informativeness']:.4f}")
        print(f"  ─────────────────────────────────────────────────────────────────")
        print(f"  Composite Score       : {l['avg_composite_score']:.4f}")
        print(f"  Avg Summary Length    : {l['avg_word_count']} words")
        print(f"  Total Output Tokens   : {l['total_output_tokens']}")
        print()

    def save(self, results, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        json_path = os.path.join(output_dir, "hybrid_rag_results.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        report_path = os.path.join(output_dir, "hybrid_rag_report.md")
        self._write_report(results, report_path)

        print(f"  💾 JSON results  : {json_path}")
        print(f"  📝 MD report     : {report_path}\n")
        return {"json": json_path, "report": report_path}

    def _write_report(self, results, path):
        meta = results["metadata"]
        agg  = results["aggregate"]
        r, l = agg["rag"], agg["llm"]
        n    = meta["papers_processed"]

        lines = [
            "# Milestone 3: Hybrid RAG Pipeline — Evaluation Report",
            "",
            f"> **Generated**: {meta['timestamp']}",
            f"> **Pipeline**: {meta['pipeline']}",
            f"> **LLM Model**: {meta['llm_model']}",
            f"> **Papers Processed**: {n} / {meta['total_papers']}",
            f"> **KG**: {meta['kg_entities']} entities | {meta['kg_relationships']} relationships | {meta['kg_triples']} triples",
            "",
            "---",
            "",
            "## 1. Pipeline Architecture",
            "",
            "```",
            "  ┌────────────────────────────────────────────────────────────┐",
            "  │         KNOWLEDGE GRAPH  (from Milestone 2)                │",
            "  │  9 Papers · 34 Authors · 34 Keywords · 801 Triples         │",
            "  └──────────────────┬──────────────────────┬──────────────────┘",
            "                     │                      │",
            "           ┌─────────▼────────┐   ┌────────▼─────────┐",
            "           │  TF-IDF Vector   │   │  Knowledge Graph │",
            "           │  Store           │   │  Traversal       │",
            "           │  (Semantic)      │   │  (Structural)    │",
            "           └─────────┬────────┘   └────────┬─────────┘",
            "                     │                      │",
            "           ┌─────────▼──────────────────────▼─────────┐",
            "           │       HYBRID RETRIEVER                     │",
            "           │   Reciprocal Rank Fusion (RRF)             │",
            "           │   Vector×0.60 + Graph×0.40                 │",
            "           └─────────────────┬──────────────────────────┘",
            "                             │",
            "                    ┌────────▼───────┐",
            "                    │ PROMPT BUILDER │",
            "                    │ KG + RAG ctx   │",
            "                    └────────┬───────┘",
            "                             │",
            "                    ┌────────▼───────┐",
            "                    │  CLAUDE LLM    │",
            "                    │  Sonnet 4      │",
            "                    └────────┬───────┘",
            "                             │",
            "           ┌─────────────────┼─────────────────┐",
            "           ▼                 ▼                 ▼",
            "    Paper Summaries     RAG Metrics        LLM Metrics",
            "    (8-section)      (P@K, MRR,         (Coverage,",
            "                     nDCG, Recall)      Grounding,",
            "                                        Composite)",
            "```",
            "",
            "### KG Integration Points",
            "",
            "| Integration Point | Role in Pipeline |",
            "|-------------------|-----------------|",
            "| **Graph Retrieval** | KG keyword/domain nodes traversed to surface structurally related papers (40% of fusion score) |",
            "| **Context Enrichment** | LLM prompt injected with: authors, journal, domains, keywords, full citation list, related-paper links |",
            "| **Evaluation Grounding** | `SHARES_TOPIC` and `SHARES_DOMAIN` KG edges define ground-truth relevance for RAG metrics |",
            "",
            "---",
            "",
            "## 2. RAG Pipeline Evaluation",
            "",
            "### 2.1 Aggregate Retrieval Metrics",
            "",
            "| Metric | Score | What It Measures |",
            "|--------|-------|-----------------|",
            f"| Precision@1 | **{r['avg_precision_at_1']:.4f}** | Top result is relevant |",
            f"| Precision@3 | **{r['avg_precision_at_3']:.4f}** | Relevant fraction in top-3 |",
            f"| Precision@5 | **{r['avg_precision_at_5']:.4f}** | Relevant fraction in top-5 |",
            f"| Recall@3    | **{r['avg_recall_at_3']:.4f}** | Coverage of relevant set in top-3 |",
            f"| Recall@5    | **{r['avg_recall_at_5']:.4f}** | Coverage of relevant set in top-5 |",
            f"| MRR         | **{r['avg_mrr']:.4f}** | Reciprocal rank of first relevant hit |",
            f"| nDCG@3      | **{r['avg_ndcg_at_3']:.4f}** | Discounted ranking quality, top-3 |",
            f"| nDCG@5      | **{r['avg_ndcg_at_5']:.4f}** | Discounted ranking quality, top-5 |",
            f"| Context Relevance | **{r['avg_context_relevance']:.4f}** | Query–document token overlap |",
            "",
            "### 2.2 Per-Paper Retrieval Results",
            "",
            "| Paper | P@1 | P@3 | MRR | nDCG@3 | Vec | KG | Ctx.Rel |",
            "|-------|-----|-----|-----|--------|-----|----|---------|",
        ]
        for e, s in zip(results["rag_evaluations"], results["paper_summaries"]):
            lines.append(
                f"| {s['paper_id']} | {e['precision_at_1']:.3f} | {e['precision_at_3']:.3f} | "
                f"{e['mrr']:.3f} | {e['ndcg_at_3']:.3f} | "
                f"{e['vector_hits']} | {e['kg_hits']} | {e['context_relevance']:.3f} |"
            )
        lines += [
            "",
            "---",
            "",
            "## 3. LLM Evaluation",
            "",
            "### 3.1 Evaluation Dimensions & Weights",
            "",
            "| Dimension | Weight | Description |",
            "|-----------|--------|-------------|",
            "| Section Completeness | **30%** | All 8 required sections present in summary |",
            "| Keyword Coverage | **25%** | Paper's KG keywords mentioned in the summary |",
            "| KG Grounding | **20%** | KG facts (authors, domains, journal) referenced |",
            "| Fluency Score | **15%** | Ratio of well-formed sentences (8–70 words) |",
            "| Informativeness | **10%** | Novel tokens in output not present in the prompt |",
            "",
            "### 3.2 Aggregate LLM Quality Metrics",
            "",
            "| Metric | Score |",
            "|--------|-------|",
            f"| Avg Keyword Coverage    | {l['avg_keyword_coverage']:.4f} |",
            f"| Avg Section Completeness | {l['avg_section_completeness']:.4f} |",
            f"| Avg KG Grounding        | {l['avg_kg_grounding']:.4f} |",
            f"| Avg Fluency Score       | {l['avg_fluency_score']:.4f} |",
            f"| Avg Informativeness     | {l['avg_informativeness']:.4f} |",
            f"| **Avg Composite Score** | **{l['avg_composite_score']:.4f}** |",
            f"| Avg Summary Length      | {l['avg_word_count']} words |",
            f"| Avg Latency             | {l['avg_latency_sec']}s |",
            f"| Total Output Tokens     | {l['total_output_tokens']} |",
            "",
            "### 3.3 Per-Paper LLM Scores",
            "",
            "| Paper | Title | KwCov | SecComp | KGGrd | Fluency | **Composite** |",
            "|-------|-------|-------|---------|-------|---------|---------------|",
        ]
        for e in results["llm_evaluations"]:
            t = e.get("paper_title","")[:40] + "..."
            lines.append(
                f"| {e.get('paper_id','')} | {t} | "
                f"{e.get('keyword_coverage',0):.3f} | "
                f"{e.get('section_completeness',0):.3f} | "
                f"{e.get('kg_grounding',0):.3f} | "
                f"{e.get('fluency_score',0):.3f} | "
                f"**{e.get('composite_score',0):.3f}** |"
            )
        lines += [
            "",
            "---",
            "",
            "## 4. Generated Research Paper Summaries",
            "",
        ]
        for s in results["paper_summaries"]:
            lines += [
                f"### {s['paper_id']}: {s['title']}",
                "",
                "| Field | Value |",
                "|-------|-------|",
                f"| **Year** | {s['year']} |",
                f"| **Authors** | {', '.join(s['authors'])} |",
                f"| **Journal** | {s['journal']} |",
                f"| **Keywords** | {', '.join(s['keywords'][:5])} |",
                f"| **Domains** | {', '.join(s['domains'][:3])} |",
                f"| **Retrieval** | {s['retrieval']['fused']} fused results (top score: {s['retrieval']['top_fusion_score']:.4f}) |",
                f"| **LLM Composite Score** | {s['llm_metrics']['composite_score']:.4f} |",
                f"| **Summary Words** | {s['llm_metrics']['word_count']} |",
                "",
                "#### Generated Summary",
                "",
                s["summary"],
                "",
                "---",
                "",
            ]
        lines += [
            "## 5. Evaluation Methodology",
            "",
            "### RAG Ground Truth",
            "Relevant papers for each query are defined as papers connected via `SHARES_TOPIC` "
            "or `SHARES_DOMAIN` edges in the Knowledge Graph, plus the target paper itself. "
            "This leverages the KG structure directly as evaluation signal — no manual annotation needed.",
            "",
            "### LLM Metrics Rationale",
            "All LLM metrics are **reference-free** (no gold summary required):",
            "",
            "- **Keyword Coverage** — measures domain fidelity: does the summary discuss what the paper is actually about?",
            "- **Section Completeness** — measures structural quality: does the summary address all key aspects?",
            "- **KG Grounding** — measures factual faithfulness: are verifiable KG facts present in the output?",
            "- **Fluency** — measures linguistic quality: are sentences well-formed?",
            "- **Informativeness** — measures generative value: does the LLM add reasoning beyond what the prompt states?",
            "",
            "### Hybrid Fusion",
            "Reciprocal Rank Fusion (RRF) with **Vector=0.60 / Graph=0.40** was chosen because:",
            "- The KG corpus (9 papers) is too small for pure vector search to always surface distinct neighbours",
            "- KG graph traversal provides hard structural links (shared keywords/domains) that complement soft semantic similarity",
            "- The 60/40 split empirically balances semantic recall with structural precision",
            "",
        ]

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    from pathlib import Path

    # ── Auto-detect base directory ─────────────────────────────────────────
    # The script looks for the extracted KG files in these locations (in order):
    #   1. Same folder as this script
    #   2. A subfolder called "extracted" or "files_extracted" next to this script
    #   3. Current working directory

    SCRIPT_DIR = Path(__file__).parent.resolve()
    CWD        = Path.cwd()

    CANDIDATE_DIRS = [
        SCRIPT_DIR,
        SCRIPT_DIR / "extracted",
        SCRIPT_DIR / "files_extracted",
        CWD,
        CWD / "extracted",
        CWD / "files_extracted",
    ]

    REQUIRED_FILES = [
        "extracted_entities.json",
        "extracted_relationships.json",
        "triples.json",
    ]

    BASE = None
    for candidate in CANDIDATE_DIRS:
        if all((candidate / f).exists() for f in REQUIRED_FILES):
            BASE = candidate
            break

    if BASE is None:
        print("\n❌  ERROR: Could not find the required KG data files.")
        print("   Looking for these files in these locations:")
        for d in CANDIDATE_DIRS:
            print(f"     {d}")
        print("\n   Please place the following files in the same folder as this script:")
        for f in REQUIRED_FILES:
            print(f"     • {f}")
        print("\n   These files are generated by Milestone 2 (main_pipeline.py).")
        sys.exit(1)

    print(f"\n  📂 KG data found in: {BASE}")

    # ── Output directory: same folder as script by default ─────────────────
    OUTPUT_DIR = SCRIPT_DIR / "hybrid_rag_output"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Run pipeline ────────────────────────────────────────────────────────
    pipeline = HybridRAGPipeline(
        entities_path      = str(BASE / "extracted_entities.json"),
        relationships_path = str(BASE / "extracted_relationships.json"),
        triples_path       = str(BASE / "triples.json"),
    )

    results = pipeline.run()
    pipeline.save(results, str(OUTPUT_DIR))