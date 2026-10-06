import re
import hashlib


def normalize_for_fingerprint(value):
    if value is None:
        return ""

    value = str(value).lower()

    value = re.sub(r"[^\w\s]", "", value)

    value = " ".join(value.split())

    return value

def create_book_fingerprint(record):
    source = normalize_for_fingerprint(record.get("source"))
    title = normalize_for_fingerprint(record.get("name_or_title"))

    fingerprint_text = source + "|" + title

    return hashlib.sha256(
        fingerprint_text.encode("utf-8")
    ).hexdigest()


def create_quote_fingerprint(record):
    source = normalize_for_fingerprint(record.get("source"))
    author = normalize_for_fingerprint(record.get("author"))
    quote = normalize_for_fingerprint(record.get("name_or_title"))

    quote = quote[:50]

    fingerprint_text = source + "|" + author + "|" + quote

    return hashlib.sha256(
        fingerprint_text.encode("utf-8")
    ).hexdigest()

def deduplicate_records(records):
    unique_records = []
    seen_fingerprints = set()
    duplicate_count = 0

    for record in records:

        if record.get("source") == "books":
            fingerprint = create_book_fingerprint(record)

        elif record.get("source") == "quotes":
            fingerprint = create_quote_fingerprint(record)

        else:
            fingerprint = ""

        if fingerprint in seen_fingerprints:
            duplicate_count += 1
            continue

        seen_fingerprints.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicate_count