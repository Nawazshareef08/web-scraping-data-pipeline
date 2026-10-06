from urllib.parse import urlsplit, urlunsplit
from datetime import datetime, timezone
def clean_text(value):
    if value is None:
        return ""

    value = str(value)

    value = value.strip()

    value = " ".join(value.split())

    return value

def strip_quotes(value):
    if value is None:
        return ""

    value = str(value).strip()

    if len(value) >= 2:
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]

    return value

def clean_price(value):
    if value is None:
        return ""

    value = str(value)

    value = value.replace("Â£", "")
    value = value.replace("£", "")
    value = value.strip()

    try:
        return float(value)
    except ValueError:
        return ""

def clean_rating(value):
    if value is None:
        return ""

    value = str(value).strip().lower()

    rating_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5
    }

    return rating_map.get(value, "")

def clean_tags(value):
    if value is None:
        return ""

    value = str(value)

    tags = value.split(",")

    cleaned_tags = []

    for tag in tags:
        tag = clean_text(tag)

        if tag:
            cleaned_tags.append(tag)

    return ", ".join(cleaned_tags)

def normalize_url(value):
    if value is None:
        return ""

    value = str(value).strip()

    if not value:
        return ""

    parts = urlsplit(value)

    normalized = urlunsplit((
        parts.scheme.lower(),
        parts.netloc.lower(),
        parts.path,
        parts.query,
        ""
    ))

    return normalized

def clean_record(record):
    cleaned = {
        "source": clean_text(record.get("source")),
        "source_url": normalize_url(record.get("source_url")),
        "name_or_title": clean_text(record.get("name_or_title")),
        "category": clean_text(record.get("category")),
        "price": clean_price(record.get("price")),
        "rating": clean_rating(record.get("rating")),
        "author": clean_text(record.get("author")),
        "tags": clean_tags(record.get("tags")),
        "description": clean_text(record.get("description")),
        "scraped_at": record.get(
        "scraped_at",
        datetime.now(timezone.utc).isoformat()
)
    }

    return cleaned