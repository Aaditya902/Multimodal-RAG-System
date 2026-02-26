"""Processor for plain text files"""

from typing import List
import streamlit as st

from .base import BaseProcessor
from models.chunk import Chunk

class TextProcessor(BaseProcessor):
    """Process plain text files"""
    
    def __init__(self):
        self._extensions = ['.txt', '.md', '.rtf']
    
    def process(self, file_path: str, source_name: str) -> List[Chunk]:
        """Process text file"""
        
        chunks = []
        
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                st.warning(f"Could not decode {source_name} with any encoding")
                return chunks
            
            if text.strip():
                chunks = self.chunk_text(text, source_name)
                
                # Add metadata
                for chunk in chunks:
                    chunk.metadata['type'] = 'text'
                    chunk.metadata['encoding'] = encoding
                    chunk.metadata['size'] = len(text)
        
        except Exception as e:
            st.warning(f"Text processing failed: {str(e)}")
        
        return chunks
    
    def supports(self, file_type: str) -> bool:
        return file_type.lower() == 'text'
    
    @property
    def supported_extensions(self) -> List[str]:
        return self._extensions