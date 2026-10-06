import logging
import time
import json
import csv
from datetime import datetime, timezone
from pathlib import Path
from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper
from processing.pipeline import process_records


BOOKS_URL = "https://books.toscrape.com/"
QUOTES_URL = "https://quotes.toscrape.com/"

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "scraper.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def save_csv(records):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "final_dataset.csv"

    fieldnames = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "scraped_at"
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(records)

    return output_file

def save_summary(
    raw_count,
    cleaned_count,
    rejected_count,
    duplicate_count,
    final_count,
    start_time,
    end_time,
    duration
):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    report = {
        "raw_records": raw_count,
        "cleaned_records": cleaned_count,
        "rejected_records": rejected_count,
        "duplicate_records": duplicate_count,
        "final_records": final_count,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": duration
    }

    output_file = output_dir / "summary_report.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    return output_file

def main():
    start_time = datetime.now(timezone.utc)
    logger.info("Starting scraping...")

    books_scraper = BooksScraper()
    quotes_scraper = QuotesScraper()

    books = []

    try:
        books = books_scraper.scrape_all(BOOKS_URL)
        logger.info(f"Books scraped: {len(books)}")

    except Exception as error:
        logger.error(f"Books scraping failed: {error}")


    quotes = []

    try:
        quotes = quotes_scraper.scrape_all(QUOTES_URL)
        logger.info(f"Quotes scraped: {len(quotes)}")

    except Exception as error:
        logger.error(f"Quotes scraping failed: {error}")

    all_records = books + quotes

    logger.info(f"Total raw records: {len(all_records)}")

    final_records, rejected_count, duplicate_count = process_records(
        all_records
    )

    logger.info(f"Rejected records: {rejected_count}")
    logger.info(f"Duplicate records: {duplicate_count}")
    logger.info(f"Final records: {len(final_records)}")

    cleaned_count = len(all_records) - rejected_count

    output_file = save_csv(final_records)

    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()

    summary_file = save_summary(
    len(all_records),
    cleaned_count,
    rejected_count,
    duplicate_count,
    len(final_records),
    start_time.isoformat(),
    end_time.isoformat(),
    duration
)

    logger.info(f"CSV saved to: {output_file}")
    logger.info(f"Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()