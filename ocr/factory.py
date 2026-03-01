from typing import Optional, Dict, Any, List
from .base import BaseOCR
from .easyocr_engine import EasyOCREngine

class OCRFactory:
    
    _instances: Dict[str, BaseOCR] = {}
    
    @classmethod
    def create(cls,
               engine_type: str = 'easyocr',
               languages: List[str] = None,
               gpu: bool = False,
               cache: bool = True,
               **kwargs) -> Optional[BaseOCR]:

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
        
        if cache and instance and instance.is_available():
            cls._instances[cache_key] = instance
        
        return instance
    
    @classmethod
    def get_available_engines(cls) -> Dict[str, bool]:
        """Check availability of all OCR engines"""
        engines = {}
        
        try:
            easyocr = cls.create('easyocr', cache=False)
            engines['easyocr'] = easyocr.is_available() if easyocr else False
        except:
            engines['easyocr'] = False
        
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