from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_db
from app.models.snapshot import Snapshot

router = APIRouter()


@router.get("/trends/volume")
def listening_volume(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.date(Snapshot.played_at).label("day"),
            func.count(Snapshot.id).label("play_count"),
        )
        .group_by(func.date(Snapshot.played_at))
        .order_by(func.date(Snapshot.played_at))
        .all()
    )

    return {
        "data": [
            {"date": str(row.day), "play_count": row.play_count}
            for row in results
        ]
    }

@router.get("/trends/artist-turnover")
def artist_turnover(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.date_trunc("week", Snapshot.played_at).label("week"),
            Snapshot.artist_name,
        )
        .distinct()
        .order_by(func.date_trunc("week", Snapshot.played_at))
        .all()
    )

    weeks: dict[str, set[str]] = {}
    for row in results:
        week_key = str(row.week.date())
        weeks.setdefault(week_key, set()).add(row.artist_name)

    sorted_weeks = sorted(weeks.keys())
    output = []
    seen_artists: set[str] = set()

    for week in sorted_weeks:
        current_artists = weeks[week]
        new_artists = current_artists - seen_artists
        output.append(
            {
                "week": week,
                "total_unique_artists": len(current_artists),
                "new_artists": sorted(new_artists),
                "new_artist_count": len(new_artists),
            }
        )
        seen_artists |= current_artists

    return {"data": output}