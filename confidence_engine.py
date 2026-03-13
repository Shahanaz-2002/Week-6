# confidence_engine.py

from typing import List, Dict


class ConfidenceEngine:
    

    def __init__(self, max_cases: int = 5):
        self.max_cases = max_cases

    def compute_average_similarity(self, cases: List[Dict]) -> float:
        
        if not cases:
            return 0.0

        scores = [case["similarity"] for case in cases]

        return sum(scores) / len(scores)

    def compute_support_factor(self, cases: List[Dict]) -> float:
        
        if not cases:
            return 0.0

        support = len(cases) / self.max_cases
        return min(support, 1.0)

    def compute_confidence_score(self, cases: List[Dict]) -> float:
        
        if not cases:
            return 0.0

        avg_similarity = self.compute_average_similarity(cases)
        support_factor = self.compute_support_factor(cases)

        confidence = (0.7 * avg_similarity) + (0.3 * support_factor)

        return round(confidence, 4)

    def classify_confidence(self, score: float) -> str:
        
        if score >= 0.85:
            return "Very High"
        elif score >= 0.70:
            return "High"
        elif score >= 0.50:
            return "Moderate"
        else:
            return "Low"

    def evaluate(self, cases: List[Dict]) -> Dict:
        

        score = self.compute_confidence_score(cases)
        level = self.classify_confidence(score)

        return {
            "confidence_score": score,
            "confidence_level": level,
            "supporting_cases": len(cases)
        }