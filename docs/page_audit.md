# Audit Halaman & Endpoint

Format ringkas untuk memantau kondisi tiap halaman (UI) dan endpoint (API). Update berkala saat ada perubahan signifikan.

Legenda Status:
- OK: Berfungsi sesuai kebutuhan sekarang.
- IMPROVE: Ada peningkatan direkomendasikan (performansi / keamanan / DX).
- PENDING: Belum diimplementasikan penuh.
- PLANNED: Direncanakan, belum mulai.

## Ringkasan Cepat
| Resource | Tipe | Tujuan | Status | Prioritas | Catatan Singkat |
|----------|------|--------|--------|-----------|-----------------|
| `/` | API | Splash root info | OK | Low | Statik sederhana. |
| `/health` | API | Cek konektivitas DB | OK | High | Sudah gunakan SELECT 1. Bisa tambah latency metrics. |
| `/auth/signup` | API | Registrasi user | OK | High | Validasi dasar ada; butuh rate limit & email verification (IMPROVE). |
| `/register` | API | Alias signup | IMPROVE | Medium | Duplikasi fungsional, rencana konsolidasi. |
| `/auth/login` | API | Login & JWT issuance | OK | High | Tambah brute-force mitigation (rate limit). |
| `/auth/token` | API | OAuth2 form login (Docs) | OK | Medium | Sinkron dengan `/auth/login`. |
| `/me` | API | Data user saat ini | OK | Medium | Tambah caching ringan? Rendah dampak. |
| `/categories/` GET | API | List kategori | OK | Medium | Indeks belum spesifik (nama). Bisa tambah unique constraint & search. |
| `/categories/` POST | API | Buat kategori | OK | Medium | Tambah audit log & name uniqueness enforce. |
| `/products/` GET | API | List produk (paging/filter) | OK | High | Sudah selectinload & indeks baru. Monitor query plan. |
| `/products/{id}` GET | API | Detail produk | OK | Medium | Eager load kategori sudah. |
| `/products/` POST | API | Buat produk | OK | High | Validasi harga > 0 disarankan. |
| `/products/{id}` PATCH | API | Update produk | OK | High | Partial update; perlu audit log. |
| `/products/{id}` DELETE | API | Hapus produk | IMPROVE | Medium | Hard delete; pertimbangkan soft delete. |
| Flask `/dashboard/` | UI | Ringkas status | IMPROVE | Medium | Data dummy; perlu integrasi API & caching. |
| Flask `/auth/login` | UI | Form login | OK | Medium | Integrasi backend auth belum final. |
| Flask `/auth/register` | UI | Form register | OK | Medium | Belum panggil API signup. |
| Flash Messages | UI | Feedback terstruktur | OK | Low | Auto-dismiss sudah. |
| Asset Bundling | UI | Minify CSS/JS | OK | Medium | Hash fingerprint (cache-bust) bisa ditambah. |
| Alembic Migrations | Infra | Skema DB versi | OK | High | Indeks tambahan sudah ditambah. |
| Celery (planned) | Infra | Tugas berat async | PLANNED | High | Belum integrasi broker/worker. |
| Redis (planned) | Infra | Cache, rate limit, task queue | PLANNED | High | Belum di docker-compose. |
| Secrets / Config | Infra | Manajemen konfigurasi | IMPROVE | High | Perlu ekstensi Settings & .env.example. |

## Detail Audit per Resource
### 1. Root `/`
- Fungsi: Memberi pesan selamat datang.
- Performansi: Nyaris nol beban; tidak perlu caching.
- Keamanan: Tidak ada data sensitif.
- TODO: Tambah versi API, build commit (optional).

### 2. Health `/health`
- Fungsi: Mengetes koneksi DB melalui `SELECT 1`.
- Performansi: Sederhana; dapat ditambah waktu eksekusi & uptime metrics.
- Keamanan: Aman; tidak bocor skema.
- TODO: Tambah status komponen lain (Redis, Celery) setelah integrasi.

### 3. Auth Signup `/auth/signup` & `/register`
- Fungsi: Membuat user baru.
- Performansi: Single insert; ringan.
- Keamanan: Password hashing pbkdf2. Perlu rate limit & email verification opsional.
- TODO: Konsolidasi endpoint (pilih satu). Tambah validasi password policy.

### 4. Auth Login `/auth/login` & `/auth/token`
- Fungsi: Menghasilkan JWT.
- Performansi: Query user by email + hash verify.
- Keamanan: Perlu rate limit brute-force, deteksi IP anomali.
- TODO: Refresh token workflow (jika dibutuhkan), revoke list (Redis).

### 5. Current User `/me`
- Fungsi: Mengambil profil minimal user.
- Performansi: Single SELECT; bisa difold ke cache jika beban tinggi.
- Keamanan: Butuh validasi token; sudah via dependency.
- TODO: Perlu return field tambahan (roles) jika role-based access ditambah.

### 6. Categories Endpoints
- GET: Tanpa pagination; aman untuk kini (jumlah kecil). Tambah pagination bila tumbuh.
- POST: Validasi duplikasi manual; bisa enforce unique index + error code terstandar.
- Indeks: Belum ada idx name spesifik; dapat ditambah jika query by name sering.

### 7. Products Endpoints
- List: Sudah paging, filter available/category, eager load category, indeks komposit baru dibuat.
- Detail: Eager load kategori; OK.
- Create: Perlu validasi numerik (harga > 0). Pastikan category exists (already).
- Patch: Partial update via `ProductUpdate`; audit log belum.
- Delete: Hard delete; pertimbangkan soft delete (flag deleted_at) untuk jejak data.

### 8. Flask UI Pages
- Dashboard: Static; data dummy. Perlu fetch API & caching summary.
- Login/Register: Form sudah pakai WTForms & CSRF; belum dihubungkan ke backend.
- Assets: Bundling OK; perlu fingerprint/hashing untuk long-term caching (improve).

### 9. Flash Messages
- Sudah terstruktur dengan kategori + auto-dismiss (non-error). Bisa tambah ARIA role lebih spesifik (alertdialog vs alert) bila perlu.

### 10. Migrations
- Baseline + indeks tambahan (users email, products composite). Rutin audit query plan.

### 11. Planned: Celery & Redis
- Celery: Untuk tugas berat (AI, processing gambar). Perlu menambah broker (Redis) & worker container.
- Redis: Cache query, rate limiting, token blacklist (jika refresh token implement).

### 12. Konfigurasi & Secrets
- Saat ini: Settings minimal (DATABASE_URL, SECRET_KEY, dll.).
- Peningkatan: Tambah ENV, LOG_LEVEL, REDIS_URL, FEATURE_FLAGS, validasi panjang SECRET_KEY.
- .env.example: Belum ada → PRIORITAS.

## Audit Performa (Ringkas)
- Indeks utama ditambahkan untuk filter produk (category_id, is_available, created_at).
- selectinload menghindari N+1 untuk kategori produk.
- GZip diaktifkan (minimum_size=1000).
- Belum ada caching (Redis) → rencana.

## Audit Keamanan (Ringkas)
| Area | Status | Catatan |
|------|--------|---------|
| Password Hash | OK | pbkdf2_sha256 (passlib) |
| JWT Secret | IMPROVE | Gunakan secret panjang (>=32 char), regex check di startup |
| Rate Limiting | PENDING | Akan pakai Redis / middleware custom |
| CSRF (Flask) | OK | Flask-WTF CSRF aktif |
| Input Validation | IMPROVE | Tambah harga > 0, email domain patterns optional |
| Logging Secrets | OK | Tidak melog password/token secara langsung |

## Saran Prioritas Berikutnya
1. Konfigurasi & Secrets: Extend `Settings` + buat `.env.example`.
2. Redis + Celery integrasi untuk tugas berat & rate limiting.
3. Konsolidasi endpoint `/register` → `/auth/signup` saja.
4. Validasi tambahan (harga produk, kebijakan kata sandi).
5. Soft delete produk (flag) + audit trail perubahan.
6. Implementasi refresh token & revoke list (jika diperlukan sesi panjang).

## Template Update Log
Gunakan format berikut ketika melakukan perubahan signifikan:
```
[YYYY-MM-DD] RESOURCE: /products/ (LIST)
CHANGE: Tambah indeks komposit category_id+is_available+created_at
REASON: Percepat filter & sort gabungan
IMPACT: Query latency turun ~X% (ukur setelah deploy)
```

## Catatan Penutup
File ini dimaksudkan sebagai living document. Lakukan peninjauan berkala (misal mingguan) dan sinkronkan dengan board tugas.
