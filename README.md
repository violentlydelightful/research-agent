# Research Agent: Autonomous AI Research Assistant

## The Problem

Research is tedious. You have a question, so you Google it, open 10 tabs, skim articles, try to synthesize what you learned, and realize you've spent an hour getting a surface-level understanding. For complex topics, this cycle repeats endlessly.

I wanted to explore: **what if an AI could do the grunt work of research autonomously?** Not just answer questions from its training data, but actually plan a research strategy, search the web, analyze multiple sources, and synthesize findings into something actionable.

## What I Built

An autonomous research agent that:

1. **Plans** - Breaks down complex questions into searchable sub-queries
2. **Searches** - Executes queries in parallel across multiple sources
3. **Analyzes** - Extracts key findings and rates confidence levels
4. **Synthesizes** - Generates structured reports with insights and recommendations

The key insight: research isn't just retrieval—it's a multi-step reasoning process. The agent mirrors how a human researcher would approach a topic, but faster.

## Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  PLANNING PHASE                                          │
│  GPT breaks query into 3-8 sub-questions based on depth │
│  Generates optimized search queries for each            │
│  Temperature: 0.7 (more creative exploration)           │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  SEARCH PHASE (Parallel)                                 │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                       │
│  │ Q1  │ │ Q2  │ │ Q3  │ │ Qn  │  ← Concurrent via     │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘    asyncio + aiohttp  │
│     └───────┴───────┴───────┘                           │
│              Serper API                                  │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  ANALYSIS PHASE                                          │
│  Extract 2-3 findings per source                        │
│  Rate confidence: high / medium / low                   │
│  Temperature: 0.3 (more deterministic)                  │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  SYNTHESIS PHASE                                         │
│  • Executive summary                                     │
│  • Key insights with explanations                       │
│  • Conclusions                                          │
│  • Limitations (honest about gaps)                      │
│  • Actionable recommendations                           │
└─────────────────────────────────────────────────────────┘
```

## Key Decisions & Tradeoffs

### Why separate temperature settings per phase?

Planning needs creativity (0.7) to generate diverse sub-questions. Analysis needs precision (0.3) to extract facts accurately. Synthesis needs balance (0.5). This isn't documented in most tutorials—I discovered it through experimentation when early versions produced either boring plans or hallucinated findings.

### Why parallel search execution?

The naive approach is sequential: search, wait, search, wait. With async/await and `asyncio.gather()`, all searches execute concurrently. For a "deep" research (8 queries), this cuts latency from ~16 seconds to ~3 seconds. The code is more complex, but the UX improvement is dramatic.

### Why confidence ratings?

Early versions just listed findings as facts. But web sources vary wildly in reliability. Adding confidence ratings (high/medium/low) based on source type and corroboration makes the output more honest. This is something I'd want if I were the user—know what to trust.

### Why a demo mode?

API keys are a barrier to trying things. The app detects missing keys and falls back to realistic simulated data. Someone can clone the repo and see it working in 30 seconds. This matters for portfolio projects.

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Backend | Flask + aiohttp | Flask for simplicity, aiohttp for async HTTP |
| AI | OpenAI GPT-3.5-turbo | Good balance of capability and cost |
| Search | Serper API | Google results via API, 2500 free/month |
| Frontend | Vanilla JS | No build step, just works |

## What I'd Do Differently

**1. Add source caching.** Currently, if you research similar topics, it re-searches everything. A simple cache keyed on query hash would reduce API costs and latency.

**2. Implement streaming.** The synthesis phase can take 5-10 seconds. Streaming the report as it generates would improve perceived performance significantly.

**3. Add citation tracking.** Findings reference sources, but there's no way to click through to the original. Proper citation linking would make the output more verifiable.

**4. Consider different models per phase.** GPT-4 for planning (better reasoning), GPT-3.5-turbo for extraction (faster, cheaper). The current one-model approach is simpler but not optimal.

## Running It

```bash
# Clone and install
git clone https://github.com/[username]/research-agent
cd research-agent
pip install -r requirements.txt

# Demo mode (no API keys)
python app.py
# → http://localhost:5015

# Full mode
cp .env.example .env
# Add OPENAI_API_KEY and SERPER_API_KEY
python app.py
```

## What This Demonstrates

- **Autonomous AI agents**: Multi-step reasoning, not just Q&A
- **Async orchestration**: Parallel execution for performance
- **Prompt engineering**: Different temperatures for different tasks
- **Graceful degradation**: Works without external dependencies
- **Structured output**: JSON schemas for reliable parsing

---

*This project explores what's possible when you let AI plan and execute, not just respond. The architecture patterns here—planning → parallel execution → synthesis—apply to many autonomous agent use cases.*
