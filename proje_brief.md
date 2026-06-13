# Haber Öneri Sistemi - Proje Brief'i

## Proje Amacı

Çeşitli Türk haber sitelerinden (RSS ile) düzenli olarak haber toplayan, bu
haberleri kullanıcılara gösteren ve kullanıcıların ilgi alanlarına göre
**kişiselleştirilmiş haber önerileri** sunan bir web platformu geliştiriyoruz.
Bu bir üniversite veri madenciliği dersi projesi (4 kişilik takım).

## Teknoloji Stack

- **Backend:** FastAPI
- **Görev kuyruğu / zamanlama:** Celery + Celery Beat + Redis
- **Veritabanı:** PostgreSQL (ileride embedding için pgvector eklenebilir)
- **Frontend:** React
- **ML/NLP:** scikit-learn (TF-IDF), sentence-transformers (çok dilli /
  Türkçe embedding modelleri). Ağır LLM kullanımı planlanmıyor; öneri motoru
  klasik veri madenciliği + embedding tabanlı olacak.

## Aşamalı Yol Haritası (öncelik sırası)

1. **Backend iskeleti + veritabanı şeması** (bu brief'te detaylı)
2. **Frontend iskeleti**: haber listesi, haber detay, basit login/kayıt
3. **RSS toplama hattı**: feedparser ile RSS okuma + trafilatura ile tam
   metin çekme, Celery Beat ile periyodik çalıştırma
4. **Kullanıcı etkileşim loglama**: tıklama, okuma süresi gibi event'leri
   `user_interactions` tablosuna kaydetme
5. **Öneri motoru v1**: TF-IDF + kosinüs benzerliği ile "benzer haberler"
6. **Öneri motoru v2**: sentence-transformers embedding'leri + kullanıcı
   profil vektörü ile kişiselleştirilmiş öneriler (hibrit)
7. **Değerlendirme**: precision@k / recall@k gibi metrikler, basit bir
   karşılaştırma raporu

Şu an **sıfırdan başlıyoruz**. İlk hedef madde 1 ve 2'dir (backend +
frontend iskeleti). RSS scraping ve öneri motoru sonraki adımlarda ayrı
ayrı ele alınacak, şimdilik sadece şemanın bunlara uygun olması yeterli.

## Veritabanı Şeması (taslak)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    full_text TEXT,
    url TEXT UNIQUE NOT NULL,
    category VARCHAR(50),
    published_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT now()
    -- ileride: embedding VECTOR(384)
);

CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    news_id INTEGER REFERENCES news(id),
    action VARCHAR(20),          -- 'click', 'read_full', 'like' vb.
    dwell_time_sec INTEGER,
    created_at TIMESTAMP DEFAULT now()
);
```

`news.url` UNIQUE olmalı (RSS taramalarında aynı haberin tekrar tekrar
kaydedilmesini önlemek için, `ON CONFLICT DO NOTHING` ile insert).

## Backend Klasör Yapısı (önerilen)

```
backend/
  app/
    main.py
    core/
      config.py            # ortam değişkenleri, ayarlar
      celery_app.py         # celery instance + beat schedule
      security.py           # auth/JWT
    db/
      database.py           # SQLAlchemy engine/session
      models.py              # ORM modelleri (User, News, UserInteraction)
      schemas.py              # Pydantic request/response şemaları
    api/
      v1/
        router.py
        endpoints/
          auth.py
          news.py
          interactions.py
          recommendations.py
    services/
      rss_fetcher.py         # feedparser ile feed okuma (henüz boş/iskelet)
      text_extractor.py        # trafilatura ile tam metin çekme (iskelet)
      recommender.py             # öneri motoru (iskelet, sonra doldurulacak)
    tasks/
      scraping_tasks.py       # Celery task'ları (iskelet)
  alembic/                     # migration'lar
  requirements.txt
  Dockerfile
```

## Frontend Klasör Yapısı (önerilen)

```
frontend/
  src/
    api/
      client.js              # axios/fetch wrapper, backend base URL
    components/
      NewsCard.jsx
      NewsList.jsx
      RecommendationFeed.jsx (sonraki adım)
    pages/
      HomePage.jsx
      NewsDetailPage.jsx
      LoginPage.jsx
      RegisterPage.jsx
    hooks/
      useAuth.js
      useInteractionTracker.js   (sonraki adım)
    App.jsx
    main.jsx
  package.json
```

## İlk Adım İçin Talimat

Şu an için sadece **backend ve frontend iskeletini** kur:

- Backend: yukarıdaki klasör yapısına uygun bir FastAPI projesi, PostgreSQL
  bağlantısı (SQLAlchemy + Alembic ile migration), yukarıdaki üç tablo için
  modeller, basit auth (kayıt/login, JWT), ve `/news` için CRUD olmayan
  sadece "listele" endpoint'i (şimdilik test verisiyle doldurulabilir).
- Frontend: React projesi (Vite ile), backend'e bağlanan basit bir haber
  listesi sayfası, login/kayıt sayfaları, temel routing.
- RSS scraping (`rss_fetcher.py`, `text_extractor.py`), Celery task'ları ve
  öneri motoru (`recommender.py`) için sadece **boş iskelet dosyalar /
  fonksiyon imzaları** oluştur, içini doldurma — bunları ayrı adımlarda ele
  alacağız.
- Docker Compose ile backend, frontend, PostgreSQL ve Redis'i ayağa
  kaldıracak bir geliştirme ortamı kurulması faydalı olur.

Sorularını veya alternatif önerilerini belirtmekten çekinme; bu bir başlangıç
taslağıdır, gerekirse birlikte revize ederiz.
