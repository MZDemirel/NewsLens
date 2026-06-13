from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import feedparser

logger = logging.getLogger(__name__)

_SOURCES_PATH = Path(__file__).parent.parent / "core" / "rss_sources.json"


def _parse_time(time_struct) -> datetime | None:
    if time_struct is None:
        return None
    try:
        return datetime(*time_struct[:6])
    except Exception:
        return None


def fetch_feed(source: dict) -> list[dict]:
    """
    Tek bir RSS kaynağını feedparser ile çeker.

    Args:
        source: {"name": str, "category": str, "url": str}

    Returns:
        Her haber için {"title", "url", "summary", "published_at", "source", "category"} içeren dict listesi.
    """
    parsed = feedparser.parse(source["url"])
    items = []
    for entry in parsed.entries:
        link = entry.get("link") or entry.get("id")
        title = entry.get("title")
        if not link or not title:
            continue
        items.append({
            "title": title.strip(),
            "url": link,
            "summary": entry.get("summary") or entry.get("description") or None,
            "published_at": _parse_time(entry.get("published_parsed")),
            "source": source["name"],
            "category": source["category"],
        })
    return items


def fetch_all_feeds() -> list[dict]:
    """
    rss_sources.json'daki tüm kaynakları çeker, birleştirilmiş listeyi döner.
    Hatalı kaynaklar atlanır.
    """
    with open(_SOURCES_PATH, encoding="utf-8") as f:
        sources = json.load(f)["sources"]

    all_items: list[dict] = []
    for source in sources:
        try:
            items = fetch_feed(source)
            all_items.extend(items)
            logger.info("Fetched %d items from %s", len(items), source["name"])
        except Exception as exc:
            logger.warning("Failed to fetch %s: %s", source["name"], exc)

    return all_items
