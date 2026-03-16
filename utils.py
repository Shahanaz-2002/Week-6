# utils.py

import pandas as pd
from typing import Dict, Any, List, Tuple


# DATA LOADER

def load_case_database(file_path: str) -> Dict[str, Dict[str, Any]]:
    

    df = pd.read_csv(file_path)
    case_database: Dict[str, Dict[str, Any]] = {}

    for _, row in df.iterrows():

        case_id = str(row["case_id"]).strip()

        # Convert symptoms string into list
        symptoms_raw = str(row.get("symptoms", ""))
        symptoms_list = [s.strip() for s in symptoms_raw.split(",") if s.strip()]

        case_database[case_id] = {
            "symptoms": symptoms_list,
            "diagnosis": str(row.get("diagnosis", "")).strip(),
            "treatment": str(row.get("treatment", "")).strip(),
            "notes": str(row.get("doctor_notes", "")).strip(),
            "duration_days": row.get("duration_days"),
            "clinic_id": row.get("clinic_id"),
            "patient_age": row.get("patient.age"),
            "patient_gender": row.get("patient.gender"),
            "outcome": str(row.get("outcome", "")).strip(),
            "recovery_days": row.get("recovery_days"),
        }

    return case_database


# INPUT VALIDATION

def validate_case_input(case_input: Dict[str, Any]) -> bool:
    

    required_fields = ["symptoms"]

    for field in required_fields:
        if field not in case_input:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(case_input["symptoms"], list):
        raise ValueError("Symptoms must be provided as a list.")

    return True


# OUTPUT FORMATTER

def format_output(
    query_case_id: str,
    top_matches: List[Tuple[str, float]],
    insight: Dict[str, Any]
) -> str:
    

    result = "\n==== CCMS-AI RESULT ====\n\n"

    result += f"Query Case ID: {query_case_id}\n\n"

    # Similar cases
    result += "🔎 Top Similar Cases:\n"

    if not top_matches:
        result += "No similar cases found.\n"
    else:
        for case_id, similarity in top_matches:
            result += f"- Case ID: {case_id} | Similarity: {similarity:.4f}\n"

    # Diagnosis
    diagnosis = insight.get(
        "diagnosis",
        "No confident diagnosis could be inferred from the retrieved cases."
    )

    result += "\n🩺 Predicted Diagnosis:\n"
    result += f"{diagnosis}\n"

    # Treatment
    treatment = insight.get(
        "treatment",
        "No treatment recommendation available due to insufficient matching cases."
    )

    result += "\n💊 Suggested Treatment:\n"
    result += f"{treatment}\n"

    # Confidence output
    confidence_score = insight.get("confidence_score", "N/A")
    confidence_level = insight.get(
        "confidence_level",
        "Confidence could not be determined."
    )

    result += "\n📊 Confidence Score:\n"
    result += f"{confidence_score}\n"

    result += "\n📈 Confidence Level:\n"
    result += f"{confidence_level}\n"

    # Clinical Explanation (NEW SECTION)
    explanation = insight.get(
        "clinical_explanation",
        "No clinical explanation available."
    )

    result += "\n🧠 Clinical Explanation:\n"
    result += f"{explanation}\n"

    result += "\n===============================================\n"

    return result


# LOGGER

def log(message: str) -> None:
    
    print(f"[CCMS-AI] {message}")