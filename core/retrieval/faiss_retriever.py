"""FAISS-based retriever implementation"""

import numpy as np
import faiss
from typing import List, Tuple, Optional, Any
import heapq
from datetime import datetime

from .base import BaseRetriever
from models.chunk import Chunk
from models.result import SearchResult
from core.embedding.base import BaseEmbedding

class FAISSRetriever(BaseRetriever):
    """Retriever using FAISS for similarity search"""
    
    def __init__(self, 
                 embedding_model: BaseEmbedding,
                 similarity_threshold: float = 0.3,
                 use_heap: bool = True):
        
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        self.use_heap = use_heap
        
        self.index: Optional[faiss.Index] = None
        self.chunks: List[Chunk] = []
        self.embeddings: Optional[np.ndarray] = None
    
    def add_documents(self, chunks: List[Chunk]) -> None:
        """Add chunks to FAISS index"""
        if not chunks:
            return
        
        # Get embeddings
        texts = [chunk.content for chunk in chunks]
        new_embeddings = self.embedding_model.embed_documents(texts)
        
        # Initialize index if needed
        if self.index is None:
            self.index = faiss.IndexFlatL2(new_embeddings.shape[1])
            self.chunks = chunks
            self.embeddings = new_embeddings
        else:
            # Append to existing
            self.chunks.extend(chunks)
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
        
        # Add to FAISS
        self.index.add(new_embeddings)
    
    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        """Search for relevant chunks"""
        if self.index is None or not self.chunks:
            return []
        
        # Get query embedding
        query_embedding = self.embedding_model.embed_query(query)
        query_embedding = np.array([query_embedding])
        
        # Search
        search_k = min(k * 3, len(self.chunks))
        distances, indices = self.index.search(query_embedding, search_k)
        
        if self.use_heap:
            results = self._search_with_heap(distances[0], indices[0], query, k)
        else:
            results = self._search_simple(distances[0], indices[0], query, k)
        
        return results
    
    def _search_simple(self, distances, indices, query: str, k: int) -> List[SearchResult]:
        """Simple search without heap"""
        results = []
        for i, idx in enumerate(indices):
            if idx != -1 and idx < len(self.chunks):
                similarity = 1 / (1 + distances[i])
                if similarity >= self.similarity_threshold:
                    results.append(SearchResult(
                        chunk=self.chunks[idx],
                        score=similarity,
                        query=query,
                        rank=len(results) + 1
                    ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:k]
    
    def _search_with_heap(self, distances, indices, query: str, k: int) -> List[SearchResult]:
        """Search using heap for better performance"""
        heap = []
        
        for i, idx in enumerate(indices):
            if idx != -1 and idx < len(self.chunks):
                similarity = 1 / (1 + distances[i])
                if similarity >= self.similarity_threshold:
                    if len(heap) < k:
                        heapq.heappush(heap, (similarity, idx))
                    else:
                        heapq.heappushpop(heap, (similarity, idx))
        
        # Extract results in order
        results = []
        rank = len(heap)
        while heap:
            sim, idx = heapq.heappop(heap)
            results.append(SearchResult(
                chunk=self.chunks[idx],
                score=sim,
                query=query,
                rank=rank
            ))
            rank -= 1
        
        return results[::-1]  # Reverse for descending order
    
    def delete_documents(self, document_ids: List[str]) -> None:
        """Delete documents (reindex needed for FAISS)"""
        # FAISS doesn't support deletion easily
        # This would require rebuilding index
        raise NotImplementedError("FAISS requires reindexing for deletion")
    
    def clear(self) -> None:
        """Clear all documents"""
        self.index = None
        self.chunks = []
        self.embeddings = None
    
    @property
    def total_documents(self) -> int:
        return len(self.chunks)