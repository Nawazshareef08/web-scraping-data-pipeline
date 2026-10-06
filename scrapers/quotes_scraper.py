from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import logging

from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class QuotesScraper(BaseScraper):

    def scrape_page(self, url):
        html = self.fetch_page(url)

        soup = BeautifulSoup(html, "lxml")

        quotes = []

        quote_items = soup.select("div.quote")

        for quote in quote_items:

            text_element = quote.select_one("span.text")
            author_element = quote.select_one("small.author")

            tag_elements = quote.select("a.tag")

            text = text_element.get_text(strip=True)
            author = author_element.get_text(strip=True)

            tags = []

            for tag in tag_elements:
                tags.append(tag.get_text(strip=True))

            author_link_element = quote.select_one(
                'a[href^="/author/"]'
            )

            if author_link_element:
                author_url = urljoin(
                    url,
                    author_link_element.get("href")
                )
            else:
                author_url = ""

            quotes.append({
                "source": "quotes",
                "source_url": author_url,
                "name_or_title": text,
                "category": "",
                "price": "",
                "rating": "",
                "author": author,
                "tags": ", ".join(tags),
                "description": ""
            })

        next_link = soup.select_one("li.next > a")

        if next_link:
            next_url = urljoin(
                url,
                next_link.get("href")
            )
        else:
            next_url = None

        return quotes, next_url

    def scrape_all(self, start_url):
        all_quotes = []
        current_url = start_url

        while current_url:

            logger.info(f"Scraping quotes page: {current_url}")

            page_quotes, next_url = self.scrape_page(current_url)

            all_quotes.extend(page_quotes)

            current_url = next_url

            if current_url:
                time.sleep(0.5)

        return all_quotes