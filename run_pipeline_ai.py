"""
run_pipeline_ai.py — Generador de contenido IA para AlvGolf Dashboard

Ejecuta AgentUXWriter + AgentCoach en PARALELO y guarda el resultado en
output/ai_content.json para carga instantánea desde el dashboard (GitHub Pages).

Flujo completo recomendado:
    1. python generate_dashboard_data.py   → output/dashboard_data.json  (~3s)
    2. python run_pipeline_ai.py           → output/ai_content.json      (~2-3 min)
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


# ── Agentes ───────────────────────────────────────────────────────────────────

async def run_ux_writer(dashboard_data: dict) -> dict:
    """Ejecuta AgentUXWriter y devuelve el contenido JSON (6 secciones)."""
    from app.agents.ux_writer import AgentUXWriter
    logger.info("AgentUXWriter iniciado...")
    t0 = datetime.now()

    agent = AgentUXWriter()
    result = await agent.write(USER_ID, dashboard_data=dashboard_data)

    content = deswrap_ux_content(result["content"])
    elapsed = (datetime.now() - t0).seconds
    secciones = list(content.keys())
    logger.success(f"AgentUXWriter completado en {elapsed}s ({len(secciones)} secciones)")
    return content


async def run_coach(dashboard_data: dict) -> str:
    """Ejecuta AgentCoach standalone y devuelve el informe Markdown."""
    from app.agents.coach import AgentCoach
    logger.info("AgentCoach iniciado...")
    t0 = datetime.now()

    agent = AgentCoach()
    result = await agent.coach(
        USER_ID,
        dashboard_data=dashboard_data,
        team2_analysis={}   # Standalone: sin contexto de Team 2
    )

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
