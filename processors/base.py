"""Base processor interface"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any  # Add this import
from models.chunk import Chunk

class BaseProcessor(ABC):
    """Abstract base class for all file processors"""
    
    @abstractmethod
    def process(self, file_path: str, source_name: str) -> List[Chunk]:
        """Process file and return chunks"""
        pass
    
    @abstractmethod
    def supports(self, file_type: str) -> bool:
        """Check if processor supports file type"""
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """Get list of supported file extensions"""
        pass
    
    def chunk_text(self, text: str, source_name: str, 
                   max_size: int = 1000, overlap: bool = True) -> List[Chunk]:
        """Split text into chunks"""
        
        chunks = []
        sentences = text.replace('\n', ' ').split('. ')
        current_chunk = []
        current_length = 0
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if not sentence.endswith('.'):
                sentence += '.'
            
            sentence_length = len(sentence)
            
            if current_length + sentence_length > max_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append(Chunk(
                    content=chunk_text,
                    source_file=source_name,
                    file_type=self.__class__.__name__,
                    chunk_index=len(chunks)
                ))
                current_chunk = []
                current_length = 0
            
            current_chunk.append(sentence)
            current_length += sentence_length + 1
        
        # Add last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append(Chunk(
                content=chunk_text,
                source_file=source_name,
                file_type=self.__class__.__name__,
                chunk_index=len(chunks)
            ))
        
        # Create overlapping chunks if requested
        if overlap and len(chunks) > 1:
            overlapping = []
            for i in range(len(chunks) - 1):
                combined = chunks[i].content + " " + chunks[i+1].content
                if len(combined) <= max_size * 1.5:
                    overlapping.append(Chunk(
                        content=combined,
                        source_file=source_name,
                        file_type=f"{self.__class__.__name__}_overlap",
                        chunk_index=len(chunks) + i,
                        metadata={'overlap': True, 'chunks': [i, i+1]}
                    ))
            chunks.extend(overlapping)
        
        return chunks