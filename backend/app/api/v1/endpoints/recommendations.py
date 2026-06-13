from fastapi import APIRouter, Depends

from app.api.v1.deps import get_current_user
from app.db.models import User
from app.db.schemas import NewsOut

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=list[NewsOut])
def get_recommendations(current_user: User = Depends(get_current_user)):
    # Öneri motoru v1/v2 burada implement edilecek (sonraki adım)
    return []
