from functools import lru_cache, wraps
import time
import hashlib
import pickle
from typing import Any, Callable, Optional
import streamlit as st

class TTLCache:
    
    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        self.cache[key] = (value, time.time())
    
    def clear(self):
        self.cache.clear()
    
    def remove_expired(self):
        now = time.time()
        expired = [k for k, (_, ts) in self.cache.items() if now - ts >= self.ttl]
        for k in expired:
            del self.cache[k]

def memoize(ttl: Optional[int] = None):
    def decorator(func):
        cache = TTLCache(ttl) if ttl else {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = hashlib.md5(
                pickle.dumps((args, sorted(kwargs.items())))
            ).hexdigest()
            
            if ttl:
                result = cache.get(key)
                if result is not None:
                    return result
            elif key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            
            if ttl:
                cache.set(key, result)
            else:
                cache[key] = result
            
            return result
        
        return wrapper
    return decorator

@st.cache_data(ttl=3600)
def cache_embedding(text: str, model_name: str) -> list:
    pass

def clear_all_caches():
    st.cache_data.clear()
    st.cache_resource.clear()