"""Celery scraping task'ları (Adım 3'te implement edilecek)."""
from app.core.celery_app import celery_app


@celery_app.task(name="app.tasks.scraping_tasks.fetch_all_feeds")
def fetch_all_feeds() -> dict:
    """
    Tüm RSS feed'lerini tarar, yeni haberleri DB'ye kaydeder.
    Celery Beat tarafından periyodik çağrılır.
    """
    raise NotImplementedError
