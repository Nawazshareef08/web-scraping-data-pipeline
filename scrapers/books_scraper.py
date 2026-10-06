from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import logging 

from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)



class BooksScraper(BaseScraper):

    def scrape_page(self, url):
        html = self.fetch_page(url)

        soup = BeautifulSoup(html, "lxml")

        books = []

        book_items = soup.select("article.product_pod")

        for book in book_items:

            title_element = book.select_one("h3 > a")
            price_element = book.select_one("p.price_color")
            rating_element = book.select_one("p.star-rating")
            link_element = book.select_one("h3 > a[href]")

            title = title_element.get("title", "").strip()
            price = price_element.get_text(strip=True)

            rating_classes = rating_element.get("class", [])
            rating = ""

            for class_name in rating_classes:
                if class_name != "star-rating":
                    rating = class_name
                    break

            book_url = urljoin(url, link_element.get("href"))

            books.append({
                "source": "books",
                "source_url": book_url,
                "name_or_title": title,
                "category": "",
                "price": price,
                "rating": rating,
                "author": "",
                "tags": "",
                "description": ""
            })

        next_link = soup.select_one("li.next > a")

        if next_link:
            next_url = urljoin(url, next_link.get("href"))
        else:
            next_url = None

        return books, next_url

    def scrape_all(self, start_url):
        all_books = []
        current_url = start_url

        while current_url:
            
            logger.info(f"Scraping books page: {current_url}")
            page_books, next_url = self.scrape_page(current_url)

            all_books.extend(page_books)

            current_url = next_url

            if current_url:
                time.sleep(0.5)

        return all_books