"""Groupon scraper - extracts local deals from groupon.com"""
import re
from typing import List
from bs4 import BeautifulSoup
from ..scraper_base import BaseScraper, ScrapedCoupon


class GrouponScraper(BaseScraper):
    """Scraper for Groupon local deals"""
    
    def __init__(self):
        super().__init__("groupon", "https://www.groupon.com")
    
    async def scrape(self) -> List[ScrapedCoupon]:
        """Scrape local deals from Groupon"""
        coupons = []
        
        # Categories to scrape
        categories = ['food-and-drink', 'things-to-do', 'beauty-and-spas']
        
        for category in categories:
            try:
                url = f"{self.base_url}/local/{category}"
                html = await self.fetch_page(url)
                soup = BeautifulSoup(html, 'lxml')
                
                # Find deal cards
                deal_elements = soup.find_all('div', class_=re.compile('deal-card'))
                
                for elem in deal_elements[:8]:
                    try:
                        # Extract title
                        title_elem = elem.find('h3') or elem.find('h2')
                        title = title_elem.text.strip() if title_elem else "Local Deal"
                        
                        # Extract business name
                        business_elem = elem.find('div', class_=re.compile('merchant'))
                        business = business_elem.text.strip() if business_elem else "Local Business"
                        
                        # Extract discount info
                        discount_elem = elem.find('span', class_=re.compile('discount'))
                        discount_text = discount_elem.text.strip() if discount_elem else ""
                        
                        # Extract price
                        price_elem = elem.find('span', class_=re.compile('price'))
                        price = price_elem.text.strip() if price_elem else ""
                        
                        # Map Groupon category to our categories
                        cat_map = {
                            'food-and-drink': 'Food & Grocery',
                            'things-to-do': 'Entertainment',
                            'beauty-and-spas': 'Beauty & Health'
                        }
                        category_name = cat_map.get(category, 'Other')
                        
                        disc_type, disc_val, disc_display = self.detect_discount_type(discount_text + " " + price)
                        
                        coupon = ScrapedCoupon(
                            store_name=business,
                            title=title,
                            description=f"{discount_text} - {price}" if discount_text else price,
                            code=None,
                            discount_display=disc_display or price,
                            discount_type=disc_type,
                            category=category_name,
                            expiry_date=None,
                            source_url=url,
                            image_url=None,
                            is_online_only=False,  # Groupon is local
                            raw_data={"category": category}
                        )
                        coupons.append(coupon)
                        
                    except Exception as e:
                        self.errors.append(f"Error parsing deal: {e}")
                        continue
                        
            except Exception as e:
                self.errors.append(f"Error scraping {category}: {e}")
                continue
        
        return coupons
