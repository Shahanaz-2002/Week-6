# main.py

import time
from typing import Dict

from embedding import EmbeddingEngine
from similarity_engine import SimilarityEngine
from insight_aggregator import InsightAggregator
from confidence_engine import ConfidenceEngine
from explanation_generator import ExplanationGenerator

from utils import validate_case_input, format_output, log
from config import TOP_K, EMBEDDING_DIM
from database import fetch_case_database, fetch_case_embeddings


def main():

    try:

        start_time = time.time()

        # Load Data
        log("Loading case database...")
        case_database: Dict = fetch_case_database()

        log("Loading case embeddings...")
        case_embeddings = fetch_case_embeddings()

        # Initialize Engines
        embedding_engine = EmbeddingEngine(embedding_dim=EMBEDDING_DIM)
        similarity_engine = SimilarityEngine(case_embeddings)
        insight_aggregator = InsightAggregator()
        confidence_engine = ConfidenceEngine()
        explanation_generator = ExplanationGenerator()

        # Test Query Cases
        test_cases = [
            {
                "case_id": "NEW_SKIN_003",
                "clinic_id": "CLINIC_001",
                "symptoms": ["pus-filled pimples on cheeks", "oily skin"],
                "duration_days": 60,
                "doctor_notes": "Inflammatory acne lesions with occasional scarring.",
                "diagnosis": "",
                "treatment": "",
                "outcome": "",
                "recovery_days": None,
                "patient": {"age": 24, "gender": "Female"}
            }
        ]

        # Process Each Case
        for new_case in test_cases:

            log(f"Processing {new_case['case_id']}")

            # Validate input
            validate_case_input(new_case)

            # Generate embedding
            query_embedding = embedding_engine.generate_embedding(new_case)

            # Retrieve similar cases
            top_matches = similarity_engine.retrieve_top_k(
                query_embedding,
                top_k=TOP_K
            )

            # Collect full case details
            retrieved_cases = []

            for case_id, similarity_score in top_matches:

                if case_id in case_database:

                    case = case_database[case_id].copy()
                    case["similarity"] = similarity_score
                    retrieved_cases.append(case)

            # Generate Insights
            insight = insight_aggregator.aggregate_insights(retrieved_cases)

            # Compute Confidence Score
            confidence = confidence_engine.compute_confidence(retrieved_cases)

            insight["confidence_score"] = confidence["confidence_score"]
            insight["confidence_level"] = confidence["confidence_level"]

            # Generate Clinical Explanation
            explanation = explanation_generator.generate_explanation(
                insight,
                retrieved_cases
            )

            insight["clinical_explanation"] = explanation

            # Format Final Output
            result = format_output(
                query_case_id=new_case["case_id"],
                top_matches=top_matches,
                insight=insight
            )

            print(result)

        end_time = time.time()

        log(f"Execution Time: {end_time - start_time:.2f} sec")

    except Exception as e:

        log(f"ERROR: {str(e)}")


if __name__ == "__main__":
    main()