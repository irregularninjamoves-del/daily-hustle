"""Location-based routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ...database import get_db
from ...models import Coupon, SideHustle, DeliveryService, UserProfile
from ...schemas import (
    LocationUpdate, UserLocationResponse, NearbyRequest, NearbyResponse,
    StoreMapRequest, StoreMapResponse, ZoneCheckRequest, ZoneCheckResponse,
    GeofenceCreate, GeofenceResponse
)
from ...api.deps import get_current_user, get_optional_user
from ...services import reverse_geocode, is_within_radius
from ...services.location import get_bounding_box, truncate_coordinates

router = APIRouter(prefix="/location", tags=["location"])


@router.post("/update")
async def update_location(
    data: LocationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update user's current location."""
    # Truncate coordinates for privacy (3 decimal places = ~110m accuracy)
    lat, lon = truncate_coordinates(data.lat, data.lon, decimals=3)
    
    # Get location info
    location_info = None
    if data.source == "browser":
        location_info = await reverse_geocode(lat, lon)
    
    # Update profile
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if profile:
        profile.location_lat = lat
        profile.location_lon = lon
        profile.location_updated_at = datetime.utcnow()
        if location_info:
            profile.location_city = location_info.get("city")
            profile.location_state = location_info.get("state")
    
    await db.commit()
    
    return {
        "success": True,
        "lat": lat,
        "lon": lon,
        "city": location_info.get("city") if location_info else None,
        "state": location_info.get("state") if location_info else None
    }


@router.get("/nearby-deals")
async def get_nearby_deals(
    lat: float,
    lon: float,
    radius_km: float = 10,
    category: Optional[str] = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get deals at stores near the user."""
    # Use bounding box for initial filter (fast)
    min_lat, max_lat, min_lon, max_lon = get_bounding_box(lat, lon, radius_km)
    
    query = select(Coupon).where(
        Coupon.is_expired == False,
        Coupon.is_removed == False,
        Coupon.store_lat.between(min_lat, max_lat),
        Coupon.store_lon.between(min_lon, max_lon)
    )
    
    if category:
        query = query.where(Coupon.category == category)
    
    result = await db.execute(query)
    coupons = result.scalars().all()
    
    # Filter by exact distance and sort
    nearby = []
    for coupon in coupons:
        if coupon.store_lat and coupon.store_lon:
            dist = is_within_radius(lat, lon, coupon.store_lat, coupon.store_lon, radius_km)
            if isinstance(dist, float):
                nearby.append((coupon, dist))
    
    # Sort by distance
    nearby.sort(key=lambda x: x[1])
    
    # Build response
    items = []
    for coupon, dist in nearby[:limit]:
        item = CouponResponse.model_validate(coupon)
        item.distance_km = dist
        items.append(item)
    
    return {"coupons": items, "count": len(items), "radius_km": radius_km}


@router.post("/zone-check", response_model=ZoneCheckResponse)
async def check_delivery_zone(
    data: ZoneCheckRequest,
    db: AsyncSession = Depends(get_db)
):
    """Check which delivery services operate at a location."""
    # Get location info if city not provided
    location_info = None
    if not data.city:
        location_info = await reverse_geocode(data.lat, data.lon)
        city = location_info.get("city") if location_info else None
    else:
        city = data.city
    
    # Get all active delivery services
    result = await db.execute(
        select(DeliveryService).where(DeliveryService.is_active == True)
    )
    services = result.scalars().all()
    
    operating = []
    non_operating = []
    bike_count = 0
    
    for service in services:
        # Check if operates in this area
        operates = service.nationwide or any(
            area.get("city", "").lower() == city.lower() 
            for area in service.service_areas
        ) if city else False
        
        service_data = DeliveryServiceResponse.model_validate(service)
        service_data.operates_in_user_area = operates
        
        if operates:
            operating.append(service_data)
            if service.accepts_bikes:
                bike_count += 1
        else:
            non_operating.append({
                "name": service.company_name,
                "reason": "Not available in this area"
            })
    
    return ZoneCheckResponse(
        city=city,
        state=location_info.get("state") if location_info else None,
        operating_services=operating,
        non_operating_services=non_operating,
        bike_friendly_count=bike_count
    )


from datetime import datetime  # Import at bottom to avoid circular
from ...schemas import CouponResponse  # Import here
