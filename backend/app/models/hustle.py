import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Integer, Enum, Text, JSON
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class HustleType(enum.Enum):
    FREELANCE = "freelance"
    DELIVERY = "delivery"
    SURVEYS = "surveys"
    CASHBACK = "cashback"
    MYSTERY_SHOPPING = "mystery_shopping"
    TEACHING = "teaching"
    FOCUS_GROUPS = "focus_groups"
    TASK_APPS = "task_apps"
    DRIVING = "driving"
    CAREGIVING = "caregiving"
    OTHER = "other"


class PayType(enum.Enum):
    HOURLY = "hourly"
    PER_TASK = "per_task"
    COMMISSION = "commission"
    LUMP_SUM = "lump_sum"


class SideHustle(Base):
    """Side hustle/gig opportunity model."""
    __tablename__ = "side_hustles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Company/Platform
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    hustle_type = Column(Enum(HustleType), nullable=False, index=True)
    
    # Pay
    pay_rate = Column(String, nullable=True)  # e.g., "$15-25/hr" or "$5-50 per survey"
    pay_type = Column(Enum(PayType), nullable=True)
    pay_min = Column(Float, nullable=True)
    pay_max = Column(Float, nullable=True)
    
    # Requirements
    requirements = Column(JSON, default=list)  # List of requirement strings
    time_commitment = Column(String, nullable=True)  # "Flexible", "5-10 hrs/week", etc.
    skills_needed = Column(JSON, default=list)
    equipment_needed = Column(JSON, default=list)
    
    # Location
    is_remote = Column(Boolean, default=False)
    is_bike_friendly = Column(Boolean, default=False)
    location_city = Column(String, nullable=True)
    location_state = Column(String, nullable=True)
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    is_location_based = Column(Boolean, default=False)
    
    # Apply
    apply_url = Column(String, nullable=False)
    signup_bonus = Column(String, nullable=True)
    referral_code = Column(String, nullable=True)
    
    # Engagement
    rating = Column(Float, default=0.0)  # 0-5
    review_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    saved_by = relationship("SavedHustle", back_populates="hustle")


class SavedHustle(Base):
    """User saved hustles."""
    __tablename__ = "saved_hustles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    hustle_id = Column(String, ForeignKey("side_hustles.id"), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="saved_hustles")
    hustle = relationship("SideHustle", back_populates="saved_by")
