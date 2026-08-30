"""Push notification routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...models import User
from ...api.deps import get_current_user
from ...services.notifications import send_push_notification

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/subscribe")
async def subscribe_push(
    subscription: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Subscribe to push notifications"""
    # Store subscription in user profile
    from ...models import UserProfile
    from sqlalchemy import select
    
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if profile:
        import json
        profile.push_subscription = json.dumps(subscription)
        await db.commit()
    
    return {"success": True, "message": "Subscribed to notifications"}


@router.post("/unsubscribe")
async def unsubscribe_push(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Unsubscribe from push notifications"""
    from ...models import UserProfile
    from sqlalchemy import select
    
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if profile:
        profile.push_subscription = None
        await db.commit()
    
    return {"success": True, "message": "Unsubscribed from notifications"}


@router.post("/test")
async def test_notification(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send test notification"""
    from ...models import UserProfile
    from sqlalchemy import select
    import json
    
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile or not profile.push_subscription:
        return {"success": False, "message": "No push subscription found"}
    
    subscription = json.loads(profile.push_subscription)
    
    success = await send_push_notification(
        subscription=subscription,
        title="🎉 Test Notification",
        body="Your Daily Hustle notifications are working!",
    )
    
    return {"success": success}
