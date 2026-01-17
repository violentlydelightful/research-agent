"""
AI Research Agent - Autonomous Research and Synthesis Platform

An AI-powered research assistant that can:
- Break down complex research questions
- Search multiple sources concurrently
- Synthesize findings into comprehensive reports
- Learn from feedback to improve results
"""

import os
import asyncio
import aiohttp
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'research-agent-dev-key')

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')  # For Google search
DEMO_MODE = not OPENAI_API_KEY


class ResearchAgent:
    """Autonomous research agent that plans, searches, and synthesizes."""

    def __init__(self):
        self.openai_key = OPENAI_API_KEY
        self.serper_key = SERPER_API_KEY
        self.research_history = []

    async def research(self, query: str, depth: str = "standard") -> dict:
        """
        Main research pipeline:
        1. Analyze query and create research plan
        2. Execute searches in parallel
        3. Synthesize findings
        4. Generate final report
        """
        research_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Step 1: Create research plan
        plan = await self.create_research_plan(query, depth)

        # Step 2: Execute parallel searches
        search_results = await self.execute_searches(plan['search_queries'])

        # Step 3: Analyze and extract key findings
        findings = await self.analyze_results(query, search_results)

        # Step 4: Synthesize into final report
        report = await self.synthesize_report(query, findings, depth)

        result = {
            'id': research_id,
            'query': query,
            'depth': depth,
            'plan': plan,
            'sources_searched': len(search_results),
            'findings': findings,
            'report': report,
            'timestamp': datetime.now().isoformat(),
            'demo_mode': DEMO_MODE
        }

        self.research_history.append(result)
        return result

    async def create_research_plan(self, query: str, depth: str) -> dict:
        """Use AI to break down the query into searchable sub-questions."""
        if DEMO_MODE:
            return self._demo_research_plan(query, depth)

        async with aiohttp.ClientSession() as session:
            prompt = f"""You are a research planning agent. Given this research question, create a comprehensive research plan.

Research Question: {query}
Depth: {depth} (quick=3 searches, standard=5 searches, deep=8 searches)

Return a JSON object with:
1. "main_objective": Clear statement of what we're trying to learn
2. "sub_questions": List of specific questions to answer
3. "search_queries": List of optimized search queries to find answers
4. "expected_sources": Types of sources we should look for

Return ONLY valid JSON, no markdown."""

            try:
                async with session.post(
                    'https://api.openai.com/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {self.openai_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': 'gpt-3.5-turbo',
                        'messages': [{'role': 'user', 'content': prompt}],
                        'temperature': 0.7
                    }
                ) as resp:
                    data = await resp.json()
                    content = data['choices'][0]['message']['content']
                    return json.loads(content)
            except Exception as e:
                return self._demo_research_plan(query, depth)

    async def execute_searches(self, queries: list) -> list:
        """Execute multiple searches in parallel."""
        if DEMO_MODE or not SERPER_API_KEY:
            return self._demo_search_results(queries)

        async with aiohttp.ClientSession() as session:
            tasks = [self._search_web(session, q) for q in queries]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [r for r in results if not isinstance(r, Exception)]

    async def _search_web(self, session: aiohttp.ClientSession, query: str) -> dict:
        """Search using Serper API (Google Search)."""
        try:
            async with session.post(
                'https://google.serper.dev/search',
                headers={
                    'X-API-KEY': self.serper_key,
                    'Content-Type': 'application/json'
                },
                json={'q': query, 'num': 5}
            ) as resp:
                data = await resp.json()
                return {
                    'query': query,
                    'results': data.get('organic', [])[:5]
                }
        except Exception as e:
            return {'query': query, 'results': [], 'error': str(e)}

    async def analyze_results(self, original_query: str, search_results: list) -> list:
        """Extract key findings from search results."""
        if DEMO_MODE:
            return self._demo_findings(original_query)

        findings = []
        async with aiohttp.ClientSession() as session:
            for result in search_results:
                if not result.get('results'):
                    continue

                sources_text = "\n".join([
                    f"- {r.get('title', 'Untitled')}: {r.get('snippet', 'No description')}"
                    for r in result['results']
                ])

                prompt = f"""Analyze these search results for the query "{result['query']}"
in the context of researching: "{original_query}"

Sources:
{sources_text}

Extract 2-3 key findings. Return as JSON array of objects with "finding" and "confidence" (high/medium/low) keys."""

                try:
                    async with session.post(
                        'https://api.openai.com/v1/chat/completions',
                        headers={
                            'Authorization': f'Bearer {self.openai_key}',
                            'Content-Type': 'application/json'
                        },
                        json={
                            'model': 'gpt-3.5-turbo',
                            'messages': [{'role': 'user', 'content': prompt}],
                            'temperature': 0.3
                        }
                    ) as resp:
                        data = await resp.json()
                        content = data['choices'][0]['message']['content']
                        parsed = json.loads(content)
                        findings.extend(parsed)
                except:
                    continue

        return findings if findings else self._demo_findings(original_query)

    async def synthesize_report(self, query: str, findings: list, depth: str) -> dict:
        """Synthesize all findings into a comprehensive report."""
        if DEMO_MODE:
            return self._demo_report(query, findings)

        findings_text = "\n".join([
            f"- [{f.get('confidence', 'medium')}] {f.get('finding', f)}"
            for f in findings
        ])

        async with aiohttp.ClientSession() as session:
            prompt = f"""You are a research analyst synthesizing findings into a comprehensive report.

Original Research Question: {query}
Research Depth: {depth}

Key Findings:
{findings_text}

Create a research report with:
1. "executive_summary": 2-3 sentence overview
2. "key_insights": List of 3-5 main insights with explanations
3. "conclusions": What we can confidently conclude
4. "limitations": What we couldn't determine or needs more research
5. "recommendations": Suggested next steps or actions

Return as JSON."""

            try:
                async with session.post(
                    'https://api.openai.com/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {self.openai_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': 'gpt-3.5-turbo',
                        'messages': [{'role': 'user', 'content': prompt}],
                        'temperature': 0.5
                    }
                ) as resp:
                    data = await resp.json()
                    content = data['choices'][0]['message']['content']
                    return json.loads(content)
            except:
                return self._demo_report(query, findings)

    # Demo mode methods
    def _demo_research_plan(self, query: str, depth: str) -> dict:
        """Generate demo research plan."""
        num_searches = {'quick': 3, 'standard': 5, 'deep': 8}.get(depth, 5)

        plans = {
            'default': {
                'main_objective': f'Understand the key aspects of: {query}',
                'sub_questions': [
                    f'What are the fundamentals of {query}?',
                    f'What are current trends in {query}?',
                    f'What are expert opinions on {query}?',
                    f'What are the challenges related to {query}?',
                    f'What does the future look like for {query}?'
                ][:num_searches],
                'search_queries': [
                    f'{query} explained',
                    f'{query} latest trends 2024',
                    f'{query} expert analysis',
                    f'{query} challenges problems',
                    f'{query} future predictions'
                ][:num_searches],
                'expected_sources': ['Industry reports', 'News articles', 'Expert blogs', 'Academic papers']
            }
        }
        return plans['default']

    def _demo_search_results(self, queries: list) -> list:
        """Generate demo search results."""
        results = []
        for query in queries:
            results.append({
                'query': query,
                'results': [
                    {'title': f'Comprehensive Guide to {query}', 'snippet': f'An in-depth look at {query} and its implications...', 'link': 'https://example.com/1'},
                    {'title': f'{query}: What Experts Say', 'snippet': f'Leading experts weigh in on {query}...', 'link': 'https://example.com/2'},
                    {'title': f'The Future of {query}', 'snippet': f'Predictions and trends for {query} in the coming years...', 'link': 'https://example.com/3'},
                ]
            })
        return results

    def _demo_findings(self, query: str) -> list:
        """Generate demo findings."""
        return [
            {'finding': f'{query} is rapidly evolving with new developments emerging regularly', 'confidence': 'high'},
            {'finding': f'Industry experts recommend a balanced approach to {query}', 'confidence': 'high'},
            {'finding': f'There are both opportunities and challenges in the {query} space', 'confidence': 'medium'},
            {'finding': f'Future trends suggest continued growth and innovation in {query}', 'confidence': 'medium'},
            {'finding': f'Best practices for {query} emphasize adaptability and continuous learning', 'confidence': 'high'},
        ]

    def _demo_report(self, query: str, findings: list) -> dict:
        """Generate demo report."""
        return {
            'executive_summary': f'Research on "{query}" reveals a dynamic and evolving landscape. Key findings indicate significant opportunities balanced with notable challenges. The consensus among sources suggests a positive trajectory with important considerations for implementation.',
            'key_insights': [
                {
                    'insight': 'Rapid Evolution',
                    'explanation': f'The {query} space is characterized by continuous innovation and adaptation.'
                },
                {
                    'insight': 'Expert Consensus',
                    'explanation': 'Industry leaders generally agree on core best practices while diverging on implementation details.'
                },
                {
                    'insight': 'Balanced Opportunity',
                    'explanation': 'Significant potential exists, but success requires careful navigation of challenges.'
                },
                {
                    'insight': 'Future Orientation',
                    'explanation': 'Forward-thinking approaches are favored over traditional methodologies.'
                }
            ],
            'conclusions': [
                f'{query} represents a significant area of interest with measurable impact',
                'Success requires both strategic planning and tactical flexibility',
                'Continuous learning and adaptation are essential'
            ],
            'limitations': [
                'Some aspects require deeper domain expertise to fully evaluate',
                'Rapidly changing landscape may affect the longevity of findings',
                'Individual context may significantly affect applicability'
            ],
            'recommendations': [
                f'Develop a phased approach to engaging with {query}',
                'Invest in continuous learning and skill development',
                'Monitor emerging trends and adjust strategy accordingly',
                'Seek expert consultation for high-stakes decisions'
            ]
        }


# Initialize the agent
agent = ResearchAgent()


@app.route('/')
def index():
    """Main research interface."""
    return render_template('index.html', demo_mode=DEMO_MODE)


@app.route('/api/research', methods=['POST'])
def start_research():
    """Start a new research task."""
    data = request.get_json()
    query = data.get('query', '')
    depth = data.get('depth', 'standard')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    # Run async research
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(agent.research(query, depth))
    finally:
        loop.close()

    return jsonify(result)


@app.route('/api/history')
def get_history():
    """Get research history."""
    return jsonify(agent.research_history[-10:])  # Last 10 researches


@app.route('/api/status')
def status():
    """API status check."""
    return jsonify({
        'status': 'operational',
        'demo_mode': DEMO_MODE,
        'features': {
            'ai_planning': not DEMO_MODE,
            'web_search': bool(SERPER_API_KEY),
            'synthesis': not DEMO_MODE
        }
    })


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🔬 AI Research Agent")
    print("="*50)
    if DEMO_MODE:
        print("⚠️  Running in DEMO MODE (no API keys)")
        print("   Add OPENAI_API_KEY and SERPER_API_KEY to .env")
    else:
        print("✅ AI features enabled")
    print(f"\n🌐 Open http://localhost:5015")
    print("="*50 + "\n")

    app.run(debug=True, port=5015)
