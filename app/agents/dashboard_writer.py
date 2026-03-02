"""
Dashboard Writer Agent - TIER 2

Convierte análisis técnico en texto motivacional e inspiracional.

Input: Análisis técnico de Analytics Pro (5 secciones)
Output: 3 secciones motivacionales (DNA, PROGRESS, ACTION)
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents import extract_cache_usage
import os
import json
from loguru import logger

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.3,  # Más creatividad que Analytics Pro
    max_tokens=1500,
    default_headers={
        "anthropic-beta": "prompt-caching-2024-07-31"
    }
)

SYSTEM_PROMPT = """
Eres el Dashboard Writer Agent de AlvGolf.

Tu misión: Transformar análisis técnico de golf en texto inspiracional y motivador.

INPUT: Recibes análisis técnico con datos (velocidades, ángulos, distancias, etc.)
OUTPUT: 3 secciones motivacionales para el dashboard del jugador

## ESTRUCTURA OBLIGATORIA:

### 1. TU ADN GOLFÍSTICO 🧬 (60-80 palabras)
- Resalta la IDENTIDAD única del jugador
- Celebra fortalezas con datos específicos
- Tono: Inspiracional, positivo, personal
- Ejemplo: "Tu short game es tu superpoder - con un 95% percentil estás entre los
  mejores. Tu driver a 240m te coloca en el top 20% de tu categoría..."

### 2. TU EVOLUCIÓN 📈 (50-70 palabras)
- Destaca PROGRESO reciente con métricas
- Muestra tendencia positiva
- Tono: Celebratorio pero realista
- Ejemplo: "En las últimas 4 semanas has mejorado 2.3 puntos de HCP. Tu consistencia
  ha aumentado un 18% y tu score promedio bajó de 102 a 98..."

### 3. TU PRÓXIMO NIVEL 🎯 (70-90 palabras)
- ACCIONABLE: 2-3 pasos concretos
- Vincula acción con impacto esperado
- Tono: Empoderador, claro, optimista
- Ejemplo: "Tu camino al HCP 20 tiene 3 pilares: 1) Mejora tu driver +15m (drill:
  tempo 3:1) → -2 strokes/ronda. 2) Approach consistency → -1.5 strokes. 3) Mental
  game en presión → -1 stroke. Total potencial: -4.5 strokes en 8 semanas."

## REGLAS ESTRICTAS:
- NO uses jerga técnica (face-to-path, attack angle, etc.)
- SÍ usa datos específicos pero traducidos (ej: "240m" no "165 mph ball speed")
- NO seas genérico ("sigue practicando" ❌)
- SÍ sé específico ("practica wedges 50-75m" ✅)
- Tono: TÚ (segunda persona), cercano, motivador
- Longitud total: 180-240 palabras (60-80 por sección)

## EJEMPLOS DE BUEN TONO:
✅ "Tu progreso es impresionante"
✅ "Eres top 20% en tu categoría"
✅ "Tu siguiente objetivo está a 8 semanas"
✅ "Este drill te dará +15m inmediatos"

## EJEMPLOS DE MAL TONO:
❌ "Deberías mejorar tu swing"
❌ "El análisis muestra deficiencias"
❌ "Requiere trabajo técnico avanzado"
❌ "Face-to-path de +3.2 grados"
""".strip()

async def dashboard_writer_agent(technical_analysis: str) -> dict:
    """
    Convierte análisis técnico en 3 secciones motivacionales.

    Args:
        technical_analysis: Output de Analytics Pro Agent (5 secciones técnicas)

    Returns:
        {
            "dna": str,       # Sección 1: ADN Golfístico
            "progress": str,  # Sección 2: Evolución
            "action": str     # Sección 3: Próximo Nivel
        }
    """

    logger.info("Dashboard Writer Agent: Starting conversion...")

    messages = [
        SystemMessage(content=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        }]),
        HumanMessage(content=f"""ANÁLISIS TÉCNICO (input):
{technical_analysis}

GENERA LAS 3 SECCIONES MOTIVACIONALES en formato JSON:
{{
    "dna": "texto sección 1...",
    "progress": "texto sección 2...",
    "action": "texto sección 3..."
}}

IMPORTANTE: Responde SOLO con el JSON, sin explicaciones adicionales.""")
    ]

    try:
        response = llm.invoke(messages)
        extract_cache_usage(response, "DashboardWriter")
        content = response.content.strip()

        logger.info(f"Dashboard Writer: Received response ({len(content)} chars)")

        # Parse JSON
        # Extraer JSON si viene envuelto en ```json
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        sections = json.loads(content)

        # Validar claves
        required_keys = ["dna", "progress", "action"]
        if not all(k in sections for k in required_keys):
            raise ValueError(f"Missing keys. Expected: {required_keys}, Got: {list(sections.keys())}")

        logger.info("Dashboard Writer: JSON parsed successfully")
        logger.info(f"  - DNA: {len(sections['dna'])} chars")
        logger.info(f"  - Progress: {len(sections['progress'])} chars")
        logger.info(f"  - Action: {len(sections['action'])} chars")

        return sections

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        logger.error(f"Content received: {content[:200]}...")

        # Fallback: Return error-friendly sections
        return {
            "dna": "🧬 Análisis técnico disponible. Regenera para ver versión motivacional.",
            "progress": "📈 Evolución en progreso. Regenera para actualizar.",
            "action": "🎯 Próximos pasos calculándose. Regenera para ver plan de acción."
        }

    except Exception as e:
        logger.error(f"Dashboard Writer error: {e}")
        raise
