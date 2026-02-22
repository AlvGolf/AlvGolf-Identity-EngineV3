"""
AlvGolf Agentic Analytics Engine - Pydantic Models

Data models for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


# ============ Health Check ============

class HealthResponse(BaseModel):
    """Response for GET / endpoint"""
    status: Literal["healthy", "degraded", "unhealthy"]
    version: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


# ============ Shot Data ============

class ShotData(BaseModel):
    """
    Single golf shot data.

    This represents one shot from FlightScope or similar launch monitor.
    """
    date: str = Field(..., description="Date of shot (YYYY-MM-DD)")
    source: str = Field(..., description="Data source (flightscope, trackman, garmin)")
    club: str = Field(..., description="Club used (Dr, 3W, 7i, PW, etc.)")
    hole: int = Field(0, description="Hole number (0 if practice)")
    ball_speed: float = Field(0, description="Ball speed in km/h")
    carry: float = Field(0, description="Carry distance in meters")
    launch_angle: float = Field(0, description="Launch angle in degrees")
    face_to_path: float = Field(0, description="Face-to-path angle in degrees")
    score: float = Field(0, description="Score on hole (0 if practice, can be avg)")
    notes: str = Field("", description="Optional notes")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-12-31",
                "source": "flightscope",
                "club": "Dr",
                "hole": 0,
                "ball_speed": 235.5,
                "carry": 212.8,
                "launch_angle": 12.3,
                "face_to_path": 4.2,
                "score": 0,
                "notes": "Practice session"
            }
        }


# ============ Ingest ============

class IngestRequest(BaseModel):
    """Request for POST /ingest endpoint"""
    user_id: str = Field(..., description="User ID (e.g., 'alvaro')")
    shots: List[ShotData] = Field(..., description="List of shots to ingest")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alvaro",
                "shots": [
                    {
                        "date": "2025-12-31",
                        "source": "flightscope",
                        "club": "Dr",
                        "hole": 0,
                        "ball_speed": 235.5,
                        "carry": 212.8,
                        "launch_angle": 12.3,
                        "face_to_path": 4.2,
                        "score": 0,
                        "notes": ""
                    }
                ]
            }
        }


class IngestResponse(BaseModel):
    """Response for POST /ingest endpoint"""
    status: Literal["ok", "error"]
    chunks_ingested: int
    message: Optional[str] = None


# ============ Query ============

class QueryRequest(BaseModel):
    """Request for POST /query endpoint"""
    user_id: str = Field(..., description="User ID")
    prompt: str = Field(..., description="Question to ask about golf data")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alvaro",
                "prompt": "What is my driver pattern?"
            }
        }


class QueryResponse(BaseModel):
    """Response for POST /query endpoint"""
    answer: str
    context_used: Optional[List[str]] = None


# ============ Analyze ============

class AnalyzeRequest(BaseModel):
    """Request for POST /analyze endpoint"""
    user_id: str = Field(..., description="User ID")
    force_refresh: bool = Field(False, description="Force fresh analysis (ignore cache)")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alvaro",
                "force_refresh": False
            }
        }


class MotivationalSections(BaseModel):
    """3 motivational sections from Dashboard Writer Agent (TIER 2)"""
    dna: str = Field(..., description="DNA Golfístico (60-80 palabras)")
    progress: str = Field(..., description="Evolución/Progreso (50-70 palabras)")
    action: str = Field(..., description="Próximo Nivel/Acción (70-90 palabras)")


class AnalyzeResponse(BaseModel):
    """Response for POST /analyze endpoint (TIER 2)"""
    technical_analysis: str = Field(..., description="Technical analysis from Analytics Pro Agent")
    motivational_sections: MotivationalSections = Field(..., description="Motivational sections from Dashboard Writer Agent")
    generated_at: datetime = Field(default_factory=datetime.now)
    tokens_used: Optional[int] = None
    cache_hit: bool = False


# ============ Content Generation (Team 3 - UXWriter) ============

class ContentGenerateRequest(BaseModel):
    """Request for POST /generate-content endpoint"""
    user_id: str = Field(..., description="User ID")
    force_refresh: bool = Field(False, description="Force fresh content generation")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alvaro",
                "force_refresh": False
            }
        }


class ContentGenerateResponse(BaseModel):
    """Response for POST /generate-content endpoint (Team 3 - AgentUXWriter)"""
    content: dict = Field(..., description="Dashboard content sections (hero_statement, dna_profile, stat_cards, etc.)")
    metadata: dict = Field(..., description="Generation metadata (model, content_length, etc.)")
    generated_at: datetime = Field(default_factory=datetime.now)


# ============ Coach Report ============

class CoachReportRequest(BaseModel):
    """Request for POST /generate-coach endpoint"""
    user_id: str = Field(..., description="User ID")
    force_refresh: bool = Field(False, description="Force fresh report generation")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alvaro",
                "force_refresh": False
            }
        }


class CoachReportResponse(BaseModel):
    """Response for POST /generate-coach endpoint (AgentCoach standalone)"""
    report: str = Field(..., description="Coaching report in Markdown format")
    metadata: dict = Field(..., description="Generation metadata")
    generated_at: datetime = Field(default_factory=datetime.now)


# ============ Error ============

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
