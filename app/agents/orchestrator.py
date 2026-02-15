"""
LangGraph Orchestrator - TIER 2

Coordina el workflow multi-agente:
1. Analytics Pro Agent → Análisis técnico (5 secciones)
2. Dashboard Writer Agent → Conversión motivacional (3 secciones)

Output: Ambos análisis para frontend
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from loguru import logger
import sys

# Add parent directory to path for imports
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.agents.analytics_pro import analytics_agent
from app.agents.dashboard_writer import dashboard_writer_agent


class AgentState(TypedDict):
    """Estado compartido entre agentes"""
    user_id: str
    technical_analysis: str
    motivational_sections: dict
    error: str | None


async def analytics_node(state: AgentState) -> AgentState:
    """
    Nodo 1: Ejecuta Analytics Pro Agent (TIER 1)

    Genera análisis técnico con 5 secciones:
    - Patrones técnicos
    - Tendencias estadísticas
    - Gaps principales
    - Recomendaciones
    - Predicción
    """
    logger.info(f"[Orchestrator] Node 1: Analytics Pro Agent (user: {state['user_id']})")

    try:
        analysis = await analytics_agent(state["user_id"])
        state["technical_analysis"] = analysis
        logger.info(f"[Orchestrator] Analytics Pro completed ({len(analysis)} chars)")

    except Exception as e:
        error_msg = f"Analytics error: {str(e)}"
        logger.error(f"[Orchestrator] {error_msg}")
        state["error"] = error_msg

    return state


async def writer_node(state: AgentState) -> AgentState:
    """
    Nodo 2: Ejecuta Dashboard Writer Agent (TIER 2)

    Convierte análisis técnico en 3 secciones motivacionales:
    - DNA golfístico
    - Evolución/Progreso
    - Próximo nivel/Acción
    """
    logger.info("[Orchestrator] Node 2: Dashboard Writer Agent")

    try:
        # Skip si hay error previo
        if state.get("error"):
            logger.warning("[Orchestrator] Skipping writer due to previous error")
            return state

        # Convertir análisis técnico a motivacional
        sections = await dashboard_writer_agent(
            state["technical_analysis"]
        )
        state["motivational_sections"] = sections
        logger.info("[Orchestrator] Dashboard Writer completed")
        logger.info(f"   - DNA: {len(sections['dna'])} chars")
        logger.info(f"   - Progress: {len(sections['progress'])} chars")
        logger.info(f"   - Action: {len(sections['action'])} chars")

    except Exception as e:
        error_msg = f"Writer error: {str(e)}"
        logger.error(f"[Orchestrator] {error_msg}")
        state["error"] = error_msg

    return state


# Build workflow graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analytics", analytics_node)
workflow.add_node("writer", writer_node)

# Define edges (sequential: analytics → writer → end)
workflow.set_entry_point("analytics")
workflow.add_edge("analytics", "writer")
workflow.add_edge("writer", END)

# Compile graph
app = workflow.compile()


async def run_multi_agent_analysis(user_id: str) -> dict:
    """
    Ejecuta el workflow completo multi-agente.

    Flujo:
    1. Analytics Pro genera análisis técnico
    2. Dashboard Writer convierte a motivacional
    3. Retorna ambos outputs

    Args:
        user_id: Usuario a analizar (ej: "alvaro")

    Returns:
        {
            "technical_analysis": str,  # 5 secciones técnicas (Analytics Pro)
            "motivational_sections": {  # 3 secciones motivacionales (Dashboard Writer)
                "dna": str,
                "progress": str,
                "action": str
            },
            "error": str | None
        }

    Raises:
        Exception: Si hay error crítico en el workflow
    """
    logger.info("=" * 70)
    logger.info(f"[Orchestrator] Starting multi-agent workflow for user: {user_id}")
    logger.info("=" * 70)

    # Initial state
    initial_state = {
        "user_id": user_id,
        "technical_analysis": "",
        "motivational_sections": {},
        "error": None
    }

    try:
        # Execute workflow
        final_state = await app.ainvoke(initial_state)

        # Log results
        if final_state.get("error"):
            logger.error(f"[Orchestrator] Workflow completed with error: {final_state['error']}")
        else:
            logger.info("[Orchestrator] Workflow completed successfully")
            logger.info(f"   - Technical analysis: {len(final_state.get('technical_analysis', ''))} chars")
            logger.info(f"   - Motivational sections: {len(final_state.get('motivational_sections', {}))} keys")

        return {
            "technical_analysis": final_state.get("technical_analysis", ""),
            "motivational_sections": final_state.get("motivational_sections", {}),
            "error": final_state.get("error")
        }

    except Exception as e:
        error_msg = f"Orchestrator critical error: {str(e)}"
        logger.error(f"[Orchestrator] {error_msg}")
        raise Exception(error_msg)


# Export for main.py
__all__ = ["run_multi_agent_analysis", "app"]
