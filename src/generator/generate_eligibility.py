import csv
import random
import uuid
from datetime import date, timedelta
from pathlib import Path


OUTPUT_DIR = Path("data/generated")

RECORD_COUNT = 10000
ERROR_RATE = 0.05

CLIENT_CODE = "ACME_HEALTH"


FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "David",
    "Mary", "Jennifer", "Linda", "Patricia", "Susan"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Wilson", "Anderson"
]

STATES = [
    "FL", "TX", "CA", "NY", "GA", "IL"
]

PLANS = [
    "PLAN001",
    "PLAN002",
    "PLAN003",
    "PLAN004",
    "PLAN005"
]

COVERAGE_TYPES = {
    "PLAN001": "MEDICAL",
    "PLAN002": "MEDICAL",
    "PLAN003": "DENTAL",
    "PLAN004": "VISION",
    "PLAN005": "HEARING"
}


def random_date(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(
        days=random.randint(0, delta.days)
    )


def generate_valid_member(index):

    dob = random_date(
        date(1940, 1, 1),
        date(2005, 12, 31)
    )

    effective_date = random_date(
        date(2025, 1, 1),
        date(2026, 12, 31)
    )

    plan_id = random.choice(PLANS)

    return {
        "member_id": f"M{index:08d}",
        "subscriber_id": f"S{random.randint(1, 5000):08d}",
        "first_name": random.choice(FIRST_NAMES),
        "last_name": random.choice(LAST_NAMES),
        "date_of_birth": dob.isoformat(),
        "gender": random.choice(["M", "F"]),
        "state": random.choice(STATES),
        "zip_code": str(random.randint(10000, 99999)),
        "plan_id": plan_id,
        "coverage_type": COVERAGE_TYPES[plan_id],
        "effective_date": effective_date.isoformat(),
        "termination_date": "",
        "source_record_id": str(uuid.uuid4()),
        "source_client": CLIENT_CODE
    }


def inject_error(record, previous_records):

    error_type = random.choice([
        "MISSING_MEMBER_ID",
        "MISSING_DOB",
        "INVALID_PLAN",
        "INVALID_GENDER",
        "INVALID_ZIP",
        "INVALID_DATE_RANGE",
        "DUPLICATE_MEMBER"
    ])

    if error_type == "MISSING_MEMBER_ID":
        record["member_id"] = ""

    elif error_type == "MISSING_DOB":
        record["date_of_birth"] = ""

    elif error_type == "INVALID_PLAN":
        record["plan_id"] = "PLAN999"

    elif error_type == "INVALID_GENDER":
        record["gender"] = "X"

    elif error_type == "INVALID_ZIP":
        record["zip_code"] = "ABC12"

    elif error_type == "INVALID_DATE_RANGE":

        record["effective_date"] = "2026-12-31"
        record["termination_date"] = "2026-01-01"

    elif error_type == "DUPLICATE_MEMBER" and previous_records:

        existing = random.choice(previous_records)

        record["member_id"] = existing["member_id"]

    return record


def generate_file():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_name = (
        f"{CLIENT_CODE}_ELIGIBILITY_"
        f"{date.today().strftime('%Y%m%d')}.csv"
    )

    output_file = OUTPUT_DIR / file_name

    records = []
    injected_error_count = 0

    for index in range(1, RECORD_COUNT + 1):

        record = generate_valid_member(index)

        if random.random() < ERROR_RATE:

            record = inject_error(
                record,
                records
            )

            injected_error_count += 1

        records.append(record)

    fieldnames = list(records[0].keys())

    with output_file.open(
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

    print()
    print("========================================")
    print(" Synthetic Eligibility File Generated")
    print("========================================")
    print(f"Client            : {CLIENT_CODE}")
    print(f"File              : {output_file}")
    print(f"Total records     : {len(records):,}")
    print(f"Injected errors   : {injected_error_count:,}")
    print(
        f"Error percentage  : "
        f"{(injected_error_count / len(records)) * 100:.2f}%"
    )
    print("========================================")
    print()


if __name__ == "__main__":
    generate_file()