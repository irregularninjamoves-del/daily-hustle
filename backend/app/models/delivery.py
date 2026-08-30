import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Boolean, Integer, Text, JSON
from ..database import Base


class DeliveryService(Base):
    """Bike-friendly delivery service directory."""
    __tablename__ = "delivery_services"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Company
    company_name = Column(String, nullable=False, unique=True)
    logo_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    # Vehicle acceptance
    accepts_bikes = Column(Boolean, default=False, index=True)
    accepts_cars = Column(Boolean, default=True)
    accepts_scooters = Column(Boolean, default=False)
    accepts_walking = Column(Boolean, default=False)
    
    # Requirements
    min_age = Column(Integer, default=18)
    background_check_required = Column(Boolean, default=True)
    vehicle_inspection_required = Column(Boolean, default=False)
    insurance_required = Column(Boolean, default=False)
    
    # Pay structure
    pay_structure = Column(JSON, nullable=True)  # {"base_per_delivery": 2.0, "per_mile": 0.58, "tips": true}
    pay_estimate_hourly = Column(String, nullable=True)  # "$15-25/hr"
    pay_estimate_weekly = Column(String, nullable=True)  # "$300-700/week"
    signup_bonus = Column(String, nullable=True)
    
    # Service areas
    service_areas = Column(JSON, default=list)  # [{"city": "Austin", "state": "TX", "lat": 30.2672, "lon": -97.7431, "radius_km": 25}]
    nationwide = Column(Boolean, default=False)
    
    # Hotspots and demand
    current_demand_zones = Column(JSON, nullable=True)  # Heatmap data
    peak_hours = Column(JSON, default=list)  # ["11am-2pm", "5pm-9pm"]
    
    # Signup
    signup_url = Column(String, nullable=False)
    referral_code = Column(String, nullable=True)
    
    # Pros/Cons
    pros = Column(JSON, default=list)  # ["Flexible schedule", "Weekly pay"]
    cons = Column(JSON, default=list)  # ["Wear and tear on bike", "Weather dependent"]
    
    # Ratings
    overall_rating = Column(Float, default=0.0)
    flexibility_rating = Column(Float, default=0.0)
    pay_rating = Column(Float, default=0.0)
    support_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
