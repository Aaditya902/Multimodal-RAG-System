"""Data model for search results"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from .chunk import Chunk

@dataclass
class SearchResult:
    """Represents a search result"""
    
    chunk: Chunk
    score: float
    query: str
    rank: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def confidence_level(self) -> str:
        """Get confidence level based on score"""
        if self.score > 0.7:
            return "high"
        elif self.score > 0.4:
            return "medium"
        else:
            return "low"
    
    @property
    def confidence_color(self) -> str:
        """Get color for confidence level"""
        return {
            "high": "green",
            "medium": "orange",
            "low": "red"
        }.get(self.confidence_level, "gray")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'chunk': self.chunk.to_dict(),
            'score': self.score,
            'query': self.query,
            'rank': self.rank,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat(),
            'confidence_level': self.confidence_level
        }

@dataclass
class SearchResponse:
    """Represents a complete search response"""
    
    query: str
    results: List[SearchResult]
    total_found: int
    processing_time: float
    model_used: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def top_result(self) -> Optional[SearchResult]:
        """Get top result"""
        return self.results[0] if self.results else None
    
    @property
    def average_score(self) -> float:
        """Get average score of results"""
        if not self.results:
            return 0.0
        return sum(r.score for r in self.results) / len(self.results)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'query': self.query,
            'results': [r.to_dict() for r in self.results],
            'total_found': self.total_found,
            'processing_time': self.processing_time,
            'model_used': self.model_used,
            'metadata': self.metadata,
            'average_score': self.average_score
        }