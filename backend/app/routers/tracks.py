from fastapi import APIRouter, HTTPException, Query
from typing import Literal

from app.routers.auth import get_spotify_oauth
import spotipy

router = APIRouter()

TimeRange = Literal["short_term", "medium_term", "long_term"]


def get_spotify_client() -> spotipy.Spotify:
    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        raise HTTPException(
            status_code=401,
            detail="No cached Spotify token found. Visit /login first.",
        )
    return spotipy.Spotify(auth=token_info["access_token"])


@router.get("/me/top-tracks")
def top_tracks(time_range: TimeRange = Query(default="medium_term"), limit: int = 20):
    sp = get_spotify_client()
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
def top_artists(time_range: TimeRange = Query(default="medium_term"), limit: int = 20):
    sp = get_spotify_client()
    results = sp.current_user_top_artists(time_range=time_range, limit=limit)

    artists = [
        {
            "name": item["name"],
            "spotify_id": item["id"],
        }
        for item in results["items"]
    ]
    return {"time_range": time_range, "count": len(artists), "artists": artists}