# insight_aggregator.py

class InsightAggregator:

    def aggregate_insights(self, retrieved_cases):

        if not retrieved_cases:
            return {
                "diagnosis": "N/A",
                "treatment": "N/A",
                "confidence": "N/A"
            }

        diagnosis_count = {}
        treatment_count = {}

        for case in retrieved_cases:

            diagnosis = case.get("diagnosis")
            treatment = case.get("treatment")
            similarity = case.get("similarity", 0)

            if diagnosis:

                if diagnosis not in diagnosis_count:
                    diagnosis_count[diagnosis] = 0

                diagnosis_count[diagnosis] += similarity

            if treatment:

                if treatment not in treatment_count:
                    treatment_count[treatment] = 0

                treatment_count[treatment] += similarity

        if not diagnosis_count:
            predicted_diagnosis = "N/A"
        else:
            predicted_diagnosis = max(diagnosis_count, key=diagnosis_count.get)

        if not treatment_count:
            predicted_treatment = "N/A"
        else:
            predicted_treatment = max(treatment_count, key=treatment_count.get)

        confidence = round(max(diagnosis_count.values()), 3) if diagnosis_count else "N/A"

        return {
            "diagnosis": predicted_diagnosis,
            "treatment": predicted_treatment,
            "confidence": confidence
        }