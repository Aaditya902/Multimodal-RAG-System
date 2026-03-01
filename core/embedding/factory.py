
from typing import Optional, Dict, Any
from .base import BaseEmbedding
from .sentence_transformer import SentenceTransformerEmbedding

class EmbeddingFactory:
    
    _instances: Dict[str, BaseEmbedding] = {}
    
    @classmethod
    def create(cls, 
               model_type: str = 'sentence_transformer',
               model_name: Optional[str] = None,
               cache: bool = True,
               **kwargs) -> BaseEmbedding:

        cache_key = f"{model_type}:{model_name}"
        
        if cache and cache_key in cls._instances:
            return cls._instances[cache_key]
        
        if model_type == 'sentence_transformer':
            if model_name is None:
                model_name = 'all-MiniLM-L6-v2'
            instance = SentenceTransformerEmbedding(model_name)
        else:
            raise ValueError(f"Unknown embedding type: {model_type}")
        
        if cache:
            cls._instances[cache_key] = instance
        
        return instance
    
    @classmethod
    def clear_cache(cls):
        cls._instances.clear()