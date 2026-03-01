from typing import List, Optional
import streamlit as st
import os
from PIL import Image
import pytesseract
import cv2
import numpy as np

from .base import BaseProcessor
from models.chunk import Chunk
from ocr.factory import OCRFactory

class ImageProcessor(BaseProcessor):
    
    def __init__(self, gemini_client=None):
        self.gemini_client = gemini_client
        self.ocr_engine = None
        self._extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        self._initialize_ocr()
    
    def _initialize_ocr(self):
        try:
            self.ocr_engine = OCRFactory.create('easyocr', cache=True)
            if self.ocr_engine and self.ocr_engine.is_available():
                st.success("✅ EasyOCR initialized successfully")
                return
        except Exception as e:
            st.warning(f"EasyOCR initialization failed: {str(e)}")
        
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            self.use_tesseract = True
            st.success("✅ Tesseract OCR initialized successfully")
        except:
            self.use_tesseract = False
            st.warning("⚠️ No OCR engine available. Install EasyOCR or Tesseract.")
    
    def set_gemini_client(self, client):
        self.gemini_client = client
    
    def process(self, file_path: str, source_name: str) -> List[Chunk]:
        
        chunks = []
        
        preprocessed_path = self._preprocess_image(file_path)
        
        ocr_text = self._extract_text_with_multiple_engines(preprocessed_path)
        
        if ocr_text:
            chunk = Chunk(
                content=f"[OCR Text from image]:\n{ocr_text}",
                source_file=source_name,
                file_type='image_ocr',
                chunk_index=len(chunks),
                metadata={'ocr': True, 'has_text': True, 'extracted_text': ocr_text}
            )
            chunks.append(chunk)
            
            st.session_state['ocr_calls'] = st.session_state.get('ocr_calls', 0) + 1
        
        metadata = self._extract_image_metadata(file_path)
        if metadata:
            meta_chunk = Chunk(
                content=f"[Image Metadata]:\n{metadata}",
                source_file=source_name,
                file_type='image_metadata',
                chunk_index=len(chunks),
                metadata={'type': 'metadata'}
            )
            chunks.append(meta_chunk)
        
        if self.gemini_client and self._needs_gemini_analysis(file_path, ocr_text):
            analysis = self._analyze_with_gemini(file_path, ocr_text)
            if analysis:
                chunk = Chunk(
                    content=analysis,
                    source_file=source_name,
                    file_type='image_analysis',
                    chunk_index=len(chunks),
                    metadata={'gemini': True, 'has_ocr': bool(ocr_text)}
                )
                chunks.append(chunk)
        
        if not chunks:
            basic_info = self._get_basic_image_info(file_path)
            chunk = Chunk(
                content=f"[Image with no extractable text]\n{basic_info}",
                source_file=source_name,
                file_type='image',
                chunk_index=0,
                metadata={'empty': True}
            )
            chunks.append(chunk)
        
        return chunks
    
    def _preprocess_image(self, image_path: str) -> str:
        try:
            img = cv2.imread(image_path)
            if img is None:
                return image_path
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
            gray = cv2.medianBlur(gray, 3)
            
            preprocessed_path = image_path.replace('.', '_preprocessed.')
            cv2.imwrite(preprocessed_path, gray)
            
            return preprocessed_path
            
        except Exception as e:
            st.warning(f"Image preprocessing failed: {str(e)}")
            return image_path
    
    def _extract_text_with_multiple_engines(self, image_path: str) -> str:
        """Extract text using multiple OCR engines"""
        
        all_text = []
        
        if self.ocr_engine and self.ocr_engine.is_available():
            try:
                text = self.ocr_engine.extract_text(image_path)
                if text:
                    all_text.append(f"[EasyOCR]: {text}")
            except Exception as e:
                st.warning(f"EasyOCR failed: {str(e)}")
        
        if hasattr(self, 'use_tesseract') and self.use_tesseract:
            try:
                # Try different Tesseract configurations
                configs = [
                    '--oem 3 --psm 6',  # Assume uniform block of text
                    '--oem 3 --psm 3',  # Fully automatic
                    '--oem 3 --psm 4',  # Assume single column
                    '--oem 3 --psm 12',  # Sparse text
                ]
                
                for config in configs:
                    try:
                        text = pytesseract.image_to_string(image_path, config=config)
                        if text and len(text.strip()) > 50:
                            all_text.append(f"[Tesseract]: {text}")
                            break
                    except:
                        continue
                        
            except Exception as e:
                st.warning(f"Tesseract failed: {str(e)}")
        
        combined = '\n'.join(all_text)
        return combined
    
    def _extract_image_metadata(self, image_path: str) -> str:
        """Extract metadata from image"""
        try:
            img = Image.open(image_path)
            metadata = []
            
            metadata.append(f"Format: {img.format}")
            metadata.append(f"Size: {img.size[0]} x {img.size[1]} pixels")
            metadata.append(f"Mode: {img.mode}")
            
            if hasattr(img, '_getexif') and img._getexif():
                exif = img._getexif()
                if exif:
                    metadata.append("EXIF data present")
            
            return '\n'.join(metadata)
            
        except Exception as e:
            return f"Metadata extraction failed: {str(e)}"
    
    def _get_basic_image_info(self, image_path: str) -> str:
        """Get basic image information"""
        try:
            img = Image.open(image_path)
            return f"Image: {img.size[0]}x{img.size[1]} pixels, Format: {img.format}"
        except:
            return "Unable to read image information"
    
    def _needs_gemini_analysis(self, file_path: str, ocr_text: str) -> bool:
        """Determine if image needs Gemini analysis"""
        
        if len(ocr_text) < 50:
            return True
        
        complex_keywords = ['diagram', 'chart', 'graph', 'figure', 'screenshot', 
                           'table', 'flowchart', 'map', 'illustration']
        if any(keyword in ocr_text.lower() for keyword in complex_keywords):
            return True
        
        try:
            img = Image.open(file_path)
            if img.size[0] * img.size[1] > 1000000:  # > 1MP
                return True
        except:
            pass
        
        return False
    
    def _analyze_with_gemini(self, file_path: str, ocr_text: str) -> str:
        try:
            from PIL import Image
            
            img = Image.open(file_path)
            
            prompt = f"""Analyze this image in detail.

OCR text found: {ocr_text if ocr_text else 'No text found'}

Please provide:
1. A detailed description of what you see
2. Any text visible in the image
3. If it's a chart/diagram, explain what it represents
4. Important details or context
5. The overall purpose or message of this image

Analysis:"""

            response = self.gemini_client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=[prompt, img],
                config={"temperature": 0.3, "max_output_tokens": 1024}
            )
            
            return f"[Gemini Vision Analysis]:\n{response.text}"
            
        except Exception as e:
            return f"[Image analysis failed: {str(e)}]"
    
    def supports(self, file_type: str) -> bool:
        return file_type.lower() == 'image'
    
    @property
    def supported_extensions(self) -> List[str]:
        return self._extensions