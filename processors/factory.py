from typing import Dict, List, Optional  
from .base import BaseProcessor
from .pdf_processor import PDFProcessor
from .image_processor import ImageProcessor
from .document_processor import DocumentProcessor
from .text_processor import TextProcessor

class ProcessorFactory:
    """Factory for creating file processors"""
    
    _processors: Dict[str, BaseProcessor] = {}
    
    def __init__(self):
        self._initialize_processors()
    
    def _initialize_processors(self):
        """Initialize all processors"""
        self._processors = {
            'pdf': PDFProcessor(),
            'image': ImageProcessor(),
            'word': DocumentProcessor(),
            'excel': DocumentProcessor(),
            'powerpoint': DocumentProcessor(),
            'text': TextProcessor(),
        }
    
    def get_processor(self, file_type: str, **kwargs) -> Optional[BaseProcessor]:
        """Get processor for file type"""
        
        processor = self._processors.get(file_type.lower())
        
        if processor and kwargs:
            if 'gemini_client' in kwargs and hasattr(processor, 'set_gemini_client'):
                processor.set_gemini_client(kwargs['gemini_client'])
            if 'ocr_engine' in kwargs and hasattr(processor, 'set_ocr_engine'):
                processor.set_ocr_engine(kwargs['ocr_engine'])
        
        return processor
    
    def get_all_processors(self) -> Dict[str, BaseProcessor]:
        """Get all processors"""
        return self._processors.copy()
    
    def get_supported_extensions(self) -> Dict[str, List[str]]:
        """Get all supported extensions by processor type"""
        result = {}
        for processor_type, processor in self._processors.items():
            result[processor_type] = processor.supported_extensions
        return result