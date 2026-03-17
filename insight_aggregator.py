# insight_aggregator.py

class InsightAggregator:

    def aggregate_insights(self, retrieved_cases):

        if not retrieved_cases:
            return {
                "diagnosis": "No similar cases found",
                "treatment": "No treatment pattern available"
            }

        diagnosis_count = {}
        treatment_count = {}

        for case in retrieved_cases:

            diagnosis = case.get("diagnosis")
            treatment = case.get("treatment")
            similarity = float(case.get("similarity", 0))

            if diagnosis:
                diagnosis_count[diagnosis] = (
                    diagnosis_count.get(diagnosis, 0) + similarity
                )

            if treatment:
                treatment_count[treatment] = (
                    treatment_count.get(treatment, 0) + similarity
                )

        # Determine most likely diagnosis
        if diagnosis_count:
            predicted_diagnosis = max(diagnosis_count, key=diagnosis_count.get)
        else:
            predicted_diagnosis = "Unknown condition"

        # Determine most frequent treatment
        if treatment_count:
            predicted_treatment = max(treatment_count, key=treatment_count.get)
        else:
            predicted_treatment = "No treatment pattern found"

        return {
            "diagnosis": predicted_diagnosis,
            "treatment": predicted_treatment
        }