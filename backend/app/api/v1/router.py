from fastapi import APIRouter

from app.api.v1.endpoints import auth, interactions, news, recommendations

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(news.router)
router.include_router(interactions.router)
router.include_router(recommendations.router)
