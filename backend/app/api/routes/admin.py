"""Admin dashboard routes"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from ...database import get_db
from ...models import User, Coupon, SideHustle, DeliveryService, ScraperRun, UserInteraction
from ...api.deps import get_current_user
from ...services.scraper_manager import scraper_manager

router = APIRouter(prefix="/admin", tags=["admin"])


def is_admin(user: User):
    """Check if user is admin (simplified - check email domain)"""
    return user.email.endswith("@admin.com") or user.is_active  # Adjust as needed


@router.get("/dashboard")
async def admin_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin dashboard stats"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # User stats
    result = await db.execute(select(func.count()).select_from(select(User)))
    total_users = result.scalar()
    
    # Coupon stats
    result = await db.execute(select(func.count()).select_from(select(Coupon)))
    total_coupons = result.scalar()
    
    result = await db.execute(
        select(func.count()).select_from(
            select(Coupon).where(Coupon.is_expired == False)
        )
    )
    active_coupons = result.scalar()
    
    # Hustle stats
    result = await db.execute(select(func.count()).select_from(select(SideHustle)))
    total_hustles = result.scalar()
    
    # Delivery stats
    result = await db.execute(
        select(func.count()).select_from(
            select(DeliveryService).where(DeliveryService.accepts_bikes == True)
        )
    )
    bike_delivery = result.scalar()
    
    # Today's interactions
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    result = await db.execute(
        select(func.count()).select_from(
            select(UserInteraction).where(UserInteraction.timestamp >= today)
        )
    )
    today_interactions = result.scalar()
    
    return {
        "users": {"total": total_users},
        "coupons": {"total": total_coupons, "active": active_coupons},
        "hustles": {"total": total_hustles},
        "delivery": {"bike_friendly": bike_delivery},
        "engagement": {"today_interactions": today_interactions},
        "scrapers": scraper_manager.get_scraper_names()
    }


@router.post("/scrapers/trigger/{scraper_name}")
async def trigger_scraper(
    scraper_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually trigger a scraper"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await scraper_manager.scrape_single(scraper_name)
    
    return {
        "scraper": scraper_name,
        "result": result,
        "triggered_at": datetime.utcnow()
    }


@router.post("/scrapers/trigger-all")
async def trigger_all_scrapers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger all scrapers"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    results = await scraper_manager.scrape_all()
    
    return {
        "results": results,
        "triggered_at": datetime.utcnow()
    }


@router.get("/users")
async def list_users(
    page: int = 1,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all users (admin only)"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.execute(
        select(User)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    users = result.scalars().all()
    
    return [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]


@router.post("/hustles/create")
async def create_hustle(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new hustle (admin only)"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    hustle = SideHustle(**data)
    db.add(hustle)
    await db.commit()
    
    return {"id": hustle.id, "message": "Hustle created successfully"}


@router.post("/delivery/create")
async def create_delivery_service(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new delivery service (admin only)"""
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    service = DeliveryService(**data)
    db.add(service)
    await db.commit()
    
    return {"id": service.id, "message": "Delivery service created successfully"}
