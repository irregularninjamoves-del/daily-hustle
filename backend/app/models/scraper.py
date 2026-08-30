import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Enum, Text
from ..database import Base
import enum


class ScraperStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


class ScraperRun(Base):
    """Track scraper runs for monitoring."""
    __tablename__ = "scraper_runs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_name = Column(String, nullable=False, index=True)  # e.g., "retailmenot", "slickdeals"
    status = Column(Enum(ScraperStatus), default=ScraperStatus.PENDING)
    
    # Results
    items_found = Column(Integer, default=0)
    items_new = Column(Integer, default=0)
    items_updated = Column(Integer, default=0)
    items_expired = Column(Integer, default=0)
    
    # Errors
    errors = Column(Text, nullable=True)
    error_count = Column(Integer, default=0)
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
