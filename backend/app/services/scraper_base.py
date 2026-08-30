"""Base scraper classes."""
import asyncio
import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import re
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
]


@dataclass
class ScrapedCoupon:
    """Standardized coupon data."""
    store_name: str
    title: str
    description: Optional[str]
    code: Optional[str]
    discount_display: Optional[str]
    discount_type: str
    category: str
    expiry_date: Optional[datetime]
    source_url: str
    image_url: Optional[str]
    is_online_only: bool
    raw_data: Dict[str, Any]


class BaseScraper(ABC):
    """Base class for all scrapers."""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.client: Optional[httpx.AsyncClient] = None
        self.results: List[ScrapedCoupon] = []
        self.errors: List[str] = []
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True,
            headers={"User-Agent": random.choice(USER_AGENTS)})
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def fetch_page(self, url: str, params: Optional[Dict] = None) -> str:
        if not self.client:
            raise RuntimeError("Scraper not initialized")
        await asyncio.sleep(random.uniform(1, 3))
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.text
    
    def detect_discount_type(self, text: str) -> tuple:
        text_lower = text.lower()
        pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
        if pct_match:
            value = float(pct_match.group(1))
            if value <= 100:
                return ("percentage", value, f"{int(value)}% off")
        dollar_match = re.search(r'\$?\s*(\d+(?:\.\d+)?)\s*(?:off|\$)', text_lower)
        if dollar_match:
            value = float(dollar_match.group(1))
            return ("dollar", value, f"${int(value)} off")
        if any(x in text_lower for x in ['bogo', 'buy one get one']):
            return ("bogo", None, "BOGO")
        if 'free shipping' in text_lower:
            return ("shipping", None, "Free Shipping")
        if 'free' in text_lower:
            return ("free", None, "Free")
        return ("other", None, text[:50])
    
    def categorize(self, store: str, title: str, description: str) -> tuple:
        text = f"{store} {title} {description}".lower()
        if any(x in text for x in ['food', 'restaurant', 'pizza', 'coffee', 'grocery', 'doordash', 'starbucks']):
            return ("Food & Grocery", "Restaurants")
        if any(x in text for x in ['clothing', 'fashion', 'shoes', 'nike', 'macys']):
            return ("Clothing & Fashion", "Apparel")
        if any(x in text for x in ['electronics', 'computer', 'laptop', 'phone', 'best buy']):
            return ("Electronics", "Tech")
        if any(x in text for x in ['home', 'furniture', 'ikea', 'home depot']):
            return ("Home & Garden", "Home")
        if any(x in text for x in ['beauty', 'makeup', 'sephora', 'walgreens']):
            return ("Beauty & Health", "Beauty")
        if any(x in text for x in ['travel', 'hotel', 'flight', 'expedia']):
            return ("Travel", "Travel")
        if any(x in text for x in ['entertainment', 'netflix', 'spotify']):
            return ("Entertainment", "Streaming")
        return ("Other", "General")
    
    @abstractmethod
    async def scrape(self) -> List[ScrapedCoupon]:
        pass
    
    async def run(self) -> Dict[str, Any]:
        try:
            async with self:
                coupons = await self.scrape()
                return {"success": True, "source": self.name, "coupons_found": len(coupons), "coupons": coupons, "errors": self.errors}
        except Exception as e:
            return {"success": False, "source": self.name, "coupons_found": 0, "coupons": [], "errors": [str(e)]}
