from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Literal
import spotipy

from app.db.session import get_db
from app.services.token_service import get_valid_access_token

router = APIRouter()

TimeRange = Literal["short_term", "medium_term", "long_term"]


def get_spotify_client(db: Session) -> spotipy.Spotify:
    try:
        access_token = get_valid_access_token(db)
    except RuntimeError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return spotipy.Spotify(auth=access_token)


@router.get("/me/top-tracks")
def top_tracks(
    time_range: TimeRange = Query(default="medium_term"),
    limit: int = 20,
    db: Session = Depends(get_db),
):
    sp = get_spotify_client(db)
    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)

    tracks = [
        {
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "spotify_id": item["id"],
        }
        for item in results["items"]
    ]
    return {"time_range": time_range, "count": len(tracks), "tracks": tracks}


@router.get("/me/top-artists")
def top_artists(
    time_range: TimeRange = Query(default="medium_term"),
    limit: int = 20,
    db: Session = Depends(get_db),
):
    sp = get_spotify_client(db)
    results = sp.current_user_top_artists(time_range=time_range, limit=limit)

    artists = [
        {"name": item["name"], "spotify_id": item["id"]}
        for item in results["items"]
    ]
    return {"time_range": time_range, "count": len(artists), "artists": artists}