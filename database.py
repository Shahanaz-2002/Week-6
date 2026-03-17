# database.py

from pymongo import MongoClient
import numpy as np
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME


# CONNECT TO MONGODB

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


# FETCH FULL CASE DATABASE

def fetch_case_database():

    case_database = {}

    try:

        records = list(collection.find({}))

        for record in records:

            case_id = record.get("case_id")

            if not case_id:
                continue

            case_id = str(case_id)

            # Get symptoms
            symptoms = record.get("symptoms", "")

            # Convert symptoms string → list
            if isinstance(symptoms, str):
                symptoms = [s.strip() for s in symptoms.split(",") if s.strip()]

            # Clinical fields
            diagnosis = record.get("diagnosis")
            treatment = record.get("treatment")

            case_database[case_id] = {
                "symptoms": symptoms,
                "diagnosis": diagnosis if diagnosis else None,
                "treatment": treatment if treatment else None,
                "notes": record.get("doctor_notes", ""),
                "embedding": record.get("embedding"),
                "embedding_version": record.get("embedding_version")
            }

    except Exception as e:
        print("MongoDB Error while fetching case database:", e)

    return case_database


# FETCH STORED EMBEDDINGS

def fetch_case_embeddings():

    embeddings = {}

    try:

        records = list(collection.find({}))

        for record in records:

            case_id = record.get("case_id")

            if not case_id:
                continue

            case_id = str(case_id)

            embedding = record.get("embedding")

            if embedding is not None and len(embedding) > 0:

                embeddings[case_id] = np.array(embedding, dtype=float)

    except Exception as e:
        print("MongoDB Error while fetching embeddings:", e)

    return embeddings