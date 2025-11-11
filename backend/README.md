# Repositori Backend (dieHantar-backend)

Repositori ini berisi semua layanan backend, konfigurasi infrastruktur, dan API untuk aplikasi dieHantar.

## Struktur

- `auth/`: Layanan otentikasi
- `order/`: Layanan pesanan
- `infra/`: Konfigurasi Kubernetes
- `openapi/`: Spesifikasi OpenAPI
- `scripts/`: Skrip untuk pengujian dan deployment
- `docker-compose.yml`: Konfigurasi Docker Compose untuk pengembangan lokal

## Jalankan Secara Lokal (FastAPI)

1. Siapkan environment variables (contoh minimal):

	- `DATABASE_URL` (contoh: `mysql+pymysql://user:pass@localhost:3306/diehantar`)
	- `SECRET_KEY` untuk JWT

2. Instal dependensi (lihat `backend/requirements.txt`).

3. Migrasi database (menggunakan Alembic):

```bash
# dari folder repo root
export PYTHONPATH=backend
alembic -c backend/app/alembic.ini upgrade head
```

4. Jalankan server dev (contoh):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Catatan: `Base.metadata.create_all` dinonaktifkan secara default. Untuk keperluan dev cepat, Anda dapat mengaktifkan dengan `DEV_AUTO_CREATE=1`, namun alur utama adalah migrasi Alembic.

## Konfigurasi & Secrets

Semua konfigurasi dibaca dari environment variables (lihat `backend/.env.example`).

Prinsip:
- Jangan commit secrets nyata. Gunakan `.env` lokal untuk dev, Docker/K8s Secrets untuk staging/production.
- Fail-fast untuk SECRET_KEY lemah (wajib >= 32 chars).
- Feature flags dapat diatur via `FEATURE_FLAGS_JSON`.

Contoh `.env` dev (salin dari `.env.example`):
```
DATABASE_URL=mysql+pymysql://root:example@mysql:3306/diehantar_db
SECRET_KEY=REPLACE_WITH_LONG_RANDOM_>=32_CHARS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV=development
LOG_LEVEL=info
# Optional Redis/Celery
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
FEATURE_FLAGS_JSON={"ENABLE_CATEGORIES_CREATE": true}
```

### Docker Compose (Secrets)
- Gunakan `env_file: backend/.env` untuk pengembangan lokal.
- Untuk production, gunakan Docker Swarm/K8s secrets, jangan plain env file.

### Kubernetes
- Simpan secrets di `Secret` (Opaque), non-secrets di `ConfigMap`.
- Injeksi via `envFrom` ke Deployment.
- Rotasi secrets: deploy versi baru dengan secret baru, lakukan rolling update.

### CI/CD (GitHub Actions)
- Simpan secrets di GitHub Secrets (DB URL, SECRET_KEY, registry token).
- Injeksi secrets pada step deploy; hindari menuliskan secrets pada layer Docker.
