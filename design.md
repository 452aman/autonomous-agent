# Autonomous Agent — Requirements & Design

---

## Assignment Summary

Build a Python API that acts as an autonomous AI agent. It accepts a plain English request, plans its own steps, executes them using an LLM, and returns a polished Word (.docx) document.

- **Time limit:** 60 minutes build
- **Video:** 8–10 minutes demo + explanation

---

## Core Requirements

| # | Requirement | Detail |
|---|-------------|--------|
| 1 | Python API | FastAPI with `POST /agent` endpoint |
| 2 | Input | JSON `{"request": "..."}` — plain English |
| 3 | Autonomous Planning | Agent generates its own task list from the request |
| 4 | Execution | Agent runs each task by calling the LLM |
| 5 | Output | JSON response + downloadable `.docx` Word file |
| 6 | LLM | Free tier — **Groq** (recommended) |
| 7 | Engineering Improvement | **Reflection / Self-Check** (chosen) |
| 8 | Mock data | Allowed where needed |

---

## LLM Choice

**Groq** — free API key, fast, no local setup needed.

```
GROQ_API_KEY=your_key_here   ← stored in .env
```

---

## Engineering Improvement — Reflection / Self-Check

After generating all document content, the agent sends its own output back to the LLM and asks it to score each section out of 10. Any section scoring below 7 is rewritten automatically.

```
Normal Agent:      Request → Plan → Execute → Output
                                                 ↑ done

With Reflection:   Request → Plan → Execute → Reflect → Fix weak parts → Output
                                                 ↑
                                      "score each section 1-10,
                                       redo anything below 7"
```

**Why chosen:**
- Visually impressive in demo
- Shows true autonomous behaviour ("agent marks its own homework")
- Genuinely improves output quality
- Easy to explain in video
- ~20 lines of extra code

---

## Document Types Supported

The agent auto-detects which type fits the request:

- Project Plan
- Business Proposal
- Meeting Minutes
- Business Report
- Technical Design Document
- SOP (Standard Operating Procedure)
- Product Specification

---

## Two Test Inputs

### Test 1 — Simple Request

```
{"request": "Write meeting minutes for a weekly team standup"}
```

- Clear document type → Meeting Minutes
- Known structure → Attendees, Discussion, Action Items
- No assumptions needed
- Tests: does the agent work at all?

**Expected output sections:**
- Attendees
- Agenda
- Discussion Points
- Action Items
- Next Steps

---

### Test 2 — Complex / Ambiguous Request

```
{
  "request": "We need something for our new product launch but we're not
  sure what format, could be a plan or a proposal, the deadline is sometime
  next month, and we might need budget info but we don't have exact numbers yet"
}
```

- Document type unclear → agent must decide
- Deadline vague → agent assumes 4 weeks
- Budget missing → agent uses placeholder
- Tests: can the agent handle real-world messy input?

**Agent behaviour:**
- Chooses "Product Launch Proposal" as best fit
- States all assumptions at top of document
- Uses placeholder budget with note to confirm

---

## Project Structure

```
autonomous-agent/
├── main.py                  ← FastAPI app, POST /agent endpoint
├── .env                     ← GROQ_API_KEY
├── requirements.txt         ← all dependencies
│
├── models/
│   └── schemas.py           ← Pydantic request/response shapes
│
├── llm/
│   ├── __init__.py
│   └── groq_client.py       ← ask_llm(prompt) wrapper around Groq API
│
├── agent/
│   ├── __init__.py
│   ├── planner.py           ← sends request to LLM, gets back task list
│   ├── executor.py          ← runs each task through LLM, collects content
│   └── reflection.py        ← scores each section, re-runs weak ones
│
└── document/
    ├── __init__.py
    └── word_builder.py      ← assembles all content into .docx file
```

---

## Data Flow

```
USER
 │
 │  POST /agent  {"request": "..."}
 ▼
main.py           → receives and validates request
 │
 ▼
planner.py        → LLM generates task list from request
 │                   output: ["Task 1", "Task 2", ...]
 ▼
executor.py       → LLM runs each task, generates section content
 │                   output: {"overview": "...", "scope": "...", ...}
 ▼
reflection.py     → LLM scores each section, re-runs any below 7/10
 │                   output: improved content dict
 ▼
word_builder.py   → assembles content into formatted .docx file
 │                   output: saved file path
 ▼
main.py           → returns JSON response + file download to user
```

---

## File-by-File Responsibility

| File | Does What |
|------|-----------|
| `main.py` | Defines the API, wires all modules together |
| `models/schemas.py` | Pydantic models — validates input/output shapes |
| `llm/groq_client.py` | Single function `ask_llm(prompt)` → returns LLM text |
| `agent/planner.py` | Takes request → returns ordered task list |
| `agent/executor.py` | Takes task list → returns dict of section content |
| `agent/reflection.py` | Takes content dict → scores + rewrites weak sections |
| `document/word_builder.py` | Takes content dict → builds and saves `.docx` |

---

## Libraries

| Library | Purpose |
|---------|---------|
| `fastapi` | API framework |
| `uvicorn` | Runs the FastAPI server |
| `groq` | Groq LLM API client |
| `python-docx` | Creates `.docx` Word files |
| `pydantic` | Validates JSON input/output |
| `python-dotenv` | Loads `.env` file (API keys) |

---

## Video Breakdown (8–10 min)

| Section | Time | Content |
|---------|------|---------|
| Live Demo | 3–4 min | Show both test inputs end-to-end, agent task list + Word doc |
| What You Built | 2–3 min | Architecture, LLM integration, reflection logic, API design |
| Debugging Insight | 1–2 min | One real issue faced + how you fixed it |
| Tradeoff Discussion | 1–2 min | e.g. Autonomous Planning vs Deterministic Workflows |

---

## Current Build Status

- [x] Requirements installed
- [x] Project folder structure created
- [x] `.env` created with Groq API key
- [x] `models/schemas.py` — AgentRequest, AgentResponse
- [ ] `llm/groq_client.py`
- [ ] `agent/planner.py`
- [ ] `agent/executor.py`
- [ ] `agent/reflection.py`
- [ ] `document/word_builder.py`
- [ ] `main.py`
