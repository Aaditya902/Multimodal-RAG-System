import os
import streamlit as st
from dotenv import load_dotenv
from constants.file_types import get_all_supported_extensions, get_extensions_by_category, FileCategory

load_dotenv()

def get_api_key() -> str:
    
    try:
        if hasattr(st, 'secrets') and st.secrets is not None:
            if 'GOOGLE_API_KEY' in st.secrets:
                return st.secrets['GOOGLE_API_KEY']
    except Exception:
        pass
    
    if 'GOOGLE_API_KEY' in os.environ:
        return os.environ['GOOGLE_API_KEY']
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key
    
    return ""

GOOGLE_API_KEY = get_api_key()

GEMINI_MODELS = {
    "flash": "models/gemini-2.5-flash",
    "pro": "models/gemini-2.5-pro",
}

DEFAULT_GEMINI_MODEL = GEMINI_MODELS["flash"]


MAX_CHUNK_SIZE = 1000 
CHUNK_OVERLAP = True   
CHUNK_OVERLAP_FACTOR = 1.5  

SIMILARITY_THRESHOLD = 0.3  
TOP_K_RESULTS = 5           
USE_HEAP_OPTIMIZATION = True  


BATCH_SIZE = 32  
MAX_OCR_PAGES = 10  


MAX_FILE_SIZE_MB = 50
MAX_TOTAL_SIZE_MB = 500

SUPPORTED_FILES = {
    'pdf': {
        'extensions': get_extensions_by_category(FileCategory.PDF),
        'mime_types': ['application/pdf'],
        'max_size_mb': 50,
        'processor': 'pdf'
    },
    'image': {
        'extensions': get_extensions_by_category(FileCategory.IMAGE),
        'mime_types': ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/tiff'],
        'max_size_mb': 20,
        'processor': 'image'
    },
    'word': {
        'extensions': get_extensions_by_category(FileCategory.WORD),
        'mime_types': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'],
        'max_size_mb': 30,
        'processor': 'document'
    },
    'excel': {
        'extensions': get_extensions_by_category(FileCategory.EXCEL),
        'mime_types': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel', 'text/csv'],
        'max_size_mb': 30,
        'processor': 'document'
    },
    'powerpoint': {
        'extensions': get_extensions_by_category(FileCategory.POWERPOINT),
        'mime_types': ['application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.ms-powerpoint'],
        'max_size_mb': 50,
        'processor': 'document'
    },
    'text': {
        'extensions': get_extensions_by_category(FileCategory.TEXT),
        'mime_types': ['text/plain', 'text/markdown', 'application/rtf'],
        'max_size_mb': 10,
        'processor': 'text'
    }
}

ALLOWED_EXTENSIONS = get_all_supported_extensions()


OCR_LANGUAGES = ['en']  
OCR_CONFIDENCE_THRESHOLD = 0.5  
OCR_GPU_ENABLED = False  
OCR_ENGINE = 'easyocr' 

USE_GEMINI_VISION_FOR_COMPLEX_IMAGES = True
GEMINI_VISION_THRESHOLD = 0.3  
MAX_GEMINI_VISION_CALLS = 10  


EMBEDDING_MODELS = {
    'mini': 'all-MiniLM-L6-v2',  
    'base': 'all-mpnet-base-v2', 
    'large': 'all-roberta-large-v1',  

DEFAULT_EMBEDDING_MODEL = EMBEDDING_MODELS['mini']
EMBEDDING_DIMENSION = 384  


DEFAULT_TEMPERATURE = 0.3  
DEFAULT_MAX_TOKENS = 1024  
DEFAULT_TOP_P = 0.9  
DEFAULT_TOP_K = 40  

INCLUDE_SOURCES_IN_RESPONSE = True  
MAX_SOURCES_TO_SHOW = 3  


CACHE_TTL_SECONDS = 3600  
CACHE_MAX_SIZE = 100  
ENABLE_EMBEDDING_CACHE = True  
ENABLE_OCR_CACHE = True  


APP_TITLE = "🔄 Multimodal RAG System with Gemini"
APP_ICON = "🔄"
APP_LAYOUT = "wide"
APP_INITIAL_SIDEBAR_STATE = "expanded"

PRIMARY_COLOR = "#1E88E5"
SECONDARY_COLOR = "#0D47A1"
SUCCESS_COLOR = "#4CAF50"
WARNING_COLOR = "#FF9800"
ERROR_COLOR = "#F44336"
BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#262730"


TRACK_API_USAGE = True  
SHOW_COST_ESTIMATES = True  
RESET_STATS_ON_CLEAR = True  

LOG_PERFORMANCE = True  
KEEP_LAST_N_TIMINGS = 100  


TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

for directory in [TEMP_DIR, CACHE_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)


def validate_config() -> dict:
    
    issues = []
    warnings = []
    
    if not GOOGLE_API_KEY:
        issues.append("GOOGLE_API_KEY is not set")
    elif len(GOOGLE_API_KEY) < 20:
        warnings.append("GOOGLE_API_KEY looks too short - may be invalid")
    
    for dir_path in [TEMP_DIR, CACHE_DIR, LOG_DIR]:
        if not os.access(dir_path, os.W_OK):
            warnings.append(f"Cannot write to {dir_path}")
    
    if SIMILARITY_THRESHOLD < 0 or SIMILARITY_THRESHOLD > 1:
        issues.append("SIMILARITY_THRESHOLD must be between 0 and 1")
    
    if MAX_CHUNK_SIZE < 100:
        warnings.append("MAX_CHUNK_SIZE is very small - may affect retrieval quality")
    elif MAX_CHUNK_SIZE > 5000:
        warnings.append("MAX_CHUNK_SIZE is very large - may cause memory issues")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings
    }


if os.getenv('ENVIRONMENT') == 'production':
    CACHE_TTL_SECONDS = 7200  
    LOG_PERFORMANCE = True
    SHOW_COST_ESTIMATES = False  
    
elif os.getenv('ENVIRONMENT') == 'test':
    MAX_FILE_SIZE_MB = 5  
    MAX_OCR_PAGES = 2  
    CACHE_TTL_SECONDS = 60  
    LOG_PERFORMANCE = False