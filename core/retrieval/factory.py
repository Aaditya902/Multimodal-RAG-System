"""Retriever factory for creating retriever instances"""

from typing import Optional, Dict, Any
from .base import BaseRetriever
from .faiss_retriever import FAISSRetriever
from core.embedding.factory import EmbeddingFactory

class RetrieverFactory:
    """Factory for creating retrievers"""
    
    _instances: Dict[str, BaseRetriever] = {}
    
    @classmethod
    def create(cls,
               retriever_type: str = 'faiss',
               embedding_model: Optional[str] = None,
               similarity_threshold: float = 0.3,
               use_heap: bool = True,
               cache: bool = True,
               **kwargs) -> BaseRetriever:
        """
        Create a retriever instance
        
        Args:
            retriever_type: Type of retriever ('faiss', 'simple', etc.)
            embedding_model: Name of embedding model to use
            similarity_threshold: Minimum similarity score
            use_heap: Use heap for optimization
            cache: Whether to cache the instance
            **kwargs: Additional arguments
        
        Returns:
            BaseRetriever instance
        """
        cache_key = f"{retriever_type}:{embedding_model}:{similarity_threshold}"
        
        if cache and cache_key in cls._instances:
            return cls._instances[cache_key]
        
        # Create embedding model
        if embedding_model:
            embedder = EmbeddingFactory.create(
                model_type='sentence_transformer',
                model_name=embedding_model
            )
        else:
            embedder = EmbeddingFactory.create()
        
        instance = None
        
        if retriever_type == 'faiss':
            instance = FAISSRetriever(
                embedding_model=embedder,
                similarity_threshold=similarity_threshold,
                use_heap=use_heap,
                **kwargs
            )
        elif retriever_type == 'simple':
            from .simple_retriever import SimpleRetriever
            instance = SimpleRetriever(embedder, similarity_threshold, **kwargs)
        else:
            raise ValueError(f"Unknown retriever type: {retriever_type}")
        
        if cache:
            cls._instances[cache_key] = instance
        
        return instance
    
    @classmethod
    def clear_cache(cls):
        """Clear all cached instances"""
        cls._instances.clear()