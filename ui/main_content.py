"""Main content area UI"""

import streamlit as st
from datetime import datetime

from .components import result_card, file_badge, info_box
from services.query_service import QueryService

def render_main_content():
    """Render the main content area"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_file_section()
    
    with col2:
        render_query_section()

def render_file_section():
    """Render the file management section"""
    
    st.header("📄 Processed Files")
    
    if st.session_state.get('processed_files'):
        st.success(f"✅ {len(st.session_state.processed_files)} files ready")
        
        # File list
        with st.expander("View processed files"):
            for filename in st.session_state.processed_files:
                file_badge(filename, 'pdf' if filename.endswith('.pdf') else 'other')
        
        # Document stats
        if st.session_state.get('total_chunks'):
            st.metric(
                "Total Chunks",
                st.session_state.total_chunks,
                help="Number of text chunks available for search"
            )
    else:
        info_box("No files processed yet. Upload files using the sidebar.", "info")

def render_query_section():
    """Render the query/QA section"""
    
    st.header("💬 Ask Questions")
    
    if not st.session_state.get('processed_files'):
        info_box("👈 Upload files to start asking questions", "info")
        return
    
    # Query input
    query = st.text_area(
        "Your question:",
        placeholder="What would you like to know about your documents?",
        height=100,
        key="query_input"
    )
    
    # Additional options
    with st.expander("⚙️ Query Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            max_results = st.number_input(
                "Max Results",
                min_value=1,
                max_value=20,
                value=st.session_state.get('max_chunks', 5)
            )
        
        with col2:
            threshold = st.slider(
                "Similarity Threshold",
                min_value=0.1,
                max_value=0.9,
                value=st.session_state.get('similarity_threshold', 0.3),
                step=0.1
            )
    
    # Submit button
    if st.button("🔍 Get Answer", type="primary", use_container_width=True):
        if not query.strip():
            info_box("Please enter a question", "warning")
            return
        
        process_query(query, max_results, threshold)

def process_query(query: str, max_results: int, threshold: float):
    """Process and display query results"""
    
    if not st.session_state.get('query_service'):
        info_box("Query service not initialized", "error")
        return
    
    with st.spinner("🤔 Thinking..."):
        # Get answer
        result = st.session_state.query_service.answer(
            query,
            k=max_results,
            threshold=threshold
        )
    
    # Display answer
    st.markdown("### 📝 Answer")
    st.markdown(result['answer'])
    
    # Display metadata
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Time", f"{result['processing_time']:.2f}s")
    
    with col2:
        st.metric("Sources", result['total_found'])
    
    with col3:
        st.metric("Model", result['model'].split('/')[-1])
    
    # Display sources
    if result['sources']:
        with st.expander(f"🔍 View Sources ({len(result['sources'])})"):
            for i, source in enumerate(result['sources'], 1):
                st.markdown(f"**Source {i}** from `{source['file']}` (relevance: {source['relevance']:.2f})")
                st.markdown(source['preview'])
                st.divider()
    
    # Display detailed results
    if result['results']:
        with st.expander("📊 Detailed Results"):
            for i, res in enumerate(result['results'], 1):
                from models.result import SearchResult
                from models.chunk import Chunk
                
                # Reconstruct objects (simplified)
                chunk = Chunk(
                    content=res['chunk']['content'],
                    source_file=res['chunk']['source_file'],
                    file_type=res['chunk']['file_type']
                )
                search_result = SearchResult(
                    chunk=chunk,
                    score=res['score'],
                    query=query,
                    rank=res['rank']
                )
                result_card(search_result, i)