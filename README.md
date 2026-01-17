# AI Research Agent

An autonomous AI-powered research assistant that plans, searches, analyzes, and synthesizes comprehensive reports on any topic.

## What It Does

- **Autonomous Research Planning**: AI breaks down complex questions into searchable sub-queries
- **Parallel Source Discovery**: Searches multiple sources concurrently
- **Intelligent Analysis**: Extracts and rates key findings by confidence
- **Report Synthesis**: Generates structured reports with insights and recommendations
- **Demo Mode**: Works without API keys using simulated data

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Research Agent                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐                                              │
│   │ User Query   │                                              │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │  Step 1: Research Planning                                │  │
│   │  • Analyze query intent                                   │  │
│   │  • Break into sub-questions                               │  │
│   │  • Generate optimized search queries                      │  │
│   └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │  Step 2: Parallel Search Execution                        │  │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  │
│   │  │ Query 1 │  │ Query 2 │  │ Query 3 │  │ Query N │      │  │
│   │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘      │  │
│   │       └────────────┴────────────┴────────────┘            │  │
│   │                    Serper API (Google Search)             │  │
│   └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │  Step 3: Finding Extraction                               │  │
│   │  • Analyze each source                                    │  │
│   │  • Extract key findings                                   │  │
│   │  • Rate confidence (high/medium/low)                      │  │
│   └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │  Step 4: Report Synthesis                                 │  │
│   │  • Executive summary                                      │  │
│   │  • Key insights with explanations                         │  │
│   │  • Conclusions                                            │  │
│   │  • Limitations                                            │  │
│   │  • Actionable recommendations                             │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Features

### Multi-Step AI Reasoning
The agent doesn't just search—it thinks. It breaks down your question, plans the research strategy, and adapts based on what it finds.

### Confidence-Rated Findings
Each finding comes with a confidence rating (high/medium/low) based on source quality and corroboration.

### Depth Control
- **Quick**: 3 sources, fast results
- **Standard**: 5 sources, balanced
- **Deep**: 8 sources, comprehensive

### Structured Reports
Get actionable output: executive summary, key insights, conclusions, limitations, and recommendations.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run (demo mode - no API keys needed)
python app.py

# Open http://localhost:5015
```

## Full Setup

1. Copy `.env.example` to `.env`
2. Add your API keys:
   - [OpenAI](https://platform.openai.com) - AI planning and synthesis
   - [Serper](https://serper.dev) - Google Search API (2,500 free searches/month)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main research interface |
| `/api/research` | POST | Start a research task |
| `/api/history` | GET | Get recent research history |
| `/api/status` | GET | Check API status |

### Start Research
```bash
curl -X POST http://localhost:5015/api/research \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest trends in AI?", "depth": "standard"}'
```

## Example Research Queries

- "What are the latest trends in AI and machine learning for business?"
- "How is remote work changing company culture and productivity?"
- "What are the most promising renewable energy technologies?"
- "How are companies using automation to improve efficiency?"

## Tech Stack

- **Backend**: Python, Flask, aiohttp (async HTTP)
- **AI**: OpenAI GPT-3.5 for planning and synthesis
- **Search**: Serper API (Google Search)
- **Frontend**: Vanilla JS with real-time updates

## Why This Matters

This project demonstrates:
1. **Autonomous AI agents** - AI that plans and executes multi-step tasks
2. **Async orchestration** - Parallel API calls for performance
3. **Structured reasoning** - Breaking complex problems into steps
4. **Confidence calibration** - Honest uncertainty in AI outputs
5. **Graceful degradation** - Full demo mode without APIs

---

*Research smarter, not harder.*
