# insight_generator.py

from typing import Dict, List, Tuple
from collections import Counter


class InsightGenerator:

    def __init__(self, case_database: Dict[str, Dict]):
        self.case_database = case_database


    
    # MAIN INSIGHT GENERATION FUNCTION
   
    def generate_insight(
        self,
        top_matches: List[Tuple[str, float]]
    ) -> Dict:

        # No Similar Cases Found
        if not top_matches:
            return {
                "predicted_diagnosis": "N/A",
                "suggested_treatment": "N/A",
                "confidence_score": 0.0,
                "confidence_reason": "Insufficient similarity data.",
                "explanation": "No similar historical cases found."
            }

        diagnoses = []
        treatments = []

        # Collect Diagnosis & Treatment
        for case_id, score in top_matches:
            case_data = self.case_database.get(case_id, {})

            diagnosis = case_data.get("diagnosis", "insufficient data")
            treatment = case_data.get("treatment", "insufficient data")

            if diagnosis:
                diagnoses.append(diagnosis)

            if treatment:
                treatments.append(treatment)

        # Most common values
        most_common_diagnosis = self._most_common(diagnoses)
        recommended_treatment = self._most_common(treatments)

        # Generate explanation
        summary = self._generate_summary(
            most_common_diagnosis,
            recommended_treatment
        )

        # Confidence
        confidence_reason = self._generate_confidence(top_matches)
        confidence_score = self._numeric_confidence(top_matches)

        # Final structured output
        return {
            "predicted_diagnosis": most_common_diagnosis,
            "suggested_treatment": recommended_treatment,
            "confidence_score": confidence_score,
            "confidence_reason": confidence_reason,
            "explanation": summary
        }


    
    # SUMMARY GENERATION 
    
    def _generate_summary(
        self,
        diagnosis: str,
        treatment: str
    ) -> str:

        if diagnosis == "insufficient data" and treatment == "insufficient data":
            return (
                "Similar cases were identified, but structured diagnosis "
                "and treatment data are not available for recommendation."
            )

        if diagnosis != "insufficient data" and treatment == "insufficient data":
            return (
                f"In similar past cases, patients were commonly diagnosed with "
                f"{diagnosis}. Treatment patterns were not consistently recorded."
            )

        if diagnosis == "insufficient data" and treatment != "insufficient data":
            return (
                f"In similar past cases, patients responded well to "
                f"{treatment}, although diagnosis data was limited."
            )

        return (
            f"In similar past cases, patients were commonly diagnosed with "
            f"{diagnosis} and responded well to {treatment}."
        )


    
    # MOST COMMON ITEM
   
    @staticmethod
    def _most_common(items: List[str]) -> str:
        if not items:
            return "insufficient data"
        return Counter(items).most_common(1)[0][0]


    
    # TEXT CONFIDENCE
    
    @staticmethod
    def _generate_confidence(
        top_matches: List[Tuple[str, float]]
    ) -> str:

        if not top_matches:
            return "Insufficient similarity data."

        scores = [score for _, score in top_matches]

        avg_score = sum(scores) / len(scores)
        max_score = max(scores)

        if avg_score > 0.85 and max_score > 0.9:
            return "High confidence based on strong similarity with historical cases."
        elif avg_score > 0.65:
            return "Moderate confidence based on similarity patterns."
        else:
            return "Low similarity confidence. Clinical review advised."


   
    # NUMERIC CONFIDENCE
   
    @staticmethod
    def _numeric_confidence(
        top_matches: List[Tuple[str, float]]
    ) -> float:

        if not top_matches:
            return 0.0

        scores = [score for _, score in top_matches]
        return round(sum(scores) / len(scores), 2)