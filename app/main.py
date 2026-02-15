"""
AlvGolf Agentic Analytics Engine - FastAPI Application

Main API server with 4 endpoints:
- GET /              Health check
- POST /ingest       Ingest shots to vector database
- POST /query        Query RAG with question
- POST /analyze      Full analysis with Multi-Agent System (TIER 2)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from datetime import datetime

from app.config import settings, validate_settings
from app.models import (
    HealthResponse,
    IngestRequest, IngestResponse,
    QueryRequest, QueryResponse,
    AnalyzeRequest, AnalyzeResponse,
    ErrorResponse
)
from app.rag import ingest_shots, rag_answer
from app.agents.analytics_pro import analytics_agent
from app.agents.orchestrator import run_multi_agent_analysis  # TIER 2


# ============ Logging Configuration ============

logger.remove()
logger.add(
    sys.stdout,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)


# ============ FastAPI App ============

app = FastAPI(
    title="AlvGolf Agentic API",
    version="1.0.0",
    description="Backend for AlvGolf Agentic Analytics Engine (TIER 1)",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ============ CORS Middleware ============

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ Startup Event ============

@app.on_event("startup")
async def startup_event():
    """
    Runs on app startup.
    Validates configuration and logs startup info.
    """
    logger.info("="*60)
    logger.info("AlvGolf Agentic API Starting...")
    logger.info("="*60)

    # Validate settings
    try:
        validate_settings()
        logger.success("Configuration validated successfully")
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise

    logger.info(f"Environment: {settings.env}")
    logger.info(f"API Host: {settings.api_host}:{settings.api_port}")
    logger.info(f"Pinecone Index: {settings.pinecone_index_name}")
    logger.info("="*60)
    logger.success("AlvGolf Agentic API Ready!")
    logger.info("="*60)


# ============ Endpoints ============

@app.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns API status and version.
    """
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        message="AlvGolf Agentic API is running (TIER 2 - Multi-Agent)"
    )


@app.post("/ingest", response_model=IngestResponse)
async def ingest_data(request: IngestRequest):
    """
    Ingest golf shots data to Pinecone vector database.

    This endpoint vectorizes shot data and stores it in Pinecone
    for later retrieval by the RAG system.

    Args:
        request: IngestRequest with user_id and list of shots

    Returns:
        IngestResponse with status and number of chunks ingested
    """
    try:
        logger.info(f"Ingesting {len(request.shots)} shots for user {request.user_id}")

        # Ingest to Pinecone
        count = ingest_shots(request.user_id, request.shots)

        logger.success(f"Ingested {count} chunks for user {request.user_id}")

        return IngestResponse(
            status="ok",
            chunks_ingested=count,
            message=f"Successfully ingested {count} shots"
        )

    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query RAG system with a question about golf data.

    Uses Pinecone for semantic search and Claude for answer generation.

    Args:
        request: QueryRequest with user_id and prompt

    Returns:
        QueryResponse with answer from Claude
    """
    try:
        logger.info(f"Query from user {request.user_id}: {request.prompt[:50]}...")

        # Query RAG
        answer = rag_answer(request.user_id, request.prompt)

        logger.success(f"Query answered ({len(answer)} chars)")

        return QueryResponse(answer=answer)

    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_golf(request: AnalyzeRequest):
    """
    Full golf performance analysis with Multi-Agent System (TIER 2).

    Workflow:
    1. Analytics Pro Agent → Technical analysis (5 sections)
    2. Dashboard Writer Agent → Motivational sections (3 sections)

    Technical sections:
    1. Technical Patterns
    2. Statistical Trends
    3. Main Gaps
    4. Recommendations
    5. Prediction

    Motivational sections:
    1. DNA Golfístico (identity)
    2. Evolución/Progreso (progress)
    3. Próximo Nivel/Acción (action plan)

    Args:
        request: AnalyzeRequest with user_id

    Returns:
        AnalyzeResponse with both technical and motivational analysis
    """
    try:
        logger.info(f"[TIER 2] Multi-agent analysis request from user {request.user_id}")

        # Run multi-agent workflow (LangGraph orchestrator)
        result = await run_multi_agent_analysis(request.user_id)

        # Check for errors
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])

        logger.success(f"[TIER 2] Multi-agent analysis completed for {request.user_id}")

        from app.models import MotivationalSections

        return AnalyzeResponse(
            technical_analysis=result["technical_analysis"],
            motivational_sections=MotivationalSections(**result["motivational_sections"]),
            generated_at=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ Run Server ============

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower()
    )
