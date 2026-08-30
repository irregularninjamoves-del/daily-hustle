"""Scraper manager for running multiple scrapers."""
from typing import List, Dict, Any
import asyncio
from .scraper_base import BaseScraper
from .mock_scraper import MockScraper
from .scrapers import RetailMeNotScraper, SlickdealsScraper, GrouponScraper


class ScraperManager:
    """Manages multiple scrapers."""
    
    def __init__(self):
        self.scrapers: List[BaseScraper] = []
        # Register all scrapers
        self.register_scraper(MockScraper())
        self.register_scraper(RetailMeNotScraper())
        self.register_scraper(SlickdealsScraper())
        self.register_scraper(GrouponScraper())
    
    def register_scraper(self, scraper: BaseScraper):
        self.scrapers.append(scraper)
    
    async def scrape_all(self) -> List[Dict[str, Any]]:
        tasks = [scraper.run() for scraper in self.scrapers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({"success": False, "error": str(result)})
            else:
                processed_results.append(result)
        return processed_results
    
    async def scrape_single(self, name: str) -> Dict[str, Any]:
        """Run a single scraper by name."""
        for scraper in self.scrapers:
            if scraper.name == name:
                return await scraper.run()
        return {"success": False, "error": f"Scraper '{name}' not found"}
    
    def get_scraper_names(self) -> List[str]:
        return [s.name for s in self.scrapers]


# Global instance
scraper_manager = ScraperManager()
