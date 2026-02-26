"""Sentence Transformers embedding implementation"""

from typing import List, Union, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st

from .base import BaseEmbedding

class SentenceTransformerEmbedding(BaseEmbedding):
    """Embedding using Sentence Transformers"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # Use private variable, not property
        self._model_name = model_name
        self._model = None
        self._dimension = None
    
    @property
    def model(self):
        """Lazy load model"""
        if self._model is None:
            self._model = self._load_model()
        return self._model
    
    # FIXED: Add underscore to self parameter to prevent hashing
    @staticmethod
    @st.cache_resource
    def _load_model_static(model_name):
        """Static method to load and cache the model"""
        return SentenceTransformer(model_name)
    
    def _load_model(self):
        """Wrapper to call static cached method"""
        return self._load_model_static(self._model_name)
    
    def embed(self, text: Union[str, List[str]]) -> np.ndarray:
        """Generate embeddings"""
        if isinstance(text, str):
            return self.model.encode([text])[0]
        return self.model.encode(text)
    
    def embed_query(self, text: str) -> np.ndarray:
        """Generate query embedding (same as document for this model)"""
        return self.embed(text)
    
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """Generate document embeddings"""
        return self.embed(texts)
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension"""
        if self._dimension is None:
            # Get dimension by encoding a test string
            test_embedding = self.embed("test")
            self._dimension = len(test_embedding)
        return self._dimension
    
    @property
    def model_name(self) -> str:
        """Get model name"""
        return self._model_name
    
    def __repr__(self) -> str:
        return f"SentenceTransformerEmbedding(model='{self._model_name}', dim={self.dimension})"