# AlvGolf Agentic Engine - Plan de Implementación TIER 1

**Fecha inicio:** 2026-02-14
**Tiempo estimado:** 3-4 días
**Objetivo:** MVP funcional con FastAPI + RAG + Analytics Pro Agent

---

## 🎯 Objetivo TIER 1

Implementar la infraestructura completa del sistema agentic:
- ✅ Backend FastAPI operacional
- ✅ RAG Core funcional (Pinecone + Claude)
- ✅ Analytics Pro Agent generando análisis
- ✅ 1 sección IA en dashboard

**Sin cambiar el dashboard actual** (trabaja en paralelo)

---

## 📅 Cronograma Detallado

### **DÍA 1: Setup + Backend Base**

#### Fase 0: Pre-requisitos (1-2h)
- [ ] Backup completo con Git
  ```bash
  cd C:\Users\alvar\Documents\AlvGolf
  git add .
  git commit -m "backup: pre-agentic (v5.1.1 stable)"
  git push origin main
  git checkout -b feature/agentic-tier1
  ```
- [ ] Verificar Python 3.11+
  ```bash
  python --version  # Should be 3.11 or higher
  ```
- [ ] Crear cuenta Anthropic
  - URL: https://console.anthropic.com
  - Generar API key
  - Guardar en `.env`
- [ ] Crear cuenta Pinecone
  - URL: https://www.pinecone.io
  - Plan: Starter (free)
  - Crear index: `alvgolf-rag`
  - Generar API key
  - Guardar en `.env`

#### Fase 1: Estructura del Proyecto (1h)
```
AlvGolf/
├── app/                          # ← NUEVO (Backend)
│   ├── __init__.py
│   ├── main.py                   # FastAPI app
│   ├── config.py                 # Environment variables
│   ├── models.py                 # Pydantic models
│   ├── rag.py                    # RAG core
│   └── agents/
│       ├── __init__.py
│       └── analytics_pro.py      # Analytics Pro Agent
├── requirements.txt              # ← NUEVO
├── .env                          # ← NUEVO (gitignored)
├── .gitignore                    # ← ACTUALIZAR
├── dashboard_agentic.html        # ← NUEVO (copia de dashboard_dynamic.html)
├── dashboard_dynamic.html        # ← SIN CAMBIOS
├── dashboard_data.json           # ← SIN CAMBIOS
├── generate_dashboard_data.py   # ← SIN CAMBIOS
└── [resto sin cambios]
```

Tareas:
- [ ] Crear carpeta `app/`
- [ ] Crear `requirements.txt`
- [ ] Crear `.env` template
- [ ] Actualizar `.gitignore`
- [ ] Copiar `dashboard_dynamic.html` → `dashboard_agentic.html`

#### Fase 2: Dependencias (30min)
```bash
# requirements.txt
fastapi==0.110.0
uvicorn[standard]==0.27.1
anthropic==0.18.1
langchain-anthropic==0.2.1
langchain-community==0.2.16
langchain-pinecone==0.2.0
pinecone-client==3.0.3
sentence-transformers==2.3.1
pydantic==2.6.1
pydantic-settings==2.1.0
python-dotenv==1.0.0
loguru==0.7.2
```

Instalación:
```bash
cd C:\Users\alvar\Documents\AlvGolf
pip install -r requirements.txt
```

Verificación:
```bash
python -c "import fastapi; import anthropic; import pinecone; print('✅ All deps installed')"
```

#### Fase 3: Configuración (.env) (15min)
```bash
# .env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
PINECONE_API_KEY=pcxxxxxxxxxxxxxxx
PINECONE_INDEX_NAME=alvgolf-rag
PINECONE_ENVIRONMENT=us-east-1
ENV=local
```

- [ ] Copiar API keys
- [ ] Verificar sintaxis
- [ ] Añadir `.env` a `.gitignore`

#### Fase 4: FastAPI Skeleton (2h)
```python
# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.models import HealthResponse, IngestRequest, QueryRequest, AnalyzeRequest
from app.rag import ingest_shots, rag_answer
from app.agents.analytics_pro import analytics_agent

# Logging
logger.remove()
logger.add(sys.stdout, level="INFO")

# FastAPI app
app = FastAPI(
    title="AlvGolf Agentic API",
    version="1.0.0",
    description="Backend for AlvGolf Agentic Analytics Engine"
)

# CORS (permite requests desde localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "message": "AlvGolf Agentic API is running"
    }

@app.post("/ingest")
async def ingest_data(request: IngestRequest):
    """Ingest shots data to Pinecone"""
    try:
        count = ingest_shots(request.user_id, request.shots)
        logger.info(f"Ingested {count} chunks for user {request.user_id}")
        return {"status": "ok", "chunks_ingested": count}
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_rag(request: QueryRequest):
    """Query RAG for information"""
    try:
        answer = rag_answer(request.user_id, request.prompt)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_golf(request: AnalyzeRequest):
    """Analyze golf performance with Analytics Pro Agent"""
    try:
        analysis = await analytics_agent(request.user_id)
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Tareas:
- [ ] Implementar skeleton
- [ ] Probar `GET /` → debe retornar health check
- [ ] Documentar en README

---

### **DÍA 2: RAG Core + Ingesta Inicial**

#### Fase 5: RAG Core (3h)
```python
# app/rag.py
import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_anthropic import ChatAnthropic
from app.models import ShotData

# Config
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Pinecone init
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(PINECONE_INDEX_NAME)

# Embeddings (local, free)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# LLM (Claude)
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=ANTHROPIC_API_KEY,
    temperature=0.1,
    max_tokens=2000
)

def _shot_to_text(user_id: str, shot: ShotData) -> str:
    """Convert ShotData to text for vectorization"""
    return (
        f"User: {user_id} | Date: {shot.date} | Source: {shot.source} | "
        f"Club: {shot.club} | Hole: {shot.hole} | "
        f"BallSpeed: {shot.ball_speed} | Carry: {shot.carry} | "
        f"Launch: {shot.launch_angle} | FaceToPath: {shot.face_to_path} | "
        f"Score: {shot.score} | Notes: {shot.notes}"
    )

def ingest_shots(user_id: str, shots: List[ShotData]) -> int:
    """Ingest shots to Pinecone"""
    texts = [_shot_to_text(user_id, s) for s in shots]
    metadatas = [
        {"user_id": user_id, "date": s.date, "source": s.source}
        for s in shots
    ]

    vectorstore = PineconeVectorStore.from_texts(
        texts=texts,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME,
        metadatas=metadatas,
        namespace=user_id
    )

    return len(texts)

def rag_answer(user_id: str, prompt: str) -> str:
    """Answer question using RAG"""
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
        namespace=user_id
    )

    # Retrieve
    docs = vectorstore.similarity_search(prompt, k=5)
    context = "\n".join([d.page_content for d in docs])

    # Augment + Generate
    full_prompt = f"""
Eres un analista de golf profesional.

Contexto del jugador:
{context}

Pregunta:
{prompt}

Responde con análisis técnico basado en datos.
    """.strip()

    response = llm.invoke(full_prompt)
    return response.content
```

Tareas:
- [ ] Implementar RAG core
- [ ] Probar embeddings locales
- [ ] Verificar conexión Pinecone
- [ ] Verificar conexión Claude

#### Fase 6: Ingesta Inicial (2h)
Script para convertir `dashboard_data.json` → Pinecone:

```python
# scripts/ingest_initial_data.py
import json
import requests
from app.models import ShotData

# Cargar JSON
with open("output/dashboard_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convertir club_statistics → shots
shots = []
for club in data["club_statistics"]:
    shot = ShotData(
        date="2025-12-31",  # Placeholder (datos agregados)
        source="dashboard_json",
        club=club["palo"],
        hole=0,
        ball_speed=club.get("speed_raw", 0),
        carry=club.get("distance_raw", 0),
        launch_angle=club.get("launch_angle_mean", 0),
        face_to_path=0,  # No disponible en JSON actual
        score=0,
        notes=f"Agregado: {club['n_shots']} shots"
    )
    shots.append(shot)

# Ingestar a Pinecone vía API
response = requests.post(
    "http://localhost:8000/ingest",
    json={"user_id": "alvaro", "shots": [s.dict() for s in shots]}
)

print(response.json())
```

Tareas:
- [ ] Crear script
- [ ] Ejecutar ingesta inicial
- [ ] Verificar en Pinecone UI (11 vectores)
- [ ] Probar query simple: `POST /query`

---

### **DÍA 3: Analytics Pro Agent**

#### Fase 7: System Prompt Engineering (2h)
```python
# app/agents/analytics_pro.py
from langchain_anthropic import ChatAnthropic
from app.rag import rag_answer
import os

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.1,
    max_tokens=2000
)

SYSTEM_PROMPT = """
Eres el Analytics Pro Agent de AlvGolf, especializado en análisis técnico de golf.

Tu misión: Generar un informe estructurado y profesional basado en datos reales del jugador.

Estructura OBLIGATORIA del informe:

## 1. PATRONES TÉCNICOS
- Tendencia de vuelo (slice/hook/straight/fade/draw)
- Face-to-path promedio (valores + interpretación)
- Attack angle tendencia (valores + efecto en distancia)
- Club speed vs PGA Tour (% comparación)

## 2. TENDENCIAS ESTADÍSTICAS
- Evolución distancia últimas 4 semanas (mejora/declive/estable)
- Evolución consistencia (stddev temporal)
- Comparación vs benchmarks (PGA Tour, HCP 15, HCP 23)
- Percentiles destacados (top/bottom)

## 3. GAPS PRINCIPALES
- Top 3 áreas de mejora priorizadas
- Impacto estimado en strokes por área
- Datos específicos que respaldan cada gap

## 4. RECOMENDACIONES
- Drill técnico #1 (más impactante)
- Drill técnico #2 (segundo impacto)
- Cambio mental/estratégico

## 5. PREDICCIÓN
- HCP proyectado a 30 días (con condiciones)
- Score objetivo próxima ronda
- Confianza de la predicción (alta/media/baja)

IMPORTANTE:
- Usa datos numéricos específicos (velocidad, distancia, ángulos)
- Compara siempre vs benchmarks relevantes
- Sé preciso pero accesible (no jerga excesiva)
- Longitud total: 150-200 palabras
""".strip()

async def analytics_agent(user_id: str) -> str:
    """
    Analytics Pro Agent: Análisis técnico profundo.

    Args:
        user_id: Usuario a analizar

    Returns:
        str: Análisis estructurado en formato texto
    """
    # Obtener contexto desde RAG
    context = rag_answer(
        user_id,
        "Dame un resumen completo de mis datos: driver, wedges, HCP, rondas recientes"
    )

    # Prompt completo
    full_prompt = f"""
{SYSTEM_PROMPT}

Datos del jugador (extraídos de base vectorial):
{context}

Genera el análisis siguiendo la estructura de 5 secciones.
    """.strip()

    # Invoke Claude
    response = llm.invoke(full_prompt)

    return response.content
```

Tareas:
- [ ] Implementar agent
- [ ] Probar con datos reales
- [ ] Iterar prompt hasta obtener output deseado
- [ ] Documentar ejemplos de output

#### Fase 8: Testing Backend (1h)
```python
# tests/test_agent.py
import asyncio
from app.agents.analytics_pro import analytics_agent

async def test_analytics():
    result = await analytics_agent("alvaro")
    print("=" * 60)
    print("ANALYTICS PRO OUTPUT:")
    print("=" * 60)
    print(result)
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_analytics())
```

Tareas:
- [ ] Ejecutar test
- [ ] Verificar estructura 5 secciones
- [ ] Verificar datos numéricos correctos
- [ ] Verificar longitud (~150-200 palabras)

---

### **DÍA 4: Integración Dashboard**

#### Fase 9: Dashboard Agentic v1 (3h)
Modificar `dashboard_agentic.html`:

```html
<!-- Después del header, antes de charts -->
<div id="ai-sections-container">
  <!-- SECCIÓN 1: ADN GOLFÍSTICO -->
  <div class="ai-section" id="dna-section">
    <h3>🧠 Tu ADN Golfístico</h3>
    <div id="dna-content" class="ai-content">
      <!-- Loading skeleton -->
      <div class="skeleton-loading">
        <div class="skeleton-title"></div>
        <div class="skeleton-text"></div>
        <div class="skeleton-text"></div>
        <div class="skeleton-text short"></div>
      </div>
    </div>
    <div class="ai-metadata">
      <span>🤖 Generado por Analytics Pro</span>
      <span id="dna-timestamp">🕐 Cargando...</span>
    </div>
  </div>

  <!-- Botón regenerar -->
  <button id="regenerate-btn" class="btn-primary">
    🔄 Regenerar Análisis IA
  </button>
</div>

<style>
/* CSS de DASHBOARD_AI_SECTIONS.md */
.ai-section { /* ... */ }
/* ... resto de estilos ... */
</style>

<script>
// Cargar secciones IA al inicio
document.addEventListener('DOMContentLoaded', async () => {
  await loadAISections();
});

async function loadAISections() {
  try {
    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_id: 'alvaro'})
    });

    if (!response.ok) throw new Error('API error');

    const data = await response.json();
    updateDNASection(data.analysis);

  } catch (error) {
    console.error('Error loading AI sections:', error);
    showErrorState();
  }
}

function updateDNASection(analysis) {
  const content = document.getElementById('dna-content');
  content.innerHTML = `<p>${analysis}</p>`;

  const timestamp = document.getElementById('dna-timestamp');
  timestamp.textContent = `🕐 Actualizado: ${new Date().toLocaleTimeString('es-ES')}`;
}

function showErrorState() {
  const content = document.getElementById('dna-content');
  content.innerHTML = `
    <p style="color: #E88B7A;">
      ❌ Error al cargar análisis IA. Verifica que el backend esté corriendo
      en http://localhost:8000
    </p>
  `;
}

// Botón regenerar
document.getElementById('regenerate-btn').addEventListener('click', async () => {
  const btn = document.getElementById('regenerate-btn');
  btn.disabled = true;
  btn.innerHTML = '⏳ Analizando...';

  await loadAISections();

  btn.innerHTML = '✅ Actualizado';
  setTimeout(() => {
    btn.disabled = false;
    btn.innerHTML = '🔄 Regenerar Análisis IA';
  }, 2000);
});
</script>
```

Tareas:
- [ ] Copiar HTML skeleton
- [ ] Implementar CSS
- [ ] Implementar JavaScript
- [ ] Probar en navegador
- [ ] Verificar loading states
- [ ] Verificar error handling

#### Fase 10: Testing End-to-End (1h)
```bash
# Terminal 1: Backend
cd C:\Users\alvar\Documents\AlvGolf
python -m app.main

# Terminal 2: Dashboard
python start_dashboard_server.py

# Navegador
http://localhost:8001/dashboard_agentic.html
```

Checklist:
- [ ] Backend responde en `localhost:8000`
- [ ] Dashboard carga en `localhost:8001`
- [ ] Sección IA se genera automáticamente
- [ ] Botón "Regenerar" funciona
- [ ] Loading skeleton aparece
- [ ] Error handling funciona (apagar backend y probar)
- [ ] Charts estáticos siguen funcionando

---

## 📊 Métricas de Éxito TIER 1

Al final del Día 4, debes tener:

### Backend
- [x] FastAPI corriendo en localhost:8000
- [x] 4 endpoints funcionales (/, /ingest, /query, /analyze)
- [x] Pinecone con 11+ vectores ingresados
- [x] Claude respondiendo análisis técnicos
- [x] Logs claros en terminal
- [x] 0 errores críticos

### Frontend
- [x] dashboard_agentic.html accesible
- [x] Sección "ADN Golfístico" renderizada
- [x] Análisis IA personalizado visible
- [x] Botón regenerar funcional
- [x] Loading states elegantes
- [x] Charts estáticos intactos
- [x] 0 errores en consola navegador

### Calidad
- [x] Código comentado y limpio
- [x] README actualizado con instrucciones
- [x] Git commits incrementales
- [x] .env no committed
- [x] Dashboard original sin cambios

---

## 🐛 Troubleshooting Común

### Error: "Module 'app' not found"
```bash
# Solución: Ejecutar desde raíz del proyecto
cd C:\Users\alvar\Documents\AlvGolf
python -m app.main
```

### Error: "Pinecone index not found"
```bash
# Solución: Crear index en Pinecone UI
# Name: alvgolf-rag
# Dimension: 384 (all-MiniLM-L6-v2)
# Metric: cosine
```

### Error: "CORS policy blocked"
```python
# Solución: Verificar CORS en main.py
allow_origins=["http://localhost:8000", "http://localhost:8001"]
```

### Error: "Claude API rate limit"
```python
# Solución: Añadir retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_claude():
    return llm.invoke(prompt)
```

---

## 💰 Costos Estimados TIER 1 Development

### Durante desarrollo (Día 1-4)
- Llamadas testing: ~50 requests
- Tokens por request: ~3,000 (input + output)
- Total tokens: 150,000
- Costo: 150K × $3/1M = **€0.42**

### Post-desarrollo (uso normal)
- Análisis/día: 1-2
- Análisis/mes: 30-60
- Costo mensual: **€0.38** (con caching)

**Total TIER 1:** €0.42 (dev) + €0.38/mes (uso) = **€0.80 primer mes**

---

## ✅ Checklist Final TIER 1

Antes de considerar TIER 1 completado:

- [ ] Backend corriendo sin errores
- [ ] RAG ingesta datos correctamente
- [ ] Analytics Pro genera análisis coherentes
- [ ] Dashboard muestra sección IA
- [ ] Botón regenerar funciona
- [ ] Dashboard original intacto
- [ ] Git branch limpio
- [ ] Documentación actualizada
- [ ] README con instrucciones claras
- [ ] .env.example creado
- [ ] Costos monitoreados
- [ ] Screenshots del resultado
- [ ] Commit final con tag: `v1.0-tier1`

```bash
git add .
git commit -m "feat: TIER 1 complete - FastAPI + RAG + Analytics Pro"
git tag v1.0-tier1
git push origin feature/agentic-tier1 --tags
```

---

## 🚀 Próximos Pasos (Post-TIER 1)

Una vez TIER 1 esté completo y probado:

1. **Pausa de 1-2 días**
   - Usar el sistema
   - Identificar mejoras
   - Decidir si continuar a TIER 2

2. **Si continúas a TIER 2:**
   - Añadir Dashboard Writer Agent
   - Implementar LangGraph orchestration
   - Dinamizar 2 secciones adicionales

3. **Si te quedas en TIER 1:**
   - Merge a main branch
   - Deploy local permanente
   - Monitorear costos

---

**Última actualización:** 2026-02-14
**Autor:** Claude Code Assistant
**Status:** ✅ Plan detallado listo para ejecución
