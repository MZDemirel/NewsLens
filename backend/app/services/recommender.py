"""Öneri motoru (Adım 5-6'da implement edilecek)."""
from __future__ import annotations


def get_similar(news_id: int, top_k: int = 10) -> list[int]:
    """
    TF-IDF + kosinüs benzerliği ile en benzer haberlerin ID listesini döner (v1).

    Returns:
        news_id listesi (benzerlik sırasına göre).
    """
    raise NotImplementedError


def get_personalized(user_id: int, top_k: int = 10) -> list[int]:
    """
    Kullanıcı profil vektörü + embedding benzerliği ile kişiselleştirilmiş öneri listesi (v2).

    Returns:
        news_id listesi (skor sırasına göre).
    """
    raise NotImplementedError
