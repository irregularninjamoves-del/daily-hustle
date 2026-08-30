import asyncio
from datetime import datetime
from sqlalchemy import select
from app.database import AsyncSessionLocal, init_db
from app.models import SideHustle, DeliveryService, Coupon
from app.services.mock_scraper import MockScraper

SIDE_HUSTLES = [
    {"title": "DoorDash Delivery", "company": "DoorDash", "description": "Deliver food", "hustle_type": "delivery", "pay_rate": "$15-25/hr", "is_bike_friendly": True, "requirements": ["18+"], "time_commitment": "Flexible", "apply_url": "https://doordash.com", "pros": ["Flexible"], "cons": ["Wear"], "rating": 4.2},
    {"title": "Uber Eats", "company": "Uber", "description": "Deliver food", "hustle_type": "delivery", "pay_rate": "$12-22/hr", "is_bike_friendly": True, "requirements": ["18+"], "time_commitment": "Flexible", "apply_url": "https://uber.com", "pros": ["Instant Pay"], "cons": ["Expenses"], "rating": 4.0},
    {"title": "Upwork", "company": "Upwork", "description": "Freelance", "hustle_type": "freelance", "pay_rate": "$10-100+/hr", "is_remote": True, "requirements": ["Skills"], "time_commitment": "Flexible", "apply_url": "https://upwork.com", "pros": ["Remote"], "cons": ["Fees"], "rating": 4.3},
]

DELIVERY_SERVICES = [
    {"company_name": "DoorDash", "accepts_bikes": True, "min_age": 18, "background_check_required": True, "pay_estimate_hourly": "$15-25", "nationwide": True, "signup_url": "https://doordash.com", "pros": ["Bike mode"], "cons": ["Wear"], "overall_rating": 4.2},
    {"company_name": "Uber Eats", "accepts_bikes": True, "accepts_walking": True, "min_age": 18, "background_check_required": True, "pay_estimate_hourly": "$12-22", "nationwide": True, "signup_url": "https://uber.com", "pros": ["Walking"], "cons": ["Expenses"], "overall_rating": 4.0},
]

async def seed_hustles(db):
    for data in SIDE_HUSTLES:
        result = await db.execute(select(SideHustle).where(SideHustle.title == data["title"]))
        if not result.scalar_one_or_none():
            db.add(SideHustle(**data))
    await db.commit()

async def seed_delivery_services(db):
    for data in DELIVERY_SERVICES:
        result = await db.execute(select(DeliveryService).where(DeliveryService.company_name == data["company_name"]))
        if not result.scalar_one_or_none():
            db.add(DeliveryService(**data))
    await db.commit()

async def seed_coupons(db):
    scraper = MockScraper()
    coupons = await scraper.scrape()
    for scraped in coupons:
        result = await db.execute(select(Coupon).where(Coupon.store_name == scraped.store_name, Coupon.title == scraped.title))
        if not result.scalar_one_or_none():
            db.add(Coupon(store_name=scraped.store_name, store_name_normalized=scraped.store_name.lower().replace(" ", "-"), title=scraped.title, description=scraped.description, code=scraped.code, discount_display=scraped.discount_display, discount_type=scraped.discount_type, category=scraped.category, subcategory=scraped.category, source="mock", source_url=scraped.source_url, is_online_only=scraped.is_online_only, scraped_at=datetime.utcnow()))
    await db.commit()

async def main():
    print("Seeding...")
    await init_db()
    async with AsyncSessionLocal() as db:
        await seed_hustles(db)
        await seed_delivery_services(db)
        await seed_coupons(db)
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
