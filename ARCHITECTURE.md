# AlvGolf - Architecture Diagrams v3.0.1

**Version:** 3.0.1 - Multi-Agent System + UXWriter Dashboard Integration  
**Date:** 2026-02-17  
**Purpose:** Comprehensive architectural reference for future development sessions

---

## 1. Complete System Architecture (v3.0.1)

```mermaid
graph TB
    subgraph "User Layer"
        U[Usuario / Browser]
    end

    subgraph "Frontend Layer"
        FD[dashboard_dynamic.htmlv5.1.1 - 36 Charts + AI Content]
        FA[dashboard_agentic.htmlMulti-Agent Insights v3.0]
    end

    subgraph "FastAPI Backend - localhost:8000"
        EP1["GET / (health)"]
        EP2["POST /ingest"]
        EP3["POST /query"]
        EP4["POST /analyze (5 agents)"]
        EP5["POST /generate-content (UXWriter)"]
    end

    subgraph "Multi-Agent Orchestrator (LangGraph)"
        DL[data_loader_node106.9 KB JSON, 0 RAG]

        subgraph "TEAM 2 - Analytics (Parallel)"
            A1[AgentAnalistaPerformance Analysis650 lines]
            A2[AgentTecnicoBiomechanics550 lines]
            A3[AgentEstrategaPractice Design600 lines]
        end

        subgraph "TEAM 3 - Content (Parallel)"
            A4[AgentUXWriterDashboard Content752 lines]
            A5[AgentCoachCoaching Reports807 lines]
        end

        WR[Dashboard WriterMotivational Sections]
    end

    subgraph "Data Processing"
        GEN[generate_dashboard_data.py52 functions, v5.1.0]
    end

    subgraph "Data Storage"
        JSON[dashboard_data.json106.9 KB, 52 keys]
        PC[Pinecone Vector DB120 vectors, namespace: alvaro]
        RAW[Raw DataFlightScope (493 shots)Tarjetas (52 rounds)]
    end

    subgraph "External Services"
        CLAUDE[Anthropic Claude Sonnet 4LLM + Prompt Caching]
        PCAPI[Pinecone Embeddingsmultilingual-e5-large, 1024 dim]
    end

    U -->|Browse| FD
    U -->|Click IA Insights| FA
    FD -->|"POST /generate-content(async, 60-70s)"| EP5
    FA -->|"POST /analyze(5.3 min)"| EP4

    EP4 --> DL
    EP5 --> A4

    DL -->|"100% data"| A1 & A2 & A3
    A1 & A2 & A3 -->|"Team 2 output20,400 chars"| A4 & A5
    A4 & A5 -->|"Team 3 output20,065 chars"| WR
    WR -->|Response| FA

    EP5 -->|"Load JSON"| JSON
    A4 -->|"Content JSON"| FD

    RAW -->|ETL| GEN
    GEN -->|Generate| JSON
    JSON -->|"fetch() on load"| FD
    JSON -->|Load| DL

    A1 & A2 & A3 & A4 & A5 -->|LLM Calls| CLAUDE
    EP2 -->|Embed + Store| PC
    EP3 -->|"Embed + Search"| PCAPI
    PCAPI --> PC
```

---

## 2. UXWriter Dashboard Integration Flow

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

    Note over FE: Charts visible (< 1s)

    FE->>API: POST /generate-content{user_id: "alvaro"}
    Note over FE: Non-blocking async call

    API->>FS: Load dashboard_data.json
    FS-->>API: 106.9 KB

    API->>UXW: agent.write(user_id, dashboard_data)
    UXW->>UXW: Build prompt with skill(~6,000 tokens cached)
    UXW->>CL: invoke(skill + data context)

    Note over CL: Generate 10 sectionsin Spanish (60-70s)

    CL-->>UXW: JSON content response
    UXW->>UXW: Parse + validate content
    UXW-->>API: {content: {...}, metadata: {...}}

    API-->>FE: ContentGenerateResponse

    FE->>FE: insertUXContent(content)
    FE->>FE: 1. Insert hero_statement (Tab 1)
    FE->>FE: 2. Insert dna_profile (Tab 1)
    FE->>FE: 3. Update chart_titles (All tabs)
    FE->>FE: 4. Insert quick_wins (Tab 6)
    FE->>FE: 5. Insert roi_cards (Tab 6)
    FE->>FE: 6. Insert insight_boxes (Tab 5)

    Note over FE: AI content appears (~70s after load)

    FE-->>U: Dashboard fully enhanced
```

---

## 3. AI Content Lifecycle in Dashboard

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

    InsertContent --> HeroInserted: hero_statement in Tab 1
    InsertContent --> DNAInserted: dna_profile in Tab 1
    InsertContent --> TitlesUpdated: chart_titles across tabs
    InsertContent --> QuickWinsInserted: quick_wins in Tab 6
    InsertContent --> ROIInserted: roi_cards in Tab 6
    InsertContent --> InsightsInserted: insight_boxes in Tab 5

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

## 4. Multi-Agent Orchestration Workflow

```mermaid
graph LR
    subgraph "Phase 1: Data Loading (~0.05s)"
        DL[data_loader_node]
        JSON[(dashboard_data.json106.9 KB)]
        JSON --> DL
    end

    subgraph "Phase 2: Team 2 Analytics (~148s)"
        direction TB
        T2[team2_parallel_node]
        AN[AgentAnalista6,154 chars]
        TE[AgentTecnico5,389 chars]
        ES[AgentEstratega8,857 chars]
        T2 --> AN & TE & ES
    end

    subgraph "Phase 3: Team 3 Content (~156s)"
        direction TB
        T3[team3_parallel_node]
        UX[AgentUXWriter10,223 chars]
        CO[AgentCoach9,842 chars]
        T3 --> UX & CO
    end

    subgraph "Phase 4: Output (~13s)"
        WR[writer_node1,236 chars]
        OUT[Final Output41,701 chars total]
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

---

## 5. Data Flow: Frontend-Backend-AI

```mermaid
flowchart TD
    subgraph "Raw Data Sources"
        FS[FlightScope CSV493 shots, 11 clubs]
        TC[Tarjetas XLSX52 rounds, 11 courses]
        PDF[RFEG PDFOfficial HCP history]
    end

    subgraph "Backend Generator (Python)"
        GEN[generate_dashboard_data.py52 functions]
        ETL["ETL Pipeline:1. Load raw data2. Calculate metrics3. Generate charts data4. Output JSON"]
    end

    subgraph "Static Data Layer"
        DJ[dashboard_data.json106.9 KB, 52 keys]
    end

    subgraph "Frontend (HTML + JS)"
        LOAD["fetch('dashboard_data.json')"]
        CHARTS[Chart.js Rendering36 dynamic charts]
        UXLOAD["loadUXContent()POST /generate-content"]
        INSERT["insertUXContent()6 content mappings"]
    end

    subgraph "AI Layer (FastAPI + Claude)"
        ENDPOINT["/generate-content endpoint"]
        AGENT[AgentUXWriterSkill: 6,000 tokens]
        LLM[Claude Sonnet 4Prompt Caching]
    end

    subgraph "Dashboard Output"
        TAB1["Tab 1: Mi Identidad+ hero_statement+ dna_profile"]
        TAB5["Tab 5: Analisis Profundo+ insight_boxes"]
        TAB6["Tab 6: Estrategia+ quick_wins+ roi_cards"]
        TITLES["All Tabs+ chart_titles"]
    end

    FS & TC & PDF --> GEN
    GEN --> ETL --> DJ

    DJ --> LOAD --> CHARTS
    DJ --> ENDPOINT

    LOAD -.->|"After charts ready"| UXLOAD
    UXLOAD --> ENDPOINT
    ENDPOINT --> AGENT --> LLM
    LLM --> AGENT --> ENDPOINT --> UXLOAD
    UXLOAD --> INSERT

    INSERT --> TAB1 & TAB5 & TAB6 & TITLES
```

---

## 6. Cost and Performance Architecture

```mermaid
graph TB
    subgraph "Execution Costs (Monthly: $0.52)"
        direction LR
        COLD["Cold Call: $0.185(1x/month)"]
        CACHED["Cached Calls: $0.110(3x/month)"]
        TOTAL["Total: $0.515/month~EUR 0.46/month"]
        COLD --> TOTAL
        CACHED --> TOTAL
    end

    subgraph "Performance Breakdown (317.7s total)"
        P1["Data Loader0.05s (0.02%)"]
        P2["Team 2 Parallel148.4s (46.7%)"]
        P3["Team 3 Parallel156.3s (49.2%)"]
        P4["Writer Node13.1s (4.1%)"]
        P1 --> P2 --> P3 --> P4
    end

    subgraph "Optimization Techniques"
        O1["0 RAG Queries(eliminated bottleneck)"]
        O2["Prompt Caching(90% input savings)"]
        O3["Parallel Execution(2 parallel stages)"]
        O4["Single JSON Load(vs 4 RAG queries)"]
    end

    subgraph "Performance Evolution"
        V1["MVP: 80s, 1 agent, $0.13"]
        V2["Team 2: 166s, 3 agents, $0.50"]
        V3["Team 3: 318s, 5 agents, $0.52"]
        V1 --> V2 --> V3
    end
```

---

## 7. API Endpoint Architecture

```mermaid
graph LR
    subgraph "FastAPI Application (localhost:8000)"
        direction TB

        H["GET /Health Check<100ms"]
        I["POST /ingestData Ingestion~2s"]
        Q["POST /queryRAG Query10-15s"]
        A["POST /analyzeFull Multi-Agent~5.3 min"]
        C["POST /generate-contentUXWriter Only~60-70s"]
    end

    subgraph "Dependencies"
        RAG[RAG CorePinecone + Embeddings]
        ORCH[OrchestratorLangGraph Workflow]
        UXW[AgentUXWriterStandalone]
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

## 8. Pydantic Models Architecture (Updated v3.0.1)

```mermaid
classDiagram
    class HealthResponse {
        +status: Literal[healthy, degraded, unhealthy]
        +version: str
        +message: str
        +timestamp: datetime
    }

    class ShotData {
        +date: str
        +source: str
        +club: str
        +hole: int
        +ball_speed: float
        +carry: float
        +launch_angle: float
        +face_to_path: float
        +score: float
        +notes: str
    }

    class IngestRequest {
        +user_id: str
        +shots: List~ShotData~
    }

    class IngestResponse {
        +status: Literal[ok, error]
        +chunks_ingested: int
        +message: str
    }

    class QueryRequest {
        +user_id: str
        +prompt: str
    }

    class QueryResponse {
        +answer: str
        +context_used: List~str~
    }

    class AnalyzeRequest {
        +user_id: str
        +force_refresh: bool
    }

    class MotivationalSections {
        +dna: str
        +progress: str
        +action: str
    }

    class AnalyzeResponse {
        +technical_analysis: str
        +motivational_sections: MotivationalSections
        +generated_at: datetime
        +tokens_used: int
        +cache_hit: bool
    }

    class ContentGenerateRequest {
        +user_id: str
        +force_refresh: bool
    }

    class ContentGenerateResponse {
        +content: dict
        +metadata: dict
        +generated_at: datetime
    }

    class ErrorResponse {
        +error: str
        +detail: str
        +timestamp: datetime
    }

    IngestRequest --> ShotData
    AnalyzeResponse --> MotivationalSections
```

---

**Created by:** Claude Sonnet 4  
**Date:** 2026-02-17  
**Purpose:** Comprehensive architectural diagrams for AlvGolf Multi-Agent System v3.0.1
