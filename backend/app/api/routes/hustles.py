"""Side hustle routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ...database import get_db
from ...models import SideHustle, SavedHustle
from ...schemas import SideHustleResponse, HustleList, HustleSearch, SavedHustleCreate, SavedHustleResponse
from ...api.deps import get_current_user
from ...services import is_within_radius

router = APIRouter(prefix="/hustles", tags=["hustles"])


@router.get("/", response_model=HustleList)
async def list_hustles(
    hustle_type: Optional[str] = None,
    is_remote: Optional[bool] = None,
    is_bike_friendly: Optional[bool] = Query(default=None),
    search: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: float = Query(default=15, ge=1, le=50),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List side hustles with filtering."""
    query = select(SideHustle).where(SideHustle.is_active == True)
    
    if hustle_type:
        query = query.where(SideHustle.hustle_type == hustle_type)
    if is_remote is not None:
        query = query.where(SideHustle.is_remote == is_remote)
    if is_bike_friendly is not None:
        query = query.where(SideHustle.is_bike_friendly == is_bike_friendly)
    if search:
        query = query.where(
            SideHustle.title.ilike(f"%{search}%") | 
            SideHustle.company.ilike(f"%{search}%")
        )
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar()
    
    # Pagination
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    hustles = result.scalars().all()
    
    # Calculate distances
    response_items = []
    for hustle in hustles:
        item = SideHustleResponse.model_validate(hustle)
        if lat and lon and hustle.location_lat and hustle.location_lon:
            item.distance_km = is_within_radius(lat, lon, hustle.location_lat, hustle.location_lon, radius_km)
        response_items.append(item)
    
    return HustleList(
        items=response_items,
        total=total,
        page=page,
        limit=limit,
        has_more=(page * limit) < total
    )


@router.get("/types")
async def get_hustle_types(db: AsyncSession = Depends(get_db)):
    """Get available hustle types."""
    result = await db.execute(select(SideHustle.hustle_type).distinct())
    return {"types": [row[0] for row in result.fetchall()]}


@router.get("/bike-friendly", response_model=HustleList)
async def get_bike_friendly_hustles(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: float = Query(default=20, ge=1, le=50),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get hustles suitable for bike riders."""
    query = select(SideHustle).where(
        SideHustle.is_active == True,
        SideHustle.is_bike_friendly == True
    ).limit(limit)
    
    result = await db.execute(query)
    hustles = result.scalars().all()
    
    response_items = []
    for hustle in hustles:
        item = SideHustleResponse.model_validate(hustle)
        if lat and lon and hustle.location_lat and hustle.location_lon:
            item.distance_km = is_within_radius(lat, lon, hustle.location_lat, hustle.location_lon, radius_km)
        response_items.append(item)
    
    return HustleList(
        items=response_items,
        total=len(response_items),
        page=1,
        limit=limit,
        has_more=False
    )


@router.post("/save", response_model=SavedHustleResponse)
async def save_hustle(
    data: SavedHustleCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Save a hustle for later."""
    result = await db.execute(
        select(SavedHustle).where(
            SavedHustle.user_id == current_user.id,
            SavedHustle.hustle_id == data.hustle_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Hustle already saved")
    
    saved = SavedHustle(user_id=current_user.id, hustle_id=data.hustle_id)
    db.add(saved)
    await db.commit()
    
    return saved
