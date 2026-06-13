import logging

from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.celery_app import celery_app
from app.db.database import SessionLocal
from app.db.models import News
from app.services import rss_fetcher, text_extractor

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.scraping_tasks.fetch_all_feeds_task", bind=True, max_retries=3)
def fetch_all_feeds_task(self) -> dict:
    """
    Tüm RSS feed'lerini tarar, tam metinleri çeker ve yeni haberleri DB'ye kaydeder.
    Celery Beat tarafından saatte bir çağrılır.
    """
    items = rss_fetcher.fetch_all_feeds()
    logger.info("RSS fetch complete: %d items total", len(items))

    db = SessionLocal()
    saved = 0
    try:
        for item in items:
            full_text = text_extractor.extract_full_text(item["url"])
            stmt = (
                pg_insert(News)
                .values(
                    source=item["source"],
                    title=item["title"],
                    summary=item.get("summary"),
                    full_text=full_text,
                    url=item["url"],
                    category=item.get("category"),
                    published_at=item.get("published_at"),
                )
                .on_conflict_do_nothing(index_elements=["url"])
            )
            result = db.execute(stmt)
            saved += result.rowcount
        db.commit()
        logger.info("Saved %d new articles to DB", saved)
    except Exception as exc:
        db.rollback()
        logger.error("DB error during scraping: %s", exc)
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()

    return {"fetched": len(items), "saved": saved}
