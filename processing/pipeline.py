import logging


from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import deduplicate_records

logger = logging.getLogger(__name__)

def process_records(records):
    cleaned_records = []
    rejected_count = 0

    for record in records:
        cleaned = clean_record(record)

        if validate_record(cleaned):
            cleaned_records.append(cleaned)
        else:
            rejected_count += 1
            logger.warning(
            f"Rejected record: {record}"
    )

    unique_records, duplicate_count = deduplicate_records(
        cleaned_records
    )

    return unique_records, rejected_count, duplicate_count