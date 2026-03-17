# ccms_ai_service.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

from embedding import EmbeddingEngine
from similarity_engine import SimilarityEngine
from insight_aggregator import InsightAggregator
from confidence_engine import ConfidenceEngine
from explanation_generator import ExplanationGenerator

from database import fetch_case_database, fetch_case_embeddings
from config import TOP_K, EMBEDDING_DIM



# Initialize FastAPI App


app = FastAPI(title="CCMS AI Clinical Insight Service")



# Load database once when server starts
case_database: Dict = fetch_case_database()
case_embeddings = fetch_case_embeddings()

embedding_engine = EmbeddingEngine(embedding_dim=EMBEDDING_DIM)
similarity_engine = SimilarityEngine(case_embeddings)
insight_aggregator = InsightAggregator()
confidence_engine = ConfidenceEngine()
explanation_generator = ExplanationGenerator()



# Input Schema
class CaseInput(BaseModel):

    symptoms: List[str]
    doctor_notes: str

# API Endpoint
@app.post("/analyze-case")

def analyze_case(case: CaseInput):

    # Prepare patient case
    new_case = {
        "symptoms": case.symptoms,
        "doctor_notes": case.doctor_notes
    }

    # Generate embedding
    query_embedding = embedding_engine.generate_embedding(new_case)

    # Retrieve similar cases
    top_matches = similarity_engine.retrieve_top_k(
        query_embedding,
        top_k=TOP_K
    )

    # Safety check if nothing retrieved
    if not top_matches:
        return {
            "similar_cases": [],
            "diagnosis": "No diagnosis available",
            "treatment_pattern": "No treatment pattern found",
            "confidence": {
                "score": 0,
                "level": "Very Low Confidence"
            },
            "explanation": "No similar clinical cases were found in the database."
        }

    # Collect retrieved case data
    retrieved_cases = []

    for case_id, similarity_score in top_matches:

        if case_id in case_database:

            case_data = case_database[case_id].copy()
            case_data["similarity"] = float(similarity_score)

            retrieved_cases.append(case_data)

    # Generate insight from retrieved cases
    insight = insight_aggregator.aggregate_insights(retrieved_cases)

    # Compute confidence
    confidence = confidence_engine.compute_confidence(retrieved_cases)

    insight["confidence_score"] = confidence.get("confidence_score", 0)
    insight["confidence_level"] = confidence.get("confidence_level", "Very Low")

    # Generate clinical explanation
    explanation = explanation_generator.generate_explanation(
        insight,
        retrieved_cases
    )

    # Format similar cases for response
    similar_cases = [
        {
            "case_id": case_id,
            "similarity": round(float(sim), 4)
        }
        for case_id, sim in top_matches
    ]

    # Return API response
    return {

        "similar_cases": similar_cases,

        "diagnosis": insight.get("diagnosis", "Unknown condition"),

        "treatment_pattern": insight.get(
            "treatment",
            "No treatment pattern found"
        ),

        "confidence": {
            "score": insight.get("confidence_score", 0),
            "level": insight.get("confidence_level", "Very Low Confidence")
        },

        "explanation": explanation
    }