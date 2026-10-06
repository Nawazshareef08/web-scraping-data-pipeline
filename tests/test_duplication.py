from processing.deduplication import normalize_for_fingerprint
from processing.deduplication import (
    normalize_for_fingerprint,
    create_book_fingerprint,
    create_quote_fingerprint
)
from processing.deduplication import (
    normalize_for_fingerprint,
    create_book_fingerprint,
    create_quote_fingerprint,
    deduplicate_records
)

def test_normalize_for_fingerprint():
    assert normalize_for_fingerprint(
        "  A Light   in the Attic! "
    ) == "a light in the attic"


def test_normalize_for_fingerprint_case():
    assert normalize_for_fingerprint(
        "HELLO WORLD"
    ) == "hello world"

def test_create_book_fingerprint_same_for_formatting_changes():
    record1 = {
        "source": "books",
        "name_or_title": "A Light in the Attic"
    }

    record2 = {
        "source": "BOOKS",
        "name_or_title": "  a light in the attic! "
    }

    assert create_book_fingerprint(record1) == create_book_fingerprint(record2)


def test_create_quote_fingerprint_same_for_formatting_changes():
    record1 = {
        "source": "quotes",
        "author": "Albert Einstein",
        "name_or_title": "The world as we have created it"
    }

    record2 = {
        "source": "QUOTES",
        "author": "  albert einstein ",
        "name_or_title": "The world as we have created it!"
    }

    assert create_quote_fingerprint(record1) == create_quote_fingerprint(record2)

def test_deduplicate_books():
    records = [
        {
            "source": "books",
            "name_or_title": "A Light in the Attic"
        },
        {
            "source": "books",
            "name_or_title": "  a light in the attic! "
        },
        {
            "source": "books",
            "name_or_title": "Another Book"
        }
    ]

    unique_records, duplicate_count = deduplicate_records(records)

    assert len(unique_records) == 2
    assert duplicate_count == 1

def test_deduplicate_quotes():
    records = [
        {
            "source": "quotes",
            "author": "Albert Einstein",
            "name_or_title": "The world as we have created it"
        },
        {
            "source": "quotes",
            "author": "  albert einstein ",
            "name_or_title": "The world as we have created it!"
        }
    ]

    unique_records, duplicate_count = deduplicate_records(records)

    assert len(unique_records) == 1
    assert duplicate_count == 1