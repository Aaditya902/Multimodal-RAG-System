"""Base embedding interface"""

from abc import ABC, abstractmethod
from typing import List, Union
import numpy as np

class BaseEmbedding(ABC):
    """Abstract base class for all embedding models"""
    
    @abstractmethod
    def embed(self, text: Union[str, List[str]]) -> np.ndarray:
        """Generate embeddings for text(s)"""
        pass
    
    @abstractmethod
    def embed_query(self, text: str) -> np.ndarray:
        """Generate embedding for a query"""
        pass
    
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for documents"""
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Get embedding dimension"""
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get model name (getter only, no setter)"""
        pass
    
    def batch_embed(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings in batches"""
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_embeddings = self.embed(batch)
            all_embeddings.extend(batch_embeddings)
        return np.array(all_embeddings)