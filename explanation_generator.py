# explanation_generator.py

class ExplanationGenerator:
    """
    Generates doctor-readable explanations from aggregated insights
    and retrieved clinical cases.
    """

    def generate_explanation(self, insight, retrieved_cases):

        # If no cases retrieved
        if not retrieved_cases:
            return (
                "No similar historical clinical cases were found. "
                "Clinical recommendation should be made cautiously."
            )

        # Correct keys from insight aggregator
        diagnosis = insight.get("diagnosis", "the identified condition")
        treatment = insight.get("treatment", "the recommended treatment")

        case_count = len(retrieved_cases)

        # Calculate average similarity
        similarities = [case["similarity"] for case in retrieved_cases]
        avg_similarity = sum(similarities) / len(similarities)

        explanation = (
            f"{case_count} similar historical clinical cases were identified "
            f"with an average similarity score of {avg_similarity:.2f}. "
            f"In these cases, the most frequent diagnosis was '{diagnosis}', "
            f"and patients responded well to the treatment '{treatment}'. "
            f"Based on these previous outcomes, this treatment may be an "
            f"effective clinical option for the current patient."
        )

        return explanation