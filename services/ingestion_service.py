from typing import List, Optional  # Add Optional here
import streamlit as st
from datetime import datetime

from models.chunk import Chunk
from models.document import Document
from processors.factory import ProcessorFactory
from core.retrieval.base import BaseRetriever
from utils.file_utils import temporary_file, get_file_hash
from constants.file_types import get_file_type_from_path, FileCategory

class IngestionService:
    
    def __init__(self, retriever: BaseRetriever):
        self.retriever = retriever
        self.processor_factory = ProcessorFactory()
        self.processed_documents: List[Document] = []
    
    def process_file(self, uploaded_file) -> Optional[Document]:
        
        with temporary_file(uploaded_file) as temp_path:
            
            file_type = get_file_type_from_path(temp_path)
            
            processor = self.processor_factory.get_processor(
                file_type.category.value,
                gemini_client=st.session_state.get('gemini_client')
            )
            
            if not processor:
                st.warning(f"No processor for {file_type.category.value}")
                return None
            
            chunks = []
            start_time = datetime.now()
            
            if file_type.category.value == 'pdf':
                chunks = processor.process_pdf(temp_path, uploaded_file.name)
            
            elif file_type.category.value == 'image':
                if hasattr(processor, 'process_image'):
                    result = processor.process_image(temp_path, uploaded_file.name)
                else:
                    result = processor.process(temp_path, uploaded_file.name)
                
                chunks = self._ensure_chunk_list(result, uploaded_file.name, file_type.category.value)
            
            elif file_type.category.value in ['word', 'excel', 'powerpoint', 'text']:
                result = processor.process(temp_path, uploaded_file.name)
                chunks = self._ensure_chunk_list(result, uploaded_file.name, file_type.category.value)
            
            doc = Document(
                file_name=uploaded_file.name,
                file_path=temp_path,
                file_type=file_type.category.value,
                file_size=len(uploaded_file.getvalue()),
                chunks=chunks,
                processed_at=start_time,
                metadata={
                    'hash': get_file_hash(temp_path),
                    'processor': processor.__class__.__name__
                }
            )
            
            if chunks:
                self.retriever.add_documents(chunks)
                self.processed_documents.append(doc)
            
            return doc
    
    def _ensure_chunk_list(self, result, source_name: str, file_type: str) -> List[Chunk]:
        
        chunks = []
        
        if result is None:
            return chunks
        
        if isinstance(result, list) and all(hasattr(item, 'content') for item in result if item):
            return result
        
        elif isinstance(result, list) and all(isinstance(item, str) for item in result):
            from models.chunk import Chunk
            for i, text in enumerate(result):
                chunk = Chunk(
                    content=text,
                    source_file=source_name,
                    file_type=file_type,
                    chunk_index=i,
                    metadata={'converted': True}
                )
                chunks.append(chunk)
        
        elif isinstance(result, str):
            from models.chunk import Chunk
            chunk = Chunk(
                content=result,
                source_file=source_name,
                file_type=file_type,
                chunk_index=0,
                metadata={'converted': True}
            )
            chunks.append(chunk)
        
        elif hasattr(result, 'content'):
            chunks.append(result)
        
        return chunks
    
    def process_files(self, uploaded_files, progress_callback=None) -> List[Document]:        
        documents = []
        total = len(uploaded_files)
        
        for i, uploaded_file in enumerate(uploaded_files):
            
            if progress_callback:
                progress_callback(i, total, uploaded_file.name)
            
            doc = self.process_file(uploaded_file)
            if doc:
                documents.append(doc)
        
        return documents
    
    def get_document_stats(self) -> dict:
        return {
            'total_documents': len(self.processed_documents),
            'total_chunks': sum(doc.total_chunks for doc in self.processed_documents),
            'total_size': sum(doc.total_size for doc in self.processed_documents),
            'file_types': list(set(doc.file_type for doc in self.processed_documents))
        }
    
    def clear(self):
        self.retriever.clear()
        self.processed_documents.clear()