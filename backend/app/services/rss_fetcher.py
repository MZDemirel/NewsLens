"""RSS feed okuma servisi (Adım 3'te implement edilecek)."""
from __future__ import annotations


def fetch_feed(url: str) -> list[dict]:
    """
    Verilen RSS URL'sinden haberleri çeker.

    Returns:
        Her haber için {'title', 'url', 'summary', 'published_at', 'source'} içeren dict listesi.
    """
    raise NotImplementedError


def fetch_all_feeds(feed_urls: list[str]) -> list[dict]:
    """Birden fazla feed URL'si için fetch_feed çağırır ve sonuçları birleştirir."""
    raise NotImplementedError
