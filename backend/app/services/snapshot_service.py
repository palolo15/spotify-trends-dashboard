from datetime import datetime, timezone
import spotipy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.services.token_service import get_valid_access_token
from app.models.snapshot import Snapshot


def get_spotify_client(db: Session) -> spotipy.Spotify:
    access_token = get_valid_access_token(db)
    return spotipy.Spotify(auth=access_token)


def fetch_and_store_recently_played(db: Session) -> dict:
    sp = get_spotify_client(db)
    results = sp.current_user_recently_played(limit=50)

    inserted = 0
    skipped = 0

    for item in results["items"]:
        track = item["track"]
        played_at_str = item["played_at"]
        played_at = datetime.fromisoformat(played_at_str.replace("Z", "+00:00"))

        snapshot = Snapshot(
            track_id=track["id"],
            track_name=track["name"],
            artist_name=track["artists"][0]["name"],
            played_at=played_at,
        )

        db.add(snapshot)
        try:
            db.commit()
            inserted += 1
        except IntegrityError:
            db.rollback()
            skipped += 1

    return {
        "fetched": len(results["items"]),
        "inserted": inserted,
        "skipped_duplicates": skipped,
    }