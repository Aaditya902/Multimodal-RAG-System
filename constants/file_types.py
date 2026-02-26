"""File type constants and mappings"""

from enum import Enum
from typing import Dict, List, Optional

class FileCategory(Enum):
    """File category enumeration"""
    PDF = "pdf"
    IMAGE = "image"
    WORD = "word"
    EXCEL = "excel"
    POWERPOINT = "powerpoint"
    TEXT = "text"
    UNKNOWN = "unknown"

class FileType(Enum):
    """File type enumeration with extensions"""
    # Define UNKNOWN first
    UNKNOWN = ("", FileCategory.UNKNOWN)
    
    # Document types
    PDF = (".pdf", FileCategory.PDF)
    
    # Image types
    JPG = (".jpg", FileCategory.IMAGE)
    JPEG = (".jpeg", FileCategory.IMAGE)
    PNG = (".png", FileCategory.IMAGE)
    GIF = (".gif", FileCategory.IMAGE)
    BMP = (".bmp", FileCategory.IMAGE)
    TIFF = (".tiff", FileCategory.IMAGE)
    
    # Word types
    DOCX = (".docx", FileCategory.WORD)
    DOC = (".doc", FileCategory.WORD)
    
    # Excel types
    XLSX = (".xlsx", FileCategory.EXCEL)
    XLS = (".xls", FileCategory.EXCEL)
    CSV = (".csv", FileCategory.EXCEL)
    
    # PowerPoint types
    PPTX = (".pptx", FileCategory.POWERPOINT)
    PPT = (".ppt", FileCategory.POWERPOINT)
    
    # Text types
    TXT = (".txt", FileCategory.TEXT)
    MD = (".md", FileCategory.TEXT)
    RTF = (".rtf", FileCategory.TEXT)
    
    def __init__(self, extension: str, category: FileCategory):
        self.extension = extension
        self.category = category
    
    @classmethod
    def _missing_(cls, value):
        """Handle missing values by returning UNKNOWN"""
        return cls.UNKNOWN

# MIME type mappings
MIME_TYPE_MAP: Dict[str, FileType] = {
    'application/pdf': FileType.PDF,
    'image/jpeg': FileType.JPEG,
    'image/png': FileType.PNG,
    'image/gif': FileType.GIF,
    'image/bmp': FileType.BMP,
    'image/tiff': FileType.TIFF,
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': FileType.DOCX,
    'application/msword': FileType.DOC,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': FileType.XLSX,
    'application/vnd.ms-excel': FileType.XLS,
    'text/csv': FileType.CSV,
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': FileType.PPTX,
    
    'application/vnd.ms-powerpoint': FileType.PPT,
    'text/plain': FileType.TXT,
    'text/markdown': FileType.MD,
    'application/rtf': FileType.RTF,
}

# Extension to file type mapping
EXTENSION_MAP: Dict[str, FileType] = {
    ft.extension: ft for ft in FileType if ft.extension  # Skip UNKNOWN which has empty extension
}

SUPPORTED_EXTENSIONS = [ft.extension for ft in FileType if ft.extension]  # Skip UNKNOWN
SUPPORTED_MIME_TYPES = list(MIME_TYPE_MAP.keys())

def get_file_type_from_path(file_path: str) -> FileType:
    """Get file type from file path"""
    import os
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    return EXTENSION_MAP.get(ext, FileType.UNKNOWN)

def get_file_type_from_mime(mime_type: str) -> FileType:
    """Get file type from MIME type"""
    return MIME_TYPE_MAP.get(mime_type, FileType.UNKNOWN)

def is_supported_file(file_path: str) -> bool:
    """Check if file type is supported"""
    file_type = get_file_type_from_path(file_path)
    return file_type != FileType.UNKNOWN

def get_category_from_path(file_path: str) -> FileCategory:
    """Get file category from path"""
    file_type = get_file_type_from_path(file_path)
    return file_type.category

def get_all_supported_extensions() -> List[str]:
    """Get all supported file extensions"""
    return SUPPORTED_EXTENSIONS.copy()

def get_extensions_by_category(category: FileCategory) -> List[str]:
    """Get all extensions for a specific category"""
    return [
        ft.extension for ft in FileType 
        if ft.category == category and ft.extension
    ]