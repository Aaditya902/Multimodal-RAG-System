from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any
from models.result import SearchResult
from models.chunk import Chunk

class BaseRetriever(ABC):
    
    @abstractmethod
    def add_documents(self, chunks: List[Chunk]) -> None:
        pass
    
    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        pass
    
    @abstractmethod
    def delete_documents(self, document_ids: List[str]) -> None:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass
    
    @property
    @abstractmethod
    def total_documents(self) -> int:
        pass
    
    def batch_search(self, queries: List[str], k: int = 5) -> List[List[SearchResult]]:
        return [self.search(q, k) for q in queries]