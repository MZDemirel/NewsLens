from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "news_recommender",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.scraping_tasks"],
)

celery_app.conf.beat_schedule = {
    # "fetch-feeds-every-hour": {
    #     "task": "app.tasks.scraping_tasks.fetch_all_feeds",
    #     "schedule": 3600.0,
    # },
}
celery_app.conf.timezone = "Europe/Istanbul"
