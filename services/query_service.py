import time
from typing import List, Optional, Dict, Any
import streamlit as st

from models.result import SearchResult, SearchResponse
from core.retrieval.base import BaseRetriever
from core.generation.base import BaseGenerator

class QueryService:
    
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self.retriever = retriever
        self.generator = generator
        self.query_history = []
    
    def answer(self, query: str, **kwargs) -> Dict[str, Any]:
        
        start_time = time.time()
        
        k = kwargs.get('k', st.session_state.get('max_chunks', 5))
        threshold = kwargs.get('threshold', st.session_state.get('similarity_threshold', 0.3))
        
        results = self.retriever.search(query, k=k)
        
        results = [r for r in results if r.score >= threshold]
        
        if results:
            response = self.generator.generate_with_sources(query, results, **kwargs)
            answer = response['answer']
            sources = response['sources']
        else:
            answer = "I couldn't find relevant information in your documents."
            sources = []
        
        processing_time = time.time() - start_time
        
        search_response = SearchResponse(
            query=query,
            results=results,
            total_found=len(results),
            processing_time=processing_time,
            model_used=self.generator.model_name,
            metadata={
                'threshold': threshold,
                'k': k,
                'answer': answer,
                'sources': sources
            }
        )
        
        self.query_history.append({
            'query': query,
            'timestamp': time.time(),
            'result_count': len(results),
            'processing_time': processing_time
        })
        
        return {
            'answer': answer,
            'sources': sources,
            'results': [r.to_dict() for r in results],
            'processing_time': processing_time,
            'total_found': len(results),
            'model': self.generator.model_name
        }
    
    def stream_answer(self, query: str, **kwargs):
        
        results = self.retriever.search(query, k=kwargs.get('k', 5))
        
        if not results:
            yield "I couldn't find relevant information in your documents."
            return
        
        context = self.generator.format_context(results)
        
        prompt = f"Based on this context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        
        response = self.generator.generate(query, results, **kwargs)
        
        for word in response.split():
            yield word + " "
            time.sleep(0.05)
    
    def get_query_history(self, limit: int = 10) -> List[Dict]:
        return sorted(
            self.query_history[-limit:],
            key=lambda x: x['timestamp'],
            reverse=True
        )
    
    def clear_history(self):
        self.query_history.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        
        if not self.query_history:
            return {'total_queries': 0}
        
        total = len(self.query_history)
        avg_time = sum(q['processing_time'] for q in self.query_history) / total
        total_results = sum(q['result_count'] for q in self.query_history)
        
        return {
            'total_queries': total,
            'avg_processing_time': f"{avg_time:.2f}s",
            'total_results_found': total_results,
            'avg_results_per_query': total_results / total,
            'last_query': self.query_history[-1]['query'] if total > 0 else None
        }