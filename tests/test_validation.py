from processing.validation import validate_source
from processing.validation import (
    validate_source,
    validate_name,
    validate_url
)
from processing.validation import (
    validate_source,
    validate_name,
    validate_url,
    validate_price
)
from processing.validation import (
    validate_source,
    validate_name,
    validate_url,
    validate_price,
    validate_rating
)

from processing.validation import (
    validate_source,
    validate_name,
    validate_url,
    validate_price,
    validate_rating,
    validate_record
)

def test_validate_source():
    assert validate_source("books") is True
    assert validate_source("quotes") is True


def test_validate_invalid_source():
    assert validate_source("amazon") is False

from processing.validation import validate_source, validate_name


def test_validate_name():
    assert validate_name("A Light in the Attic") is True


def test_validate_empty_name():
    assert validate_name("") is False


def test_validate_none_name():
    assert validate_name(None) is False

def test_validate_url():
    assert validate_url(
        "https://books.toscrape.com/catalogue/book.html"
    ) is True


def test_validate_invalid_url():
    assert validate_url("not-a-url") is False


def test_validate_empty_url():
    assert validate_url("") is False

def test_validate_price():
    assert validate_price(51.77) is True
    assert validate_price(0) is True


def test_validate_negative_price():
    assert validate_price(-10) is False


def test_validate_empty_price():
    assert validate_price("") is True


def test_validate_invalid_price():
    assert validate_price("abc") is False
def test_validate_rating():
    assert validate_rating(1) is True
    assert validate_rating(3) is True
    assert validate_rating(5) is True


def test_validate_invalid_rating():
    assert validate_rating(0) is False
    assert validate_rating(6) is False


def test_validate_empty_rating():
    assert validate_rating("") is True


def test_validate_invalid_rating_text():
    assert validate_rating("abc") is False

def test_validate_record():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/book.html",
        "name_or_title": "A Light in the Attic",
        "price": 51.77,
        "rating": 3
    }

    assert validate_record(record) is True


def test_validate_invalid_record():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/book.html",
        "name_or_title": "",
        "price": 51.77,
        "rating": 3
    }

    assert validate_record(record) is False