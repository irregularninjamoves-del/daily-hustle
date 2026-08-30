import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Integer, Enum, Text, Index
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class DiscountType(enum.Enum):
    PERCENTAGE = "percentage"
    DOLLAR = "dollar"
    BOGO = "bogo"
    SHIPPING = "shipping"
    FREE = "free"
    OTHER = "other"


class Coupon(Base):
    """Coupon/deal model."""
    __tablename__ = "coupons"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Store info
    store_name = Column(String, nullable=False, index=True)
    store_name_normalized = Column(String, nullable=False, index=True)  # For dedup
    store_address = Column(String, nullable=True)
    store_lat = Column(Float, nullable=True)
    store_lon = Column(Float, nullable=True)
    store_place_id = Column(String, nullable=True)  # OSM/Google Place ID
    
    # Coupon details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    code = Column(String, nullable=True)  # Some are "click to redeem"
    discount_type = Column(Enum(DiscountType), default=DiscountType.OTHER)
    discount_value = Column(Float, nullable=True)  # Percentage or dollar amount
    discount_display = Column(String, nullable=True)  # e.g., "30% off" or "$5 off"
    
    # Categorization
    category = Column(String, nullable=False, index=True)  # e.g., "Food & Grocery"
    subcategory = Column(String, nullable=True)
    
    # Metadata
    expiry_date = Column(DateTime, nullable=True)
    is_online_only = Column(Boolean, default=False)
    source = Column(String, nullable=False)  # Which scraper found this
    source_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    
    # Engagement
    is_verified = Column(Boolean, default=False)
    times_used = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)  # 0-1
    
    # Status
    is_expired = Column(Boolean, default=False)
    is_removed = Column(Boolean, default=False)  # If source no longer has it
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scraped_at = Column(DateTime, nullable=False)
    
    # Relationships
    saved_by = relationship("SavedCoupon", back_populates="coupon")
    
    # Composite index for geospatial queries
    __table_args__ = (
        Index('ix_coupons_geo', 'store_lat', 'store_lon'),
        Index('ix_coupons_category_expiry', 'category', 'is_expired'),
    )


class SavedCoupon(Base):
    """User saved coupons."""
    __tablename__ = "saved_coupons"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    coupon_id = Column(String, ForeignKey("coupons.id"), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="saved_coupons")
    coupon = relationship("Coupon", back_populates="saved_by")
