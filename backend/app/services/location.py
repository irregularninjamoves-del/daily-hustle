import math
import httpx
from typing import Optional
from ..config import get_settings

settings = get_settings()


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees).
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r


def is_within_radius(
    center_lat: float, 
    center_lon: float, 
    point_lat: float, 
    point_lon: float, 
    radius_km: float
) -> bool:
    """Check if a point is within a radius from center."""
    return haversine_distance(center_lat, center_lon, point_lat, point_lon) <= radius_km


def get_bounding_box(lat: float, lon: float, radius_km: float) -> tuple:
    """
    Get approximate bounding box for a radius search.
    Returns (min_lat, max_lat, min_lon, max_lon).
    """
    # Approximate degrees per km
    lat_delta = radius_km / 111  # 1 degree lat ≈ 111 km
    lon_delta = radius_km / (111 * math.cos(math.radians(lat)))  # Adjust for longitude
    
    return (
        lat - lat_delta,  # min_lat
        lat + lat_delta,  # max_lat
        lon - lon_delta,  # min_lon
        lon + lon_delta   # max_lon
    )


async def geocode_address(address: str) -> Optional[dict]:
    """
    Geocode an address using OpenStreetMap Nominatim.
    Returns {lat, lon, display_name} or None.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.GEOCODING_API_URL}/search",
                params={
                    "q": address,
                    "format": "json",
                    "limit": 1
                },
                headers={
                    "User-Agent": "DailyHustle/1.0"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                return {
                    "lat": float(data[0]["lat"]),
                    "lon": float(data[0]["lon"]),
                    "display_name": data[0]["display_name"],
                    "place_id": data[0].get("place_id")
                }
            return None
    except Exception:
        return None


async def reverse_geocode(lat: float, lon: float) -> Optional[dict]:
    """
    Reverse geocode coordinates to get city/state.
    Returns {city, state, display_name} or None.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.GEOCODING_API_URL}/reverse",
                params={
                    "lat": lat,
                    "lon": lon,
                    "format": "json"
                },
                headers={
                    "User-Agent": "DailyHustle/1.0"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            if "address" in data:
                address = data["address"]
                return {
                    "city": address.get("city") or address.get("town") or address.get("village"),
                    "state": address.get("state"),
                    "country": address.get("country"),
                    "display_name": data.get("display_name")
                }
            return None
    except Exception:
        return None


def format_distance(distance_km: float) -> str:
    """Format distance for display."""
    if distance_km < 1:
        return f"{int(distance_km * 1000)}m"
    elif distance_km < 10:
        return f"{distance_km:.1f}km"
    else:
        return f"{int(distance_km)}km"


def truncate_coordinates(lat: float, lon: float, decimals: int = 3) -> tuple:
    """
    Truncate coordinates to N decimal places for privacy.
    ~3 decimals = ~110m accuracy, good for nearby deals while protecting exact location.
    """
    factor = 10 ** decimals
    return (math.trunc(lat * factor) / factor, math.trunc(lon * factor) / factor)
