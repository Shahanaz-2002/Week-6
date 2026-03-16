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

    # Create case object similar to main pipeline
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

    retrieved_cases = []

    for case_id, similarity_score in top_matches:

        if case_id in case_database:

            case_data = case_database[case_id].copy()
            case_data["similarity"] = similarity_score
            retrieved_cases.append(case_data)

    # Generate insight
    insight = insight_aggregator.aggregate_insights(retrieved_cases)

    # Compute confidence
    confidence = confidence_engine.compute_confidence(retrieved_cases)

    insight["confidence_score"] = confidence["confidence_score"]
    insight["confidence_level"] = confidence["confidence_level"]

    # Generate explanation
    explanation = explanation_generator.generate_explanation(
        insight,
        retrieved_cases
    )

    # Format similar cases
    similar_cases = [
        {
            "case_id": case_id,
            "similarity": round(sim, 4)
        }
        for case_id, sim in top_matches
    ]

    # API Response
    return {
        "similar_cases": similar_cases,
        "treatment_pattern": insight.get("treatment"),
        "confidence": {
            "score": insight.get("confidence_score"),
            "level": insight.get("confidence_level")
        },
        "explanation": explanation
    }