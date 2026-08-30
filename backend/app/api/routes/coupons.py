"""Coupon routes."""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from ...database import get_db
from ...models import Coupon, SavedCoupon
from ...schemas import CouponResponse, CouponList, CouponSearch, SavedCouponCreate, SavedCouponResponse
from ...api.deps import get_current_user, get_optional_user
from ...services import is_within_radius

router = APIRouter(prefix="/coupons", tags=["coupons"])


@router.get("/", response_model=CouponList)
async def list_coupons(
    search: Optional[str] = None,
    category: Optional[str] = None,
    discount_type: Optional[str] = None,
    store: Optional[str] = None,
    is_online_only: Optional[bool] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: float = Query(default=10, ge=1, le=50),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_optional_user)
):
    """List coupons with optional filtering."""
    query = select(Coupon).where(Coupon.is_expired == False).where(Coupon.is_removed == False)
    
    # Apply filters
    if search:
        search_filter = or_(
            Coupon.store_name.ilike(f"%{search}%"),
            Coupon.title.ilike(f"%{search}%"),
            Coupon.description.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    if category:
        query = query.where(Coupon.category == category)
    
    if discount_type:
        query = query.where(Coupon.discount_type == discount_type)
    
    if store:
        query = query.where(Coupon.store_name.ilike(f"%{store}%"))
    
    if is_online_only is not None:
        query = query.where(Coupon.is_online_only == is_online_only)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar()
    
    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    coupons = result.scalars().all()
    
    # Calculate distances if location provided
    response_items = []
    for coupon in coupons:
        item = CouponResponse.model_validate(coupon)
        if lat and lon and coupon.store_lat and coupon.store_lon:
            item.distance_km = is_within_radius(lat, lon, coupon.store_lat, coupon.store_lon, radius_km)
        response_items.append(item)
    
    return CouponList(
        items=response_items,
        total=total,
        page=page,
        limit=limit,
        has_more=(page * limit) < total
    )


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all unique categories."""
    result = await db.execute(select(Coupon.category).distinct())
    return {"categories": [row[0] for row in result.fetchall()]}


@router.get("/trending", response_model=CouponList)
async def get_trending(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get trending coupons (most used)."""
    query = select(Coupon).where(
        Coupon.is_expired == False
    ).order_by(Coupon.times_used.desc()).limit(limit)
    
    result = await db.execute(query)
    coupons = result.scalars().all()
    
    return CouponList(
        items=[CouponResponse.model_validate(c) for c in coupons],
        total=len(coupons),
        page=1,
        limit=limit,
        has_more=False
    )


@router.post("/save", response_model=SavedCouponResponse)
async def save_coupon(
    data: SavedCouponCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Save a coupon for later."""
    # Check if already saved
    result = await db.execute(
        select(SavedCoupon).where(
            SavedCoupon.user_id == current_user.id,
            SavedCoupon.coupon_id == data.coupon_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Coupon already saved")
    
    saved = SavedCoupon(user_id=current_user.id, coupon_id=data.coupon_id)
    db.add(saved)
    await db.commit()
    
    return saved
