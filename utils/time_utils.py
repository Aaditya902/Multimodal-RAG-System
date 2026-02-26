"""Time and timing utilities"""

import time
from datetime import datetime, timedelta
from contextlib import contextmanager
from typing import Optional, Dict, Any
import streamlit as st

class Timer:
    """Simple timer for measuring execution time"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed = None
    
    def start(self):
        """Start the timer"""
        self.start_time = time.time()
        return self
    
    def stop(self):
        """Stop the timer"""
        if self.start_time is not None:
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time
        return self.elapsed
    
    def reset(self):
        """Reset the timer"""
        self.start_time = None
        self.end_time = None
        self.elapsed = None
    
    @property
    def current(self) -> Optional[float]:
        """Get current elapsed time without stopping"""
        if self.start_time is not None:
            return time.time() - self.start_time
        return None
    
    def __enter__(self):
        return self.start()
    
    def __exit__(self, *args):
        self.stop()

@contextmanager
def timing(label: str = "Operation", log: bool = True):
    """Context manager for timing operations"""
    
    timer = Timer()
    timer.start()
    
    try:
        yield timer
    finally:
        elapsed = timer.stop()
        
        if log:
            st.session_state.setdefault('timings', []).append({
                'label': label,
                'elapsed': elapsed,
                'timestamp': datetime.now()
            })
            
            # Keep only last 100 timings
            if len(st.session_state.timings) > 100:
                st.session_state.timings = st.session_state.timings[-100:]

def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    
    if seconds < 0.001:
        return f"{seconds*1000000:.1f}µs"
    elif seconds < 1:
        return f"{seconds*1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def get_time_ago(timestamp: datetime) -> str:
    """Get human-readable time ago string"""
    
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return f"{diff.seconds} seconds ago"

def get_performance_summary() -> Dict[str, Any]:
    """Get summary of recent timings"""
    
    timings = st.session_state.get('timings', [])
    
    if not timings:
        return {'total_operations': 0}
    
    # Calculate statistics
    operations = {}
    for t in timings:
        label = t['label']
        if label not in operations:
            operations[label] = []
        operations[label].append(t['elapsed'])
    
    summary = {
        'total_operations': len(timings),
        'average_time': sum(t['elapsed'] for t in timings) / len(timings),
        'slowest': max(t['elapsed'] for t in timings),
        'fastest': min(t['elapsed'] for t in timings),
        'by_operation': {}
    }
    
    for label, times in operations.items():
        summary['by_operation'][label] = {
            'count': len(times),
            'average': sum(times) / len(times),
            'min': min(times),
            'max': max(times)
        }
    
    return summary

def wait_with_progress(seconds: float, message: str = "Waiting..."):
    """Wait with progress bar"""
    
    progress_bar = st.progress(0)
    steps = 20
    
    for i in range(steps):
        time.sleep(seconds / steps)
        progress_bar.progress((i + 1) / steps)
    
    progress_bar.empty()

def retry_with_backoff(func, max_retries: int = 3, initial_delay: float = 1.0):
    """Retry function with exponential backoff"""
    
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            time.sleep(delay)
            delay *= 2  # Exponential backoff
    
    return None