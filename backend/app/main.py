from fastapi import FastAPI

from app.routers import auth, tracks, trends
from app.db.session import engine, Base
from app.models import snapshot  # noqa: F401 — needed so SQLAlchemy registers the model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spotify Trends Dashboard API")

app.include_router(auth.router, tags=["auth"])
app.include_router(tracks.router, tags=["tracks"])
app.include_router(trends.router, tags=["trends"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Spotify Trends Dashboard API"}

from app.db.session import SessionLocal
from app.models.snapshot import Snapshot


@app.get("/snapshots/status")
def snapshot_status():
    db = SessionLocal()
    try:
        total = db.query(Snapshot).count()
        recent = (
            db.query(Snapshot)
            .order_by(Snapshot.played_at.desc())
            .limit(5)
            .all()
        )
        return {
            "total_rows": total,
            "most_recent": [
                {
                    "track": r.track_name,
                    "artist": r.artist_name,
                    "played_at": r.played_at.isoformat(),
                }
                for r in recent
            ],
        }
    finally:
        db.close()