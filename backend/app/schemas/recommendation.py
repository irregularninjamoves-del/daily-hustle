from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

from .coupon import CouponResponse
from .hustle import SideHustleResponse
from .delivery import DeliveryServiceResponse


class ItemType(str, Enum):
    COUPON = "coupon"
    HUSTLE = "hustle"
    DELIVERY = "delivery"


class RecommendationRequest(BaseModel):
    limit: int = 20
    types: list[ItemType] = [ItemType.COUPON, ItemType.HUSTLE]
    include_exploration: bool = True
    lat: Optional[float] = None  # Optional - will use saved location if not provided
    lon: Optional[float] = None
    radius_km: Optional[float] = None  # Optional - will use profile setting


class RecommendationItem(BaseModel):
    id: str
    type: ItemType
    item: CouponResponse | SideHustleResponse | DeliveryServiceResponse
    score: float  # 0-1 similarity score
    ml_score: float  # Raw ML score
    freshness_boost: float
    proximity_score: Optional[float] = None
    total_score: float  # Final computed score
    explanation: str  # e.g., "Because you saved grocery coupons" or "Near your location"
    is_exploration: bool = False


class RecommendationResponse(BaseModel):
    items: list[RecommendationItem]
    total: int
    has_more: bool
    user_vector_last_updated: Optional[datetime] = None
    exploration_ratio: float  # How many items are exploration (vs personalized)
    

class MLProfileResponse(BaseModel):
    total_interactions: int
    top_categories: list[dict]  # [{"category": "Grocery", "score": 0.85}]
    preferred_discount_types: list[dict]
    activity_heatmap: list[dict]  # Activity by hour/day
    vector_dimension: int
    last_trained_at: Optional[datetime] = None
    learning_progress: str  # e.g., "75% - Keep interacting to improve recommendations!"
