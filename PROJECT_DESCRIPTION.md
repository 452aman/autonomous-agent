# Autonomous Document Generation Agent

---

## Problem Statement

Enterprises frequently need professional business documents — project plans, proposals, meeting minutes, SOPs — but drafting them is time-consuming and requires structured thinking. The challenge is building a system that can take a plain English request (including vague or ambiguous ones), reason about what steps are needed, execute those steps autonomously, and produce a polished Word document — without any hardcoded templates or human intervention.

---

## Approach

Rather than building a rigid template-based system, I designed an autonomous agent that uses an LLM as its reasoning engine across four independent stages:

```
Request → Classify → Plan → Execute → Reflect → Word Document
```

1. **Classify** — the agent first identifies what type of document to produce
2. **Plan** — generates its own task list from the request (no hardcoded steps)
3. **Execute** — runs each task through the LLM to generate section content
4. **Reflect** — scores each section 1-10, rewrites anything below 7 (max 2 iterations)

This architecture means the agent handles any document type and any phrasing — including ambiguous requests with missing information — by making its own reasonable assumptions.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Framework | FastAPI | REST API with async support and auto-generated docs |
| LLM Provider | Groq (llama-3.3-70b-versatile) | Free-tier LLM for planning, execution, classification, reflection |
| Document Generation | python-docx | Programmatic Word (.docx) file creation |
| Data Validation | Pydantic v2 | Request/response schema validation with custom guardrails |
| Environment Config | python-dotenv | Secure API key management |
| Server | Uvicorn | ASGI server for FastAPI |
| Language | Python 3.9+ | Core language |

---

## Features Built

### Core
- `POST /agent` — accepts natural language request, returns `.docx` file
- Autonomous task planning — LLM generates its own execution plan
- Multi-step execution — one LLM call per section for focused, quality output
- Reflection & self-check — quality scoring loop with bounded retries

### Engineering Improvements
- **Input validation & guardrails** — rejects empty, too-short, or nonsensical requests with clear error messages before hitting the LLM
- **Document type auto-classification** — LLM classifies request into one of 7 document types before planning begins
- **GET /health** — health check endpoint, industry standard API design
- **GET /history** — in-memory request history tracking all agent runs with metadata
- **Structured logging** — step-by-step logs for every agent run (classify → plan → execute → reflect → build)
- **Async endpoint** — non-blocking FastAPI async handler
- **System prompt architecture** — separated system and user roles in LLM calls for better output quality

---

## API Endpoints

```
POST /agent       → run the autonomous agent, returns .docx file
GET  /health      → server health check
GET  /history     → list of all past requests with metadata
```

### Sample Request
```json
POST /agent
{
  "request": "Write a project plan for a food delivery mobile app"
}
```

### Sample Response Headers
```
X-Document-Type: Project Plan
X-Tasks-Completed: 7
X-Reflection-Iterations: 1
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

---

## Document Types Supported

The agent auto-detects and handles:
- Project Plan
- Business Proposal
- Meeting Minutes
- Business Report
- Technical Design Document
- Standard Operating Procedure (SOP)
- Product Specification

---

## Agent Architecture

```
User Request (natural language)
        │
        ▼
  [Guardrails]        ← reject invalid input before any LLM call
        │
        ▼
  [Classifier]        ← identify document type (Project Plan, SOP, etc.)
        │
        ▼
  [Planner]           ← LLM generates task list autonomously
        │
        ▼
  [Executor]          ← LLM runs each task, builds content dict
        │
        ▼
  [Reflection Loop]   ← score each section, rewrite weak ones (max 2 iters)
        │
        ▼
  [Word Builder]      ← assemble .docx with headings and paragraphs
        │
        ▼
  FileResponse + History Entry + Structured Logs
```

---

## Engineering Tradeoff

**Autonomous Planning vs Deterministic Workflow**

Chose autonomous planning — the LLM decides the steps itself rather than following hardcoded sequences. This makes the agent flexible enough to handle any document type and any phrasing without pre-defined rules. The tradeoff is reduced predictability (task count and names vary per run), partially addressed by the reflection layer which enforces quality regardless of structure.

---

## Resume Bullet Points

```
• Built an autonomous AI agent using FastAPI and Groq LLM (llama-3.3-70b) that
  accepts natural language requests, self-generates execution plans, and produces
  professional Word documents end-to-end

• Implemented a reflection loop with quality scoring — agent rates its own output
  1-10 and rewrites sections below threshold, with bounded retry logic to prevent
  infinite loops

• Designed REST API with input validation guardrails, document type classification,
  health monitoring (/health), and in-memory request history (/history)

• Integrated structured logging across all agent stages (classify → plan → execute
  → reflect → build) for full observability of autonomous decision-making

• Handled ambiguous and incomplete user requests by designing the agent to make
  reasonable assumptions and surface them explicitly in the generated document
```

---

## Project Structure

```
autonomous-agent/
├── main.py                  ← FastAPI app, async endpoints, logging, history
├── .env                     ← GROQ_API_KEY (not committed)
├── requirements.txt
│
├── models/
│   └── schemas.py           ← Pydantic models with input validation
│
├── llm/
│   └── groq_client.py       ← ask_llm() with system/user prompt separation
│
├── agent/
│   ├── classifier.py        ← document type detection
│   ├── planner.py           ← autonomous task list generation
│   ├── executor.py          ← per-task LLM execution
│   └── reflection.py        ← quality scoring + bounded rewrite loop
│
└── document/
    └── word_builder.py      ← python-docx assembly
```
