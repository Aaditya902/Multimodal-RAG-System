from typing import List, Union, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st

from .base import BaseEmbedding

class SentenceTransformerEmbedding(BaseEmbedding):
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # Use private variable, not property
        self._model_name = model_name
        self._model = None
        self._dimension = None
    
    @property
    def model(self):
        if self._model is None:
            self._model = self._load_model()
        return self._model
    
    @staticmethod
    @st.cache_resource
    def _load_model_static(model_name):
        return SentenceTransformer(model_name)
    
    def _load_model(self):
        return self._load_model_static(self._model_name)
    
    def embed(self, text: Union[str, List[str]]) -> np.ndarray:
        if isinstance(text, str):
            return self.model.encode([text])[0]
        return self.model.encode(text)
    
    def embed_query(self, text: str) -> np.ndarray:
        return self.embed(text)
    
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        return self.embed(texts)
    
    @property
    def dimension(self) -> int:
        if self._dimension is None:
            test_embedding = self.embed("test")
            self._dimension = len(test_embedding)
        return self._dimension
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    def __repr__(self) -> str:
        return f"SentenceTransformerEmbedding(model='{self._model_name}', dim={self.dimension})"