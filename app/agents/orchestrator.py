"""
LangGraph Orchestrator - TEAM 3 COMPLETE (OPTIMIZED)

Coordina el workflow multi-agente con ejecución PARALELA y datos optimizados:
1. Data Loader → Carga dashboard_data.json completo (197 KB, 100% de datos)
2. TEAM 2 PARALLEL:
   - AgentAnalista → Performance analysis
   - AgentTecnico → Biomechanics analysis
   - AgentEstratega → Practice program design
3. TEAM 3 PARALLEL:
   - AgentUXWriter → Dashboard content generation
   - AgentCoach → Comprehensive coaching reports
4. Dashboard Writer Agent → Conversión motivacional (usa combined análisis)

OPTIMIZACIÓN: Eliminado cuello de botella Analytics Pro + RAG queries múltiples.
Ahora: 1 carga JSON → Teams 2+3 reciben 100% de datos del backend.

Output: 5 análisis especializados + motivacional para frontend
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from loguru import logger
import sys
import asyncio
import json

# Add parent directory to path for imports
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.agents.analista import AgentAnalista
from app.agents.tecnico import AgentTecnico
from app.agents.estratega import AgentEstratega
from app.agents.ux_writer import AgentUXWriter
from app.agents.coach import AgentCoach
from app.agents.dashboard_writer import dashboard_writer_agent


class AgentState(TypedDict):
    """Estado compartido entre agentes"""
    user_id: str
    dashboard_data: dict           # JSON completo del backend (197 KB) - OPTIMIZED
    analista_output: dict          # AgentAnalista (performance) - TEAM 2
    tecnico_output: dict           # AgentTecnico (biomechanics) - TEAM 2
    estratega_output: dict         # AgentEstratega (practice) - TEAM 2
    ux_writer_output: dict         # AgentUXWriter (dashboard content) - TEAM 3
    coach_output: dict             # AgentCoach (coaching reports) - TEAM 3
    motivational_sections: dict
    error: str | None


async def data_loader_node(state: AgentState) -> AgentState:
    """
    Nodo 1: Data Loader (OPTIMIZED)

    Carga dashboard_data.json completo (197 KB) con TODA la información del backend:
    - 52 funciones de análisis
    - Todos los clubs statistics
    - Todas las rondas
    - Todo el análisis temporal
    - Todos los benchmarks

    Esto elimina el cuello de botella de Analytics Pro y las 4 queries RAG.
    Team 2 recibe 100% de los datos de una sola vez.
    """
    logger.info(f"[Orchestrator] Node 1: Data Loader (user: {state['user_id']})")

    try:
        # Buscar dashboard_data.json en dos ubicaciones posibles
        project_root = Path(__file__).parent.parent.parent
        json_paths = [
            project_root / "output" / "dashboard_data.json",
            project_root / "dashboard_data.json"
        ]

        data = None
        for json_path in json_paths:
            if json_path.exists():
                logger.info(f"[Orchestrator] Loading data from: {json_path}")
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                break

        if not data:
            raise FileNotFoundError("dashboard_data.json not found in output/ or root")

        state["dashboard_data"] = data

        # Log data summary
        metadata = data.get("metadata", {})
        logger.info(f"[Orchestrator] Data loaded successfully:")
        logger.info(f"   - Version: {metadata.get('version', 'unknown')}")
        logger.info(f"   - Clubs: {len(data.get('club_statistics', []))}")
        logger.info(f"   - Size: {len(json.dumps(data)) / 1024:.1f} KB")
        logger.info(f"   - Functions: {len(metadata.get('changes', []))}")

    except Exception as e:
        error_msg = f"Data loader error: {str(e)}"
        logger.error(f"[Orchestrator] {error_msg}")
        state["error"] = error_msg

    return state


async def team2_parallel_node(state: AgentState) -> AgentState:
    """
    Nodo 2: Ejecuta TEAM 2 en PARALELO

    Los 3 especialistas trabajan simultáneamente:
    - AgentAnalista: Performance & stats
    - AgentTecnico: Biomechanics & technique
    - AgentEstratega: Practice program & ROI

    Usando asyncio.gather() para ejecución paralela.
    """
    logger.info("[Orchestrator] Node 2: TEAM 2 PARALLEL EXECUTION")
    logger.info("   - Launching 3 specialists simultaneously...")

    try:
        # Skip si hay error previo
        if state.get("error"):
            logger.warning("[Orchestrator] Skipping Team 2 due to previous error")
            return state

        # Crear instancias de los 3 agentes
        agent_analista = AgentAnalista()
        agent_tecnico = AgentTecnico()
        agent_estratega = AgentEstratega()

        # Pasar dashboard_data completo a cada agente (OPTIMIZED)
        dashboard_data = state.get("dashboard_data", {})

        if not dashboard_data:
            raise ValueError("dashboard_data not loaded - data_loader_node failed")

        # Ejecutar los 3 agentes EN PARALELO con datos completos
        logger.info("[Orchestrator] Running agents in parallel with full data...")
        start_time = asyncio.get_event_loop().time()

        results = await asyncio.gather(
            agent_analista.analyze(state["user_id"], dashboard_data=dashboard_data),
            agent_tecnico.analyze(state["user_id"], dashboard_data=dashboard_data),
            agent_estratega.design(state["user_id"], dashboard_data=dashboard_data),
            return_exceptions=True  # Capturar errores individuales
        )

        end_time = asyncio.get_event_loop().time()
        parallel_time = end_time - start_time

        # Procesar resultados
        analista_result, tecnico_result, estratega_result = results

        # Verificar errores
        errors = []
        if isinstance(analista_result, Exception):
            errors.append(f"AgentAnalista: {analista_result}")
        else:
            state["analista_output"] = analista_result
            logger.info(f"   ✓ AgentAnalista: {analista_result['metadata']['analysis_length']} chars")

        if isinstance(tecnico_result, Exception):
            errors.append(f"AgentTecnico: {tecnico_result}")
        else:
            state["tecnico_output"] = tecnico_result
            logger.info(f"   ✓ AgentTecnico: {tecnico_result['metadata']['analysis_length']} chars")

        if isinstance(estratega_result, Exception):
            errors.append(f"AgentEstratega: {estratega_result}")
        else:
            state["estratega_output"] = estratega_result
            logger.info(f"   ✓ AgentEstratega: {estratega_result['metadata']['program_length']} chars")

        logger.info(f"[Orchestrator] TEAM 2 parallel execution completed in {parallel_time:.1f}s")

        if errors:
            state["error"] = "; ".join(errors)
            logger.error(f"[Orchestrator] Team 2 errors: {state['error']}")

    except Exception as e:
        error_msg = f"Team 2 parallel error: {str(e)}"
        logger.error(f"[Orchestrator] {error_msg}")
        state["error"] = error_msg

    return state


async def team3_parallel_node(state: AgentState) -> AgentState:
    """
    Nodo 3: Ejecuta TEAM 3 en PARALELO

    Los 2 especialistas de contenido trabajan simultáneamente:
    - AgentUXWriter: Dashboard content generation
    - AgentCoach: Comprehensive coaching reports

    Usando asyncio.gather() para ejecución paralela.
    """
    logger.info("[Orchestrator] Node 3: TEAM 3 PARALLEL EXECUTION")
    logger.info("   - Launching 2 content specialists simultaneously...")

    try:
        # Skip si hay error previo
        if state.get("error"):
            logger.warning("[Orchestrator] Skipping Team 3 due to previous error")
            return state

        # Crear instancias de los 2 agentes
        agent_ux_writer = AgentUXWriter()
        agent_coach = AgentCoach()

        # Pasar dashboard_data completo a ambos agentes
        dashboard_data = state.get("dashboard_data", {})

        if not dashboard_data:
            raise ValueError("dashboard_data not loaded - data_loader_node failed")

        # Preparar Team 2 analysis para AgentCoach
        team2_analysis = {
            "analista": state.get("analista_output", {}).get("analysis", ""),
            "tecnico": state.get("tecnico_output", {}).get("analysis", ""),
            "estratega": state.get("estratega_output", {}).get("program", "")
        }

        # Ejecutar los 2 agentes EN PARALELO con datos completos
        logger.info("[Orchestrator] Running Team 3 agents in parallel...")
        start_time = asyncio.get_event_loop().time()

        results = await asyncio.gather(
            agent_ux_writer.write(state["user_id"], dashboard_data=dashboard_data),
            agent_coach.coach(state["user_id"], dashboard_data=dashboard_data, team2_analysis=team2_analysis),
            return_exceptions=True  # Capturar errores individuales
        )

        end_time = asyncio.get_event_loop().time()
        parallel_time = end_time - start_time

        # Procesar resultados
        ux_writer_result, coach_result = results

        # Verificar errores
        errors = []
        if isinstance(ux_writer_result, Exception):
            errors.append(f"AgentUXWriter: {ux_writer_result}")
        else:
            state["ux_writer_output"] = ux_writer_result
            content_len = len(json.dumps(ux_writer_result.get("content", {})))
            logger.info(f"   ✓ AgentUXWriter: {content_len} chars")

        if isinstance(coach_result, Exception):
            errors.append(f"AgentCoach: {coach_result}")
        else:
            state["coach_output"] = coach_result
            logger.info(f"   ✓ AgentCoach: {coach_result['metadata']['report_length']} chars")

        logger.info(f"[Orchestrator] TEAM 3 parallel execution completed in {parallel_time:.1f}s")

        if errors:
            state["error"] = "; ".join(errors)
            logger.error(f"[Orchestrator] Team 3 errors: {state['error']}")

    except Exception as e:
        error_msg = f"Team 3 parallel error: {str(e)}"
        logger.error(f"[Orchestrator] {error_msg}")
        state["error"] = error_msg

    return state


async def writer_node(state: AgentState) -> AgentState:
    """
    Nodo 4: Ejecuta Dashboard Writer Agent

    Convierte análisis combinado (Team 2) en 3 secciones motivacionales:
    - DNA golfístico
    - Evolución/Progreso
    - Próximo nivel/Acción

    Combina outputs de AgentAnalista + AgentTecnico + AgentEstratega.
    """
    logger.info("[Orchestrator] Node 3: Dashboard Writer Agent")

    try:
        # Skip si hay error previo
        if state.get("error"):
            logger.warning("[Orchestrator] Skipping writer due to previous error")
            return state

        # Combinar análisis de los 3 agentes
        combined_analysis = ""

        if state.get("analista_output"):
            combined_analysis += "## PERFORMANCE ANALYSIS\n\n"
            combined_analysis += state["analista_output"].get("analysis", "") + "\n\n"

        if state.get("tecnico_output"):
            combined_analysis += "## BIOMECHANICS ANALYSIS\n\n"
            combined_analysis += state["tecnico_output"].get("analysis", "") + "\n\n"

        if state.get("estratega_output"):
            combined_analysis += "## PRACTICE PROGRAM\n\n"
            combined_analysis += state["estratega_output"].get("program", "") + "\n\n"

        # Fallback a Analytics Pro si Team 2 no disponible
        if not combined_analysis:
            logger.warning("[Orchestrator] Team 2 outputs not available, using Analytics Pro")
            combined_analysis = state["technical_analysis"]

        # Convertir análisis combinado a motivacional
        sections = await dashboard_writer_agent(combined_analysis)
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

# Add nodes (TEAM 3 COMPLETE with data_loader optimization)
workflow.add_node("data_loader", data_loader_node)    # Load JSON completo
workflow.add_node("team2", team2_parallel_node)       # TEAM 2 PARALLEL (3 agents)
workflow.add_node("team3", team3_parallel_node)       # TEAM 3 PARALLEL (2 agents)
workflow.add_node("writer", writer_node)              # Dashboard Writer

# Define edges (sequential with parallel sections)
workflow.set_entry_point("data_loader")   # Start with data load
workflow.add_edge("data_loader", "team2")  # After data loaded, launch Team 2 parallel
workflow.add_edge("team2", "team3")        # After Team 2, launch Team 3 parallel
workflow.add_edge("team3", "writer")       # After Team 3, write motivational
workflow.add_edge("writer", END)

# Compile graph
app = workflow.compile()


async def run_multi_agent_analysis(user_id: str) -> dict:
    """
    Ejecuta el workflow completo multi-agente (TEAM 3 COMPLETE - OPTIMIZED).

    Flujo:
    1. Data Loader carga dashboard_data.json completo (100% datos backend)
    2. TEAM 2 en PARALELO (AgentAnalista + AgentTecnico + AgentEstratega)
       - Reciben datos completos directamente (no RAG queries)
    3. TEAM 3 en PARALELO (AgentUXWriter + AgentCoach)
       - Reciben dashboard_data + Team 2 analysis
    4. Dashboard Writer convierte análisis combinado a motivacional
    5. Retorna todos los outputs

    Args:
        user_id: Usuario a analizar (ej: "alvaro")

    Returns:
        {
            "dashboard_data": dict,         # JSON completo del backend
            "analista_output": {            # AgentAnalista (performance)
                "analysis": str,
                "metadata": dict
            },
            "tecnico_output": {             # AgentTecnico (biomechanics)
                "analysis": str,
                "metadata": dict
            },
            "estratega_output": {           # AgentEstratega (practice program)
                "program": str,
                "metadata": dict
            },
            "ux_writer_output": {           # AgentUXWriter (dashboard content)
                "content": dict,
                "metadata": dict
            },
            "coach_output": {               # AgentCoach (coaching reports)
                "report": str,
                "metadata": dict
            },
            "motivational_sections": {      # Dashboard Writer
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
    logger.info(f"[Orchestrator] Starting TEAM 3 COMPLETE workflow for user: {user_id}")
    logger.info("=" * 70)

    # Initial state
    initial_state = {
        "user_id": user_id,
        "dashboard_data": {},
        "analista_output": {},
        "tecnico_output": {},
        "estratega_output": {},
        "ux_writer_output": {},
        "coach_output": {},
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
            data_size = len(json.dumps(final_state.get('dashboard_data', {})))
            logger.info(f"   - Dashboard data: {data_size / 1024:.1f} KB")
            logger.info(f"   - AgentAnalista: {len(final_state.get('analista_output', {}).get('analysis', ''))} chars")
            logger.info(f"   - AgentTecnico: {len(final_state.get('tecnico_output', {}).get('analysis', ''))} chars")
            logger.info(f"   - AgentEstratega: {len(final_state.get('estratega_output', {}).get('program', ''))} chars")
            logger.info(f"   - AgentUXWriter: {len(json.dumps(final_state.get('ux_writer_output', {}).get('content', {})))} chars")
            logger.info(f"   - AgentCoach: {len(final_state.get('coach_output', {}).get('report', ''))} chars")
            logger.info(f"   - Motivational sections: {len(final_state.get('motivational_sections', {}))} keys")

        return {
            "dashboard_data": final_state.get("dashboard_data", {}),
            "analista_output": final_state.get("analista_output", {}),
            "tecnico_output": final_state.get("tecnico_output", {}),
            "estratega_output": final_state.get("estratega_output", {}),
            "ux_writer_output": final_state.get("ux_writer_output", {}),
            "coach_output": final_state.get("coach_output", {}),
            "motivational_sections": final_state.get("motivational_sections", {}),
            "error": final_state.get("error")
        }

    except Exception as e:
        error_msg = f"Orchestrator critical error: {str(e)}"
        logger.error(f"[Orchestrator] {error_msg}")
        raise Exception(error_msg)


# Export for main.py
__all__ = ["run_multi_agent_analysis", "app"]
