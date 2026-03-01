from enum import Enum
from typing import Dict, List, Optional

class FileCategory(Enum):
    PDF = "pdf"
    IMAGE = "image"
    WORD = "word"
    EXCEL = "excel"
    POWERPOINT = "powerpoint"
    TEXT = "text"
    UNKNOWN = "unknown"

class FileType(Enum):
    UNKNOWN = ("", FileCategory.UNKNOWN)
    
    PDF = (".pdf", FileCategory.PDF)
    
    JPG = (".jpg", FileCategory.IMAGE)
    JPEG = (".jpeg", FileCategory.IMAGE)
    PNG = (".png", FileCategory.IMAGE)
    GIF = (".gif", FileCategory.IMAGE)
    BMP = (".bmp", FileCategory.IMAGE)
    TIFF = (".tiff", FileCategory.IMAGE)
    
    DOCX = (".docx", FileCategory.WORD)
    DOC = (".doc", FileCategory.WORD)
    
    XLSX = (".xlsx", FileCategory.EXCEL)
    XLS = (".xls", FileCategory.EXCEL)
    CSV = (".csv", FileCategory.EXCEL)
    
    PPTX = (".pptx", FileCategory.POWERPOINT)
    PPT = (".ppt", FileCategory.POWERPOINT)
    
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

EXTENSION_MAP: Dict[str, FileType] = {
    ft.extension: ft for ft in FileType if ft.extension  
}

SUPPORTED_EXTENSIONS = [ft.extension for ft in FileType if ft.extension]  # Skip UNKNOWN
SUPPORTED_MIME_TYPES = list(MIME_TYPE_MAP.keys())

def get_file_type_from_path(file_path: str) -> FileType:
    import os
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    return EXTENSION_MAP.get(ext, FileType.UNKNOWN)

def get_file_type_from_mime(mime_type: str) -> FileType:
    return MIME_TYPE_MAP.get(mime_type, FileType.UNKNOWN)

def is_supported_file(file_path: str) -> bool:
    file_type = get_file_type_from_path(file_path)
    return file_type != FileType.UNKNOWN

def get_category_from_path(file_path: str) -> FileCategory:
    file_type = get_file_type_from_path(file_path)
    return file_type.category

def get_all_supported_extensions() -> List[str]:
    return SUPPORTED_EXTENSIONS.copy()

def get_extensions_by_category(category: FileCategory) -> List[str]:
    return [
        ft.extension for ft in FileType 
        if ft.category == category and ft.extension
    ]