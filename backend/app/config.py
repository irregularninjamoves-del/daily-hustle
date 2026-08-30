from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./daily_hustle.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # App
    APP_NAME: str = "Daily Hustle"
    DEBUG: bool = False
    
    # Scraper
    SCRAPE_INTERVAL_HOURS: int = 6
    MAX_CONCURRENT_SCRAPERS: int = 3
    
    # ML
    ML_RETRAIN_INTERVAL_HOURS: int = 24
    TFIDF_MAX_FEATURES: int = 500
    EXPLORATION_RATIO: float = 0.2
    
    # Location
    DEFAULT_SEARCH_RADIUS_KM: int = 10
    MAX_SEARCH_RADIUS_KM: int = 50
    GEOCODING_API_URL: str = "https://nominatim.openstreetmap.org"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
