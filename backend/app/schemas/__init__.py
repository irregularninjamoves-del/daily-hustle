from .auth import UserCreate, UserResponse, UserLogin, TokenResponse
from .coupon import CouponCreate, CouponResponse, CouponSearch, CouponList, SavedCouponCreate
from .hustle import SideHustleCreate, SideHustleResponse, HustleSearch, HustleList, SavedHustleCreate
from .delivery import DeliveryServiceCreate, DeliveryServiceResponse, DeliverySearch, DeliveryList
from .interaction import InteractionCreate, InteractionResponse, InteractionHistory
from .recommendation import RecommendationRequest, RecommendationResponse, RecommendationItem
from .location import LocationUpdate, NearbyRequest, NearbyResponse, GeofenceCreate, GeofenceResponse

__all__ = [
    "UserCreate",
    "UserResponse",
    "UserLogin",
    "TokenResponse",
    "CouponCreate",
    "CouponResponse",
    "CouponSearch",
    "CouponList",
    "SavedCouponCreate",
    "SideHustleCreate",
    "SideHustleResponse",
    "HustleSearch",
    "HustleList",
    "SavedHustleCreate",
    "DeliveryServiceCreate",
    "DeliveryServiceResponse",
    "DeliverySearch",
    "DeliveryList",
    "InteractionCreate",
    "InteractionResponse",
    "InteractionHistory",
    "RecommendationRequest",
    "RecommendationResponse",
    "RecommendationItem",
    "LocationUpdate",
    "NearbyRequest",
    "NearbyResponse",
    "GeofenceCreate",
    "GeofenceResponse",
]