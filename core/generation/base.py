from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from models.result import SearchResponse, SearchResult

class BaseGenerator(ABC):
    
    @abstractmethod
    def generate(self, query: str, context: List[SearchResult], **kwargs) -> str:
        pass
    
    @abstractmethod
    def generate_with_sources(self, query: str, context: List[SearchResult], **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
    
    def batch_generate(self, queries: List[str], contexts: List[List[SearchResult]]) -> List[str]:
        return [self.generate(q, c) for q, c in zip(queries, contexts)]
    
    def format_context(self, results: List[SearchResult], max_chunks: int = 3) -> str:
        context_parts = []
        
        for i, result in enumerate(results[:max_chunks]):
            source = result.chunk.source_file
            content = result.chunk.content
            context_parts.append(f"[Document {i+1} from {source}]:\n{content}")
        
        return '\n\n'.join(context_parts)