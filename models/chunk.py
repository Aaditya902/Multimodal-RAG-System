"""Data model for document chunks"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime
import hashlib

@dataclass
class Chunk:
    """Represents a chunk of text from a document"""
    
    content: str
    source_file: str
    file_type: str
    page_number: Optional[int] = None
    chunk_index: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Generate unique ID after initialization"""
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique ID for chunk"""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()[:8]
        return f"{self.source_file}_{self.chunk_index}_{content_hash}"
    
    @property
    def preview(self) -> str:
        """Get preview of content"""
        return self.content[:200] + "..." if len(self.content) > 200 else self.content
    
    @property
    def size(self) -> int:
        """Get content size in characters"""
        return len(self.content)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'source_file': self.source_file,
            'file_type': self.file_type,
            'page_number': self.page_number,
            'chunk_index': self.chunk_index,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'preview': self.preview,
            'size': self.size
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chunk':
        """Create from dictionary"""
        return cls(
            content=data['content'],
            source_file=data['source_file'],
            file_type=data['file_type'],
            page_number=data.get('page_number'),
            chunk_index=data.get('chunk_index', 0),
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        )