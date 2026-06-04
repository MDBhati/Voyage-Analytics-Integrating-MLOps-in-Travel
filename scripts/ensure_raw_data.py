#!/usr/bin/env python3
"""CLI entrypoint for CI to ensure raw datasets exist."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.bootstrap import ensure_users_csv

if __name__ == "__main__":
    ensure_users_csv()
    print("Raw data check complete.")
