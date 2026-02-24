"""
LangGraph Orchestrator v4.1 — asyncio.to_thread() paralelismo real

Flujo de 6 nodos con scoring determinista previo al análisis IA:
1. data_loader    → Carga dashboard_data.json completo
2. scoring_node   → ScoringEngine: 8 dimensiones 0-10 (< 10ms, sin IA)
3. archetype_node → ArchetypeClassifier: Golf Identity (< 5ms, sin IA)
4. team2 PARALLEL → AgentAnalista + AgentTecnico + AgentEstratega  (~49s)
                    (reciben scoring_profile + golf_identity en el contexto)
5. team3 PARALLEL → AgentUXWriter + AgentCoach                     (~86s)
6. writer         → Dashboard Writer: secciones motivacionales

PARALELISMO REAL (v4.1):
- llm.invoke() es síncrono — asyncio.gather() solo no paralleliza
- asyncio.to_thread() mueve cada agente a su propio thread del pool del SO
- Cada thread crea su propio event loop para ejecutar el agente
- Resultado: Team 2 ~49s (vs ~148s antes), Team 3 ~86s (vs ~156s antes)
- Total /analyze: ~2.25 min (vs ~5.3 min antes) — ahorro de ~168s (53%)

VENTAJAS v4.1 vs v4.0:
- Paralelismo real entre los 5 agentes IA
- Sin cambios en la arquitectura de nodos ni en los agentes
- UXWriter permanece en Team 3 (óptimo: si estuviera en Team 2 sería 21s más lento)

Output: scoring_profile + golf_identity + 5 análisis especializados + motivacional
"""

from typing import TypedDict, Annotated, Any
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


# ── Blacklist: claves de pura visualización UI, sin valor analítico para LLMs ─
UI_ONLY_KEYS = frozenset({
    'shot_zones_heatmap',      # 21.4 KB — grid de coords XY crudas para Chart.js heatmap
    'dispersion_by_club',      # 11.8 KB — scatter plots crudos por palo (Chart.js)
    'metadata',                #  3.6 KB — versión, timestamps, config del generador
    'generated_at',            #  0.0 KB — timestamp de generación
    'scoring_zones_by_course', #  0.0 KB — datos vacíos de zonas por campo
})
# Total filtrado: ~36.8 KB = 34.5% del JSON. Ratio señal/ruido sube de ~65% a ~100%.


def _filter_for_agents(data: dict) -> dict:
    """Filtra claves de pura visualización UI antes de pasar datos a agentes IA."""
    return {k: v for k, v in data.items() if k not in UI_ONLY_KEYS}


# ── Helper de threading ───────────────────────────────────────────────────────

def _agent_thread_runner(agent_class, method_name: str, *args, **kwargs):
    """
    Ejecuta un método async de agente en un thread dedicado con su propio
    event loop. Necesario porque llm.invoke() es síncrono bloqueante —
    asyncio.gather() solo no puede paralelizar llamadas síncronas.

    Uso:
        await asyncio.to_thread(_agent_thread_runner, AgentAnalista, 'analyze',
                                user_id, dashboard_data=data)
    """
    import asyncio as _asyncio
    loop = _asyncio.new_event_loop()
    _asyncio.set_event_loop(loop)
    try:
        agent = agent_class()
        coro = getattr(agent, method_name)(*args, **kwargs)
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ─────────────────────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    """Estado compartido entre todos los nodos del workflow."""
    user_id: str
    dashboard_data: dict        # JSON completo del backend (enriquecido progresivamente)
    scoring_result: Any         # ScoringResult object (del ScoringEngine)
    archetype_result: Any       # ArchetypeResult object (del ArchetypeClassifier)
    analista_output: dict       # AgentAnalista (performance) - TEAM 2
    tecnico_output: dict        # AgentTecnico (biomechanics) - TEAM 2
    estratega_output: dict      # AgentEstratega (practice) - TEAM 2
    ux_writer_output: dict      # AgentUXWriter (dashboard content) - TEAM 3
    coach_output: dict          # AgentCoach (coaching reports) - TEAM 3
    motivational_sections: dict
    error: str | None


# ══════════════════════════════════════════════════════════════
# NODO 1: DATA LOADER
# ══════════════════════════════════════════════════════════════

async def data_loader_node(state: AgentState) -> AgentState:
    """
    Nodo 1: Carga dashboard_data.json completo.

    Busca en output/ primero, luego en la raíz del proyecto.
    El JSON resultante se enriquecerá en los nodos 2 y 3 con scoring + arquetipo.
    """
    logger.info(f"[Orchestrator v4.0] Node 1/6: Data Loader (user: {state['user_id']})")

    try:
        project_root = Path(__file__).parent.parent.parent
        json_paths = [
            project_root / "output" / "dashboard_data.json",
            project_root / "dashboard_data.json",
        ]

        data = None
        for json_path in json_paths:
            if json_path.exists():
                logger.info(f"[Orchestrator] Loading from: {json_path}")
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                break

        if not data:
            raise FileNotFoundError("dashboard_data.json not found in output/ or root")

        state["dashboard_data"] = data

        metadata = data.get("metadata", {})
        logger.info(f"[Orchestrator] Data loaded: {len(json.dumps(data)) / 1024:.1f} KB, "
                    f"version {metadata.get('version', 'unknown')}")

    except Exception as e:
        logger.error(f"[Orchestrator] Data loader error: {e}")
        state["error"] = f"Data loader error: {e}"

    return state


# ══════════════════════════════════════════════════════════════
# NODO 2: SCORING NODE
# ══════════════════════════════════════════════════════════════

async def scoring_node(state: AgentState) -> AgentState:
    """
    Nodo 2: Scoring Engine determinista (< 10ms, sin IA).

    Extrae métricas del dashboard_data cargado y calcula las 8 dimensiones
    de juego con puntuaciones 0-10. El resultado se guarda en:
    - state['scoring_result']          → objeto ScoringResult completo
    - state['dashboard_data']['scoring_profile'] → dict serializado para agentes IA
    """
    logger.info("[Orchestrator v4.0] Node 2/6: Scoring Engine")

    if state.get("error"):
        logger.warning("[Orchestrator] Skipping scoring due to previous error")
        return state

    try:
        from app.scoring_engine import ScoringEngine
        from app.scoring_integration import _extract_metrics_from_json

        dashboard_data = state["dashboard_data"]
        hcp = float(dashboard_data.get("player_stats", {}).get("handicap_actual", 23.2))
        player_id = state["user_id"]

        # Extraer métricas y calcular scores (determinista, < 10ms)
        metrics = _extract_metrics_from_json(dashboard_data)
        engine = ScoringEngine()
        result = engine.score(player_id=player_id, player_hcp=hcp, metrics=metrics)

        state["scoring_result"] = result

        # Serializar scoring_profile en dashboard_data para que los agentes lo vean
        state["dashboard_data"]["scoring_profile"] = {
            "player_hcp":        hcp,
            "overall_score":     result.overall_score,
            "tee_to_green":      result.tee_to_green,
            "scoring_game":      result.scoring_game,
            "data_completeness": result.data_completeness,
            "dimensions": {
                name: {
                    "score":      dim.score,
                    "percentile": dim.percentile,
                    "zone":       dim.zone.value,
                    "confidence": dim.confidence.value,
                    "notes":      dim.notes,
                }
                for name, dim in [
                    ("long_game",   result.long_game),
                    ("mid_game",    result.mid_game),
                    ("short_game",  result.short_game),
                    ("putting",     result.putting),
                    ("consistency", result.consistency),
                    ("mental",      result.mental),
                    ("power",       result.power),
                    ("accuracy",    result.accuracy),
                ]
            },
            "ranking":       result.dimensions_by_score(),
            "top_strength":  result.top_strength(),
            "top_gap":       result.top_gap(),
        }

        logger.info(f"[Orchestrator] Scoring OK: overall={result.overall_score}/10 | "
                    f"top={result.top_strength()[0]} ({result.top_strength()[1]}) | "
                    f"gap={result.top_gap()[0]} ({result.top_gap()[1]})")

    except Exception as e:
        logger.error(f"[Orchestrator] Scoring node error: {e}")
        # No bloqueamos el workflow — agentes IA pueden continuar sin scoring
        state["scoring_result"] = None

    return state


# ══════════════════════════════════════════════════════════════
# NODO 3: ARCHETYPE NODE
# ══════════════════════════════════════════════════════════════

async def archetype_node(state: AgentState) -> AgentState:
    """
    Nodo 3: Archetype Classifier determinista (< 5ms, sin IA).

    Clasifica el perfil de juego en uno de 12 arquetipos basándose
    en el vector de scores calculado por scoring_node. El resultado:
    - state['archetype_result']          → objeto ArchetypeResult completo
    - state['dashboard_data']['golf_identity'] → dict serializado para agentes IA
    """
    logger.info("[Orchestrator v4.0] Node 3/6: Archetype Classifier")

    if state.get("error"):
        logger.warning("[Orchestrator] Skipping archetype due to previous error")
        return state

    scoring_result = state.get("scoring_result")
    if scoring_result is None:
        logger.warning("[Orchestrator] No scoring_result available, skipping archetype")
        return state

    try:
        from app.archetype_classifier import ArchetypeClassifier

        classifier = ArchetypeClassifier()
        arch_result = classifier.classify(scoring_result)

        state["archetype_result"] = arch_result

        # Serializar golf_identity en dashboard_data
        arch = arch_result.archetype
        state["dashboard_data"]["golf_identity"] = {
            "archetype_id":          arch.id,
            "archetype_name":        arch.name_es,
            "archetype_tagline":     arch.tagline_es,
            "archetype_description": arch.description_es,
            "archetype_strategy":    arch.strategy_es,
            "fit_score":             arch_result.fit_score,
            "primary_strength": {
                "dimension": arch_result.primary_strength_dim,
                "score":     arch_result.primary_strength_val,
            },
            "primary_gap": {
                "dimension": arch_result.primary_gap_dim,
                "score":     arch_result.primary_gap_val,
            },
            "similar_archetypes": [
                {"id": sid, "name": sname, "similarity": ssim}
                for sid, sname, ssim in arch_result.similar_archetypes
            ],
            "evolution_target": {
                "id":   arch_result.evolution_target[0],
                "name": arch_result.evolution_target[1],
            } if arch_result.evolution_target else None,
            "personalized_insight": arch_result.personalized_insight_es,
            "pro_references":       arch.pro_references,
            "defining_strengths":   arch.defining_strengths,
            "defining_gaps":        arch.defining_gaps,
        }

        logger.info(f"[Orchestrator] Archetype OK: {arch.id} — {arch.name_es} "
                    f"(fit={arch_result.fit_score:.0%})")

    except Exception as e:
        logger.error(f"[Orchestrator] Archetype node error: {e}")
        state["archetype_result"] = None

    return state


# ══════════════════════════════════════════════════════════════
# NODO 4: TEAM 2 PARALELO
# ══════════════════════════════════════════════════════════════

async def team2_parallel_node(state: AgentState) -> AgentState:
    """
    Nodo 4: TEAM 2 en PARALELO (3 agentes IA).

    Los agentes reciben dashboard_data ENRIQUECIDO con scoring_profile
    y golf_identity calculados en los nodos 2-3. Esto permite análisis
    más precisos y personalizados al perfil del jugador.

    - AgentAnalista:  Performance & stats
    - AgentTecnico:   Biomechanics & technique
    - AgentEstratega: Practice program & ROI
    """
    logger.info("[Orchestrator v4.0] Node 4/6: TEAM 2 PARALLEL")

    if state.get("error"):
        logger.warning("[Orchestrator] Skipping Team 2 due to previous error")
        return state

    try:
        dashboard_data = state.get("dashboard_data", {})
        if not dashboard_data:
            raise ValueError("dashboard_data not loaded")

        # Filtrar claves de pura visualización UI (ahorra ~36.8 KB / 34.5% del input)
        agent_data = _filter_for_agents(dashboard_data)
        logger.info(f"[Orchestrator] Data filtered for agents: {len(json.dumps(agent_data))/1024:.1f} KB "
                    f"(was {len(json.dumps(dashboard_data))/1024:.1f} KB, -{len(UI_ONLY_KEYS)} UI keys)")

        logger.info("[Orchestrator] Launching 3 specialists in parallel (threads)...")
        start_time = asyncio.get_event_loop().time()

        results = await asyncio.gather(
            asyncio.to_thread(_agent_thread_runner, AgentAnalista,  'analyze', state["user_id"], dashboard_data=agent_data),
            asyncio.to_thread(_agent_thread_runner, AgentTecnico,   'analyze', state["user_id"], dashboard_data=agent_data),
            asyncio.to_thread(_agent_thread_runner, AgentEstratega, 'design',  state["user_id"], dashboard_data=agent_data),
            return_exceptions=True,
        )

        elapsed = asyncio.get_event_loop().time() - start_time
        analista_result, tecnico_result, estratega_result = results

        errors = []
        if isinstance(analista_result, Exception):
            errors.append(f"AgentAnalista: {analista_result}")
        else:
            state["analista_output"] = analista_result
            logger.info(f"   OK AgentAnalista: {analista_result['metadata']['analysis_length']} chars")

        if isinstance(tecnico_result, Exception):
            errors.append(f"AgentTecnico: {tecnico_result}")
        else:
            state["tecnico_output"] = tecnico_result
            logger.info(f"   OK AgentTecnico: {tecnico_result['metadata']['analysis_length']} chars")

        if isinstance(estratega_result, Exception):
            errors.append(f"AgentEstratega: {estratega_result}")
        else:
            state["estratega_output"] = estratega_result
            logger.info(f"   OK AgentEstratega: {estratega_result['metadata']['program_length']} chars")

        logger.info(f"[Orchestrator] TEAM 2 completed in {elapsed:.1f}s")

        if errors:
            state["error"] = "; ".join(errors)
            logger.error(f"[Orchestrator] Team 2 errors: {state['error']}")

    except Exception as e:
        logger.error(f"[Orchestrator] Team 2 error: {e}")
        state["error"] = f"Team 2 error: {e}"

    return state


# ══════════════════════════════════════════════════════════════
# NODO 5: TEAM 3 PARALELO
# ══════════════════════════════════════════════════════════════

async def team3_parallel_node(state: AgentState) -> AgentState:
    """
    Nodo 5: TEAM 3 en PARALELO (2 agentes IA de contenido).

    Reciben dashboard_data enriquecido con scoring + arquetipo + análisis Team 2.

    - AgentUXWriter: Dashboard content (hero, DNA, charts, insights)
    - AgentCoach:    Comprehensive coaching report
    """
    logger.info("[Orchestrator v4.0] Node 5/6: TEAM 3 PARALLEL")

    if state.get("error"):
        logger.warning("[Orchestrator] Skipping Team 3 due to previous error")
        return state

    try:
        dashboard_data = state.get("dashboard_data", {})
        if not dashboard_data:
            raise ValueError("dashboard_data not loaded")

        # Coach recibe datos filtrados; UXWriter tiene su propio _compact() interno
        agent_data = _filter_for_agents(dashboard_data)

        team2_analysis = {
            "analista":  state.get("analista_output", {}).get("analysis", ""),
            "tecnico":   state.get("tecnico_output", {}).get("analysis", ""),
            "estratega": state.get("estratega_output", {}).get("program", ""),
        }

        logger.info("[Orchestrator] Launching 2 content specialists in parallel (threads)...")
        start_time = asyncio.get_event_loop().time()

        results = await asyncio.gather(
            asyncio.to_thread(_agent_thread_runner, AgentUXWriter, 'write', state["user_id"], dashboard_data=dashboard_data),
            asyncio.to_thread(_agent_thread_runner, AgentCoach,    'coach', state["user_id"], dashboard_data=agent_data, team2_analysis=team2_analysis),
            return_exceptions=True,
        )

        elapsed = asyncio.get_event_loop().time() - start_time
        ux_writer_result, coach_result = results

        errors = []
        if isinstance(ux_writer_result, Exception):
            errors.append(f"AgentUXWriter: {ux_writer_result}")
        else:
            state["ux_writer_output"] = ux_writer_result
            content_len = len(json.dumps(ux_writer_result.get("content", {})))
            logger.info(f"   OK AgentUXWriter: {content_len} chars")

        if isinstance(coach_result, Exception):
            errors.append(f"AgentCoach: {coach_result}")
        else:
            state["coach_output"] = coach_result
            logger.info(f"   OK AgentCoach: {coach_result['metadata']['report_length']} chars")

        logger.info(f"[Orchestrator] TEAM 3 completed in {elapsed:.1f}s")

        if errors:
            state["error"] = "; ".join(errors)
            logger.error(f"[Orchestrator] Team 3 errors: {state['error']}")

    except Exception as e:
        logger.error(f"[Orchestrator] Team 3 error: {e}")
        state["error"] = f"Team 3 error: {e}"

    return state


# ══════════════════════════════════════════════════════════════
# NODO 6: WRITER
# ══════════════════════════════════════════════════════════════

async def writer_node(state: AgentState) -> AgentState:
    """
    Nodo 6: Dashboard Writer Agent.

    Convierte análisis combinado (Team 2) en 3 secciones motivacionales:
    - DNA golfístico
    - Evolución/Progreso
    - Próximo nivel/Acción
    """
    logger.info("[Orchestrator v4.0] Node 6/6: Dashboard Writer")

    if state.get("error"):
        logger.warning("[Orchestrator] Skipping writer due to previous error")
        return state

    try:
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

        if not combined_analysis:
            logger.warning("[Orchestrator] No Team 2 analysis available for writer")
            state["motivational_sections"] = {"dna": "", "progress": "", "action": ""}
            return state

        sections = await dashboard_writer_agent(combined_analysis)
        state["motivational_sections"] = sections
        logger.info(f"[Orchestrator] Writer OK: dna={len(sections['dna'])} | "
                    f"progress={len(sections['progress'])} | action={len(sections['action'])} chars")

    except Exception as e:
        logger.error(f"[Orchestrator] Writer error: {e}")
        state["error"] = f"Writer error: {e}"

    return state


# ══════════════════════════════════════════════════════════════
# GRAFO LANGGRAPH v4.0
# ══════════════════════════════════════════════════════════════

workflow = StateGraph(AgentState)

# Registrar los 6 nodos
workflow.add_node("data_loader",  data_loader_node)   # Nodo 1: carga JSON
workflow.add_node("scoring",      scoring_node)        # Nodo 2: scoring determinista
workflow.add_node("archetype",    archetype_node)      # Nodo 3: golf identity
workflow.add_node("team2",        team2_parallel_node) # Nodo 4: 3 agentes IA paralelos
workflow.add_node("team3",        team3_parallel_node) # Nodo 5: 2 agentes IA paralelos
workflow.add_node("writer",       writer_node)         # Nodo 6: secciones motivacionales

# Flujo secuencial con secciones paralelas internas
workflow.set_entry_point("data_loader")
workflow.add_edge("data_loader", "scoring")
workflow.add_edge("scoring",     "archetype")
workflow.add_edge("archetype",   "team2")
workflow.add_edge("team2",       "team3")
workflow.add_edge("team3",       "writer")
workflow.add_edge("writer",      END)

# Compilar
app = workflow.compile()


# ══════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════

async def run_multi_agent_analysis(user_id: str) -> dict:
    """
    Ejecuta el workflow completo multi-agente v4.0.

    Flujo de 6 nodos:
    1. data_loader  → Carga dashboard_data.json
    2. scoring      → ScoringEngine 8 dimensiones (determinista, < 10ms)
    3. archetype    → ArchetypeClassifier Golf Identity (determinista, < 5ms)
    4. team2        → AgentAnalista + AgentTecnico + AgentEstratega (paralelo)
    5. team3        → AgentUXWriter + AgentCoach (paralelo)
    6. writer       → Secciones motivacionales

    Args:
        user_id: Identificador del usuario (ej: "alvaro")

    Returns:
        dict con todos los outputs del workflow
    """
    logger.info("=" * 70)
    logger.info(f"[Orchestrator v4.0] Starting workflow for user: {user_id}")
    logger.info("=" * 70)

    initial_state = {
        "user_id":              user_id,
        "dashboard_data":       {},
        "scoring_result":       None,
        "archetype_result":     None,
        "analista_output":      {},
        "tecnico_output":       {},
        "estratega_output":     {},
        "ux_writer_output":     {},
        "coach_output":         {},
        "motivational_sections": {},
        "error":                None,
    }

    try:
        final_state = await app.ainvoke(initial_state)

        if final_state.get("error"):
            logger.error(f"[Orchestrator] Workflow error: {final_state['error']}")
        else:
            logger.info("[Orchestrator v4.0] Workflow completed successfully")

            sp = final_state.get("dashboard_data", {}).get("scoring_profile", {})
            gi = final_state.get("dashboard_data", {}).get("golf_identity", {})
            if sp:
                logger.info(f"   Scoring: overall={sp.get('overall_score')}/10")
            if gi:
                logger.info(f"   Identity: {gi.get('archetype_id')} — {gi.get('archetype_name')}")
            logger.info(f"   AgentAnalista:  {len(final_state.get('analista_output', {}).get('analysis', ''))} chars")
            logger.info(f"   AgentTecnico:   {len(final_state.get('tecnico_output', {}).get('analysis', ''))} chars")
            logger.info(f"   AgentEstratega: {len(final_state.get('estratega_output', {}).get('program', ''))} chars")
            logger.info(f"   AgentUXWriter:  {len(json.dumps(final_state.get('ux_writer_output', {}).get('content', {})))} chars")
            logger.info(f"   AgentCoach:     {len(final_state.get('coach_output', {}).get('report', ''))} chars")

        # ── Guardar contenido UXWriter en disco (caché estática) ────────────
        try:
            ux_content = final_state.get("ux_writer_output", {}).get("content", {})
            # Deswrappear raw_content si AgentUXWriter devolvió markdown fences
            if ux_content and ux_content.get("raw_content") and not ux_content.get("hero_statement"):
                raw = ux_content["raw_content"]
                if raw.startswith("```"):
                    raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                ux_content = json.loads(raw)
                logger.info("[Orchestrator] raw_content deswrappeado correctamente")
            if ux_content and ux_content.get("hero_statement"):
                output_path = Path(__file__).parent.parent.parent / "output" / "ai_content.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(ux_content, f, ensure_ascii=False, indent=2)
                logger.info(f"[Orchestrator] ai_content.json guardado ({len(ux_content)} secciones)")
            else:
                logger.warning("[Orchestrator] ux_writer_output vacío o sin hero_statement — ai_content.json no guardado")
        except Exception as e:
            logger.warning(f"[Orchestrator] No se pudo guardar ai_content.json: {e}")
        # ─────────────────────────────────────────────────────────────────────

        return {
            "dashboard_data":       final_state.get("dashboard_data", {}),
            "scoring_result":       final_state.get("scoring_result"),
            "archetype_result":     final_state.get("archetype_result"),
            "analista_output":      final_state.get("analista_output", {}),
            "tecnico_output":       final_state.get("tecnico_output", {}),
            "estratega_output":     final_state.get("estratega_output", {}),
            "ux_writer_output":     final_state.get("ux_writer_output", {}),
            "coach_output":         final_state.get("coach_output", {}),
            "motivational_sections": final_state.get("motivational_sections", {}),
            "error":                final_state.get("error"),
        }

    except Exception as e:
        error_msg = f"Orchestrator critical error: {e}"
        logger.error(f"[Orchestrator] {error_msg}")
        raise Exception(error_msg)


# Export para main.py
__all__ = ["run_multi_agent_analysis", "app"]
