from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path

from app.config import settings
from app.db.session import get_db

router = APIRouter()

SCOPES = "user-top-read user-read-recently-played"

CACHE_PATH = Path(__file__).resolve().parent.parent.parent.parent / ".spotify_cache"


def get_spotify_oauth() -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=settings.spotify_client_id,
        client_secret=settings.spotify_client_secret,
        redirect_uri=settings.spotify_redirect_uri,
        scope=SCOPES,
        cache_path=str(CACHE_PATH),
    )


@router.get("/login")
def login():
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)


@router.get("/callback")
def callback(code: str | None = None, error: str | None = None, db: Session = Depends(get_db)):
    if error:
        raise HTTPException(status_code=400, detail=f"Spotify auth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="No authorization code returned")

    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_access_token(code, as_dict=True)

    from app.services.token_service import save_tokens
    save_tokens(db, token_info)

    return {
        "message": "Authenticated successfully and saved to database",
        "access_token_preview": token_info["access_token"][:15] + "...",
        "expires_in": token_info["expires_in"],
        "has_refresh_token": "refresh_token" in token_info,
    }