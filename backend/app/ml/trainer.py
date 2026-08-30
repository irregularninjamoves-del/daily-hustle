"""ML Model Training and Retraining"""
import asyncio
from datetime import datetime
from sqlalchemy import select
from typing import List, Dict

from .engine import recommendation_engine, serialize_vector
from ..database import AsyncSessionLocal
from ..models import User, UserInteraction, UserPreferenceVector, Coupon, SideHustle


async def get_all_interactions(db, user_id: str) -> List[UserInteraction]:
    """Get all interactions for a user"""
    result = await db.execute(
        select(UserInteraction).where(UserInteraction.user_id == user_id)
    )
    return result.scalars().all()


async def get_interacted_items(db, interactions: List[UserInteraction]) -> Dict[str, any]:
    """Fetch items that user has interacted with"""
    items = {}
    
    for interaction in interactions:
        item_key = f"{interaction.item_type.value}:{interaction.item_id}"
        
        if interaction.item_type.value == "coupon":
            result = await db.execute(
                select(Coupon).where(Coupon.id == interaction.item_id)
            )
            item = result.scalar_one_or_none()
            if item:
                items[item_key] = item
        elif interaction.item_type.value == "hustle":
            result = await db.execute(
                select(SideHustle).where(SideHustle.id == interaction.item_id)
            )
            item = result.scalar_one_or_none()
            if item:
                items[item_key] = item
    
    return items


async def train_user_vectors():
    """Train/retrain user preference vectors for all users"""
    from ..config import get_settings
    settings = get_settings()
    
    async with AsyncSessionLocal() as db:
        # Get all coupons for fitting vectorizer
        result = await db.execute(select(Coupon).where(Coupon.is_expired == False))
        all_coupons = result.scalars().all()
        
        # Also get side hustles
        result = await db.execute(select(SideHustle).where(SideHustle.is_active == True))
        all_hustles = result.scalars().all()
        
        all_items = list(all_coupons) + list(all_hustles)
        
        if not all_items:
            return
        
        # Fit vectorizer on all items
        recommendation_engine.fit_vectorizer(all_items)
        
        # Get all users
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        for user in users:
            # Get user interactions
            interactions = await get_all_interactions(db, user.id)
            
            if not interactions:
                continue
            
            # Get items for interactions
            items_dict = await get_interacted_items(db, interactions)
            
            # Compute user vector
            user_vector = recommendation_engine.compute_user_vector(interactions, items_dict)
            
            # Save or update preference vector
            result = await db.execute(
                select(UserPreferenceVector).where(UserPreferenceVector.user_id == user.id)
            )
            pref_vector = result.scalar_one_or_none()
            
            if pref_vector:
                pref_vector.vector = serialize_vector(user_vector)
                pref_vector.last_trained_at = datetime.utcnow()
            else:
                pref_vector = UserPreferenceVector(
                    user_id=user.id,
                    vector=serialize_vector(user_vector),
                    dimension=len(user_vector),
                    last_trained_at=datetime.utcnow()
                )
                db.add(pref_vector)
        
        await db.commit()
        print(f"✅ Trained vectors for {len(users)} users")


async def retrain_all():
    """Full retraining - scheduled job"""
    print("🔄 Starting ML retraining...")
    await train_user_vectors()
    print("✅ ML retraining complete")


# For APScheduler
async def scheduled_retrain():
    """Wrapper for scheduled retraining"""
    await retrain_all()
