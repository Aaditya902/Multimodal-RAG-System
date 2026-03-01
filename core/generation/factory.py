from typing import Optional, Dict, Any
from .base import BaseGenerator
from .gemini_generator import GeminiGenerator

class GeneratorFactory:
    
    _instances: Dict[str, BaseGenerator] = {}
    
    @classmethod
    def create(cls, 
               generator_type: str = 'gemini',
               client=None,
               model_name: Optional[str] = None,
               cache: bool = True,
               **kwargs) -> Optional[BaseGenerator]:

        cache_key = f"{generator_type}:{model_name}"
        
        if cache and cache_key in cls._instances:
            return cls._instances[cache_key]
        
        instance = None
        
        if generator_type == 'gemini':
            if client is None:
                raise ValueError("Gemini client required for gemini generator")
            instance = GeminiGenerator(client, model_name, **kwargs)
        elif generator_type == 'mock':
            # For testing
            instance = MockGenerator(**kwargs)
        else:
            raise ValueError(f"Unknown generator type: {generator_type}")
        
        if cache and instance and instance.is_available():
            cls._instances[cache_key] = instance
        
        return instance
    
    @classmethod
    def clear_cache(cls):
        cls._instances.clear()

class MockGenerator(BaseGenerator):
    
    def __init__(self, **kwargs):
        self._model_name = kwargs.get('model_name', 'mock-model')
    
    def generate(self, query: str, context: List, **kwargs) -> str:
        return f"Mock answer for: {query}"
    
    def generate_with_sources(self, query: str, context: List, **kwargs) -> Dict[str, Any]:
        return {
            'answer': self.generate(query, context),
            'sources': [c.chunk.source_file for c in context[:2]],
            'model': self.model_name
        }
    
    def is_available(self) -> bool:
        return True
    
    @property
    def model_name(self) -> str:
        return self._model_name