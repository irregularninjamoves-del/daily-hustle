from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    has_bike: bool = False
    location_city: Optional[str] = None
    location_state: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfileResponse(BaseModel):
    preferred_categories: list[str] = []
    preferred_discount_types: list[str] = []
    has_bike: bool = False
    max_travel_radius_km: int = 10
    bike_travel_radius_km: int = 15
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    home_lat: Optional[float] = None
    home_lon: Optional[float] = None
    work_lat: Optional[float] = None
    work_lon: Optional[float] = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    profile: Optional[UserProfileResponse] = None

    class Config:
        from_attributes = True


class UserPreferencesUpdate(BaseModel):
    preferred_categories: Optional[list[str]] = None
    preferred_discount_types: Optional[list[str]] = None
    has_bike: Optional[bool] = None
    max_travel_radius_km: Optional[int] = None
    bike_travel_radius_km: Optional[int] = None
    home_lat: Optional[float] = None
    home_lon: Optional[float] = None
    work_lat: Optional[float] = None
    work_lon: Optional[float] = None
