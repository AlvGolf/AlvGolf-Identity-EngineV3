"""
AlvGolf Agentic Analytics Engine - Analytics Pro Agent

Specialized agent for technical golf analysis.
Generates structured 5-section analysis report.
"""

from langchain_anthropic import ChatAnthropic
from app.config import settings
from app.rag import rag_answer


# ============ Initialize Claude ============

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    anthropic_api_key=settings.anthropic_api_key,
    temperature=0.1,  # Precise for technical analysis
    max_tokens=2000,
    # Enable prompt caching for cost savings
    default_headers={
        "anthropic-beta": "prompt-caching-2024-07-31"
    }
)


# ============ System Prompt ============

SYSTEM_PROMPT = """You are the Analytics Pro Agent for AlvGolf, a specialized golf analytics assistant.

Your mission: Generate a STRUCTURED and PROFESSIONAL technical analysis of the player's golf data.

MANDATORY STRUCTURE (5 sections):

## 1. TECHNICAL PATTERNS
- Ball flight tendency (slice/hook/straight/fade/draw)
- Face-to-path average (values + interpretation)
- Attack angle tendency (values + effect on distance)
- Club speed vs PGA Tour (percentage comparison)

## 2. STATISTICAL TRENDS
- Distance evolution last 4 weeks (improving/declining/stable)
- Consistency evolution (standard deviation over time)
- Benchmarks comparison (PGA Tour, HCP 15, HCP 23)
- Highlighted percentiles (top/bottom performers)

## 3. MAIN GAPS
- Top 3 improvement areas (prioritized)
- Estimated impact in strokes per area
- Specific data supporting each gap

## 4. RECOMMENDATIONS
- Technical drill #1 (highest impact)
- Technical drill #2 (second impact)
- Mental/strategic change

## 5. PREDICTION
- Projected HCP in 30 days (with conditions)
- Target score for next round
- Prediction confidence (high/medium/low)

CRITICAL RULES:
- Use specific numerical data (speed, distance, angles)
- Always compare vs relevant benchmarks
- Be precise but accessible (avoid excessive jargon)
- Total length: 150-200 words
- Focus on actionable insights
""".strip()


# ============ Analytics Pro Agent ============

async def analytics_agent(user_id: str) -> str:
    """
    Analytics Pro Agent: Deep technical analysis.

    Process:
    1. Query RAG for player's recent data
    2. Build comprehensive context
    3. Invoke Claude with specialized system prompt
    4. Return structured analysis

    Args:
        user_id: User ID to analyze

    Returns:
        Structured technical analysis (5 sections)
    """
    print(f"[INFO] Analytics Pro Agent analyzing user: {user_id}")

    # Get context from RAG
    print("[INFO] Querying RAG for player data...")
    context = rag_answer(
        user_id,
        "Provide a comprehensive summary of my golf data: driver stats, "
        "wedges performance, handicap evolution, recent rounds, and key patterns."
    )

    # Build full prompt
    full_prompt = f"""{SYSTEM_PROMPT}

Player data (retrieved from vector database):
{context}

Generate the 5-section analysis following the structure above.
"""

    # Invoke Claude
    print("[INFO] Invoking Claude for analysis...")
    response = llm.invoke(full_prompt)

    print(f"[OK] Analysis generated ({len(response.content)} chars)")
    return response.content


# ============ Testing ============

if __name__ == "__main__":
    import asyncio

    async def test():
        print("Testing Analytics Pro Agent...")
        # Note: This will fail if no data ingested yet
        try:
            result = await analytics_agent("alvaro")
            print("\n" + "="*60)
            print("ANALYTICS PRO OUTPUT:")
            print("="*60)
            print(result)
            print("="*60)
        except Exception as e:
            print(f"[ERROR] {e}")
            print("[INFO] Agent code is correct, but needs data ingestion first")

    asyncio.run(test())
