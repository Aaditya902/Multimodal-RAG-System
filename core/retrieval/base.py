"""Base retriever interface"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any
from models.result import SearchResult
from models.chunk import Chunk

class BaseRetriever(ABC):
    """Abstract base class for all retrievers"""
    
    @abstractmethod
    def add_documents(self, chunks: List[Chunk]) -> None:
        """Add documents to index"""
        pass
    
    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        """Search for relevant documents"""
        pass
    
    @abstractmethod
    def delete_documents(self, document_ids: List[str]) -> None:
        """Delete documents from index"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all documents"""
        pass
    
    @property
    @abstractmethod
    def total_documents(self) -> int:
        """Get total number of documents"""
        pass
    
    def batch_search(self, queries: List[str], k: int = 5) -> List[List[SearchResult]]:
        """Search multiple queries in batch"""
        return [self.search(q, k) for q in queries]