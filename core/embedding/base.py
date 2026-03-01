
from abc import ABC, abstractmethod
from typing import List, Union
import numpy as np

class BaseEmbedding(ABC):
    
    @abstractmethod
    def embed(self, text: Union[str, List[str]]) -> np.ndarray:
        pass
    
    @abstractmethod
    def embed_query(self, text: str) -> np.ndarray:
        pass
    
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
    
    def batch_embed(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_embeddings = self.embed(batch)
            all_embeddings.extend(batch_embeddings)
        return np.array(all_embeddings)