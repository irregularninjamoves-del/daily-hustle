import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey, Integer, Enum, JSON, Text
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class User(Base):
    """User authentication model."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    interactions = relationship("UserInteraction", back_populates="user")
    saved_coupons = relationship("SavedCoupon", back_populates="user")
    saved_hustles = relationship("SavedHustle", back_populates="user")
    geofence_alerts = relationship("GeofenceAlert", back_populates="user")


class UserProfile(Base):
    """Extended user profile with preferences and location."""
    __tablename__ = "user_profiles"
    
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    
    # Preferences
    preferred_categories = Column(JSON, default=list)  # List of category strings
    preferred_discount_types = Column(JSON, default=list)  # ["percentage", "dollar", "bogo", "shipping"]
    has_bike = Column(Boolean, default=False)
    max_travel_radius_km = Column(Integer, default=10)
    bike_travel_radius_km = Column(Integer, default=15)
    
    # Location
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    location_updated_at = Column(DateTime, nullable=True)
    location_city = Column(String, nullable=True)
    location_state = Column(String, nullable=True)
    
    # Saved locations
    home_lat = Column(Float, nullable=True)
    home_lon = Column(Float, nullable=True)
    work_lat = Column(Float, nullable=True)
    work_lon = Column(Float, nullable=True)
    
    # ML state
    last_interaction_count = Column(Integer, default=0)  # For triggering retraining
    
    # Relationship
    user = relationship("User", back_populates="profile")


class InteractionType(enum.Enum):
    VIEW = "view"
    CLICK = "click"
    SAVE = "save"
    DISMISS = "dismiss"
    COPY = "copy"
    APPLY = "apply"


class ItemType(enum.Enum):
    COUPON = "coupon"
    HUSTLE = "hustle"
    DELIVERY = "delivery"


class UserInteraction(Base):
    """User interactions with items - training data for ML."""
    __tablename__ = "user_interactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    item_type = Column(Enum(ItemType), nullable=False)
    item_id = Column(String, nullable=False)
    action = Column(Enum(InteractionType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Context (optional)
    context_lat = Column(Float, nullable=True)  # Where was user when interaction happened
    context_lon = Column(Float, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="interactions")


class UserPreferenceVector(Base):
    """Persisted ML preference vector for each user."""
    __tablename__ = "user_preference_vectors"
    
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    vector = Column(Text, nullable=False)  # JSON-serialized numpy array
    dimension = Column(Integer, nullable=False)
    last_trained_at = Column(DateTime, default=datetime.utcnow)


class GeofenceAlert(Base):
    """Geofence subscriptions for push notifications."""
    __tablename__ = "geofence_alerts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    coupon_id = Column(String, ForeignKey("coupons.id"), nullable=False)
    trigger_radius_m = Column(Integer, default=500)  # meters
    is_active = Column(Boolean, default=True)
    last_triggered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="geofence_alerts")
    coupon = relationship("Coupon")
