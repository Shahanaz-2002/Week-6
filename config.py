# config.py

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "ccms_training"
COLLECTION_NAME = "clinic_cases"

# Retrieval Configuration
TOP_K = 3
EMBEDDING_DIM = 768

# API Configuration
API_HOST = "127.0.0.1"
API_PORT = 8000

# Confidence Thresholds
VERY_HIGH_CONFIDENCE = 0.85
HIGH_CONFIDENCE = 0.70
MODERATE_CONFIDENCE = 0.50