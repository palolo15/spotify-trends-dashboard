from datetime import datetime, timezone
import spotipy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.routers.auth import get_spotify_oauth
from app.models.snapshot import Snapshot


def get_spotify_client() -> spotipy.Spotify:
    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        raise RuntimeError(
            "No cached Spotify token found. Run the app and visit /login first."
        )
    return spotipy.Spotify(auth=token_info["access_token"])


def fetch_and_store_recently_played(db: Session) -> dict:
    sp = get_spotify_client()
    results = sp.current_user_recently_played(limit=50)

    inserted = 0
    skipped = 0

    for item in results["items"]:
        track = item["track"]
        played_at_str = item["played_at"]  # ISO 8601 string from Spotify
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