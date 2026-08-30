from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class ItemType(str, Enum):
    COUPON = "coupon"
    HUSTLE = "hustle"
    DELIVERY = "delivery"


class InteractionType(str, Enum):
    VIEW = "view"
    CLICK = "click"
    SAVE = "save"
    DISMISS = "dismiss"
    COPY = "copy"
    APPLY = "apply"


class InteractionCreate(BaseModel):
    item_type: ItemType
    item_id: str
    action: InteractionType


class InteractionResponse(BaseModel):
    id: str
    item_type: ItemType
    item_id: str
    action: InteractionType
    timestamp: datetime
    
    class Config:
        from_attributes = True


class InteractionHistory(BaseModel):
    total_interactions: int
    by_type: dict[str, int]
    recent: list[InteractionResponse]
    category_engagement: dict[str, float]  # ML-derived preference scores
