"""Sidebar UI components"""

import streamlit as st
from typing import Callable, List
from datetime import datetime

def render_sidebar(on_process: Callable, on_clear: Callable):
    """Render the main sidebar"""
    
    with st.sidebar:
        st.header("📁 File Upload")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'png', 'jpg', 'jpeg', 'txt', 'docx', 'xlsx', 'pptx'],
            accept_multiple_files=True,
            key="file_uploader"
        )
        
        if uploaded_files:
            if st.button("🚀 Process Files", type="primary", use_container_width=True):
                with st.spinner(f"Processing {len(uploaded_files)} files..."):
                    on_process(uploaded_files)
        
        if st.button("🗑️ Clear All", use_container_width=True):
            on_clear()
            st.rerun()
        
        st.divider()
        
        render_usage_stats()
        
        st.divider()
        
        render_settings()

def render_usage_stats():
    """Render usage statistics"""
    st.subheader("📊 Usage Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "OCR Calls",
            st.session_state.get('ocr_calls', 0),
            help="Free local OCR calls"
        )
        st.metric(
            "Gemini Vision",
            st.session_state.get('gemini_vision_calls', 0),
            help="Gemini Vision API calls"
        )
    
    with col2:
        st.metric(
            "Gemini Text",
            st.session_state.get('gemini_text_calls', 0),
            help="Gemini Text API calls"
        )
        st.metric(
            "Chunks",
            st.session_state.get('total_chunks', 0),
            help="Total text chunks"
        )
    
    ocr_calls = st.session_state.get('ocr_calls', 0)
    if ocr_calls > 0:
        savings = ocr_calls * 0.01 
        st.success(f"💰 Saved ~${savings:.2f} using OCR!")

def render_settings():
    """Render settings panel"""
    st.subheader("⚙️ Settings")
    
    models = ["models/gemini-2.5-flash", "models/gemini-2.5-pro"]
    selected_model = st.selectbox(
        "Gemini Model",
        models,
        index=0,
        help="Select which model to use"
    )
    st.session_state['selected_model'] = selected_model
    
    threshold = st.slider(
        "Similarity Threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.3,
        step=0.1,
        help="Lower = more results, Higher = stricter"
    )
    st.session_state['similarity_threshold'] = threshold
    
    max_chunks = st.number_input(
        "Max Results",
        min_value=1,
        max_value=20,
        value=5,
        help="Number of chunks to retrieve"
    )
    st.session_state['max_chunks'] = max_chunks
    
    if st.button("🔄 Reset Stats", use_container_width=True):
        st.session_state['ocr_calls'] = 0
        st.session_state['gemini_vision_calls'] = 0
        st.session_state['gemini_text_calls'] = 0
        st.rerun()