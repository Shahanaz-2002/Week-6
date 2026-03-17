from pydantic import BaseModel, Field
from typing import List


# REQUEST MODEL
class CaseRequest(BaseModel):
    symptoms: List[str] = Field(..., min_items=1)
    doctor_notes: str = Field(..., min_length=3)



# SIMILAR CASE MODEL
class SimilarCase(BaseModel):
    case_id: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)


# SYSTEM METRICS MODEL
class SystemMetrics(BaseModel):
    response_time_ms: float = Field(..., ge=0)
    output_quality: str = Field(..., min_length=1)


# FINAL RESPONSE MODEL 
class CaseResponse(BaseModel):
    similar_cases: List[SimilarCase]

    predicted_diagnosis: str = Field(..., min_length=1)
    suggested_treatment: str = Field(..., min_length=1)

    confidence_score: float = Field(..., ge=0.0, le=1.0)
    confidence_reason: str = Field(..., min_length=1)

    explanation: str = Field(..., min_length=1)

    system_metrics: SystemMetrics