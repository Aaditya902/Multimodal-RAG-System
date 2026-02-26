"""Configuration settings for the RAG system"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# ============================================================================
# API Configuration
# ============================================================================

def get_api_key() -> str:
    """Get Google API key from various sources"""
    
    # Check if running in Streamlit cloud (with secrets)
    try:
        # This will fail gracefully if no secrets file exists
        if hasattr(st, 'secrets') and st.secrets is not None:
            if 'GOOGLE_API_KEY' in st.secrets:
                return st.secrets['GOOGLE_API_KEY']
    except Exception:
        # No secrets file - continue to other methods
        pass
    
    # Try environment variable
    if 'GOOGLE_API_KEY' in os.environ:
        return os.environ['GOOGLE_API_KEY']
    
    # Try .env file
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key
    
    # If we get here, no API key found
    return ""

# Google Gemini API
GOOGLE_API_KEY = get_api_key()

# Available Gemini models
GEMINI_MODELS = {
    "flash": "models/gemini-2.5-flash",
    "pro": "models/gemini-2.5-pro",
}

DEFAULT_GEMINI_MODEL = GEMINI_MODELS["flash"]

# ============================================================================
# RAG Configuration
# ============================================================================

# Chunking settings
MAX_CHUNK_SIZE = 1000  # Maximum characters per chunk
CHUNK_OVERLAP = True   # Create overlapping chunks for better retrieval
CHUNK_OVERLAP_FACTOR = 1.5  # Overlap size multiplier

# Retrieval settings
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity score (0-1)
TOP_K_RESULTS = 5           # Number of chunks to retrieve
USE_HEAP_OPTIMIZATION = True  # Use heap for efficient top-k selection

# Batch processing
BATCH_SIZE = 32  # Batch size for embeddings
MAX_OCR_PAGES = 10  # Maximum pages to OCR per PDF

# ============================================================================
# File Processing Configuration
# ============================================================================

from constants.file_types import get_all_supported_extensions, get_extensions_by_category, FileCategory

# File size limits (in MB)
MAX_FILE_SIZE_MB = 50
MAX_TOTAL_SIZE_MB = 500

# Supported file types by category - using the constants
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

# Flatten extensions list for file uploader
ALLOWED_EXTENSIONS = get_all_supported_extensions()

# ============================================================================
# OCR Configuration
# ============================================================================

# OCR settings
OCR_LANGUAGES = ['en']  # Languages for OCR (English by default)
OCR_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for OCR results
OCR_GPU_ENABLED = False  # Use GPU for OCR (if available)
OCR_ENGINE = 'easyocr'  # Default OCR engine

# When to use Gemini Vision (instead of OCR)
USE_GEMINI_VISION_FOR_COMPLEX_IMAGES = True
GEMINI_VISION_THRESHOLD = 0.3  # If OCR confidence < this, use Gemini
MAX_GEMINI_VISION_CALLS = 10  # Max Vision calls per session

# ============================================================================
# Embedding Configuration
# ============================================================================

# Embedding models
EMBEDDING_MODELS = {
    'mini': 'all-MiniLM-L6-v2',  # Fast, 384 dim
    'base': 'all-mpnet-base-v2',  # More accurate, 768 dim
    'large': 'all-roberta-large-v1',  # Most accurate, 1024 dim
}

DEFAULT_EMBEDDING_MODEL = EMBEDDING_MODELS['mini']
EMBEDDING_DIMENSION = 384  # For mini model

# ============================================================================
# Generation Configuration
# ============================================================================

# LLM generation settings
DEFAULT_TEMPERATURE = 0.3  # Lower = more focused, Higher = more creative
DEFAULT_MAX_TOKENS = 1024  # Maximum tokens in response
DEFAULT_TOP_P = 0.9  # Nucleus sampling parameter
DEFAULT_TOP_K = 40  # Top-k sampling parameter

# Response formatting
INCLUDE_SOURCES_IN_RESPONSE = True  # Show which documents were used
MAX_SOURCES_TO_SHOW = 3  # Number of sources to display

# ============================================================================
# Cache Configuration
# ============================================================================

# Cache settings
CACHE_TTL_SECONDS = 3600  # Cache TTL (1 hour)
CACHE_MAX_SIZE = 100  # Maximum cache entries
ENABLE_EMBEDDING_CACHE = True  # Cache embeddings
ENABLE_OCR_CACHE = True  # Cache OCR results

# ============================================================================
# UI Configuration
# ============================================================================

# App settings
APP_TITLE = "🔄 Multimodal RAG System with Gemini"
APP_ICON = "🔄"
APP_LAYOUT = "wide"
APP_INITIAL_SIDEBAR_STATE = "expanded"

# Theme colors
PRIMARY_COLOR = "#1E88E5"
SECONDARY_COLOR = "#0D47A1"
SUCCESS_COLOR = "#4CAF50"
WARNING_COLOR = "#FF9800"
ERROR_COLOR = "#F44336"
BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#262730"

# ============================================================================
# Monitoring Configuration
# ============================================================================

# Usage tracking
TRACK_API_USAGE = True  # Track API calls for monitoring
SHOW_COST_ESTIMATES = True  # Show estimated costs in UI
RESET_STATS_ON_CLEAR = True  # Reset stats when clearing data

# Performance monitoring
LOG_PERFORMANCE = True  # Log timing information
KEEP_LAST_N_TIMINGS = 100  # Keep last N timing records

# ============================================================================
# Path Configuration
# ============================================================================

# Directory paths
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

# Create directories if they don't exist
for directory in [TEMP_DIR, CACHE_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# ============================================================================
# Validation Functions
# ============================================================================

def validate_config() -> dict:
    """Validate configuration and return status"""
    
    issues = []
    warnings = []
    
    # Check API key
    if not GOOGLE_API_KEY:
        issues.append("GOOGLE_API_KEY is not set")
    elif len(GOOGLE_API_KEY) < 20:
        warnings.append("GOOGLE_API_KEY looks too short - may be invalid")
    
    # Check directories
    for dir_path in [TEMP_DIR, CACHE_DIR, LOG_DIR]:
        if not os.access(dir_path, os.W_OK):
            warnings.append(f"Cannot write to {dir_path}")
    
    # Check thresholds
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

# ============================================================================
# Environment-specific overrides
# ============================================================================

# Override settings based on environment
if os.getenv('ENVIRONMENT') == 'production':
    # Production settings
    CACHE_TTL_SECONDS = 7200  # Longer cache in production
    LOG_PERFORMANCE = True
    SHOW_COST_ESTIMATES = False  # Hide costs in production
    
elif os.getenv('ENVIRONMENT') == 'test':
    # Test settings
    MAX_FILE_SIZE_MB = 5  # Smaller files for testing
    MAX_OCR_PAGES = 2  # Limit OCR in tests
    CACHE_TTL_SECONDS = 60  # Short cache for testing
    LOG_PERFORMANCE = False

# ============================================================================
# Export all settings
# ============================================================================

__all__ = [
    # API
    'GOOGLE_API_KEY',
    'GEMINI_MODELS',
    'DEFAULT_GEMINI_MODEL',
    
    # RAG
    'MAX_CHUNK_SIZE',
    'CHUNK_OVERLAP',
    'CHUNK_OVERLAP_FACTOR',
    'SIMILARITY_THRESHOLD',
    'TOP_K_RESULTS',
    'USE_HEAP_OPTIMIZATION',
    'BATCH_SIZE',
    'MAX_OCR_PAGES',
    
    # File Processing
    'SUPPORTED_FILES',
    'ALLOWED_EXTENSIONS',
    'MAX_FILE_SIZE_MB',
    'MAX_TOTAL_SIZE_MB',
    
    # OCR
    'OCR_LANGUAGES',
    'OCR_CONFIDENCE_THRESHOLD',
    'OCR_GPU_ENABLED',
    'OCR_ENGINE',
    'USE_GEMINI_VISION_FOR_COMPLEX_IMAGES',
    'GEMINI_VISION_THRESHOLD',
    'MAX_GEMINI_VISION_CALLS',
    
    # Embedding
    'EMBEDDING_MODELS',
    'DEFAULT_EMBEDDING_MODEL',
    'EMBEDDING_DIMENSION',
    
    # Generation
    'DEFAULT_TEMPERATURE',
    'DEFAULT_MAX_TOKENS',
    'DEFAULT_TOP_P',
    'DEFAULT_TOP_K',
    'INCLUDE_SOURCES_IN_RESPONSE',
    'MAX_SOURCES_TO_SHOW',
    
    # Cache
    'CACHE_TTL_SECONDS',
    'CACHE_MAX_SIZE',
    'ENABLE_EMBEDDING_CACHE',
    'ENABLE_OCR_CACHE',
    
    # UI
    'APP_TITLE',
    'APP_ICON',
    'APP_LAYOUT',
    'APP_INITIAL_SIDEBAR_STATE',
    'PRIMARY_COLOR',
    'SECONDARY_COLOR',
    'SUCCESS_COLOR',
    'WARNING_COLOR',
    'ERROR_COLOR',
    'BACKGROUND_COLOR',
    'TEXT_COLOR',
    
    # Monitoring
    'TRACK_API_USAGE',
    'SHOW_COST_ESTIMATES',
    'RESET_STATS_ON_CLEAR',
    'LOG_PERFORMANCE',
    'KEEP_LAST_N_TIMINGS',
    
    # Paths
    'TEMP_DIR',
    'CACHE_DIR',
    'LOG_DIR',
    
    # Functions
    'validate_config',
]