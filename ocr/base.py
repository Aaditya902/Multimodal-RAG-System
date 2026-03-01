from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any
import numpy as np

class BaseOCR(ABC):
    
    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        pass
    
    @abstractmethod
    def extract_text_with_confidence(self, image_path: str) -> List[Tuple[str, float, List]]:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass
    
    @property
    @abstractmethod
    def languages(self) -> List[str]:
        pass
    
    def extract_text_batch(self, image_paths: List[str]) -> List[str]:
        return [self.extract_text(path) for path in image_paths]
    
    def extract_text_from_array(self, image_array: np.ndarray) -> str:
        import tempfile
        import os
        from PIL import Image
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            Image.fromarray(image_array).save(tmp.name)
            text = self.extract_text(tmp.name)
            os.unlink(tmp.name)
            return text