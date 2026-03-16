# confidence_engine.py

from config import TOP_K


class ConfidenceEngine:

    def compute_confidence(self, retrieved_cases):

        # If no cases retrieved
        if not retrieved_cases:
            return {
                "confidence_score": 0.0,
                "confidence_level": "No similar cases found"
            }

        # Extract similarity scores
        similarities = [case["similarity"] for case in retrieved_cases]

        # Average similarity
        avg_similarity = sum(similarities) / len(similarities)

        # Number of supporting cases
        support_ratio = len(retrieved_cases) / TOP_K

        # Confidence formula
        confidence_score = (0.7 * avg_similarity) + (0.3 * support_ratio)

        # Threshold logic
        if confidence_score >= 0.85:
            level = "Very High Confidence"
        elif confidence_score >= 0.70:
            level = "High Confidence"
        elif confidence_score >= 0.50:
            level = "Moderate Confidence"
        else:
            level = "Low Confidence"

        return {
            "confidence_score": round(confidence_score, 3),
            "confidence_level": level
        }