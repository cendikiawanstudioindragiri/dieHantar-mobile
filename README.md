# dieHantar-mobile

Ringkasan arsitektur tingkat-tinggi untuk proyek mobile "dieHantar" (template).

Tujuan: dokumen ini menjelaskan arsitektur umum yang direkomendasikan untuk super-app pengiriman "dieHantar", komponen utama, pola komunikasi, dan teknologi yang umum digunakan. Gunakan ini sebagai referensi saat menambahkan kode sumber atau saat membuat monorepo layanan terkait.

---

## 1. Gambaran Singkat

`dieHantar` adalah super-app pengiriman (delivery super app) yang biasanya terdiri dari aplikasi mobile untuk pelanggan dan kurir, API/Backend-for-Frontend, layanan mikro untuk domain bisnis (order, delivery, payment, dll.), serta infrastruktur pendukung (DB, cache, message broker, object storage, monitoring).

Dokumen ini adalah template arsitektur — repo saat ini hanya berisi placeholder. Jika Anda ingin deteksi otomatis stack dari kode, pastikan file kode (mis. `package.json`, `pubspec.yaml`, `go.mod`, dsb.) ada di repo.

## 2. Komponen Utama

- Frontend Mobile
	- Mobile app untuk Customer dan Driver (Flutter atau React Native / Native).
	- Komunikasi: HTTPS (REST/GraphQL), WebSocket untuk realtime, FCM/APNs untuk push.

- API Gateway / BFF
	- Titik masuk tunggal untuk klien mobile (routing, auth, aggregasi response).

- Microservices
	- Layanan domain: Auth, User, Order, Delivery, Payment, Notification, Merchant, Catalog.
	- Komunikasi internal: REST/gRPC (sync), Message broker (async/event-driven).

- Persistence
	- Relasional: PostgreSQL
	- NoSQL: MongoDB/DynamoDB (opsional)
	- Cache: Redis
	- Object storage: S3 / MinIO

- Real-time
	- WebSocket / Socket.IO / MQTT untuk update lokasi dan status order.

- Messaging / Streaming
	- RabbitMQ atau Kafka untuk event bus dan decoupling.

- Integrasi Pihak Ketiga
	- Payment gateway, Maps (Google/Mapbox), SMS/Email provider.

## 3. Pola Komunikasi (ringkas)

- Mobile App → API Gateway: HTTPS (REST/GraphQL) dengan JWT/OAuth2.
- API Gateway → Microservices: HTTP/gRPC untuk operasi sinkron.
- Microservices ↔ Microservices: Event-driven via Kafka/RabbitMQ untuk tugas async (notifikasi, billing, assignment).
- Mobile ↔ Realtime Service: WebSocket untuk lokasi dan status.
- Payment Gateway ↔ Payment Service: Webhook untuk konfirmasi.

## 4. Stack Teknologi (opsional umum)

- Mobile: Flutter (Dart) atau React Native (TypeScript)
- Backend: Node.js (NestJS/Express) / Go (Gin) / Python (FastAPI)
- Database: PostgreSQL
- Cache: Redis
- Message Broker: RabbitMQ atau Kafka
- Object Storage: AWS S3 / MinIO
- Container / Orchestration: Docker + Kubernetes
- CI/CD: GitHub Actions / GitLab CI
- Observability: Prometheus + Grafana, ELK / Loki, Jaeger

## 5. Cara Verifikasi Stack di Repo (daftar file kunci)

Periksa keberadaan file-file ini untuk menentukan stack yang sebenarnya:

- `pubspec.yaml` → Flutter
- `package.json` → React Native / Node.js
- `go.mod` → Go services
- `requirements.txt` / `pyproject.toml` → Python services
- `Dockerfile`, `.github/workflows/`, `k8s/`, `charts/` → infra/CI/CD/kubernetes

Jika file-file ini belum ada, pertimbangkan menambahkan struktur monorepo seperti:

- `mobile/` (mobile app)
- `services/` (microservices each in its own folder)
- `infrastructure/` (k8s manifests, helm charts)
- `README-ARCHITECTURE.md` (dokumen arsitektur lebih lengkap)

## 6. Langkah Selanjutnya (saya bisa bantu)

1. Deteksi otomatis stack di repo Anda dan laporkan hasil — saya bisa menjalankan pencarian file kunci sekarang.
2. Jika repo kosong untuk kode, saya dapat membuat template monorepo awal:
	 - Struktur folder dasar (mobile/, services/, infra/)
	 - Contoh `package.json` atau `pubspec.yaml` minimal
	 - Contoh Dockerfile dan `k8s/` manifest sederhana
3. Buat diagram arsitektur (ASCII atau file gambar) dan kontrak API (OpenAPI/GraphQL schema).

---

Dokumen ini dibuat sebagai titik awal. Pilih langkah selanjutnya: deteksi otomatis file di repo (A) atau buat template monorepo/README arsitektur lebih lengkap (B). Saya sudah menyiapkan kedua opsi dan bisa langsung mengerjakan yang Anda pilih.

