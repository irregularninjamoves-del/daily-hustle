from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class HustleType(str, Enum):
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


class PayType(str, Enum):
    HOURLY = "hourly"
    PER_TASK = "per_task"
    COMMISSION = "commission"
    LUMP_SUM = "lump_sum"


class SideHustleBase(BaseModel):
    title: str
    company: str
    description: str
    hustle_type: HustleType
    pay_rate: Optional[str] = None
    pay_type: Optional[PayType] = None
    pay_min: Optional[float] = None
    pay_max: Optional[float] = None
    is_remote: bool = False
    is_bike_friendly: bool = False
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    is_location_based: bool = False
    time_commitment: Optional[str] = None


class SideHustleCreate(SideHustleBase):
    requirements: list[str] = []
    skills_needed: list[str] = []
    equipment_needed: list[str] = []
    apply_url: str
    signup_bonus: Optional[str] = None
    referral_code: Optional[str] = None
    pros: list[str] = []
    cons: list[str] = []


class SideHustleResponse(SideHustleBase):
    id: str
    requirements: list[str]
    skills_needed: list[str]
    equipment_needed: list[str]
    apply_url: str
    signup_bonus: Optional[str] = None
    referral_code: Optional[str] = None
    rating: float
    review_count: int
    is_active: bool
    is_featured: bool
    created_at: datetime
    pros: list[str]
    cons: list[str]
    distance_km: Optional[float] = None
    ml_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class HustleSearch(BaseModel):
    hustle_type: Optional[HustleType] = None
    is_remote: Optional[bool] = None
    is_bike_friendly: Optional[bool] = None
    search: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    radius_km: Optional[float] = 15
    page: int = 1
    limit: int = 20


class HustleList(BaseModel):
    items: list[SideHustleResponse]
    total: int
    page: int
    limit: int
    has_more: bool


class SavedHustleCreate(BaseModel):
    hustle_id: str


class SavedHustleResponse(BaseModel):
    id: str
    hustle: SideHustleResponse
    saved_at: datetime
    
    class Config:
        from_attributes = True
