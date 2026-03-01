import streamlit as st
from typing import List, Optional, Callable
from models.result import SearchResult

def metric_card(label: str, value: str, delta: Optional[str] = None, help_text: Optional[str] = None):
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.metric(
            label=label,
            value=value,
            delta=delta,
            help=help_text
        )

def result_card(result: SearchResult, index: int):
    
    confidence_color = result.confidence_color
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**Result {index}** from `{result.chunk.source_file}`")
            st.markdown(result.chunk.preview)
        
        with col2:
            st.markdown(f"**Score:** :{confidence_color}[{result.score:.2f}]")
            st.markdown(f"**Confidence:** {result.confidence_level}")
        
        st.divider()

def file_badge(filename: str, file_type: str, size: Optional[int] = None):
    
    icons = {
        'pdf': '📄',
        'image': '🖼️',
        'word': '📝',
        'excel': '📊',
        'powerpoint': '📽️',
        'text': '📃',
    }
    
    icon = icons.get(file_type, '📁')
    
    if size:
        from utils.file_utils import get_file_size_str
        size_str = get_file_size_str(size)
        label = f"{icon} {filename} ({size_str})"
    else:
        label = f"{icon} {filename}"
    
    st.markdown(f"`{label}`")

def progress_step(current: int, total: int, label: str = "Processing"):
    
    percent = int((current / total) * 100)
    return st.markdown(f"**{label}:** {current}/{total} ({percent}%)")

def info_box(message: str, type: str = "info"):
    
    styles = {
        "info": {"icon": "ℹ️", "color": "blue"},
        "success": {"icon": "✅", "color": "green"},
        "warning": {"icon": "⚠️", "color": "orange"},
        "error": {"icon": "❌", "color": "red"},
    }
    
    style = styles.get(type, styles["info"])
    
    st.markdown(
        f"""
        <div style="
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: {style['color']}10;
            border-left: 4px solid {style['color']};
            margin: 1rem 0;
        ">
            {style['icon']} {message}
        </div>
        """,
        unsafe_allow_html=True
    )

def action_button(label: str, on_click: Callable, icon: Optional[str] = None):
    
    button_label = f"{icon} {label}" if icon else label
    
    if st.button(button_label, use_container_width=True):
        on_click()