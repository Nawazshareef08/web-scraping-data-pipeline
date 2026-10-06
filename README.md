# Web Scraping and ETL Assignment

## About the Project

This project is a Python-based web scraping and data processing project. The main goal is to collect data from two websites, clean and validate the collected data, remove duplicate records, and finally save the processed data into a CSV file.

The two websites used in this project are:

* Books: https://books.toscrape.com/
* Quotes: https://quotes.toscrape.com/

The complete process is handled by `main.py`, so the project can be run using a single command.

```bash
python main.py
```

The overall process is:

**Scrape → Clean → Validate → Remove Duplicates → Save**

---

## Project Structure

```text
scraping_assignment/
│
├── main.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   ├── deduplication.py
│   └── pipeline.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_validation.py
│   ├── test_deduplication.py
│   └── test_pipeline.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
└── logs/
    └── scraper.log
```

---

## Requirements

The project uses Python 3.10–3.12.

The main Python libraries used are:

* requests
* beautifulsoup4
* lxml
* pytest

The dependencies can be installed using:

```bash
python -m pip install -r requirements.txt
```

---

## How to Run

First, activate the virtual environment if it is not already active.

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Then run:

```bash
python main.py
```

The scraper follows the `next` links provided by the websites instead of using fixed page numbers.

A short delay is also added between requests to avoid sending requests too quickly.

---

## What the Project Does

### 1. Scraping

The project collects information from both websites.

For Books, the scraper collects information such as:

* Book title
* Price
* Rating
* Book URL

For Quotes, it collects:

* Quote
* Author
* Tags
* Author URL

The scraper continues until there is no `next` page available.

### 2. Cleaning

The collected values are cleaned before being processed further.

Some of the cleaning operations include:

* Removing extra spaces
* Cleaning text values
* Converting book prices into numeric values
* Converting ratings into numbers from 1 to 5
* Cleaning tags
* Normalizing URLs
* Adding the time at which the record was processed

### 3. Validation

Each cleaned record is checked before being added to the final dataset.

The validation checks include:

* Whether the source is known
* Whether the title or name is present
* Whether the URL is valid
* Whether the price is valid and non-negative
* Whether the rating is between 1 and 5

Invalid records are rejected and recorded in the log.

### 4. Deduplication

Duplicate records are removed before creating the final dataset.

For books, the duplicate check is based on the source and book title.

For quotes, it uses the source, author, and the first 50 characters of the quote.

The values are normalized before creating the fingerprint so that differences such as capitalization, punctuation, or extra spaces do not result in separate records.

---

## Output Files

After running the project, the following files are generated.

### `output/final_dataset.csv`

This contains the final processed records.

The columns are:

```text
source
source_url
name_or_title
category
price
rating
author
tags
description
scraped_at
```

### `output/summary_report.json`

This contains information about the scraping run, including:

* Number of raw records
* Number of cleaned records
* Number of rejected records
* Number of duplicate records
* Number of final records
* Start time
* End time
* Total duration

### `logs/scraper.log`

This file keeps track of the scraping process.

It includes information about:

* Pages being scraped
* Rejected records
* Request errors
* Final record counts

---

## Results

The complete run of the project produced the following results:

| Description       | Count |
| ----------------- | ----: |
| Books scraped     | 1,000 |
| Quotes scraped    |   100 |
| Raw records       | 1,100 |
| Rejected records  |     0 |
| Duplicate records |     1 |
| Final records     | 1,099 |

The final count matches the expected calculation:

```text
1100 - 0 - 1 = 1099
```

---

## Limitation

The book listing pages do not contain the category and full description information that is required for those fields.

For this version of the project, I decided not to make additional detail-page requests for every book. Therefore, the `category` and `description` fields are left empty.

This limitation is documented instead of assuming or generating values that were not collected.

---

## Testing

Tests have been added for the main processing components of the project.

They cover:

* Data cleaning
* Data validation
* Deduplication
* The complete processing pipeline

The tests can be run using:

```bash
python -m pytest
```

The current test suite passes all **44 tests**.

---

## Error Handling

A shared HTTP session is used for the scrapers.

The request handling includes:

* A User-Agent
* Request timeout
* Retries for temporary HTTP errors such as 429, 500, 502, 503 and 504

The Books and Quotes scrapers are also handled separately. If one source fails, the other source can still continue processing.

---

## Purpose

This project was developed as part of a Python scraping and ETL assignment. It helped me practice web scraping, data cleaning, validation, deduplication, logging, testing, and working with structured output files.
