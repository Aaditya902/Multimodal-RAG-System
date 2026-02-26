"""Main Streamlit application"""

import streamlit as st
from datetime import datetime

from config import GOOGLE_API_KEY
from core.embedding.factory import EmbeddingFactory
from core.retrieval.faiss_retriever import FAISSRetriever
from core.generation.gemini_generator import GeminiGenerator
from services.ingestion_service import IngestionService
from services.query_service import QueryService
from services.monitoring_service import MonitoringService
from ui.sidebar import render_sidebar
from ui.main_content import render_main_content
from utils.cache_utils import clear_all_caches
from google import genai

# Page configuration
st.set_page_config(
    page_title="Multimodal RAG System",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    
    defaults = {
        'ocr_calls': 0,
        'gemini_vision_calls': 0,
        'gemini_text_calls': 0,
        'total_chunks': 0,
        'processed_files': [],
        'selected_model': 'models/gemini-2.5-flash',
        'similarity_threshold': 0.3,
        'max_chunks': 5,
        'retriever': None,
        'ingestion_service': None,
        'query_service': None,
        'monitoring_service': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize services
@st.cache_resource
def init_services():
    """Initialize core services"""
    
    # Check API key
    if not GOOGLE_API_KEY:
        st.error("⚠️ Google API key not found")
        return None, None, None
    
    # Initialize Gemini client
    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    # Initialize embedding model
    embedding_model = EmbeddingFactory.create(
        model_type='sentence_transformer',
        model_name='all-MiniLM-L6-v2'
    )
    
    # Initialize retriever
    retriever = FAISSRetriever(
        embedding_model=embedding_model,
        similarity_threshold=st.session_state.similarity_threshold
    )
    
    # Initialize generator
    generator = GeminiGenerator(
        client=client,
        model_name=st.session_state.selected_model
    )
    
    # Initialize services
    ingestion = IngestionService(retriever)
    query = QueryService(retriever, generator)
    monitoring = MonitoringService()
    
    return ingestion, query, monitoring

def process_files(uploaded_files):
    """Handle file processing"""
    
    if not st.session_state.ingestion_service:
        st.error("Services not initialized")
        return
    
    def progress_callback(current, total, filename):
        progress = (current + 1) / total
        st.progress(progress, text=f"Processing {filename} ({current+1}/{total})")
    
    # Process files
    documents = st.session_state.ingestion_service.process_files(
        uploaded_files,
        progress_callback
    )
    
    # Update stats
    stats = st.session_state.ingestion_service.get_document_stats()
    st.session_state.total_chunks = stats['total_chunks']
    st.session_state.processed_files = [doc.file_name for doc in documents]
    
    st.success(f"✅ Processed {len(documents)} files with {stats['total_chunks']} chunks")
    st.rerun()

def clear_all():
    """Clear all data and reset"""
    st.session_state.retriever = None
    st.session_state.ingestion_service = None
    st.session_state.query_service = None
    st.session_state.processed_files = []
    st.session_state.total_chunks = 0
    clear_all_caches()

def main():
    """Main application entry point"""
    
    # Initialize
    init_session_state()
    
    # Initialize services if needed
    if not st.session_state.ingestion_service:
        ingestion, query, monitoring = init_services()
        st.session_state.ingestion_service = ingestion
        st.session_state.query_service = query
        st.session_state.monitoring_service = monitoring
    
    # Title
    st.title("🔄 Multimodal RAG System with Gemini")
    st.markdown("Upload any file - PDF, Images, Word, Excel - and ask questions!")
    
    # Render sidebar
    render_sidebar(process_files, clear_all)
    
    # Render main content
    render_main_content()

if __name__ == "__main__":
    main()