"""Mock scraper for development."""
from typing import List
from .scraper_base import BaseScraper, ScrapedCoupon


class MockScraper(BaseScraper):
    """Returns sample coupons for development."""
    
    SAMPLE_COUPONS = [
        {"store": "Target", "title": "20% off home items", "code": "HOME20", "discount": "20% off"},
        {"store": "Walgreens", "title": "$5 off $25+", "code": "GET5", "discount": "$5 off"},
        {"store": "Pizza Hut", "title": "BOGO Free", "code": None, "discount": "BOGO"},
        {"store": "Nike", "title": "Free shipping", "code": None, "discount": "Free Shipping"},
        {"store": "Amazon", "title": "40% off electronics", "code": None, "discount": "40% off"},
        {"store": "Starbucks", "title": "$2 off grande", "code": "COFFEE2", "discount": "$2 off"},
        {"store": "Best Buy", "title": "$50 off laptops", "code": "LAPTOP50", "discount": "$50 off"},
        {"store": "DoorDash", "title": "50% off first order", "code": "YUMMY50", "discount": "50% off"},
        {"store": "Macy's", "title": "25% off sale", "code": "EXTRA25", "discount": "25% off"},
        {"store": "Uber Eats", "title": "$10 off $30+", "code": "EATS10", "discount": "$10 off"},
        {"store": "Kroger", "title": "$5 off $40+", "code": "SAVE5", "discount": "$5 off"},
        {"store": "CVS", "title": "30% off beauty", "code": "BEAUTY30", "discount": "30% off"},
    ]
    
    def __init__(self):
        super().__init__("mock", "https://example.com")
    
    async def scrape(self) -> List[ScrapedCoupon]:
        coupons = []
        for data in self.SAMPLE_COUPONS:
            disc_type, disc_val, disc_display = self.detect_discount_type(data["discount"])
            cat, subcat = self.categorize(data["store"], data["title"], "")
            coupons.append(ScrapedCoupon(
                store_name=data["store"],
                title=data["title"],
                description=None,
                code=data["code"],
                discount_display=disc_display,
                discount_type=disc_type,
                category=cat,
                expiry_date=None,
                source_url="https://example.com",
                image_url=None,
                is_online_only=True,
                raw_data=data
            ))
        return coupons
