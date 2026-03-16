# insight_aggregator.py

class InsightAggregator:

    def aggregate_insights(self, retrieved_cases):

        if not retrieved_cases:
            return {
                "diagnosis": "No similar clinical cases were retrieved from the database.",
                "treatment": "Treatment recommendation cannot be generated due to lack of similar cases.",
                "confidence": "Confidence score unavailable because no case similarity was established."
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
            predicted_diagnosis = "No confident diagnosis could be inferred from the retrieved cases."
        else:
            predicted_diagnosis = max(diagnosis_count, key=diagnosis_count.get)

        if not treatment_count:
            predicted_treatment = "No treatment recommendation available due to insufficient matching cases."
        else:
            predicted_treatment = max(treatment_count, key=treatment_count.get)

        confidence = (
            round(max(diagnosis_count.values()), 3)
            if diagnosis_count
            else "Confidence score unavailable because no valid diagnosis was determined."
        )

        return {
            "diagnosis": predicted_diagnosis,
            "treatment": predicted_treatment,
            "confidence": confidence
        }