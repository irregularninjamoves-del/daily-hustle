from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    DOLLAR = "dollar"
    BOGO = "bogo"
    SHIPPING = "shipping"
    FREE = "free"
    OTHER = "other"


class CouponBase(BaseModel):
    store_name: str
    title: str
    description: Optional[str] = None
    code: Optional[str] = None
    discount_type: DiscountType = DiscountType.OTHER
    discount_value: Optional[float] = None
    discount_display: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_online_only: bool = False
    store_address: Optional[str] = None
    store_lat: Optional[float] = None
    store_lon: Optional[float] = None


class CouponCreate(CouponBase):
    source: str
    source_url: Optional[str] = None
    image_url: Optional[str] = None


class CouponResponse(CouponBase):
    id: str
    source: str
    source_url: Optional[str] = None
    image_url: Optional[str] = None
    is_verified: bool
    times_used: int
    success_rate: float
    is_expired: bool
    created_at: datetime
    distance_km: Optional[float] = None  # Computed for nearby queries
    ml_score: Optional[float] = None  # Computed for recommendations
    
    class Config:
        from_attributes = True


class CouponSearch(BaseModel):
    search: Optional[str] = None
    category: Optional[str] = None
    discount_type: Optional[DiscountType] = None
    store: Optional[str] = None
    is_online_only: Optional[bool] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    radius_km: Optional[float] = 10
    page: int = 1
    limit: int = 20


class CouponList(BaseModel):
    items: list[CouponResponse]
    total: int
    page: int
    limit: int
    has_more: bool


class SavedCouponCreate(BaseModel):
    coupon_id: str


class SavedCouponResponse(BaseModel):
    id: str
    coupon: CouponResponse
    saved_at: datetime
    
    class Config:
        from_attributes = True
