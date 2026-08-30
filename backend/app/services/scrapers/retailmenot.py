"""RetailMeNot scraper - extracts coupons from retailmenot.com"""
import json
import re
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup
from ..scraper_base import BaseScraper, ScrapedCoupon


class RetailMeNotScraper(BaseScraper):
    """Scraper for RetailMeNot.com"""
    
    def __init__(self):
        super().__init__("retailmenot", "https://www.retailmenot.com")
    
    async def scrape(self) -> List[ScrapedCoupon]:
        """Scrape trending coupons from RetailMeNot"""
        coupons = []
        
        # Popular stores to scrape
        stores = ['target', 'amazon', 'walmart', 'uber-eats', 'doordash', 
                  'nike', 'adidas', 'best-buy', 'macys', 'kohls']
        
        for store in stores:
            try:
                url = f"{self.base_url}/coupons/{store}"
                html = await self.fetch_page(url)
                soup = BeautifulSoup(html, 'lxml')
                
                # Find coupon containers
                coupon_elements = soup.find_all('div', {'data-testid': re.compile('coupon-tile')})
                
                for elem in coupon_elements[:5]:  # Limit per store
                    try:
                        # Extract data
                        title_elem = elem.find('h3') or elem.find('h2')
                        title = title_elem.text.strip() if title_elem else "Deal"
                        
                        code_elem = elem.find('span', {'data-testid': re.compile('code')})
                        code = code_elem.text.strip() if code_elem else None
                        
                        desc_elem = elem.find('p', {'data-testid': re.compile('description')})
                        description = desc_elem.text.strip() if desc_elem else None
                        
                        # Detect discount type
                        disc_type, disc_val, disc_display = self.detect_discount_type(title)
                        category, subcategory = self.categorize(store, title, description or "")
                        
                        coupon = ScrapedCoupon(
                            store_name=store.replace('-', ' ').title(),
                            title=title,
                            description=description,
                            code=code,
                            discount_display=disc_display,
                            discount_type=disc_type,
                            category=category,
                            expiry_date=None,  # Would need to parse from page
                            source_url=url,
                            image_url=None,
                            is_online_only=True,
                            raw_data={"store": store}
                        )
                        coupons.append(coupon)
                        
                    except Exception as e:
                        self.errors.append(f"Error parsing coupon: {e}")
                        continue
                        
            except Exception as e:
                self.errors.append(f"Error scraping {store}: {e}")
                continue
        
        return coupons
