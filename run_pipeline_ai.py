"""
run_pipeline_ai.py — Generador de contenido IA para AlvGolf Dashboard

Ejecuta AgentUXWriter + AgentCoach en PARALELO REAL y guarda el resultado en
output/ai_content.json para carga instantánea desde el dashboard (GitHub Pages).

Paralelismo real con asyncio.to_thread():
    Los agentes usan llm.invoke() síncrono internamente. asyncio.gather() solo
    no basta — se necesita asyncio.to_thread() para mover cada agente a su propio
    thread del pool del SO, permitiendo verdadero paralelismo I/O.
    Resultado: max(t_uxwriter, t_coach) en lugar de t_uxwriter + t_coach.

Flujo completo recomendado:
    1. python generate_dashboard_data.py   → output/dashboard_data.json  (~3s)
    2. python run_pipeline_ai.py           → output/ai_content.json      (~2 min)
    3. git add output/ && git commit && git push

El dashboard carga ambos archivos estáticamente. Sin servidor. Sin esperas.

Requisitos:
    - output/dashboard_data.json debe existir
    - Variables de entorno: ANTHROPIC_API_KEY (en .env)

Salida (output/ai_content.json):
    hero_statement     — 50-80 palabras, Tab 1
    dna_profile        — 30-50 palabras, Tab 1
    chart_titles       — objeto con títulos/subtítulos de gráficas
    insight_boxes      — array, Tab 5 Análisis Profundo
    quick_wins         — array, Tab 6 Estrategia
    roi_cards          — array, Tab 6 Estrategia
    coach_report       — Markdown completo (~1,500 palabras), PDF Coach
    generated_at       — ISO timestamp
    dashboard_version  — versión de dashboard_data.json para trazabilidad
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Cargar .env (ANTHROPIC_API_KEY, etc.)
load_dotenv()

# ── Configuración de logging ──────────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
)

# ── Rutas ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT    = Path(__file__).parent
DASHBOARD_JSON  = PROJECT_ROOT / "output" / "dashboard_data.json"
AI_CONTENT_JSON = PROJECT_ROOT / "output" / "ai_content.json"
USER_ID         = "alvaro"

# ── Blacklist: claves de pura visualización UI, sin valor analítico para LLMs ─
UI_ONLY_KEYS = frozenset({
    'shot_zones_heatmap',      # 21.4 KB — grid de coords XY crudas para Chart.js heatmap
    'dispersion_by_club',      # 11.8 KB — scatter plots crudos por palo (Chart.js)
    'metadata',                #  3.6 KB — versión, timestamps, config del generador
    'generated_at',            #  0.0 KB — timestamp de generación
    'scoring_zones_by_course', #  0.0 KB — datos vacíos de zonas por campo
})


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_dashboard_data() -> dict:
    """Carga dashboard_data.json. Lanza excepción si no existe."""
    if not DASHBOARD_JSON.exists():
        raise FileNotFoundError(
            f"No se encontró: {DASHBOARD_JSON}\n"
            "Ejecuta primero: python generate_dashboard_data.py"
        )
    with open(DASHBOARD_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    size_kb = DASHBOARD_JSON.stat().st_size / 1024
    version = data.get("metadata", {}).get("version", "desconocida")
    logger.info(f"dashboard_data.json cargado ({size_kb:.1f} KB, {len(data)} claves, v{version})")
    return data


def deswrap_ux_content(raw: dict) -> dict:
    """Desenvuelve raw_content si AgentUXWriter devolvió markdown fences."""
    if raw.get("raw_content") and not raw.get("hero_statement"):
        text = raw["raw_content"]
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        unwrapped = json.loads(text)
        logger.info("UXWriter: raw_content deswrappeado correctamente")
        return unwrapped
    return raw


# ── Wrappers síncronos para asyncio.to_thread() ───────────────────────────────
# llm.invoke() es bloqueante. Cada wrapper corre en su propio thread con
# un event loop dedicado, liberando el event loop principal para paralelizar.

def _ux_writer_sync(dashboard_data: dict) -> dict:
    """Wrapper síncrono de AgentUXWriter — se ejecuta en thread del pool."""
    import asyncio as _asyncio
    from app.agents.ux_writer import AgentUXWriter
    loop = _asyncio.new_event_loop()
    _asyncio.set_event_loop(loop)
    try:
        agent = AgentUXWriter()
        return loop.run_until_complete(agent.write(USER_ID, dashboard_data=dashboard_data))
    finally:
        loop.close()


def _coach_sync(dashboard_data: dict) -> dict:
    """Wrapper síncrono de AgentCoach — se ejecuta en thread del pool."""
    import asyncio as _asyncio
    from app.agents.coach import AgentCoach
    loop = _asyncio.new_event_loop()
    _asyncio.set_event_loop(loop)
    try:
        # Filtrar claves UI antes de pasar a Coach (~36.8 KB menos)
        agent_data = {k: v for k, v in dashboard_data.items() if k not in UI_ONLY_KEYS}
        agent = AgentCoach()
        return loop.run_until_complete(agent.coach(
            USER_ID,
            dashboard_data=agent_data,
            team2_analysis={}   # Standalone: sin contexto de Team 2
        ))
    finally:
        loop.close()


# ── Agentes (async — delegan al thread pool) ──────────────────────────────────

async def run_ux_writer(dashboard_data: dict) -> dict:
    """Ejecuta AgentUXWriter en un thread dedicado y devuelve 6 secciones JSON."""
    logger.info("AgentUXWriter iniciado (thread)...")
    t0 = datetime.now()

    result = await asyncio.to_thread(_ux_writer_sync, dashboard_data)

    content = deswrap_ux_content(result["content"])
    elapsed = (datetime.now() - t0).seconds
    logger.success(f"AgentUXWriter completado en {elapsed}s ({len(content)} secciones)")
    return content


async def run_coach(dashboard_data: dict) -> str:
    """Ejecuta AgentCoach en un thread dedicado y devuelve el informe Markdown."""
    logger.info("AgentCoach iniciado (thread)...")
    t0 = datetime.now()

    result = await asyncio.to_thread(_coach_sync, dashboard_data)

    report = result["report"]
    elapsed = (datetime.now() - t0).seconds
    chars = result["metadata"].get("report_length", len(report))
    logger.success(f"AgentCoach completado en {elapsed}s ({chars} chars)")
    return report


# ── Pipeline ──────────────────────────────────────────────────────────────────

async def run_pipeline(dashboard_data: dict) -> dict:
    """Ejecuta UXWriter + Coach en PARALELO y combina los resultados."""
    logger.info("Lanzando AgentUXWriter + AgentCoach en paralelo...")
    t0 = datetime.now()

    ux_content, coach_report = await asyncio.gather(
        run_ux_writer(dashboard_data),
        run_coach(dashboard_data)
    )

    elapsed = (datetime.now() - t0).seconds
    logger.info(f"Ambos agentes completados en {elapsed}s total")

    # Combinar en un único JSON con metadatos
    ai_content = {
        **ux_content,                                                      # 6 secciones UXWriter
        "coach_report":      coach_report,                                 # Informe Markdown completo
        "generated_at":      datetime.now().isoformat(timespec="seconds"), # Timestamp generación
        "dashboard_version": dashboard_data.get("metadata", {}).get("version", "unknown")
    }
    return ai_content


def save_ai_content(ai_content: dict) -> None:
    """Guarda output/ai_content.json."""
    AI_CONTENT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(AI_CONTENT_JSON, "w", encoding="utf-8") as f:
        json.dump(ai_content, f, ensure_ascii=False, indent=2)
    size_kb = AI_CONTENT_JSON.stat().st_size / 1024
    logger.success(f"ai_content.json guardado ({size_kb:.1f} KB, {len(ai_content)} campos)")
    logger.info(f"  Ruta: {AI_CONTENT_JSON}")


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    logger.info("=" * 60)
    logger.info("AlvGolf — Pipeline IA (UXWriter + Coach)")
    logger.info("Salida: output/ai_content.json")
    logger.info("=" * 60)

    try:
        dashboard_data = load_dashboard_data()
        ai_content = await run_pipeline(dashboard_data)
        save_ai_content(ai_content)

        logger.info("=" * 60)
        logger.success("PIPELINE COMPLETADO EXITOSAMENTE")
        logger.info(f"Campos: {list(ai_content.keys())}")
        logger.info("")
        logger.info("Siguiente paso:")
        logger.info("  git add output/ai_content.json")
        logger.info("  git commit -m 'feat(data): regenerar ai_content.json'")
        logger.info("  git push")
        logger.info("=" * 60)

    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error en el pipeline: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
