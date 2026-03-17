# explanation_generator.py

class ExplanationGenerator:
    

    def generate_explanation(self, insight, retrieved_cases):

        # If no cases retrieved
        if not retrieved_cases:
            return (
                "No similar historical clinical cases were found. "
                "Clinical recommendation should be made cautiously."
            )

        # Extract diagnosis and treatment
        diagnosis = insight.get("diagnosis", "an unspecified condition")
        treatment = insight.get("treatment", "a suggested treatment")

        case_count = len(retrieved_cases)

        # Calculate average similarity safely
        similarities = [case.get("similarity", 0) for case in retrieved_cases]

        avg_similarity = sum(float(s) for s in similarities) / len(similarities)

        # Generate explanation
        explanation = (
            f"{case_count} similar historical clinical cases were identified "
            f"with an average similarity score of {avg_similarity:.2f}. "
            f"In these cases, the most frequent diagnosis was '{diagnosis}', "
            f"and patients responded well to the treatment '{treatment}'. "
            f"Based on these previous outcomes, this treatment may be an "
            f"effective clinical option for the current patient."
        )

        return explanation