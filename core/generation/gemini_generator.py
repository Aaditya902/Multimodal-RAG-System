"""Gemini-based answer generator"""

from typing import List, Dict, Any, Optional
import streamlit as st

from .base import BaseGenerator
from models.result import SearchResult
from constants.messages import PROMPTS

class GeminiGenerator(BaseGenerator):
    """Answer generator using Google's Gemini"""
    
    def __init__(self, client, model_name: str = "models/gemini-2.5-flash", temperature: float = 0.3):
        self.client = client
        self._model_name = model_name
        self.temperature = temperature
        self._available = None
    
    def generate(self, query: str, context: List[SearchResult], **kwargs) -> str:
        """Generate answer using Gemini"""
        
        if not context:
            return "No relevant context found to answer the question."
        
        # Format context
        formatted_context = self.format_context(context, kwargs.get('max_chunks', 3))
        
        # Create prompt
        prompt = PROMPTS['qa_system'].format(
            context=formatted_context,
            query=query
        )
        
        try:
            # Track API call
            st.session_state['gemini_text_calls'] = st.session_state.get('gemini_text_calls', 0) + 1
            
            # Generate response
            response = self.client.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config={
                    "temperature": kwargs.get('temperature', self.temperature),
                    "max_output_tokens": kwargs.get('max_tokens', 1024),
                }
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def generate_with_sources(self, query: str, context: List[SearchResult], **kwargs) -> Dict[str, Any]:
        """Generate answer with source attribution"""
        
        answer = self.generate(query, context, **kwargs)
        
        # Extract sources
        sources = []
        for result in context[:3]:
            sources.append({
                'file': result.chunk.source_file,
                'relevance': result.score,
                'preview': result.chunk.preview
            })
        
        return {
            'answer': answer,
            'sources': sources,
            'model': self.model_name,
            'total_chunks': len(context)
        }
    
    def analyze_image(self, image_path: str, ocr_text: str = "") -> str:
        """Analyze image using Gemini Vision"""
        
        try:
            from PIL import Image
            
            img = Image.open(image_path)
            prompt = PROMPTS['image_analysis'].format(ocr_text=ocr_text)
            
            # Track Vision API call
            st.session_state['gemini_vision_calls'] = st.session_state.get('gemini_vision_calls', 0) + 1
            
            response = self.client.models.generate_content(
                model=self._model_name,
                contents=[prompt, img],
                config={"temperature": 0.3}
            )
            
            return response.text
            
        except Exception as e:
            return f"Image analysis failed: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if Gemini is available"""
        if self._available is not None:
            return self._available
        
        try:
            # Test API with simple request
            test_response = self.client.models.generate_content(
                model=self._model_name,
                contents="test",
                config={"max_output_tokens": 1}
            )
            self._available = True
        except:
            self._available = False
        
        return self._available
    
    @property
    def model_name(self) -> str:
        return self._model_name