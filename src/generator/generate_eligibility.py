import csv
import random
import uuid
from datetime import date, timedelta
from pathlib import Path


OUTPUT_DIR = Path("data/generated")

RECORD_COUNT = 1000


FIRST_NAMES = [
    "James",
    "John",
    "Robert",
    "Michael",
    "David",
    "Mary",
    "Jennifer",
    "Linda",
    "Patricia",
    "Susan",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Wilson",
    "Anderson",
]

STATES = [
    "FL",
    "TX",
    "CA",
    "NY",
    "GA",
    "IL",
]

PLANS = [
    "PLAN001",
    "PLAN002",
    "PLAN003",
    "PLAN004",
    "PLAN005",
]


def random_date(start_date, end_date):

    delta = end_date - start_date

    random_days = random.randint(0, delta.days)

    return start_date + timedelta(days=random_days)


def generate_member(index):

    dob = random_date(
        date(1940, 1, 1),
        date(2005, 12, 31)
    )

    effective_date = random_date(
        date(2025, 1, 1),
        date(2026, 12, 31)
    )

    return {
        "member_id": f"M{index:08d}",
        "subscriber_id": f"S{random.randint(1, 500):08d}",
        "first_name": random.choice(FIRST_NAMES),
        "last_name": random.choice(LAST_NAMES),
        "date_of_birth": dob.isoformat(),
        "gender": random.choice(["M", "F"]),
        "state": random.choice(STATES),
        "zip_code": str(random.randint(10000, 99999)),
        "plan_id": random.choice(PLANS),
        "coverage_type": "MEDICAL",
        "effective_date": effective_date.isoformat(),
        "termination_date": "",
        "source_record_id": str(uuid.uuid4()),
    }


def generate_file():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    file_name = (
        f"ACME_HEALTH_ELIGIBILITY_"
        f"{date.today().strftime('%Y%m%d')}.csv"
    )

    output_file = OUTPUT_DIR / file_name

    members = [
        generate_member(i)
        for i in range(1, RECORD_COUNT + 1)
    ]

    fieldnames = list(members[0].keys())

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
        writer.writerows(members)

    print("----------------------------------")
    print("Synthetic Eligibility Generator")
    print("----------------------------------")
    print(f"File: {output_file}")
    print(f"Records generated: {len(members)}")
    print("----------------------------------")


if __name__ == "__main__":
    generate_file()