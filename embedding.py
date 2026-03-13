import numpy as np
from typing import Dict, Any
import torch
from transformers import AutoTokenizer, AutoModel


class BioBERTEmbedding:

    def __init__(self):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"

        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = AutoModel.from_pretrained(self.MODEL_NAME)

        self.model.to(self.device)
        self.model.eval()

    def mean_pooling(self, model_output, attention_mask):

        token_embeddings = model_output.last_hidden_state

        input_mask_expanded = attention_mask.unsqueeze(-1).expand(
            token_embeddings.size()
        ).float()

        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)

        sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)

        return sum_embeddings / sum_mask

    def get_embedding(self, text: str) -> np.ndarray:

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        embedding = self.mean_pooling(
            outputs,
            inputs["attention_mask"]
        ).cpu().numpy()[0]

        norm = np.linalg.norm(embedding)

        if norm > 0:
            embedding = embedding / norm
        else:
            embedding = np.zeros_like(embedding)

        return embedding


class EmbeddingEngine:

    def __init__(self, embedding_dim: int = 768):

        self.embedding_dim = embedding_dim

        self.embedding_model = BioBERTEmbedding()

        # Metadata for embedding storage
        self.embedding_model_name = "BioClinicalBERT"
        self.embedding_version = "v1"

    # Generate embedding for retrieval
    def generate_embedding(self, case_data: Dict[str, Any]) -> np.ndarray:

        processed_text = self._preprocess_case(case_data)

        embedding_vector = self.embedding_model.get_embedding(processed_text)

        return embedding_vector

    # Convert embedding for MongoDB storage
    def generate_embedding_for_storage(self, case_data: Dict[str, Any]) -> Dict[str, Any]:

        embedding_vector = self.generate_embedding(case_data)

        return {
            "embedding": embedding_vector.tolist(),
            "embedding_model": self.embedding_model_name,
            "embedding_version": self.embedding_version
        }

    # Convert clinical case into text
    def _preprocess_case(self, case_data: Dict[str, Any]) -> str:

        symptoms = case_data.get("symptoms", [])

        diagnosis = case_data.get("diagnosis", "")

        notes = case_data.get("doctor_notes", case_data.get("notes", ""))

        combined_text = " ".join(symptoms) + " " + diagnosis + " " + notes

        return combined_text.lower().strip()