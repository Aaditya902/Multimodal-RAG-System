import time
from datetime import datetime, timedelta
from typing import Dict, Any, List
from collections import defaultdict
import streamlit as st

class MonitoringService:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.metrics = defaultdict(int)
        self.timings = []
        self.errors = defaultdict(int)
        self.start_time = datetime.now()
    
    def track_api_call(self, api_type: str):
        self.metrics[f"{api_type}_calls"] += 1
        self.metrics['total_api_calls'] += 1
        
        if api_type == 'ocr':
            st.session_state['ocr_calls'] = st.session_state.get('ocr_calls', 0) + 1
        elif api_type == 'vision':
            st.session_state['gemini_vision_calls'] = st.session_state.get('gemini_vision_calls', 0) + 1
        elif api_type == 'text':
            st.session_state['gemini_text_calls'] = st.session_state.get('gemini_text_calls', 0) + 1
    
    def track_processing_time(self, operation: str, duration: float):
        self.timings.append({
            'operation': operation,
            'duration': duration,
            'timestamp': datetime.now()
        })
    
    def track_error(self, error_type: str):
        self.errors[error_type] += 1
        self.metrics['total_errors'] += 1
    
    def track_chunks(self, count: int):
        self.metrics['total_chunks'] += count
        st.session_state['total_chunks'] = st.session_state.get('total_chunks', 0) + count
    
    def track_files(self, count: int):
        self.metrics['total_files'] += count
    
    def get_summary(self) -> Dict[str, Any]:
        
        uptime = datetime.now() - self.start_time
        
        avg_time = 0
        if self.timings:
            avg_time = sum(t['duration'] for t in self.timings) / len(self.timings)
        
        recent = sorted(self.timings, key=lambda x: x['timestamp'], reverse=True)[:10]
        
        return {
            'uptime': str(uptime).split('.')[0],
            'total_api_calls': self.metrics['total_api_calls'],
            'ocr_calls': self.metrics.get('ocr_calls', 0),
            'vision_calls': self.metrics.get('vision_calls', 0),
            'text_calls': self.metrics.get('text_calls', 0),
            'total_chunks': self.metrics['total_chunks'],
            'total_files': self.metrics['total_files'],
            'total_errors': self.metrics['total_errors'],
            'avg_processing_time': f"{avg_time:.2f}s",
            'errors_by_type': dict(self.errors),
            'recent_operations': recent
        }
    
    def get_cost_estimate(self) -> Dict[str, float]:
        
        costs = {
            'ocr': 0.00,  # Free
            'vision': self.metrics.get('vision_calls', 0) * 0.0025,  
            'text': self.metrics.get('text_calls', 0) * 0.0005,  
        }
        
        costs['total'] = sum(costs.values())
        costs['saved'] = self.metrics.get('ocr_calls', 0) * 0.0025  
        
        return costs