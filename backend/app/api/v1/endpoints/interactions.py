from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.db.database import get_db
from app.db.models import News, User, UserInteraction
from app.db.schemas import InteractionCreate, InteractionOut

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("/", response_model=InteractionOut, status_code=201)
def create_interaction(
    payload: InteractionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not db.query(News).filter(News.id == payload.news_id).first():
        raise HTTPException(status_code=404, detail="News not found")
    interaction = UserInteraction(
        user_id=current_user.id,
        news_id=payload.news_id,
        action=payload.action,
        dwell_time_sec=payload.dwell_time_sec,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction
