import sys
import os

# Allow importing from backend/app when running this script standalone
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.db.session import SessionLocal
from app.services.snapshot_service import fetch_and_store_recently_played


def main():
    db = SessionLocal()
    try:
        result = fetch_and_store_recently_played(db)
        print(
            f"Snapshot complete — fetched: {result['fetched']}, "
            f"inserted: {result['inserted']}, "
            f"skipped (duplicates): {result['skipped_duplicates']}"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()