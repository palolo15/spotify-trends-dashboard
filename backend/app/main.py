from fastapi import FastAPI

from app.routers import auth, tracks
from app.db.session import engine, Base
from app.models import snapshot  # noqa: F401 — needed so SQLAlchemy registers the model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spotify Trends Dashboard API")

app.include_router(auth.router, tags=["auth"])
app.include_router(tracks.router, tags=["tracks"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Spotify Trends Dashboard API"}