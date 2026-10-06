from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags
)

from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags,
    normalize_url
)

from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags,
    normalize_url,
    clean_record
)

from processing.cleaning import clean_text


def test_clean_text():
    assert clean_text("   Hello    World   ") == "Hello World"


def test_clean_text_none():
    assert clean_text(None) == ""

from processing.cleaning import clean_text, strip_quotes


def test_strip_quotes():
    assert strip_quotes('"Hello World"') == "Hello World"


def test_strip_single_quotes():
    assert strip_quotes("'Hello World'") == "Hello World"


def test_strip_quotes_without_quotes():
    assert strip_quotes("Hello World") == "Hello World"

from processing.cleaning import clean_text, strip_quotes, clean_price


def test_clean_price():
    assert clean_price("Â£51.77") == 51.77


def test_clean_price_with_pound_symbol():
    assert clean_price("£25.50") == 25.50


def test_clean_price_invalid():
    assert clean_price("invalid") == ""


from processing.cleaning import clean_text, strip_quotes, clean_price, clean_rating


def test_clean_rating():
    assert clean_rating("Three") == 3


def test_clean_rating_five():
    assert clean_rating("Five") == 5


def test_clean_rating_invalid():
    assert clean_rating("Six") == ""


def test_clean_tags():
    assert clean_tags(" change,  deep-thoughts, thinking , world ") == (
        "change, deep-thoughts, thinking, world"
    )


def test_clean_tags_empty():
    assert clean_tags("") == ""


def test_clean_tags_none():
    assert clean_tags(None) == ""

def test_normalize_url():
    assert normalize_url(
        "HTTPS://BOOKS.TOSCRAPE.COM/catalogue/book_1.html"
    ) == "https://books.toscrape.com/catalogue/book_1.html"


def test_normalize_url_removes_fragment():
    assert normalize_url(
        "https://books.toscrape.com/book.html#details"
    ) == "https://books.toscrape.com/book.html"


def test_normalize_url_empty():
    assert normalize_url("") == ""

def test_clean_record():
    record = {
        "source": "books",
        "source_url": "HTTPS://BOOKS.TOSCRAPE.COM/book.html",
        "name_or_title": "   A Light in the Attic   ",
        "category": "",
        "price": "Â£51.77",
        "rating": "Three",
        "author": "",
        "tags": "",
        "description": ""
    }

    cleaned = clean_record(record)

    assert cleaned["source"] == "books"
    assert cleaned["source_url"] == (
        "https://books.toscrape.com/book.html"
    )
    assert cleaned["name_or_title"] == "A Light in the Attic"
    assert cleaned["price"] == 51.77
    assert cleaned["rating"] == 3

def test_clean_record_adds_scraped_at():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/book.html",
        "name_or_title": "A Light in the Attic",
        "category": "",
        "price": "£51.77",
        "rating": "Three",
        "author": "",
        "tags": "",
        "description": ""
    }

    cleaned = clean_record(record)

    assert cleaned["scraped_at"] != ""