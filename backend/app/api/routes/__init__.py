from .auth import router as auth_router
from .coupons import router as coupons_router
from .hustles import router as hustles_router
from .delivery import router as delivery_router
from .location import router as location_router
from .recommendations import router as recommendations_router
from .interactions import router as interactions_router
from .admin import router as admin_router
from .notifications import router as notifications_router

__all__ = [
    "auth_router",
    "coupons_router",
    "hustles_router",
    "delivery_router",
    "location_router",
    "recommendations_router",
    "interactions_router",
    "admin_router",
    "notifications_router",
]