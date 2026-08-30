"""Recommendation API routes"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...database import get_db
from ...models import User, Coupon, SideHustle, UserInteraction, UserPreferenceVector
from ...schemas import RecommendationRequest, RecommendationResponse, RecommendationItem
from ...api.deps import get_current_user, get_optional_user
from ...ml.engine import recommendation_engine, deserialize_vector

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=RecommendationResponse)
async def get_recommendations(
    limit: int = 20,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get personalized recommendations for the user"""
    
    # Get user's preference vector
    result = await db.execute(
        select(UserPreferenceVector).where(UserPreferenceVector.user_id == current_user.id)
    )
    pref_vector = result.scalar_one_or_none()
    
    if not pref_vector:
        # Cold start - return trending items
        result = await db.execute(
            select(Coupon).where(Coupon.is_expired == False)
            .order_by(Coupon.times_used.desc())
            .limit(limit)
        )
        coupons = result.scalars().all()
        
        return RecommendationResponse(
            items=[
                RecommendationItem(
                    id=c.id,
                    type="coupon",
                    item=c,
                    score=0.5,
                    ml_score=0,
                    freshness_boost=1.0,
                    proximity_score=0,
                    total_score=0.5,
                    explanation="Popular right now",
                    is_exploration=True
                ) for c in coupons
            ],
            total=len(coupons),
            has_more=False,
            exploration_ratio=1.0
        )
    
    # Load user vector
    user_vector = deserialize_vector(pref_vector.vector)
    
    # Get all available items
    result = await db.execute(
        select(Coupon).where(Coupon.is_expired == False, Coupon.is_removed == False)
    )
    coupons = result.scalars().all()
    
    result = await db.execute(
        select(SideHustle).where(SideHustle.is_active == True)
    )
    hustles = result.scalars().all()
    
    all_items = list(coupons) + list(hustles)
    
    if not all_items:
        return RecommendationResponse(items=[], total=0, has_more=False)
    
    # Fit vectorizer if needed
    if not recommendation_engine.is_fitted:
        recommendation_engine.fit_vectorizer(all_items)
    
    # Get user location if not provided
    if lat is None and current_user.profile:
        lat = current_user.profile.location_lat
        lon = current_user.profile.location_lon
    
    # Get recommendations
    recommendations = recommendation_engine.get_recommendations(
        user_vector=user_vector,
        items=all_items,
        limit=limit,
        user_lat=lat,
        user_lon=lon
    )
    
    # Build response
    items = []
    for rec in recommendations:
        item = rec["item"]
        scores = rec["scores"]
        
        # Determine item type
        item_type = "coupon" if hasattr(item, 'store_name') else "hustle"
        
        items.append(RecommendationItem(
            id=item.id,
            type=item_type,
            item=item,
            score=scores["ml"],
            ml_score=scores["ml"],
            freshness_boost=scores["freshness"],
            proximity_score=scores["proximity"],
            total_score=scores["total"],
            explanation="Based on your interests" if not rec["is_exploration"] else "New for you to explore",
            is_exploration=rec["is_exploration"]
        ))
    
    exploration_count = sum(1 for i in items if i.is_exploration)
    
    return RecommendationResponse(
        items=items,
        total=len(items),
        has_more=len(all_items) > limit,
        user_vector_last_updated=pref_vector.last_trained_at,
        exploration_ratio=exploration_count / len(items) if items else 0
    )


@router.get("/ml-profile")
async def get_ml_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's ML learning progress"""
    
    # Get interaction count
    result = await db.execute(
        select(UserInteraction).where(UserInteraction.user_id == current_user.id)
    )
    interactions = result.scalars().all()
    
    # Get preference vector
    result = await db.execute(
        select(UserPreferenceVector).where(UserPreferenceVector.user_id == current_user.id)
    )
    pref_vector = result.scalar_one_or_none()
    
    # Calculate progress
    interaction_count = len(interactions)
    if interaction_count < 5:
        progress = "25% - Just getting started!"
    elif interaction_count < 20:
        progress = "50% - Learning your preferences"
    elif interaction_count < 50:
        progress = "75% - Getting personalized"
    else:
        progress = "100% - Fully personalized!"
    
    return {
        "total_interactions": interaction_count,
        "learning_progress": progress,
        "last_trained": pref_vector.last_trained_at if pref_vector else None,
        "message": f"Keep interacting! You've trained the bot with {interaction_count} actions."
    }
