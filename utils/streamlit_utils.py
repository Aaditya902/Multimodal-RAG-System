import streamlit as st
from typing import Any, Callable, Optional
import time

def safe_session_state(key: str, default: Any = None) -> Any:
    return st.session_state.get(key, default)

def init_session_vars(vars_dict: dict):
    for key, value in vars_dict.items():
        if key not in st.session_state:
            st.session_state[key] = value

def with_loading(message: str = "Processing..."):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            with st.spinner(message):
                return func(*args, **kwargs)
        return wrapper
    return decorator

def progress_animation(duration: float = 2.0, steps: int = 10):
    progress_bar = st.progress(0)
    for i in range(steps):
        time.sleep(duration / steps)
        progress_bar.progress((i + 1) / steps)
    progress_bar.empty()

def cache_with_ttl(ttl_seconds: int = 3600):
    def decorator(func):
        cache_key = f"_cache_{func.__name__}"
        cache_time_key = f"_cache_time_{func.__name__}"
        
        def wrapper(*args, **kwargs):
            now = time.time()
            
            if (cache_key in st.session_state and 
                cache_time_key in st.session_state and
                now - st.session_state[cache_time_key] < ttl_seconds):
                return st.session_state[cache_key]
            
            result = func(*args, **kwargs)
            st.session_state[cache_key] = result
            st.session_state[cache_time_key] = now
            
            return result
        
        return wrapper
    return decorator

def show_toast(message: str, icon: str = "✅", duration: float = 2.0):
    toast_placeholder = st.empty()
    toast_placeholder.markdown(f"{icon} {message}")
    time.sleep(duration)
    toast_placeholder.empty()

def confirm_action(message: str) -> bool:
    return st.warning(message) and st.button("Confirm")

def format_number(num: int) -> str:
    return f"{num:,}"

def truncate_text(text: str, max_length: int = 100) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."