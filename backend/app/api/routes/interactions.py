"""User interaction tracking for ML"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from ...database import get_db
from ...models import User, UserInteraction, ItemType, InteractionType
from ...schemas import InteractionCreate, InteractionResponse, InteractionHistory
from ...api.deps import get_current_user

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("/", response_model=InteractionResponse)
async def log_interaction(
    data: InteractionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Log a user interaction for ML training"""
    
    interaction = UserInteraction(
        user_id=current_user.id,
        item_type=data.item_type,
        item_id=data.item_id,
        action=data.action,
        timestamp=datetime.utcnow()
    )
    
    db.add(interaction)
    await db.commit()
    
    return interaction


@router.get("/history", response_model=InteractionHistory)
async def get_interaction_history(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's interaction history"""
    
    # Get total count
    result = await db.execute(
        select(func.count()).select_from(
            select(UserInteraction).where(UserInteraction.user_id == current_user.id)
        )
    )
    total = result.scalar()
    
    # Get recent interactions
    result = await db.execute(
        select(UserInteraction)
        .where(UserInteraction.user_id == current_user.id)
        .order_by(UserInteraction.timestamp.desc())
        .limit(limit)
    )
    recent = result.scalars().all()
    
    # Get counts by type
    result = await db.execute(
        select(UserInteraction.action, func.count())
        .where(UserInteraction.user_id == current_user.id)
        .group_by(UserInteraction.action)
    )
    by_type = {row[0].value: row[1] for row in result.fetchall()}
    
    return InteractionHistory(
        total_interactions=total,
        by_type=by_type,
        recent=recent,
        category_engagement={}  # Would need to join with items
    )


@router.get("/stats")
async def get_interaction_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get interaction statistics"""
    
    # Today's interactions
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    result = await db.execute(
        select(func.count()).select_from(
            select(UserInteraction)
            .where(UserInteraction.user_id == current_user.id)
            .where(UserInteraction.timestamp >= today)
        )
    )
    today_count = result.scalar()
    
    # This week
    week_ago = datetime.utcnow() - __import__('datetime').timedelta(days=7)
    result = await db.execute(
        select(func.count()).select_from(
            select(UserInteraction)
            .where(UserInteraction.user_id == current_user.id)
            .where(UserInteraction.timestamp >= week_ago)
        )
    )
    week_count = result.scalar()
    
    return {
        "today": today_count,
        "this_week": week_count,
        "total_engagement_score": today_count + week_count * 0.1
    }
