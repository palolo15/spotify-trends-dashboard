from fastapi import FastAPI

from app.routers import auth, tracks

app = FastAPI(title="Spotify Trends Dashboard API")

app.include_router(auth.router, tags=["auth"])
app.include_router(tracks.router, tags=["tracks"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Spotify Trends Dashboard API"}