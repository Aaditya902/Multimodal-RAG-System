import easyocr
import streamlit as st
from typing import List, Tuple, Optional
import numpy as np
from .base import BaseOCR

class EasyOCREngine(BaseOCR):
    
    def __init__(self, languages: List[str] = ['en'], gpu: bool = False):
        self._languages = languages
        self.gpu = gpu
        self._reader = None
        self._available = None
    
    @property
    def reader(self):
        if self._reader is None:
            self._reader = self._load_reader()
        return self._reader
    
    @st.cache_resource
    def _load_reader(self):
        try:
            return easyocr.Reader(self._languages, gpu=self.gpu)
        except Exception as e:
            st.error(f"Failed to load EasyOCR: {str(e)}")
            return None
    
    def extract_text(self, image_path: str) -> str:
        if not self.reader:
            return ""
        
        try:
            result = self.reader.readtext(image_path)
            texts = [item[1] for item in result if item[2] > 0.5]
            return ' '.join(texts)
        except Exception as e:
            return ""
    
    def extract_text_with_confidence(self, image_path: str) -> List[Tuple[str, float, List]]:
        if not self.reader:
            return []
        
        try:
            result = self.reader.readtext(image_path)
            return [(item[1], item[2], item[0]) for item in result]
        except Exception as e:
            return []
    
    def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        
        try:
            self._available = self.reader is not None
        except:
            self._available = False
        
        return self._available
    
    @property
    def languages(self) -> List[str]:
        return self._languages
    
    def extract_text_from_array(self, image_array: np.ndarray) -> str:
        if not self.reader:
            return ""
        
        try:
            result = self.reader.readtext(image_array)
            texts = [item[1] for item in result if item[2] > 0.5]
            return ' '.join(texts)
        except Exception as e:
            return ""