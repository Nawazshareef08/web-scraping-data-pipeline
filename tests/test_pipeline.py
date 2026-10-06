from processing.pipeline import process_records


def test_process_records():
    records = [
        {
            "source": "books",
            "source_url": "https://books.toscrape.com/book.html",
            "name_or_title": "A Light in the Attic",
            "category": "",
            "price": "£51.77",
            "rating": "Three",
            "author": "",
            "tags": "",
            "description": ""
        },
        {
            "source": "books",
            "source_url": "https://books.toscrape.com/book.html",
            "name_or_title": "  a light in the attic! ",
            "category": "",
            "price": "£51.77",
            "rating": "Three",
            "author": "",
            "tags": "",
            "description": ""
        },
        {
            "source": "books",
            "source_url": "https://books.toscrape.com/another.html",
            "name_or_title": "",
            "category": "",
            "price": "£20.00",
            "rating": "Four",
            "author": "",
            "tags": "",
            "description": ""
        }
    ]

    final_records, rejected_count, duplicate_count = process_records(
        records
    )

    assert len(final_records) == 1
    assert rejected_count == 1
    assert duplicate_count == 1