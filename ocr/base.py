"""Base OCR interface"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any
import numpy as np

class BaseOCR(ABC):
    """Abstract base class for OCR engines"""
    
    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        """Extract text from image"""
        pass
    
    @abstractmethod
    def extract_text_with_confidence(self, image_path: str) -> List[Tuple[str, float, List]]:
        """Extract text with confidence scores and bounding boxes"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if OCR engine is available"""
        pass
    
    @property
    @abstractmethod
    def languages(self) -> List[str]:
        """Get supported languages"""
        pass
    
    def extract_text_batch(self, image_paths: List[str]) -> List[str]:
        """Extract text from multiple images"""
        return [self.extract_text(path) for path in image_paths]
    
    def extract_text_from_array(self, image_array: np.ndarray) -> str:
        """Extract text from numpy array image"""
        # Default implementation - save temp and process
        import tempfile
        import os
        from PIL import Image
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            Image.fromarray(image_array).save(tmp.name)
            text = self.extract_text(tmp.name)
            os.unlink(tmp.name)
            return text