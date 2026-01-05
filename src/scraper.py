"""IndiaMART Web Scraper Module

This module implements a robust web scraper for extracting product data from IndiaMART.
It handles rate limiting, retries, and data extraction with error handling.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin, quote
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndiaMARTScraper:
    """Scraper for IndiaMART B2B marketplace"""
    
    BASE_URL = "https://www.indiamart.com"
    SEARCH_URL = "https://www.indiamart.com/search.mp"
    
    def __init__(self, delay_range=(2, 5)):
        """Initialize scraper with rate limiting
        
        Args:
            delay_range: Tuple of (min, max) seconds to wait between requests
        """
        self.delay_range = delay_range
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def _rate_limit(self):
        """Apply random delay between requests"""
        time.sleep(random.uniform(*self.delay_range))
    
    def _make_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """Make HTTP request with retry logic
        
        Args:
            url: Target URL
            max_retries: Maximum number of retry attempts
            
        Returns:
            Response object or None if failed
        """
        for attempt in range(max_retries):
            try:
                self._rate_limit()
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(5, 10))
                else:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts")
        return None
    
    def search_products(self, query: str, max_pages: int = 5) -> List[Dict]:
        """Search for products on IndiaMART
        
        Args:
            query: Search query string
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of product dictionaries
        """
        products = []
        logger.info(f"Starting search for: {query}")
        
        for page in range(1, max_pages + 1):
            url = f"{self.SEARCH_URL}?ss={quote(query)}&page={page}"
            response = self._make_request(url)
            
            if not response:
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            product_cards = soup.find_all('div', class_=re.compile(r'.*product.*card.*', re.I))
            
            if not product_cards:
                # Try alternative selectors
                product_cards = soup.find_all('div', class_=re.compile(r'.*listing.*item.*', re.I))
            
            logger.info(f"Found {len(product_cards)} products on page {page}")
            
            for card in product_cards:
                product = self._extract_product_data(card, query)
                if product:
                    products.append(product)
            
            if not product_cards:
                logger.info(f"No more products found. Stopping at page {page}")
                break
        
        logger.info(f"Total products collected: {len(products)}")
        return products
    
    def _extract_product_data(self, card, category: str) -> Optional[Dict]:
        """Extract product information from HTML card
        
        Args:
            card: BeautifulSoup element containing product data
            category: Product category/search term
            
        Returns:
            Dictionary with product information
        """
        try:
            product = {
                'category': category,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Extract product name
            name_elem = card.find(['h2', 'h3', 'div'], class_=re.compile(r'.*title.*|.*name.*', re.I))
            if name_elem:
                product['product_name'] = name_elem.get_text(strip=True)
            
            # Extract price
            price_elem = card.find(['span', 'div'], class_=re.compile(r'.*price.*', re.I))
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                product['price'] = self._clean_price(price_text)
                product['price_raw'] = price_text
            
            # Extract company/supplier name
            company_elem = card.find(['div', 'span'], class_=re.compile(r'.*company.*|.*seller.*', re.I))
            if company_elem:
                product['company_name'] = company_elem.get_text(strip=True)
            
            # Extract location
            location_elem = card.find(['span', 'div'], class_=re.compile(r'.*location.*|.*city.*', re.I))
            if location_elem:
                product['location'] = location_elem.get_text(strip=True)
            
            # Extract product link
            link_elem = card.find('a', href=True)
            if link_elem:
                product['product_url'] = urljoin(self.BASE_URL, link_elem['href'])
            
            # Extract image URL
            img_elem = card.find('img')
            if img_elem and img_elem.get('src'):
                product['image_url'] = img_elem['src']
            
            # Only return if we have at least a product name
            if product.get('product_name'):
                return product
            
        except Exception as e:
            logger.debug(f"Error extracting product data: {e}")
        
        return None
    
    def _clean_price(self, price_text: str) -> Optional[float]:
        """Extract numeric price from text
        
        Args:
            price_text: Raw price string
            
        Returns:
            Float price value or None
        """
        try:
            # Remove currency symbols and extract numbers
            numbers = re.findall(r'[\d,]+\.?\d*', price_text)
            if numbers:
                # Take the first number found and remove commas
                return float(numbers[0].replace(',', ''))
        except:
            pass
        return None
    
    def scrape_multiple_categories(self, categories: List[str], 
                                   max_pages_per_category: int = 3) -> Dict[str, List[Dict]]:
        """Scrape multiple product categories
        
        Args:
            categories: List of category/search terms
            max_pages_per_category: Pages to scrape per category
            
        Returns:
            Dictionary mapping categories to product lists
        """
        results = {}
        
        for category in categories:
            logger.info(f"\n{'='*50}\nScraping category: {category}\n{'='*50}")
            products = self.search_products(category, max_pages=max_pages_per_category)
            results[category] = products
            logger.info(f"Collected {len(products)} products for '{category}'")
        
        return results


if __name__ == "__main__":
    # Example usage
    scraper = IndiaMARTScraper()
    
    # Sample categories to scrape
    categories = [
        "industrial machinery",
        "electronics components",
        "textile machinery"
    ]
    
    results = scraper.scrape_multiple_categories(categories, max_pages_per_category=2)
    
    # Save results
    with open('scraped_data.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info("\nScraping completed. Data saved to scraped_data.json")
