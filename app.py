from fastapi import FastAPI, HTTPException
from typing import Dict
import time

from models import CaseRequest, CaseResponse, SimilarCase, SystemMetrics
from embedding import EmbeddingEngine
from similarity_engine import SimilarityEngine
from insight_generator import InsightGenerator
from database import fetch_case_database
from config import TOP_K, EMBEDDING_DIM


app = FastAPI(title="CCMS AI Similarity Engine")


embedding_engine = EmbeddingEngine(embedding_dim=EMBEDDING_DIM)
case_database: Dict = {}
similarity_engine: SimilarityEngine = None
insight_generator: InsightGenerator = None
response_cache = {}



# STARTUP INITIALIZATION

@app.on_event("startup")
def initialize_system():

    global case_database, similarity_engine, insight_generator

    case_database = fetch_case_database()

    if not case_database:
        print("⚠ No cases found in database.")
        return

    case_embeddings = {}

    for case_id, case_data in case_database.items():
        embedding = embedding_engine.generate_embedding(case_data)
        case_embeddings[case_id] = embedding

    similarity_engine = SimilarityEngine(case_embeddings)
    insight_generator = InsightGenerator(case_database)

    print("System initialized successfully.")



# OUTPUT QUALITY

def determine_output_quality(confidence_reason: str) -> str:

    if "High" in confidence_reason:
        return "High"
    elif "Moderate" in confidence_reason:
        return "Moderate"
    else:
        return "Low"



# MAIN API ENDPOINT
@app.post("/analyze-case", response_model=CaseResponse)
def analyze_case(request: CaseRequest):

    start_time = time.time()

    request_key = str(request.symptoms) + request.doctor_notes

    # CACHE CHECK
    if request_key in response_cache:
        return response_cache[request_key]

    try:

        if not case_database or similarity_engine is None:
            raise HTTPException(
                status_code=500,
                detail="System not initialized properly."
            )

        # Prepare input case
        new_case = {
            "symptoms": request.symptoms,
            "diagnosis": "",
            "notes": request.doctor_notes,
        }

        # Generate embedding
        query_embedding = embedding_engine.generate_embedding(new_case)

        # Retrieve similar cases
        top_matches = similarity_engine.retrieve_top_k(
            query_embedding,
            top_k=TOP_K
        )

        similar_cases = [
            SimilarCase(
                case_id=case_id,
                similarity_score=score
            )
            for case_id, score in top_matches
        ]

        
        # STRUCTURED INSIGHT
        
        insight = insight_generator.generate_insight(top_matches)

        predicted_diagnosis = insight["predicted_diagnosis"]
        suggested_treatment = insight["suggested_treatment"]
        confidence_score = insight["confidence_score"]
        confidence_reason = insight["confidence_reason"]
        explanation = insight["explanation"]

        # Measure Response Time
        end_time = time.time()
        response_time_ms = (end_time - start_time) * 1000

        # Determine Output Quality
        output_quality = determine_output_quality(confidence_reason)

        system_metrics = SystemMetrics(
            response_time_ms=round(response_time_ms, 2),
            output_quality=output_quality
        )

        # FINAL STRUCTURED RESPONSE
        
        response = CaseResponse(
            similar_cases=similar_cases,

            predicted_diagnosis=predicted_diagnosis,
            suggested_treatment=suggested_treatment,

            confidence_score=confidence_score,
            confidence_reason=confidence_reason,

            explanation=explanation,

            system_metrics=system_metrics
        )

        # Cache result
        response_cache[request_key] = response

        return response

    except Exception:

        return CaseResponse(
            similar_cases=[],

            predicted_diagnosis="Error",
            suggested_treatment="Error",

            confidence_score=0.0,
            confidence_reason="Unable to compute similarity.",

            explanation="System error occurred.",

            system_metrics=SystemMetrics(
                response_time_ms=0.0,
                output_quality="Error"
            )
        )