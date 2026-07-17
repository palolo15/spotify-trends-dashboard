from fastapi import FastAPI

from app.routers import auth

app = FastAPI(title="Spotify Trends Dashboard API")

app.include_router(auth.router, tags=["auth"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Spotify Trends Dashboard API"}