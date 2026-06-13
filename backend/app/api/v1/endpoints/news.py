from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import News
from app.db.schemas import NewsDetail, NewsOut

router = APIRouter(prefix="/news", tags=["news"])

_SEED_DATA = [
    {
        "id": 1,
        "source": "hurriyet",
        "title": "Test Haberi 1",
        "summary": "Bu bir test özeti.",
        "full_text": "Bu bir test haber metnidir.",
        "url": "https://example.com/haber/1",
        "category": "teknoloji",
        "published_at": None,
        "fetched_at": "2026-01-01T00:00:00",
    },
    {
        "id": 2,
        "source": "sabah",
        "title": "Test Haberi 2",
        "summary": "İkinci test özeti.",
        "full_text": "İkinci test haber metni.",
        "url": "https://example.com/haber/2",
        "category": "spor",
        "published_at": None,
        "fetched_at": "2026-01-01T01:00:00",
    },
]


@router.get("/", response_model=list[NewsOut])
def list_news(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = db.query(News).offset(skip).limit(limit).all()
    if results:
        return results
    # DB boşken seed verisiyle yanıt ver
    from datetime import datetime
    return [
        NewsOut(
            id=n["id"],
            source=n["source"],
            title=n["title"],
            summary=n["summary"],
            url=n["url"],
            category=n["category"],
            published_at=n["published_at"],
            fetched_at=datetime.fromisoformat(n["fetched_at"]),
        )
        for n in _SEED_DATA
    ]


@router.get("/{news_id}", response_model=NewsDetail)
def get_news(news_id: int, db: Session = Depends(get_db)):
    item = db.query(News).filter(News.id == news_id).first()
    if item:
        return item
    seed = next((n for n in _SEED_DATA if n["id"] == news_id), None)
    if not seed:
        raise HTTPException(status_code=404, detail="News not found")
    from datetime import datetime
    return NewsDetail(
        **{k: v for k, v in seed.items() if k != "fetched_at"},
        fetched_at=datetime.fromisoformat(seed["fetched_at"]),
    )
