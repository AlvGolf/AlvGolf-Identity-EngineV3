# AlvGolf v3.0.1 — Referencia Visual Completa

**Versión:** 3.0.1 · **Fecha:** 2026-02-20 · **Estado:** ✅ Producción Estable

> Todos los diagramas del proyecto en un único archivo.
> GitHub renderiza Mermaid automáticamente. También funciona en VS Code con la extensión *Markdown Preview Mermaid Support*.

---

## Índice

| # | Sección | Tema |
|---|---------|------|
| [1](#1-arquitectura-completa-del-sistema) | Arquitectura Completa | Sistema end-to-end v3.0.1 |
| [2](#2-flujo-multi-agente) | Flujo Multi-Agente | Orquestación LangGraph, Teams 2 y 3 |
| [3](#3-integración-uxwriter--dashboard) | Integración UXWriter | Sequence + States del contenido IA |
| [4](#4-api-y-endpoints) | API y Endpoints | FastAPI, rutas, dependencias |
| [5](#5-backend-etl--flujo-de-datos) | Backend ETL | Flujo simplificado, funciones, dependencias |
| [6](#6-frontend-dashboard) | Frontend Dashboard | Inicialización de charts, safety pattern, error handling |
| [7](#7-deployment) | Deployment | Arquitectura local y GitHub Pages |
| [8](#8-performance-y-costos) | Performance y Costos | Métricas ETL, multi-agent, costos Claude |
| [9](#9-timeline-del-proyecto) | Timeline Sprints | Gantt Fase 1, 2 y 3 completo |
| [10](#10-troubleshooting-y-acceso) | Troubleshooting y Acceso | CORS, árbol de decisión de acceso |

---

## 1. Arquitectura Completa del Sistema

> *Fuente: `ARCHITECTURE_DIAGRAMS.md` — Diagrama 1*

```mermaid
graph TB
    subgraph "User Layer"
        U[Usuario / Browser]
    end

    subgraph "Frontend Layer"
        FD[dashboard_dynamic.html<br/>v5.1.1 - 36 Charts + AI Content]
        FA[dashboard_agentic.html<br/>Multi-Agent Insights v3.0]
    end

    subgraph "FastAPI Backend - localhost:8000"
        EP1["GET / (health)"]
        EP2["POST /ingest"]
        EP3["POST /query"]
        EP4["POST /analyze (5 agents)"]
        EP5["POST /generate-content (UXWriter)"]
    end

    subgraph "Multi-Agent Orchestrator (LangGraph)"
        DL[data_loader_node<br/>106.9 KB JSON, 0 RAG]

        subgraph "TEAM 2 - Analytics (Parallel)"
            A1[AgentAnalista<br/>Performance Analysis]
            A2[AgentTecnico<br/>Biomechanics]
            A3[AgentEstratega<br/>Practice Design]
        end

        subgraph "TEAM 3 - Content (Parallel)"
            A4[AgentUXWriter<br/>Dashboard Content]
            A5[AgentCoach<br/>Coaching Reports]
        end

        WR[Dashboard Writer<br/>Motivational Sections]
    end

    subgraph "Data Layer"
        JSON[dashboard_data.json<br/>106.9 KB, 52 keys]
        PC[Pinecone Vector DB<br/>120 vectors]
        RAW[Raw Data<br/>FlightScope 493 shots<br/>Tarjetas 52 rounds]
    end

    subgraph "External Services"
        CLAUDE[Anthropic Claude Sonnet 4<br/>LLM + Prompt Caching]
    end

    U -->|Browse| FD
    U -->|Click IA Insights| FA
    FD -->|"POST /generate-content async"| EP5
    FA -->|"POST /analyze"| EP4

    EP4 --> DL
    EP5 --> A4

    DL -->|"100% data"| A1 & A2 & A3
    A1 & A2 & A3 --> A4 & A5
    A4 & A5 --> WR

    RAW --> JSON
    JSON -->|"fetch() on load"| FD
    JSON --> DL

    A1 & A2 & A3 & A4 & A5 -->|LLM Calls| CLAUDE
    EP2 --> PC
    EP3 --> PC
```

---

## 2. Flujo Multi-Agente

### 2.1 Orquestación por Fases

> *Fuente: `ARCHITECTURE_DIAGRAMS.md` — Diagrama 4*

```mermaid
graph LR
    subgraph "Phase 1: Data Loading (~0.05s)"
        DL[data_loader_node]
        JSON[(dashboard_data.json<br/>106.9 KB)]
        JSON --> DL
    end

    subgraph "Phase 2: Team 2 Analytics (~148s)"
        direction TB
        T2[team2_parallel_node]
        AN[AgentAnalista<br/>6,154 chars]
        TE[AgentTecnico<br/>5,389 chars]
        ES[AgentEstratega<br/>8,857 chars]
        T2 --> AN & TE & ES
    end

    subgraph "Phase 3: Team 3 Content (~156s)"
        direction TB
        T3[team3_parallel_node]
        UX[AgentUXWriter<br/>10,223 chars]
        CO[AgentCoach<br/>9,842 chars]
        T3 --> UX & CO
    end

    subgraph "Phase 4: Output (~13s)"
        WR[writer_node<br/>1,236 chars]
        OUT[Final Output<br/>41,701 chars total]
        WR --> OUT
    end

    DL -->|"100% data"| T2
    T2 -->|"Team 2 analysis"| T3
    T3 -->|"All content"| WR

    style DL fill:#4A9FD8,color:#fff
    style T2 fill:#5ABF8F,color:#fff
    style T3 fill:#D4B55A,color:#000
    style WR fill:#E88B7A,color:#fff
```

### 2.2 Dependencias de Funciones Backend

> *Fuente: `MERMAID_DIAGRAMS.md` — Diagrama 11*

```mermaid
graph TD
    subgraph "Core Data"
        FS_DATA[FlightScope Data<br/>493 shots]
        TR_DATA[Tarjetas Data<br/>52 rounds]
    end

    subgraph "Base Analyzers"
        LAUNCH[LaunchMetricsAnalyzer]
        DISP[DispersionAnalyzer]
        CONS[ConsistencyAnalyzer]
        SCORE[ScoreAnalyzer]
    end

    subgraph "Tier 1 Functions"
        F1[calculate_player_stats]
        F2[calculate_club_statistics]
        F3[calculate_temporal_evolution]
        F4[calculate_course_statistics]
    end

    subgraph "Tier 2 Functions"
        F5[calculate_club_gaps]
        F6[calculate_percentile_gauges]
        F7[calculate_club_distance_comparison]
    end

    subgraph "Tier 3 Functions (advanced)"
        F8[calculate_strokes_gained]
        F9[calculate_quick_wins_matrix]
        F10[calculate_swot_matrix]
        F11[calculate_roi_plan]
    end

    FS_DATA --> LAUNCH --> F1
    FS_DATA --> DISP --> F2
    TR_DATA --> CONS --> F4
    TR_DATA --> SCORE --> F3

    F2 --> F5
    F1 --> F6
    F2 --> F7

    F3 --> F8
    F2 --> F9
    F8 --> F10
    F9 --> F11

    style FS_DATA fill:#E88B7A,stroke:#C86A5A,stroke-width:2px,color:#fff
    style TR_DATA fill:#E88B7A,stroke:#C86A5A,stroke-width:2px,color:#fff
    style F11 fill:#5ABF8F,stroke:#3A7F5F,stroke-width:3px,color:#fff
```

---

## 3. Integración UXWriter → Dashboard

### 3.1 Secuencia de Carga

> *Fuente: `ARCHITECTURE_DIAGRAMS.md` — Diagrama 2*

```mermaid
sequenceDiagram
    participant U as Usuario
    participant FE as dashboard_dynamic.html
    participant API as FastAPI :8000
    participant UXW as AgentUXWriter
    participant CL as Claude Sonnet 4
    participant FS as File System

    Note over FE: Page Load Begins

    FE->>FS: fetch('dashboard_data.json')
    FS-->>FE: 106.9 KB JSON
    FE->>FE: dispatch('dashboardDataReady')
    FE->>FE: Render 36 charts immediately

    Note over FE: Charts visibles (< 1s)

    FE->>API: POST /generate-content {user_id: "alvaro"}
    Note over FE: Non-blocking async call

    API->>FS: Load dashboard_data.json
    FS-->>API: 106.9 KB
    API->>UXW: agent.write(user_id, dashboard_data)
    UXW->>CL: invoke(skill + data context)

    Note over CL: Genera 10 secciones en español (~60-70s)

    CL-->>UXW: JSON content response
    UXW-->>API: content validated
    API-->>FE: ContentGenerateResponse

    FE->>FE: insertUXContent(content)
    FE->>FE: hero_statement → Tab 1
    FE->>FE: dna_profile → Tab 1
    FE->>FE: chart_titles → All tabs
    FE->>FE: quick_wins → Tab 6
    FE->>FE: roi_cards → Tab 6
    FE->>FE: insight_boxes → Tab 5

    Note over FE: AI content aparece ~70s después del load
    FE-->>U: Dashboard completamente mejorado
```

### 3.2 Ciclo de Vida del Contenido IA

> *Fuente: `ARCHITECTURE_DIAGRAMS.md` — Diagrama 3*

```mermaid
stateDiagram-v2
    [*] --> PageLoad: User opens dashboard

    PageLoad --> ChartsReady: dashboard_data.json loaded
    PageLoad --> FetchingAI: POST /generate-content (parallel)

    ChartsReady --> DashboardVisible: 36 charts rendered
    DashboardVisible --> WaitingForAI: User sees charts, AI loading

    FetchingAI --> AgentProcessing: AgentUXWriter invoked
    AgentProcessing --> LLMCall: Claude API call (~60-70s)
    LLMCall --> ContentParsing: JSON response received
    ContentParsing --> ContentReady: 10 sections validated

    FetchingAI --> FetchFailed: Network/API error
    FetchFailed --> GracefulDegradation: Dashboard works without AI

    WaitingForAI --> ContentReady: Content arrives
    ContentReady --> InsertContent: insertUXContent() called

    InsertContent --> HeroInserted: hero_statement Tab 1
    InsertContent --> DNAInserted: dna_profile Tab 1
    InsertContent --> TitlesUpdated: chart_titles all tabs
    InsertContent --> QuickWinsInserted: quick_wins Tab 6
    InsertContent --> ROIInserted: roi_cards Tab 6
    InsertContent --> InsightsInserted: insight_boxes Tab 5

    HeroInserted --> FullyEnhanced
    DNAInserted --> FullyEnhanced
    TitlesUpdated --> FullyEnhanced
    QuickWinsInserted --> FullyEnhanced
    ROIInserted --> FullyEnhanced
    InsightsInserted --> FullyEnhanced

    GracefulDegradation --> DashboardVisible: Static content only
    FullyEnhanced --> [*]: Dashboard complete with AI content
```

---

## 4. API y Endpoints

> *Fuente: `ARCHITECTURE_DIAGRAMS.md` — Diagrama 7*

```mermaid
graph LR
    subgraph "FastAPI Application (localhost:8000)"
        direction TB
        H["GET /<br/>Health Check<br/><100ms"]
        I["POST /ingest<br/>Data Ingestion<br/>~2s"]
        Q["POST /query<br/>RAG Query<br/>10-15s"]
        A["POST /analyze<br/>Full Multi-Agent<br/>~5.3 min"]
        C["POST /generate-content<br/>UXWriter Only<br/>~60-70s"]
    end

    subgraph "Dependencies"
        RAG[RAG Core<br/>Pinecone + Embeddings]
        ORCH[Orchestrator<br/>LangGraph Workflow]
        UXW[AgentUXWriter<br/>Standalone]
    end

    subgraph "Consumers"
        DA[dashboard_agentic.html]
        DD[dashboard_dynamic.html]
        CLI[curl / scripts]
    end

    I --> RAG
    Q --> RAG
    A --> ORCH
    C --> UXW

    DA -->|"/analyze"| A
    DD -->|"/generate-content"| C
    CLI -->|"any endpoint"| H & I & Q & A & C
```

---

## 5. Backend ETL — Flujo de Datos

### 5.1 Flujo Simplificado (visión de usuario)

> *Fuente: `data-flow-simplified.md`*

```mermaid
flowchart LR
    subgraph INPUT["📥 ENTRADA: Tus Datos"]
        EXCEL1[FlightScope Excel<br/>493 shots de práctica<br/>Distancia, velocidad, altura]
        EXCEL2[Tarjetas Excel<br/>52 rondas jugadas<br/>Scores por hoyo]
    end

    subgraph PROCESS["⚙️ PROCESAMIENTO: Motor ETL"]
        ETL[generate_dashboard_data.py v5.1.0<br/><br/>52 funciones de análisis:<br/>Launch metrics · Dispersión<br/>Consistencia · Trends<br/>Motor 10 Dimensiones<br/><br/>⏱️ 3.1 segundos]
    end

    subgraph OUTPUT["📤 SALIDA"]
        JSON[dashboard_data.json<br/>106.9 KB<br/>52 keys]
    end

    subgraph VISUAL["🎨 VISUALIZACIÓN"]
        DASHBOARD[Dashboard HTML v5.1.1<br/>36 visualizaciones dinámicas<br/>6 tabs principales]
    end

    EXCEL1 --> ETL
    EXCEL2 --> ETL
    ETL -->|Genera en 3.1s| JSON
    JSON -->|fetch()| DASHBOARD

    style PROCESS fill:#d4edda,stroke:#28a745,stroke-width:3px
    style OUTPUT fill:#fff3cd,stroke:#ffc107,stroke-width:2px
```

### 5.2 Flujo Multi-Agente IA (extensión opcional)

> *Fuente: `data-flow-simplified.md` — sección v3.0.1*

```mermaid
flowchart LR
    subgraph AI["🤖 FLUJO IA (~70s)"]
        JSON2[dashboard_data.json]
        API[POST /generate-content]
        UXW[AgentUXWriter<br/>10 secciones en español]
        CLAUDE[Claude Sonnet 4<br/>Prompt caching]
        CONTENT[Contenido IA:<br/>hero, dna, titles<br/>quick_wins, insights, roi]
    end

    JSON2 --> API --> UXW --> CLAUDE --> UXW --> CONTENT
```

### 5.3 Workflow Diario (paso a paso)

> *Fuente: `data-flow-simplified.md`*

```mermaid
flowchart TD
    START[Juegas ronda de golf]
    START --> RECORD[Registras en Excel<br/>TARJETAS_RECORRIDOS.xlsx]
    RECORD --> RUN[python generate_dashboard_data.py]
    RUN --> WAIT[Esperas 3 segundos]
    WAIT --> DONE[JSON generado]
    DONE --> OPEN[python -m http.server 8000]
    OPEN --> BROWSER[Navegador: localhost:8000/dashboard_dynamic.html]
    BROWSER --> SEE[Ves tus stats actualizados]
    SEE --> IMPROVE[Identificas áreas de mejora]

    style RUN fill:#5ABF8F,stroke:#28a745,stroke-width:3px
    style DONE fill:#d4edda,stroke:#28a745
    style SEE fill:#D4B55A,stroke:#ffc107,stroke-width:2px
```

---

## 6. Frontend Dashboard

### 6.1 Secuencia de Inicialización de Charts

> *Fuente: `MERMAID_DIAGRAMS.md` — Diagrama 3*

```mermaid
sequenceDiagram
    participant Browser
    participant HTML as dashboard_dynamic.html
    participant Script as JavaScript
    participant Server as HTTP Server
    participant JSON as dashboard_data.json

    Browser->>HTML: Load page
    HTML->>Script: Parse & execute
    Script->>Script: Initialize globals<br/>window.chartInstances = {}
    Script->>Server: fetch('dashboard_data.json')

    alt Root path (GitHub Pages)
        Server-->>Script: 200 OK + JSON data
    else Fallback (localhost)
        Server--xScript: 404 Not Found
        Script->>Server: fetch('output/dashboard_data.json')
        Server-->>Script: 200 OK + JSON data
    end

    Script->>Script: window.dashboardData = data
    Script->>Browser: Dispatch 'dashboardDataReady' event
    Browser->>Script: Event listeners triggered

    loop For each chart
        Script->>Script: if (element exists)
        Script->>Script: Check window.dashboardData?.key
        Script->>Script: Destroy old chart if exists
        Script->>Script: Create new Chart()
        Script->>Script: Store in chartInstances
    end

    Script->>Browser: All charts rendered ✅
    Note over Browser,JSON: Total time: ~1.9 seconds
```

### 6.2 Safety Pattern (prevención de errores)

> *Fuente: `MERMAID_DIAGRAMS.md` — Diagrama 4*

```mermaid
flowchart TD
    START([Chart Initialization]) --> CHECK_ELEMENT{Element exists?}

    CHECK_ELEMENT -->|No| SKIP[Skip chart initialization]
    CHECK_ELEMENT -->|Yes| INIT_GLOBAL[window.chartInstances = {} || {}]

    INIT_GLOBAL --> CHECK_INSTANCE{Chart instance exists?}

    CHECK_INSTANCE -->|Yes| DESTROY[Destroy old chart:<br/>chartInstances.chart.destroy]
    CHECK_INSTANCE -->|No| CHECK_DATA

    DESTROY --> CHECK_DATA{Data available?}

    CHECK_DATA -->|No| USE_FALLBACK[Use hardcoded fallback:<br/>data || defaultData]
    CHECK_DATA -->|Yes| EXTRACT_DATA[Extract from JSON:<br/>window.dashboardData?.key]

    USE_FALLBACK --> CREATE_CHART
    EXTRACT_DATA --> CREATE_CHART[Create Chart.js instance]

    CREATE_CHART --> STORE[Store reference:<br/>chartInstances.chart = new Chart]
    STORE --> END([Chart Ready ✅])
    SKIP --> END

    style START fill:#5ABF8F,stroke:#3A7F5F,stroke-width:2px,color:#fff
    style END fill:#5ABF8F,stroke:#3A7F5F,stroke-width:2px,color:#fff
    style DESTROY fill:#E88B7A,stroke:#C86A5A,stroke-width:2px,color:#fff
    style CHECK_ELEMENT fill:#D4B55A,stroke:#B49040,stroke-width:2px,color:#000
```

### 6.3 Error Handling y Degradación Graceful

> *Fuente: `MERMAID_DIAGRAMS.md` — Diagrama 13*

```mermaid
flowchart TD
    START([User Opens Dashboard]) --> FETCH{Fetch Success?}

    FETCH -->|Yes| PARSE{Parse JSON Valid?}
    FETCH -->|No| RETRY[Try Fallback Path:<br/>output/dashboard_data.json]

    RETRY --> FETCH2{Fetch Success?}
    FETCH2 -->|Yes| PARSE
    FETCH2 -->|No| ERROR_FETCH[Display Error:<br/>Failed to load data]

    PARSE -->|Yes| ASSIGN[Assign to:<br/>window.dashboardData]
    PARSE -->|No| ERROR_PARSE[Display Error:<br/>Invalid JSON]

    ASSIGN --> EVENT[Dispatch: dashboardDataReady]
    EVENT --> INIT[Initialize Charts]

    INIT --> CHECK_ELEM{Element Exists?}
    CHECK_ELEM -->|No| SKIP[Skip - Silent fail]
    CHECK_ELEM -->|Yes| CHECK_DATA{Data Available?}

    CHECK_DATA -->|No| FALLBACK[Use Hardcoded Fallback]
    CHECK_DATA -->|Yes| USE_JSON[Use JSON Data]

    FALLBACK --> RENDER[Render Chart]
    USE_JSON --> RENDER
    RENDER --> MORE{More Charts?}
    MORE -->|Yes| INIT
    MORE -->|No| SUCCESS([Dashboard Ready ✅])

    SKIP --> MORE
    ERROR_FETCH --> DEGRADED([Degraded Mode:<br/>Hardcoded only])
    ERROR_PARSE --> DEGRADED

    style SUCCESS fill:#5ABF8F,stroke:#3A7F5F,stroke-width:3px,color:#fff
    style DEGRADED fill:#E88B7A,stroke:#C86A5A,stroke-width:2px,color:#fff
```

### 6.4 Arquitectura de Componentes (por Tab)

> *Fuente: `MERMAID_DIAGRAMS.md` — Diagrama 7 (extracto)*

```mermaid
graph TB
    subgraph "Frontend Layer - dashboard_dynamic.html"
        subgraph "Global State"
            WD[window.dashboardData 106.9 KB JSON]
            WC[window.chartInstances Chart references]
        end

        subgraph "Tab 1: Mi Identidad"
            T1C1[Current Form Chart]
            T1C2[4 Percentile Gauges]
            T1C3[HCP Trajectory]
            T1C4[Player Profile Radar 10D]
        end

        subgraph "Tab 2: Evolución"
            T2C1[Temporal Evolution]
            T2C2[Attack Angle Evolution]
            T2C3[Smash Factor Evolution]
        end

        subgraph "Tab 3: Mis Campos"
            T3C1[Campo Performance]
            T3C2[HCP Evolution RFEG]
            T3C3[Volatility Index]
            T3C4[Prediction Model]
        end

        subgraph "Tab 4: Bolsa de Palos"
            T4C1[Club Distance Compare]
            T4C2[Gap Analysis]
            T4C3[11 Dispersion Charts]
            T4C4[Smash Factor Chart]
        end

        subgraph "Tab 5: Análisis Profundo"
            T5C1[Shot Zones Heatmap]
            T5C2[Scoring Probability]
            T5C3[Swing DNA Radar]
            T5C4[Quick Wins Matrix]
            T5C5[Strokes Gained]
            T5C6[Tempo Analysis]
        end

        subgraph "Tab 6: Estrategia"
            T6C1[Six Month Projection]
            T6C2[SWOT Matrix]
            T6C3[Benchmark Radar 10D]
            T6C4[ROI Plan]
        end
    end

    WD --> T1C1 & T2C1 & T3C1 & T4C1 & T5C1 & T6C1

    style WD fill:#5ABF8F,stroke:#3A7F5F,stroke-width:3px,color:#fff
```

### 6.5 Cobertura de Charts

> *Fuente: `MERMAID_DIAGRAMS.md` — Diagrama 9*

```mermaid
pie title Chart Dynamization Coverage (v5.1.1)
    "Dynamic Charts (100%)" : 36
    "Hardcoded Legacy" : 2
```

---

## 7. Deployment

> *Fuente: `MERMAID_DIAGRAMS.md` — Diagrama 10*

```mermaid
graph LR
    subgraph "Development"
        DEV[Local Machine Windows 11]
        PY[Python 3.14<br/>generate_dashboard_data.py]
    end

    subgraph "Version Control"
        GIT[Git Repository main branch]
        GITHUB[GitHub AlvGolf-Identity-EngineV3]
    end

    subgraph "Production - GitHub Pages"
        PAGES[GitHub Pages Static Hosting]
        HTML[dashboard_dynamic.html]
        JSON_PROD[dashboard_data.json]
    end

    subgraph "Local Testing"
        SERVER[HTTP Server localhost:8000]
        BROWSER[Browser Testing Chrome/Firefox]
    end

    DEV --> PY
    PY --> JSON_LOCAL[output/dashboard_data.json]
    JSON_LOCAL --> SERVER
    SERVER --> BROWSER

    DEV --> GIT
    GIT --> GITHUB
    GITHUB --> PAGES
    PAGES --> HTML & JSON_PROD

    style PAGES fill:#5ABF8F,stroke:#3A7F5F,stroke-width:3px,color:#fff
    style BROWSER fill:#4A9FD8,stroke:#2E5F8F,stroke-width:2px,color:#fff
```

---

## 8. Performance y Costos

### 8.1 Overview General

> *Fuente: `performance-metrics.md`*

```mermaid
graph TB
    subgraph "Backend ETL (3.1s)"
        TIME[ETL: 3.1s · 52 funciones ✅]
        JSON_SIZE[JSON: 106.9 KB · 52 keys ✅]
    end

    subgraph "Frontend Dashboard (< 2s)"
        CHARTS[36 charts · 100% dinámicos ✅]
        LOAD[Carga: < 2s · 0 errors ✅]
    end

    subgraph "Multi-Agent (317.7s)"
        AGENTS[5 agentes · 2 equipos paralelos ✅]
        EXEC[317.7s total · 0 RAG queries ✅]
        COST[Costo: $0.52/mes · €0.46/mes ✅]
    end

    TIME --> JSON_SIZE --> LOAD --> CHARTS
    AGENTS --> EXEC --> COST

    style COST fill:#d4edda,stroke:#28a745,stroke-width:3px
```

### 8.2 Costos y Evolución del Rendimiento

> *Fuente: `ARCHITECTURE_DIAGRAMS.md` — Diagrama 6*

```mermaid
graph TB
    subgraph "Execution Costs (Monthly: $0.52)"
        direction LR
        COLD["Cold Call: $0.185 (1x/month)"]
        CACHED["Cached Calls: $0.110 (3x/month)"]
        TOTAL["Total: $0.515/month ~EUR 0.46/month"]
        COLD --> TOTAL
        CACHED --> TOTAL
    end

    subgraph "Performance Breakdown (317.7s total)"
        P1["Data Loader 0.05s"]
        P2["Team 2 Parallel 148.4s"]
        P3["Team 3 Parallel 156.3s"]
        P4["Writer Node 13.1s"]
        P1 --> P2 --> P3 --> P4
    end

    subgraph "Optimization Techniques"
        O1["0 RAG Queries (eliminado bottleneck)"]
        O2["Prompt Caching (90% input savings)"]
        O3["Parallel Execution (2 teams)"]
        O4["Single JSON Load (vs 4 RAG queries)"]
    end
```

---

## 9. Timeline del Proyecto

### 9.1 Fase 1: Backend ETL (Sprints 1–8)

> *Fuente: `sprint-timeline.md`*

```mermaid
gantt
    title AlvGolf - Fase 1: Backend ETL
    dateFormat YYYY-MM-DD

    section Backend ETL
    Sprint 1-2: Base + Validation        :done, s1, 2026-02-01, 2026-02-03
    Sprint 3: Important Functions (4)    :done, s3, 2026-02-03, 1d
    Sprint 4: Testing Suite              :done, s4, 2026-02-03, 1d
    Sprint 5: Visual Improvements (4)    :done, s5, 2026-02-03, 1d
    Sprint 6: Trend Improvements (4)     :done, s6, 2026-02-03, 1d
    Sprint 7: Finalization               :done, s7, 2026-02-03, 1d

    section Frontend Integration
    Sprint 8: 12 Visualizations          :done, s8, 2026-02-03, 2026-02-04

    section Fixes + Docs
    Post-Integration Bug Fixes           :done, bugs, 2026-02-04, 1d
    Initial Docs + Diagrams              :done, docs, 2026-02-06, 1d
```

### 9.2 Fase 2: Dashboard 100% Dinámico (Sprints 9–13)

> *Fuente: `sprint-timeline.md`*

```mermaid
gantt
    title AlvGolf - Fase 2: 36 Charts Dinámicos
    dateFormat YYYY-MM-DD

    section Sprint 9 (8 funcs)
    current_form, percentile_gauges      :done, s91, 2026-02-07, 1d
    hcp_trajectory, smash_factor         :done, s92, 2026-02-08, 1d

    section Sprint 10-12 (22 funcs)
    Sprint 10: campo, hcp, volatility    :done, s10, 2026-02-08, 1d
    Sprint 11: heatmap, swingDNA, SG     :done, s11, 2026-02-08, 1d
    Sprint 12: SWOT, ROI, projection     :done, s12, 2026-02-09, 1d

    section Sprint 13 Frontend
    Sprint 13A: 14 charts + bugs         :done, s13a, 2026-02-08, 2h
    Sprint 13B: 11 charts protected      :done, s13b, 2026-02-08, 2h
    Sprint 13C: 8 functions verified     :done, s13c, 2026-02-08, 2h
    v5.0.0 PRODUCTION                    :milestone, prod5, 2026-02-09, 0d
```

### 9.3 Fase 3: Mejoras + Multi-Agent System

> *Fuente: `sprint-timeline.md`*

```mermaid
gantt
    title AlvGolf - Fase 3: Features + Multi-Agent
    dateFormat YYYY-MM-DD

    section Sprint 14-15
    Sprint 14: Radar 10D + data fix      :done, s14, 2026-02-12, 1d
    Sprint 15: Heatmap + Mobile iOS      :done, s15, 2026-02-13, 1d
    v5.1.1 PRODUCTION                    :milestone, prod511, 2026-02-13, 0d

    section Multi-Agent System
    TIER 1: FastAPI + RAG + Pinecone     :done, tier1, 2026-02-15, 1d
    v3.0.0: 5 agentes producción         :done, v30, 2026-02-16, 1d
    v3.0.1: UXWriter dashboard           :done, v301, 2026-02-16, 1d
    Docs + HTML fix + Auditoría          :done, final, 2026-02-17, 2026-02-20
    v3.0.1 STABLE                        :milestone, prod301, 2026-02-20, 0d
```

---

## 10. Troubleshooting y Acceso

### 10.1 Diagnóstico CORS (error más común)

> *Fuente: `cors-troubleshooting-flow.md`*

```mermaid
flowchart TD
    START[Usuario quiere ver el dashboard]
    START --> OPEN{¿Cómo abriste<br/>dashboard_dynamic.html?}

    OPEN -->|Doble clic en el archivo| FILE[Protocolo: file:///]
    OPEN -->|python -m http.server 8000| HTTP[Protocolo: http://localhost:8000]

    FILE --> FETCH_ATTEMPT[JavaScript intenta fetch JSON]
    FETCH_ATTEMPT --> CORS_BLOCK[Navegador bloquea fetch]
    CORS_BLOCK --> ERROR_MSG["Error: Failed to fetch<br/>dashboard_data.json<br/>CORS policy blocked"]
    ERROR_MSG --> DASHBOARD_BROKEN["Dashboard roto:<br/>Gráficos vacíos · No hay datos"]
    DASHBOARD_BROKEN --> SOLUTION[SOLUCIÓN]

    SOLUTION --> TERMINAL[Abrir terminal/CMD]
    TERMINAL --> CD["cd C:\Users\alvar\Documents\AlvGolf"]
    CD --> SERVER_CMD["python -m http.server 8000"]
    SERVER_CMD --> HTTP

    HTTP --> FETCH_OK[Fetch permitido]
    FETCH_OK --> JSON_LOAD[JSON carga correctamente]
    JSON_LOAD --> SUCCESS["DASHBOARD FUNCIONAL"]

    style FILE fill:#f8d7da,stroke:#dc3545,stroke-width:3px
    style CORS_BLOCK fill:#f8d7da,stroke:#dc3545,stroke-width:3px
    style DASHBOARD_BROKEN fill:#f8d7da,stroke:#dc3545,stroke-width:3px
    style HTTP fill:#d4edda,stroke:#28a745,stroke-width:3px
    style SUCCESS fill:#d4edda,stroke:#28a745,stroke-width:3px
    style SOLUTION fill:#fff3cd,stroke:#ffc107,stroke-width:3px
```

### 10.2 Árbol de Decisión de Acceso

> *Fuente: `decision-tree-access.md`*

```mermaid
flowchart TD
    START[Necesitas acceder al dashboard]
    START --> Q1{¿Desde dónde?}

    Q1 -->|Solo desde mi PC| LOCAL[Acceso Local]
    Q1 -->|Desde cualquier dispositivo| REMOTE[Acceso Remoto]

    LOCAL --> METHOD_HTTP["✅ RECOMENDADO: Servidor HTTP Local<br/>python -m http.server 8000<br/>→ http://localhost:8000"]

    REMOTE --> Q4{¿Qué tipo?}
    Q4 -->|Privado - Solo yo| GITHUB_PRIVATE["GitHub Pages + Repo Privado<br/>$4/mes GitHub Pro"]
    Q4 -->|Público - Compartir| GITHUB_PUBLIC["GitHub Pages + Repo Público<br/>Gratis (datos públicos)"]
    Q4 -->|Con login| AUTH_FULL["Backend FastAPI + DB<br/>40-60h desarrollo · $15-30/mes"]

    style METHOD_HTTP fill:#d4edda,stroke:#28a745,stroke-width:3px
    style GITHUB_PRIVATE fill:#d4edda,stroke:#28a745,stroke-width:2px
    style AUTH_FULL fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```

---

## Referencia de Archivos

| Archivo fuente | Diagramas en este doc | Sección |
|---------------|----------------------|---------|
| `ARCHITECTURE_DIAGRAMS.md` | Diag 1, 2, 3, 4, 6, 7 | §1, §2.1, §3.1, §3.2, §4, §8.2 |
| `MERMAID_DIAGRAMS.md` | Diag 3, 4, 7, 9, 10, 13 | §6.1–6.5, §7 |
| `agentic-system-architecture.md` | Flowchart principal | §1 (incluido) |
| `data-flow-simplified.md` | Flujo ETL, IA, workflow diario | §5.1–5.3 |
| `performance-metrics.md` | Overview, costos, evolución | §8.1 |
| `sprint-timeline.md` | 3 Gantt charts | §9.1–9.3 |
| `cors-troubleshooting-flow.md` | Diagnóstico CORS | §10.1 |
| `decision-tree-access.md` | Árbol de acceso | §10.2 |

---

*Generado por Claude Sonnet 4.6 · AlvGolf Multi-Agent System v3.0.1 · 2026-02-20*
