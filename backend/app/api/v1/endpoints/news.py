from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import News
from app.db.schemas import NewsDetail, NewsOut

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/", response_model=list[NewsOut])
def list_news(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(News).order_by(News.fetched_at.desc()).offset(skip).limit(limit).all()


@router.get("/{news_id}", response_model=NewsDetail)
def get_news(news_id: int, db: Session = Depends(get_db)):
    item = db.query(News).filter(News.id == news_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    return item
