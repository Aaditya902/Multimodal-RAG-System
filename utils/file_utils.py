import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional, BinaryIO
import streamlit as st
import hashlib
import re


@contextmanager
def temporary_file(uploaded_file) -> Generator[str, None, None]:

    temp_path = None
    try:
        suffix = Path(uploaded_file.name).suffix
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = tmp.name
        
        yield temp_path
        
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as e:
                st.warning(f"Failed to delete temp file: {str(e)}")

@contextmanager
def temporary_directory() -> Generator[str, None, None]:
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
    finally:
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)

def get_file_hash(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_file_size_str(file_size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if file_size < 1024.0:
            return f"{file_size:.1f} {unit}"
        file_size /= 1024.0
    return f"{file_size:.1f} TB"

def is_file_too_large(file_size: int, max_size_mb: int = 50) -> bool:
    return file_size > max_size_mb * 1024 * 1024

def safe_filename(filename: str) -> str:
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    return filename