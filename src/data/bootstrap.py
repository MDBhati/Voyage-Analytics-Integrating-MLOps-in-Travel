from pathlib import Path

import pandas as pd

USERS_PATH = Path("data/raw/users.csv")


def _bootstrap_users_csv():
    """Create a synthetic users dataset when the real file is unavailable (e.g. CI)."""
    companies = ["4You", "Rainbow", "CloudFy", "FlyingDrops"]
    profiles = [
        ("Roy Braun", "male"),
        ("Joseph Holsten", "male"),
        ("Wilma Mcinnis", "female"),
        ("Paula Daniel", "female"),
        ("Trina Thomas", "none"),
        ("Jesse Decelle", "male"),
        ("Gregoria Gil", "female"),
        ("Jack Sabo", "none"),
        ("Debbie Helms", "none"),
        ("Virginia Roberts", "female"),
    ]

    rows = []
    for i in range(300):
        name, gender = profiles[i % len(profiles)]
        rows.append(
            {
                "code": i,
                "company": companies[i % len(companies)],
                "name": name,
                "gender": gender,
                "age": 20 + (i % 45),
            }
        )

    USERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(USERS_PATH, index=False)


def ensure_users_csv():
    if not USERS_PATH.exists():
        _bootstrap_users_csv()
