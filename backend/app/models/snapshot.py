from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime, timezone

from app.db.session import Base


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(String, nullable=False, index=True)
    track_name = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)
    played_at = Column(DateTime(timezone=True), nullable=False, index=True)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("track_id", "played_at", name="uq_track_played_at"),
    )