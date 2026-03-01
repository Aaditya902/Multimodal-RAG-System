from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from .chunk import Chunk

@dataclass
class Document:
    
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    chunks: List[Chunk] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    processed_at: datetime = field(default_factory=datetime.now)
    
    @property
    def total_chunks(self) -> int:
        return len(self.chunks)
    
    @property
    def total_size(self) -> int:
        return sum(chunk.size for chunk in self.chunks)
    
    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)
    
    def get_chunks_by_page(self, page_number: int) -> List[Chunk]:
        return [c for c in self.chunks if c.page_number == page_number]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'chunks': [chunk.to_dict() for chunk in self.chunks],
            'metadata': self.metadata,
            'processed_at': self.processed_at.isoformat(),
            'total_chunks': self.total_chunks,
            'total_size': self.total_size
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        doc = cls(
            file_name=data['file_name'],
            file_path=data['file_path'],
            file_type=data['file_type'],
            file_size=data['file_size'],
            metadata=data.get('metadata', {}),
            processed_at=datetime.fromisoformat(data['processed_at']) if 'processed_at' in data else datetime.now()
        )
        
        for chunk_data in data.get('chunks', []):
            doc.add_chunk(Chunk.from_dict(chunk_data))
        
        return doc