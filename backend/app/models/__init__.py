from .user import User, UserProfile, UserInteraction, UserPreferenceVector, GeofenceAlert
from .coupon import Coupon, SavedCoupon
from .hustle import SideHustle, SavedHustle
from .delivery import DeliveryService
from .scraper import ScraperRun

__all__ = [
    "User",
    "UserProfile",
    "UserInteraction",
    "UserPreferenceVector",
    "GeofenceAlert",
    "Coupon",
    "SavedCoupon",
    "SideHustle",
    "SavedHustle",
    "DeliveryService",
    "ScraperRun",
]