# MINIO Demo dengan Django Monolith (Docker)

Aplikasi web monolith berbasis Django untuk mendemonstrasikan object storage MINIO dalam mata kuliah Sistem Terdistribusi. Demo ini menampilkan upload/download, listing objek, presigned URL, versioning (lihat dan restore versi), serta event log via webhook. MINIO berjalan dalam mode terdistribusi (4 node) menggunakan Docker Compose.

## Arsitektur Singkat
- 4 kontainer `minio` (distributed mode) dengan volume terpisah untuk persistensi.
- 1 kontainer `django-app` (monolith) menyajikan UI berbasis template.
- 1 kontainer `mc-init` untuk inisialisasi bucket dan versioning.
- MINIO Console (web) di `http://localhost:9001` untuk administrasi.

## Prasyarat
- Docker Desktop terbaru (Windows/macOS/Linux).
- Port lokal yang tersedia: `8000` (Django), `9000` (S3 API), `9001` (MINIO Console).

## Konfigurasi
1. Salin `.env.example` menjadi `.env` dan sesuaikan jika perlu:
   - `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD` (default `minioadmin`).
   - `MINIO_REGION` (mis. `us-east-1`).
   - `MINIO_BUCKET` (default `demo-bucket`).
   - `DJANGO_SECRET_KEY` (isi nilai acak Anda).
   - `PRESIGN_TTL` (detik, default `300`).

## Menjalankan
```bash
docker compose up -d --build
```
- Buka aplikasi: `http://localhost:8000`.
- Buka MINIO Console: `http://localhost:9001` (login dengan kredensial di `.env`).

Kontainer `mc-init` akan:
- Membuat bucket `MINIO_BUCKET` bila belum ada;
- Mengaktifkan versioning pada bucket;
- Menambahkan notifikasi event (webhook) ke `django-app`.

## Fitur Aplikasi
- Upload server-side: unggah file via form; file disimpan ke MINIO menggunakan SDK.
- Listing objek: tampilkan nama, ukuran, waktu modifikasi, aksi hapus dan unduh.
- Presigned GET: generate link unduh sementara (TTL dikontrol `PRESIGN_TTL`).
- Versioning: lihat daftar versi sebuah objek dan lakukan restore ke versi tertentu.
- Event Log: menerima webhook event `put/remove` dari bucket dan menampilkannya di UI.

## Endpoint Penting
- `GET /` — Halaman upload.
- `POST /upload` — Unggah file ke MINIO.
- `GET /list` — Daftar objek pada bucket.
- `GET /presign/<key>` — Mendapatkan presigned GET URL.
- `GET /delete/<key>` — Menghapus objek (latest versi).
- `GET /versions/<key>` — Melihat daftar versi objek.
- `GET /restore/<key>/<version_id>` — Restore versi ke latest.
- `POST /events/webhook` — Endpoint webhook MINIO.
- `GET /events` — Melihat daftar event yang diterima.

## Skenario Demo yang Disarankan
1. Upload file kecil dan besar (≥128MB) untuk mengamati performa.
2. Unduh menggunakan presigned URL; uji kedaluwarsa setelah TTL berhenti.
3. Unggah ulang file beberapa kali, lihat daftar versi, dan coba restore versi sebelumnya.
4. Buka halaman Event Log, lalu lakukan upload/hapus untuk melihat notifikasi.
5. Simulasi toleransi kegagalan: hentikan satu node MINIO dan uji operasi dari aplikasi.
   ```bash
   docker compose stop minio2
   docker compose start minio2
   ```

## Opsi Presigned Upload (Client-side)
Default demo memakai upload server-side sehingga tidak memerlukan CORS. Jika ingin upload langsung dari browser menggunakan presigned PUT:
- Aktifkan CORS pada bucket melalui `mc`.
- Tambahkan view untuk presigned PUT dan form JavaScript di Django.

## Troubleshooting
- MINIO belum siap: tunggu beberapa detik; `mc-init` akan retry alias dan inisialisasi.
- Bucket tidak ditemukan: aplikasi akan memastikan bucket dibuat pada akses pertama upload/list.
- Port konflik: ubah pemetaan port di `docker-compose.yml` atau nilai di `.env`.

## Struktur Proyek
```
├─ docker-compose.yml
├─ .env.example
├─ apps/
│  └─ django-app/
│     ├─ Dockerfile
│     ├─ manage.py
│     ├─ demo_minio/
│     │  ├─ settings.py
│     │  ├─ urls.py
│     │  └─ wsgi.py
│     ├─ storage/
│     │  ├─ models.py
│     │  ├─ service.py
│     │  ├─ views.py
│     │  └─ urls.py
│     ├─ templates/
│     │  ├─ base.html
│     │  ├─ upload.html
│     │  ├─ list.html
│     │  ├─ versions.html
│     │  └─ events.html
│     └─ requirements.txt
└─ README.md
```

## Lisensi
Demo ini ditujukan untuk pembelajaran akademik. Silakan gunakan dan modifikasi sesuai kebutuhan perkuliahan.
