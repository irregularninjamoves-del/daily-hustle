from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from .coupon import CouponResponse
from .hustle import SideHustleResponse
from .delivery import DeliveryServiceResponse


class LocationUpdate(BaseModel):
    lat: float
    lon: float
    accuracy: Optional[float] = None  # GPS accuracy in meters
    source: Optional[str] = "browser"  # "browser", "manual", "geocode"


class SavedLocation(BaseModel):
    name: str  # "home", "work", "gym", etc.
    lat: float
    lon: float
    address: Optional[str] = None


class UserLocationResponse(BaseModel):
    current_lat: Optional[float] = None
    current_lon: Optional[float] = None
    location_updated_at: Optional[datetime] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    saved_locations: list[SavedLocation]
    max_travel_radius_km: int
    bike_travel_radius_km: int


class NearbyRequest(BaseModel):
    lat: float
    lon: float
    radius_km: float = 10
    category: Optional[str] = None
    limit: int = 20


class NearbyResponse(BaseModel):
    coupons: list[CouponResponse]
    hustles: list[SideHustleResponse]
    delivery_services: list[DeliveryServiceResponse]
    total_nearby: int
    radius_km: float
    center: dict  # {"lat": x, "lon": y}


class ZoneCheckRequest(BaseModel):
    lat: float
    lon: float
    city: Optional[str] = None  # For display purposes


class ZoneCheckResponse(BaseModel):
    city: Optional[str]
    state: Optional[str]
    operating_services: list[DeliveryServiceResponse]
    non_operating_services: list[dict]  # {name, reason}
    bike_friendly_count: int


class GeofenceCreate(BaseModel):
    coupon_id: str
    trigger_radius_m: int = 500  # meters


class GeofenceResponse(BaseModel):
    id: str
    coupon: CouponResponse
    trigger_radius_m: int
    is_active: bool
    last_triggered_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class StoreMapRequest(BaseModel):
    lat: float
    lon: float
    radius_km: float = 10
    category: Optional[str] = None


class StoreMapResponse(BaseModel):
    stores: list[dict]  # GeoJSON-like: {id, name, lat, lon, category, deal_count}
    center: dict
    radius_km: float
