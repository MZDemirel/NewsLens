from __future__ import annotations

import logging

import trafilatura

logger = logging.getLogger(__name__)


def extract_full_text(url: str) -> str | None:
    """
    Verilen URL'deki sayfadan trafilatura ile makale metnini çeker.

    Returns:
        Çekilen metin veya başarısız olunursa None.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None
        return trafilatura.extract(downloaded) or None
    except Exception as exc:
        logger.warning("Text extraction failed for %s: %s", url, exc)
        return None
