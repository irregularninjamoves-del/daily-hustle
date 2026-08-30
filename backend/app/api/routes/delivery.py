"""Delivery service routes."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ...database import get_db
from ...models import DeliveryService
from ...schemas import DeliveryServiceResponse, DeliveryList, DeliverySearch

router = APIRouter(prefix="/delivery", tags=["delivery"])


@router.get("/", response_model=DeliveryList)
async def list_delivery_services(
    accepts_bikes: Optional[bool] = Query(default=True),
    city: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    search: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """List delivery services, optionally filtered by bike acceptance and location."""
    query = select(DeliveryService).where(DeliveryService.is_active == True)
    
    if accepts_bikes:
        query = query.where(DeliveryService.accepts_bikes == True)
    if search:
        query = query.where(DeliveryService.company_name.ilike(f"%{search}%"))
    
    # Get total
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar()
    
    # Pagination
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    services = result.scalars().all()
    
    # Check if operates in user area
    response_items = []
    for service in services:
        item = DeliveryServiceResponse.model_validate(service)
        if city:
            # Simple check if city is in service areas
            item.operates_in_user_area = any(
                area.get("city", "").lower() == city.lower() 
                for area in service.service_areas
            ) or service.nationwide
        response_items.append(item)
    
    return DeliveryList(
        items=response_items,
        total=total,
        page=page,
        limit=limit,
        has_more=(page * limit) < total
    )


@router.get("/bike-friendly", response_model=DeliveryList)
async def get_bike_delivery_options(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get delivery services that accept bike couriers."""
    query = select(DeliveryService).where(
        DeliveryService.is_active == True,
        DeliveryService.accepts_bikes == True
    ).order_by(DeliveryService.overall_rating.desc()).limit(limit)
    
    result = await db.execute(query)
    services = result.scalars().all()
    
    return DeliveryList(
        items=[DeliveryServiceResponse.model_validate(s) for s in services],
        total=len(services),
        page=1,
        limit=limit,
        has_more=False
    )
