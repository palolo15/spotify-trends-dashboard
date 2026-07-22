from datetime import datetime, timezone
from sqlalchemy import true
from sqlalchemy.orm import Session

from app.models.token import SpotifyToken
from app.routers.auth import get_spotify_oauth


def save_tokens(db: Session, token_info: dict):
    print("=== save_tokens called ===", flush=true)
    print(f"token_info keys: {token_info.keys()}", flush=true)

    db.query(SpotifyToken).delete()
    db.commit()
    print("Deleted old tokens", flush=true)

    expires_at = datetime.fromtimestamp(token_info["expires_at"], tz=timezone.utc)
    print(f"Computed expires_at: {expires_at}", flush=true)

    token_row = SpotifyToken(
        access_token=token_info["access_token"],
        refresh_token=token_info["refresh_token"],
        expires_at=expires_at,
    )
    db.add(token_row)
    db.commit()
    print(f"Committed new token row, id={token_row.id}", flush=true)


def get_valid_access_token(db: Session) -> str:
    token_row = db.query(SpotifyToken).first()
    if not token_row:
        raise RuntimeError("No Spotify token found in database. Visit /login first.")

    now = datetime.now(timezone.utc)

    if token_row.expires_at <= now:
        sp_oauth = get_spotify_oauth()
        new_token_info = sp_oauth.refresh_access_token(token_row.refresh_token)

        token_row.access_token = new_token_info["access_token"]
        token_row.refresh_token = new_token_info.get(
            "refresh_token", token_row.refresh_token
        )
        token_row.expires_at = datetime.fromtimestamp(
            new_token_info["expires_at"], tz=timezone.utc
        )
        db.commit()

        return token_row.access_token

    return token_row.access_token