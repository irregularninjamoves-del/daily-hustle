"""Slickdeals scraper - extracts deals from slickdeals.net"""
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup
from ..scraper_base import BaseScraper, ScrapedCoupon


class SlickdealsScraper(BaseScraper):
    """Scraper for Slickdeals.net"""
    
    def __init__(self):
        super().__init__("slickdeals", "https://slickdeals.net")
    
    async def scrape(self) -> List[ScrapedCoupon]:
        """Scrape frontpage deals from Slickdeals"""
        coupons = []
        
        try:
            # Frontpage deals
            url = f"{self.base_url}/frontpage"
            html = await self.fetch_page(url)
            soup = BeautifulSoup(html, 'lxml')
            
            # Find deal cards
            deal_elements = soup.find_all('div', class_=re.compile('dealCard'))
            
            for elem in deal_elements[:15]:
                try:
                    # Extract title
                    title_elem = elem.find('a', class_=re.compile('dealTitle'))
                    title = title_elem.text.strip() if title_elem else "Deal"
                    
                    # Extract store
                    store_elem = elem.find('span', class_=re.compile('store'))
                    store = store_elem.text.strip() if store_elem else "Unknown"
                    
                    # Extract price/discount
                    price_elem = elem.find('span', class_=re.compile('price'))
                    price_info = price_elem.text.strip() if price_elem else ""
                    
                    # Extract link
                    link_elem = elem.find('a', href=True)
                    deal_url = self.base_url + link_elem['href'] if link_elem else self.base_url
                    
                    # Detect discount type
                    disc_type, disc_val, disc_display = self.detect_discount_type(title + " " + price_info)
                    category, subcategory = self.categorize(store, title, "")
                    
                    coupon = ScrapedCoupon(
                        store_name=store,
                        title=title,
                        description=None,
                        code=None,  # Slickdeals often doesn't show codes upfront
                        discount_display=disc_display,
                        discount_type=disc_type,
                        category=category,
                        expiry_date=None,
                        source_url=deal_url,
                        image_url=None,
                        is_online_only=True,
                        raw_data={"source": "frontpage"}
                    )
                    coupons.append(coupon)
                    
                except Exception as e:
                    self.errors.append(f"Error parsing deal: {e}")
                    continue
                    
        except Exception as e:
            self.errors.append(f"Error scraping frontpage: {e}")
        
        return coupons
