# Haber Öneri Sistemi

Türkçe haber sitelerinden RSS ile içerik toplayıp kullanıcılara **kişiselleştirilmiş haber önerileri** sunan web platformu. Veri madenciliği dersi final projesi.

---

## Teknoloji Stack

| Katman | Teknoloji |
|---|---|
| Backend API | FastAPI + Uvicorn |
| ORM / Migration | SQLAlchemy + Alembic |
| Veritabanı | PostgreSQL 16 |
| Görev kuyruğu | Celery + Celery Beat + Redis 7 |
| Frontend | React 19 + Vite |
| HTTP istemci | Axios + React Router v6 |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| ML / NLP | scikit-learn (TF-IDF), sentence-transformers |
| RSS / Scraping | feedparser, trafilatura |

---

## Kurulum

### Gereksinimler

- [Docker](https://docs.docker.com/get-docker/) ve [Docker Compose](https://docs.docker.com/compose/) (v2+)

### 1. Repoyu klonla

```bash
git clone <repo-url>
cd "NewsLens"
```

### 2. Ortam değişkenlerini ayarla

```bash
cp .env.example .env
# .env dosyasını açıp SECRET_KEY değerini güvenli bir değerle değiştir
```

### 3. Servisleri başlat

```bash
docker-compose up --build
```

### 4. Veritabanı tablolarını oluştur

İlk çalıştırmada, ayrı bir terminalde:

```bash
docker-compose exec backend alembic upgrade head
```

### 5. Uygulamayı kullan

| Servis | URL |
|---|---|
| React Frontend | http://localhost:5173 |
| FastAPI Swagger UI | http://localhost:8000/docs |
| FastAPI ReDoc | http://localhost:8000/redoc |

---

## Proje Yapısı

```
.
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/                  # DB migration'ları
│   │   └── versions/
│   └── app/
│       ├── main.py               # FastAPI uygulama giriş noktası
│       ├── core/
│       │   ├── config.py         # Ortam değişkenleri (pydantic-settings)
│       │   ├── security.py       # JWT + bcrypt
│       │   └── celery_app.py     # Celery instance + Beat schedule
│       ├── db/
│       │   ├── database.py       # SQLAlchemy engine / session
│       │   ├── models.py         # ORM modelleri (User, News, UserInteraction)
│       │   └── schemas.py        # Pydantic request/response şemaları
│       ├── api/v1/
│       │   ├── router.py
│       │   ├── deps.py           # Auth dependency (get_current_user)
│       │   └── endpoints/
│       │       ├── auth.py         # POST /register, POST /login
│       │       ├── news.py         # GET /news/, GET /news/{id}
│       │       ├── interactions.py # POST /interactions
│       │       └── recommendations.py # GET /recommendations
│       ├── services/
│       │   ├── rss_fetcher.py    # RSS okuma iskeleti
│       │   ├── text_extractor.py # Tam metin çekme iskeleti
│       │   └── recommender.py    # Öneri motoru iskeleti
│       └── tasks/
│           └── scraping_tasks.py # Celery task iskeleti
└── frontend/
    └── src/
        ├── api/client.js         # Axios wrapper
        ├── hooks/useAuth.js      # Token yönetimi
        ├── components/
        │   ├── NewsCard.jsx
        │   └── NewsList.jsx
        └── pages/
            ├── HomePage.jsx
            ├── NewsDetailPage.jsx
            ├── LoginPage.jsx
            └── RegisterPage.jsx
```

---

## API Endpoint'leri

| Method | Endpoint | Açıklama | Auth |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Yeni kullanıcı kaydı | — |
| POST | `/api/v1/auth/login` | Giriş, JWT döner | — |
| GET | `/api/v1/news/` | Haber listesi | — |
| GET | `/api/v1/news/{id}` | Haber detayı | — |
| POST | `/api/v1/interactions/` | Etkileşim kaydet (tıklama vb.) | JWT |
| GET | `/api/v1/recommendations/` | Kişisel öneriler | JWT |

---

## Geliştirme Yol Haritası

Proje aşamalı olarak geliştirilmektedir. Tamamlanan ve bekleyen adımlar:

- [x] **Adım 1 — Backend + Frontend iskeleti** *(mevcut durum)*
  - FastAPI, PostgreSQL, Alembic migration, JWT auth
  - React uygulaması, routing, login/kayıt sayfaları
  - Docker Compose ortamı

- [ ] **Adım 2 — RSS Toplama Hattı**
  - `backend/app/services/rss_fetcher.py` içindeki `fetch_feed()` fonksiyonunu feedparser ile doldur
  - `backend/app/services/text_extractor.py` içindeki `extract_full_text()` fonksiyonunu trafilatura ile doldur
  - `backend/app/tasks/scraping_tasks.py` içindeki Celery task'ını implement et
  - `backend/app/core/celery_app.py` içindeki beat schedule'ı aktif et (saatlik çalışacak şekilde)
  - Haber kaynağı URL listesini yapılandır

- [ ] **Adım 3 — Kullanıcı Etkileşim Loglama**
  - Frontend'de `useInteractionTracker.js` hook'unu yaz
  - Haber kartına tıklama ve okuma süresi event'lerini `/api/v1/interactions/` endpoint'ine gönder

- [ ] **Adım 4 — Öneri Motoru v1 (TF-IDF)**
  - `backend/app/services/recommender.py` içindeki `get_similar()` fonksiyonunu implement et
  - Haber metinleri üzerinde TF-IDF vektörizasyonu + kosinüs benzerliği
  - `/api/v1/recommendations/` endpoint'ini bağla
  - Frontend'de `RecommendationFeed.jsx` bileşenini ekle

- [ ] **Adım 5 — Öneri Motoru v2 (Hibrit / Kişiselleştirilmiş)**
  - sentence-transformers ile çok dilli embedding üret, `news.embedding` sütununa kaydet (pgvector)
  - Kullanıcı etkileşim geçmişinden profil vektörü oluştur
  - `get_personalized()` fonksiyonunu implement et (embedding + TF-IDF hibrit)

- [ ] **Adım 6 — Değerlendirme**
  - precision@k / recall@k metriklerini hesapla
  - v1 ve v2 öneri motorlarını karşılaştır
  - Basit bir değerlendirme raporu hazırla

---

## Geliştirme Notları

**Yeni migration oluşturmak için:**
```bash
docker-compose exec backend alembic revision --autogenerate -m "açıklama"
docker-compose exec backend alembic upgrade head
```

**Celery worker'ı başlatmak için (Adım 2 sonrası):**
```bash
docker-compose exec backend celery -A app.core.celery_app worker --loglevel=info
docker-compose exec backend celery -A app.core.celery_app beat --loglevel=info
```

**Backend loglarını izlemek için:**
```bash
docker-compose logs -f backend
```

---

## Katkıda Bulunma

1. Yeni bir branch aç: `git checkout -b feature/özellik-adı`
2. Değişikliklerini commit'le
3. Pull request aç

---

## Lisans

Bu proje eğitim amaçlıdır.
