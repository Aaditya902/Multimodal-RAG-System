"""OCR factory for creating OCR engines"""

from typing import Optional, Dict, Any, List
from .base import BaseOCR
from .easyocr_engine import EasyOCREngine

class OCRFactory:
    """Factory for creating OCR engines"""
    
    _instances: Dict[str, BaseOCR] = {}
    
    @classmethod
    def create(cls,
               engine_type: str = 'easyocr',
               languages: List[str] = None,
               gpu: bool = False,
               cache: bool = True,
               **kwargs) -> Optional[BaseOCR]:
        """
        Create an OCR engine instance
        
        Args:
            engine_type: Type of OCR engine ('easyocr', 'tesseract', etc.)
            languages: List of language codes
            gpu: Whether to use GPU
            cache: Whether to cache the instance
            **kwargs: Additional arguments
        
        Returns:
            BaseOCR instance or None if creation fails
        """
        if languages is None:
            languages = ['en']
        
        cache_key = f"{engine_type}:{'-'.join(languages)}:{gpu}"
        
        if cache and cache_key in cls._instances:
            return cls._instances[cache_key]
        
        instance = None
        
        if engine_type == 'easyocr':
            instance = EasyOCREngine(languages=languages, gpu=gpu, **kwargs)
        elif engine_type == 'tesseract':
            from .tesseract_engine import TesseractEngine
            instance = TesseractEngine(languages=languages, **kwargs)
        else:
            raise ValueError(f"Unknown OCR engine type: {engine_type}")
        
        # Only cache if available
        if cache and instance and instance.is_available():
            cls._instances[cache_key] = instance
        
        return instance
    
    @classmethod
    def get_available_engines(cls) -> Dict[str, bool]:
        """Check availability of all OCR engines"""
        engines = {}
        
        # Check EasyOCR
        try:
            easyocr = cls.create('easyocr', cache=False)
            engines['easyocr'] = easyocr.is_available() if easyocr else False
        except:
            engines['easyocr'] = False
        
        # Check Tesseract
        try:
            tesseract = cls.create('tesseract', cache=False)
            engines['tesseract'] = tesseract.is_available() if tesseract else False
        except:
            engines['tesseract'] = False
        
        return engines
    
    @classmethod
    def clear_cache(cls):
        """Clear all cached instances"""
        cls._instances.clear()