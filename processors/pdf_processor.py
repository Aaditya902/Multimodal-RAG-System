from typing import List, Optional
import PyPDF2
from pdf2image import convert_from_path
import tempfile
import os
import streamlit as st

from .base import BaseProcessor
from .image_processor import ImageProcessor
from models.chunk import Chunk

class PDFProcessor(BaseProcessor):
    
    def __init__(self, gemini_client=None):
        self.gemini_client = gemini_client
        self.image_processor = ImageProcessor(gemini_client)
        self._extensions = ['.pdf']
    
    def set_gemini_client(self, client):
        self.gemini_client = client
        self.image_processor.set_gemini_client(client)
    
    def set_ocr_engine(self, engine):
        self.image_processor.set_ocr_engine(engine)
    
    def process(self, file_path: str, source_name: str) -> List[Chunk]:
        return self.process_pdf(file_path, source_name)
    
    def process_pdf(self, file_path: str, source_name: str) -> List[Chunk]:
        
        all_chunks = []
        ocr_pages = 0
        max_ocr_pages = 10  
        
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    
                    if page_text and page_text.strip():
                        chunk = Chunk(
                            content=f"[Page {page_num+1}]\n{page_text}",
                            source_file=source_name,
                            file_type='pdf_text',
                            page_number=page_num + 1,
                            chunk_index=len(all_chunks),
                            metadata={'page': page_num + 1, 'text_length': len(page_text)}
                        )
                        all_chunks.append(chunk)
                    
                    text_length = len(page_text.strip()) if page_text else 0
                    has_images = self._page_has_images(page)
                    
                    if (has_images or text_length < 100) and ocr_pages < max_ocr_pages:
                        ocr_chunks = self._ocr_pdf_page(file_path, page_num, source_name)
                        all_chunks.extend(ocr_chunks)
                        ocr_pages += 1
        
        except Exception as e:
            st.error(f"PDF processing failed: {str(e)}")
        
        return all_chunks
    
    def _page_has_images(self, page) -> bool:
        try:
            if '/Resources' in page and '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        return True
        except:
            pass
        return False
    
    def _ocr_pdf_page(self, pdf_path: str, page_num: int, source_name: str) -> List[Chunk]:
        chunks = []
        
        try:
            images = convert_from_path(
                pdf_path,
                first_page=page_num + 1,
                last_page=page_num + 1,
                dpi=200
            )
            
            if not images:
                return chunks
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                images[0].save(tmp.name)
                tmp_path = tmp.name
            
            image_chunks = self.image_processor.process(tmp_path, f"{source_name}_page{page_num+1}")
            
            for chunk in image_chunks:
                chunk.metadata['source'] = 'pdf_ocr'
                chunk.metadata['page'] = page_num + 1
                chunk.page_number = page_num + 1
                chunks.append(chunk)
            
            os.unlink(tmp_path)
            
        except Exception as e:
            st.warning(f"Page {page_num+1} OCR failed: {str(e)}")
        
        return chunks
    
    def supports(self, file_type: str) -> bool:
        return file_type.lower() == 'pdf'
    
    @property
    def supported_extensions(self) -> List[str]:
        return self._extensions