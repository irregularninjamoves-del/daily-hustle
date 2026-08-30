from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DeliveryServiceBase(BaseModel):
    company_name: str
    accepts_bikes: bool = False
    accepts_cars: bool = True
    accepts_scooters: bool = False
    accepts_walking: bool = False


class DeliveryServiceCreate(DeliveryServiceBase):
    description: Optional[str] = None
    logo_url: Optional[str] = None
    min_age: int = 18
    background_check_required: bool = True
    vehicle_inspection_required: bool = False
    insurance_required: bool = False
    pay_structure: Optional[dict] = None
    pay_estimate_hourly: Optional[str] = None
    pay_estimate_weekly: Optional[str] = None
    signup_bonus: Optional[str] = None
    service_areas: list[dict] = []
    nationwide: bool = False
    peak_hours: list[str] = []
    signup_url: str
    referral_code: Optional[str] = None
    pros: list[str] = []
    cons: list[str] = []
    overall_rating: float = 0.0
    flexibility_rating: float = 0.0
    pay_rating: float = 0.0
    support_rating: float = 0.0


class DeliveryServiceResponse(DeliveryServiceBase):
    id: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    min_age: int
    background_check_required: bool
    vehicle_inspection_required: bool
    insurance_required: bool
    pay_structure: Optional[dict] = None
    pay_estimate_hourly: Optional[str] = None
    pay_estimate_weekly: Optional[str] = None
    signup_bonus: Optional[str] = None
    service_areas: list[dict]
    nationwide: bool
    peak_hours: list[str]
    signup_url: str
    referral_code: Optional[str] = None
    pros: list[str]
    cons: list[str]
    overall_rating: float
    flexibility_rating: float
    pay_rating: float
    support_rating: float
    review_count: int
    is_active: bool
    is_featured: bool
    created_at: datetime
    operates_in_user_area: Optional[bool] = None
    
    class Config:
        from_attributes = True


class DeliverySearch(BaseModel):
    accepts_bikes: Optional[bool] = True
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 20


class DeliveryList(BaseModel):
    items: list[DeliveryServiceResponse]
    total: int
    page: int
    limit: int
    has_more: bool


class DeliveryComparison(BaseModel):
    services: list[DeliveryServiceResponse]
    comparison_fields: list[str]  # Which fields are being compared
