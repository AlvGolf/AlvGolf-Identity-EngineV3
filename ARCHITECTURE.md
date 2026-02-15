# AlvGolf - Arquitectura del Sistema

**Versión:** 5.1.1 + TIER 1
**Fecha:** 2026-02-15

---

## 🏗️ Arquitectura General

```mermaid
graph TB
    subgraph "User Interface"
        U[Usuario]
    end

    subgraph "Frontend Layer"
        A[dashboard_dynamic.html<br/>v5.1.1 - 36 Charts]
        B[dashboard_agentic.html<br/>TIER 1 - IA Insights]
    end

    subgraph "Backend TIER 1"
        C[FastAPI Server<br/>:8000]
        D[RAG Core]
        E[Analytics Pro Agent]
    end

    subgraph "Backend v5.1.0"
        F[generate_dashboard_data.py<br/>52 functions]
    end

    subgraph "Data Storage"
        G[dashboard_data.json<br/>197 KB]
        H[Pinecone Vector DB<br/>120 vectors]
        I[Raw Data<br/>FlightScope + Tarjetas]
    end

    subgraph "External APIs"
        J[Claude Sonnet 4<br/>Anthropic]
        K[Pinecone Embeddings<br/>multilingual-e5-large]
    end

    U -->|Browse| A
    A -->|Click IA Insights| B
    B -->|POST /analyze| C
    C -->|RAG Query| D
    D -->|Embed| K
    D -->|Search| H
    C -->|Generate| E
    E -->|LLM Call| J
    I -->|Process| F
    F -->|Output| G
    G -->|Load| A
    G -->|Ingest| H
```

---

## 🔄 Data Flow - Analytics Agent

```mermaid
sequenceDiagram
    participant U as Usuario
    participant D as Dashboard
    participant F as FastAPI
    participant R as RAG Core
    participant P as Pinecone
    participant E as Embeddings API
    participant C as Claude Sonnet 4
    participant A as Analytics Agent

    U->>D: Click "Generar Análisis"
    D->>D: Show loading (30-45s)
    D->>F: POST /analyze {user_id}
    F->>A: invoke analytics_agent()
    A->>R: rag_answer(user_id, context_prompt)
    R->>E: embed_texts([prompt])
    E-->>R: embeddings [1024 dim]
    R->>P: query(vector, top_k=5, namespace)
    P-->>R: matches with metadata
    R->>R: build_context()
    R->>C: invoke(prompt + context)
    Note over C: Generate 5 sections<br/>30-45 seconds
    C-->>R: analysis text
    R-->>A: context + answer
    A->>A: format_5_sections()
    A-->>F: analysis JSON
    F-->>D: {analysis, generated_at}
    D->>D: parseAndDisplayAnalysis()
    D->>D: Hide loading, show sections
    D-->>U: Display 5 sections
```

---

## 🗂️ Estructura de Datos

### Vector Database (Pinecone)

```mermaid
erDiagram
    PINECONE_INDEX {
        string id PK
        float vector_1024_dim
        string user_id
        string date
        string source
        string club
        string text
    }

    NAMESPACE {
        string name PK
        int vector_count
    }

    DATA_SOURCES {
        string type
        int count
    }

    PINECONE_INDEX ||--o{ NAMESPACE : contains
    NAMESPACE ||--o{ DATA_SOURCES : includes

    DATA_SOURCES {
        club_statistics 22
        momentum 52
        course_performance 11
        quarterly_scoring 7
        strokes_gained 6
        hcp_evolution 5
        best_rounds 3
        worst_rounds 3
    }
```

### API Models (Pydantic)

```mermaid
classDiagram
    class ShotData {
        +string date
        +string source
        +string club
        +int hole
        +float ball_speed
        +float carry
        +float launch_angle
        +float face_to_path
        +float score
        +string notes
    }

    class IngestRequest {
        +string user_id
        +List~ShotData~ shots
    }

    class IngestResponse {
        +string status
        +int chunks_ingested
        +string message
    }

    class QueryRequest {
        +string user_id
        +string prompt
    }

    class QueryResponse {
        +string answer
    }

    class AnalyzeRequest {
        +string user_id
    }

    class AnalyzeResponse {
        +string analysis
        +datetime generated_at
    }

    IngestRequest --> ShotData
```

---

## 🎯 Analytics Pro Agent Architecture

```mermaid
graph LR
    subgraph "Input"
        A[user_id]
    end

    subgraph "RAG Context Retrieval"
        B[rag_answer]
        C[Pinecone Search<br/>top_k=5]
        D[Context Documents]
    end

    subgraph "Agent Processing"
        E[System Prompt<br/>~2000 tokens]
        F[Claude Sonnet 4<br/>temp=0.1]
        G[Prompt Caching]
    end

    subgraph "Output"
        H[5 Sections<br/>~2000 tokens]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    E --> G
    F --> H

    style G fill:#90EE90
    style H fill:#FFD700
```

### Agent Sections

1. **TECHNICAL PATTERNS** - Swing analysis
2. **STATISTICAL TRENDS** - Performance evolution
3. **MAIN GAPS** - Critical improvement areas
4. **RECOMMENDATIONS** - Drills + Strategy
5. **PREDICTION** - 30-day projection

---

## 🔐 Security Architecture

```mermaid
graph TB
    subgraph "API Security"
        A[CORS Middleware]
        B[Environment Variables]
        C[API Keys Rotation]
    end

    subgraph "Data Privacy"
        D[Namespace Isolation]
        E[Local-only Backend]
        F[No External Tracking]
    end

    subgraph "Access Control"
        G[localhost:8000-8001 only]
        H[Single User: alvaro]
        I[No Authentication<br/>Development]
    end

    A --> G
    B --> C
    D --> H
    E --> F
```

---

## 📈 Deployment Architecture (Future)

```mermaid
graph TB
    subgraph "Production - TIER 4"
        A[Vercel<br/>Frontend]
        B[Railway/Render<br/>Backend]
        C[Pinecone Cloud<br/>Vector DB]
        D[Anthropic API<br/>Claude]
    end

    subgraph "Current - TIER 1"
        E[localhost:8001<br/>Frontend]
        F[localhost:8000<br/>Backend]
        G[Pinecone Serverless<br/>US-East-1]
        H[Anthropic API<br/>Claude]
    end

    style E fill:#90EE90
    style F fill:#90EE90
    style G fill:#90EE90
    style H fill:#90EE90
```

---

## 🔄 TIER 2 Architecture (Planned)

```mermaid
graph TB
    subgraph "Multi-Agent System"
        A[FastAPI Endpoint<br/>/analyze]
        B[LangGraph Orchestrator]
        C[Analytics Pro Agent<br/>Technical Analysis]
        D[Dashboard Writer Agent<br/>Motivational Text]
    end

    subgraph "Output"
        E[3 IA Sections<br/>Motivational]
        F[5 Technical Sections<br/>Optional View]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    C -.-> F

    style B fill:#FFD700
    style D fill:#87CEEB
```

---

## 📊 Performance Architecture

```mermaid
graph LR
    subgraph "Optimization Strategies"
        A[Prompt Caching<br/>90% savings]
        B[Batching<br/>96 texts/request]
        C[Serverless<br/>Pay-per-use]
        D[Top-K Retrieval<br/>Only 5 docs]
    end

    subgraph "Performance Metrics"
        E[API Health: <100ms]
        F[RAG Query: 10-15s]
        G[Analytics: 30-45s]
        H[Cost: $0.015/analysis]
    end

    A --> H
    B --> G
    C --> H
    D --> F
```

---

## 🧪 Testing Architecture

```mermaid
graph TB
    subgraph "Test Pyramid"
        A[E2E Tests<br/>4 tests]
        B[Integration Tests<br/>API + RAG]
        C[Unit Tests<br/>Models + Utils]
    end

    subgraph "Test Coverage"
        D[API Health: 100%]
        E[Analytics Agent: 100%]
        F[Dashboard: 100%]
        G[CORS: 100%]
    end

    A --> D
    A --> E
    A --> F
    A --> G
    B --> E
```

---

## 📁 Code Architecture

```
app/
├── __init__.py
├── main.py              # FastAPI app + endpoints
├── config.py            # Settings (.env)
├── models.py            # Pydantic (10 models)
├── rag.py               # RAG Core
└── agents/
    └── analytics_pro.py # Analytics Agent

scripts/
├── ingest_full_data.py       # 120 vectors
├── test_*.py                 # 7 test scripts

dashboard_agentic.html        # 520 lines (HTML+CSS+JS)
```

---

## 🌊 Error Handling Flow

```mermaid
graph TB
    A[User Request] --> B{API Available?}
    B -->|No| C[Show Error Badge]
    B -->|Yes| D{Generate Analysis}
    D -->|Success| E[Display 5 Sections]
    D -->|Timeout| F[Show Timeout Message]
    D -->|Error| G[Show Error + Retry Button]
    C --> H[User Alerted]
    F --> H
    G --> H
    E --> I[Analysis Complete]
```

---

**Documentado por:** Claude Sonnet 4.5
**Fecha:** 2026-02-15
