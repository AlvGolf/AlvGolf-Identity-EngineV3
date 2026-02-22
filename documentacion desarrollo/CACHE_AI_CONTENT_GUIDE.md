# AlvGolf — Implementación Cache Estática de Contenido IA

## Objetivo

Cambiar el sistema actual donde la IA genera contenido cuando el usuario carga la página (70s de espera), por un sistema donde la IA genera el contenido al procesar datos nuevos y lo guarda en disco. El dashboard lo lee instantáneamente al cargar.

**Resultado final:** El usuario abre el dashboard y ve todo — gráficos + textos IA — de golpe, sin spinners, sin esperas.

---

## Flujo resultante

```
CUANDO HAY DATOS NUEVOS (ejecutado manualmente):
  python generate_dashboard_data.py    → escribe output/dashboard_data.json
  curl POST /analyze                   → corre los 5 agentes → escribe output/ai_content.json

CUANDO EL USUARIO ABRE EL DASHBOARD:
  fetch output/dashboard_data.json  ─┐
  fetch output/ai_content.json      ─┴→ render completo, todo visible de golpe
```

---

## Los 3 cambios necesarios

---

### CAMBIO 1 — `app/agents/orchestrator.py`

**Qué hace ahora:** Al terminar el workflow, devuelve los resultados como respuesta de API. El contenido IA vive en memoria y desaparece.

**Qué queremos:** Al terminar el workflow, guardar el output de `AgentUXWriter` en `output/ai_content.json`.

**Dónde exactamente:** Al final de la función `run_multi_agent_analysis()`, justo antes del `return final_state`.

**Código a añadir:**

```python
# Guardar contenido UXWriter en disco (cache estática)
ux_content = final_state.get("ux_writer_output", {}).get("content", {})
if ux_content:
    project_root = Path(__file__).parent.parent.parent
    output_path = project_root / "output" / "ai_content.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ux_content, f, ensure_ascii=False, indent=2)
    logger.info(f"[Orchestrator] ai_content.json saved to {output_path}")
else:
    logger.warning("[Orchestrator] ux_writer_output empty — ai_content.json not saved")
```

**Verificar que `Path` está importado** al principio del archivo:
```python
from pathlib import Path
```
Si ya está importado, no añadir de nuevo.

---

### CAMBIO 2 — `dashboard_dynamic.html`

**Qué hace ahora:** Al cargar la página, JS llama `loadUXContent()` que hace `POST /generate-content` y espera 60-70 segundos.

**Qué queremos:** Al cargar la página, hacer `fetch('output/ai_content.json')` junto con `dashboard_data.json`. Instantáneo.

#### Paso 2a — Eliminar la llamada async actual

Buscar en el JS cualquiera de estas formas:
```javascript
loadUXContent()
// o
fetch('/generate-content', { method: 'POST' ... })
// o
setTimeout(() => loadUXContent(), ...)
```
**Eliminar o comentar** esa llamada. La función `insertUXContent()` puede quedarse — solo hay que cambiar cuándo y cómo se llama.

#### Paso 2b — Añadir fetch del JSON cacheado

Encontrar la función principal de inicialización del dashboard (probablemente se llama `loadDashboard()`, `initDashboard()` o similar, donde ya se hace `fetch('output/dashboard_data.json')`).

Modificarla para cargar también `ai_content.json` en paralelo:

```javascript
async function loadDashboard() {
    // --- Carga de datos existente (no tocar) ---
    const dataResponse = await fetch('output/dashboard_data.json');
    const dashboardData = await dataResponse.json();

    // --- NUEVO: carga de contenido IA cacheado ---
    let aiContent = null;
    try {
        const aiResponse = await fetch('output/ai_content.json');
        if (aiResponse.ok) {
            aiContent = await aiResponse.json();
            console.log('AI content loaded from cache');
        }
    } catch (e) {
        console.log('ai_content.json no disponible — dashboard funciona sin contenido IA');
    }

    // --- Renderizar gráficos (igual que antes, no tocar) ---
    renderCharts(dashboardData);

    // --- NUEVO: insertar contenido IA inmediatamente si está disponible ---
    if (aiContent) {
        insertUXContent(aiContent);
    }
}
```

> **Importante:** El `try/catch` es esencial. Si `ai_content.json` no existe todavía (primera vez antes de correr los agentes), el dashboard sigue funcionando perfectamente sin contenido IA. No hay errores, no hay pantallas rotas.

---

### CAMBIO 3 — `main.py` (FastAPI)

**Qué hacer:** Nada funcional. El endpoint `/generate-content` puede quedarse en el código — no rompe nada y puede ser útil para tests manuales. Solo añadir un comentario para dejar claro que ya no lo llama el frontend:

```python
@app.post("/generate-content")
async def generate_content(request: ContentRequest):
    # NOTA: Este endpoint ya no se llama desde el dashboard.
    # El contenido UXWriter se genera vía POST /analyze
    # y se cachea automáticamente en output/ai_content.json
    # Se mantiene disponible para uso manual / testing.
    ...
```

---

## Orden de ejecución para implementar

1. Editar `orchestrator.py` — añadir el bloque de guardado del JSON
2. Correr el workflow manualmente: `curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{"user_id": "alvaro"}'`
3. Verificar que `output/ai_content.json` se ha creado y tiene contenido
4. Editar `dashboard_dynamic.html` — reemplazar la llamada async por el fetch del JSON
5. Abrir el dashboard y comprobar que el contenido IA aparece desde el primer instante
6. Añadir comentario en `main.py` (opcional)

---

## Qué NO tocar

- La función `insertUXContent()` y toda su lógica de DOM — queda exactamente igual
- El renderizado de gráficos — queda exactamente igual
- La estructura del `ai_content.json` — es el mismo JSON que ya genera `AgentUXWriter`
- El endpoint `/analyze` — sigue funcionando igual, solo añadimos el guardado del JSON al final

---

## Prompt para Claude Code

Copiar y pegar este prompt directamente en Claude Code:

```
I need to implement a static cache system for AI-generated content in the AlvGolf dashboard.

CONTEXT:
- Python/FastAPI backend with LangGraph multi-agent system (5 agents)
- Orchestrator file: app/agents/orchestrator.py
- Main async function: run_multi_agent_analysis(user_id: str) -> dict
- This function returns final_state dict which contains ux_writer_output.content (the AI content)
- Frontend: dashboard_dynamic.html (single HTML file with embedded JS)
- Data files served from output/ directory: output/dashboard_data.json
- FastAPI main file: main.py

CURRENT BEHAVIOR (what exists now):
- Dashboard loads → JS calls POST /generate-content → waits 60-70s → AI content appears dynamically
- AI content is lost after each request (lives in memory only, never saved to disk)

DESIRED BEHAVIOR (what we want):
- When POST /analyze is called → agents run → UXWriter output is saved to output/ai_content.json automatically
- Dashboard loads → fetches output/ai_content.json instantly alongside dashboard_data.json → all content visible immediately with zero wait
- No API calls from the dashboard to generate content at load time

CHANGE 1 — app/agents/orchestrator.py:
At the very end of the run_multi_agent_analysis() function, just before the return statement, add code to:
- Extract ux_content from final_state["ux_writer_output"]["content"]
- If ux_content is not empty, save it to output/ai_content.json using json.dump with ensure_ascii=False and indent=2
- project_root = Path(__file__).parent.parent.parent
- output_path = project_root / "output" / "ai_content.json"
- Log success or warning using the existing logger
- Make sure Path is imported (it likely already is)

CHANGE 2 — dashboard_dynamic.html:
- Find the loadUXContent() function or any fetch('/generate-content') call and remove/disable it
- Find the main dashboard initialization function where fetch('output/dashboard_data.json') is called
- Add a parallel fetch of 'output/ai_content.json' wrapped in try/catch (so dashboard works gracefully if file doesn't exist yet)
- If ai_content.json loads successfully, call insertUXContent(aiContent) immediately after renderCharts()
- Do NOT modify insertUXContent() itself — only change when it's called and how the data is passed to it
- Remove any loading spinners or "AI content loading" messages related to the old async flow

CHANGE 3 — main.py:
- Add a comment to the /generate-content endpoint explaining it's no longer called from the frontend
- No functional changes needed

IMPORTANT CONSTRAINTS:
- Dashboard must work fully if ai_content.json doesn't exist yet (graceful degradation)
- The fetch of ai_content.json should not block chart rendering
- All existing insertUXContent() DOM manipulation logic stays exactly the same
- Do not change the structure of what AgentUXWriter outputs — it's already correct JSON

After making changes, confirm:
1. What exact lines were added to orchestrator.py
2. What was changed in dashboard_dynamic.html
3. How to verify the cache is working (what to check in output/ directory)
```
