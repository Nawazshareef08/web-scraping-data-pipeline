def validate_source(source):
    return source in {"books", "quotes"}

def validate_name(name):
    return bool(name and str(name).strip())

from urllib.parse import urlparse


def validate_url(url):
    if not url:
        return False

    try:
        parsed = urlparse(str(url))

        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

    except ValueError:
        return False

def validate_price(price):
    if price == "":
        return True

    try:
        return float(price) >= 0
    except (TypeError, ValueError):
        return False

def validate_rating(rating):
    if rating == "":
        return True

    try:
        rating = int(rating)
        return 1 <= rating <= 5
    except (TypeError, ValueError):
        return False

def validate_record(record):
    if not validate_source(record.get("source")):
        return False

    if not validate_name(record.get("name_or_title")):
        return False

    if not validate_url(record.get("source_url")):
        return False

    if not validate_price(record.get("price")):
        return False

    if not validate_rating(record.get("rating")):
        return False

    return True