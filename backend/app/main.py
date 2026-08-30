"""
Daily Hustle API
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db, AsyncSessionLocal
from .api.routes import (
    auth_router,
    coupons_router,
    hustles_router,
    delivery_router,
    location_router,
    recommendations_router,
    interactions_router,
    admin_router,
    notifications_router,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    await init_db()
    
    # Seed initial data
    try:
        async with AsyncSessionLocal() as db:
            from ..seed_data import seed_hustles, seed_delivery_services, seed_coupons
            await seed_hustles(db)
            await seed_delivery_services(db)
            await seed_coupons(db)
            print("✅ Database seeded successfully")
    except Exception as e:
        print(f"⚠️ Seeding skipped: {e}")
    
    yield
    # Shutdown
    pass


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered daily deals and side hustle finder with location-aware recommendations",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(coupons_router, prefix="/api")
app.include_router(hustles_router, prefix="/api")
app.include_router(delivery_router, prefix="/api")
app.include_router(location_router, prefix="/api")
app.include_router(recommendations_router, prefix="/api")
app.include_router(interactions_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(notifications_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "auth": "/api/auth",
            "coupons": "/api/coupons",
            "hustles": "/api/hustles",
            "delivery": "/api/delivery",
            "location": "/api/location",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
