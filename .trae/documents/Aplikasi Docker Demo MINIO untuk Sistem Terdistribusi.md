## Tujuan
- Menyediakan aplikasi web monolith (Django) untuk demonstrasi object storage MINIO: upload/download, listing, versioning, presigned URL, dan event log.
- Memperlihatkan konsep sistem terdistribusi: erasure coding, kuorum, dan toleransi kegagalan dengan cluster MINIO 4 node.

## Arsitektur
- Cluster MINIO: 4 kontainer `minio1..minio4` (distributed mode) dengan volume persistensi per node.
- Aplikasi `django-app`: monolith yang menyajikan HTML (template Django) dan mengakses MINIO via SDK Python.
- Utilitas `mc-init`: sekali jalan untuk membuat bucket, mengaktifkan versioning, dan (opsional) set CORS.
- MINIO Console (web) pada `http://localhost:9001` untuk administrasi.

## Fitur Aplikasi Django
- Upload
  - Default: server-side upload (file diunggah ke Django lalu ke MINIO via SDK) — sederhana, tanpa CORS.
  - Opsional: presigned upload (Django membuat URL PUT bertanda waktu, browser unggah langsung ke MINIO) — lebih efisien; butuh CORS.
- Listing & Aksi
  - Daftar objek: nama, ukuran, waktu modifikasi; aksi unduh, hapus.
  - Detail objek: preview untuk tipe umum (gambar) via presigned GET.
- Versioning
  - Bucket versioning aktif; tampilkan daftar versi per objek.
  - Aksi restore ke versi tertentu (menjadikan versi terpilih sebagai latest).
- Share Link
  - Generate presigned GET dengan TTL singkat (mis. 300 detik) untuk berbagi akses sementara.
- Event Log
  - Notifikasi bucket MINIO dikirim ke endpoint Django (webhook).
  - Tampilkan log event `put`/`remove` di halaman admin aplikasi.
- Status Cluster (opsional)
  - Panel sederhana yang mengeksekusi operasi kecil untuk memeriksa ketersediaan dan menampilkan indikasi kesehatan.

## Komponen & Konfigurasi
- `docker-compose.yml`
  - Layanan: `minio1..4`, `django-app`, `mc-init`.
  - Port: `9000` (S3 API), `9001` (Console), `8000` (Django).
  - Volume: `minio1-data..minio4-data` untuk persistensi.
  - Healthcheck untuk menunggu MINIO siap sebelum `mc-init` dan `django-app` berjalan.
- `.env.example`
  - `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`, `MINIO_ENDPOINT`, `MINIO_REGION`, `MINIO_BUCKET`, `DJANGO_SECRET_KEY`, `PRESIGN_TTL`.
- Django
  - Dependency: `minio` (SDK resmi), `Django`, `gunicorn` (opsional), `python-dotenv`.
  - Struktur: app `storage` dengan service wrapper MINIO, views, templates, urls.
  - Model sederhana: `EventLog` untuk menyimpan webhook event; DB `sqlite` cukup.

## Rencana Implementasi
- Fase 1: Susun `docker-compose.yml` untuk cluster MINIO (4 node) + volume + healthcheck; tambahkan `mc-init`.
- Fase 2: Buat kerangka `django-app` (settings, urls, templates dasar, service MINIO) dan integrasi server-side upload/download/listing.
- Fase 3: Tambah fitur versioning (list versi, restore), presigned GET (share link), dan halaman event log (webhook endpoint + tampilan).
- Fase 4 (opsional): Aktifkan presigned upload + konfigurasi CORS di MINIO via `mc-init`.
- Fase 5: Buat skrip `scripts/init.ps1` dan `scripts/demo.ps1` untuk skenario demo dan simulasi kegagalan (stop satu node).
- Fase 6: Validasi end-to-end dan penyempurnaan UI (Bootstrap/Tailwind sederhana).

## Skenario Demo
- Upload file besar (≥128MB) dan observasi performa.
- Generate presigned link dan uji kedaluwarsa di incognito.
- Tampilkan daftar versi; lakukan restore ke versi tertentu.
- Lihat event log saat upload/hapus.
- Toleransi kegagalan: hentikan satu kontainer `minio` dan uji baca/tulis; kemudian hentikan dua untuk menunjukkan batas kuorum.

## Cara Menjalankan (Windows)
- Salin `.env.example` menjadi `.env` dan isi nilai.
- Jalankan `docker compose up -d`.
- Buka Django: `http://localhost:8000`.
- Buka MINIO Console: `http://localhost:9001`.
- Jalankan `scripts/init.ps1` untuk inisialisasi bucket/versioning; gunakan `scripts/demo.ps1` untuk skenario otomatis.

## Validasi & Pengujian
- Cek integritas: upload → download → verifikasi checksum.
- Uji TTL presigned: akses link setelah kedaluwarsa untuk pastikan tidak valid.
- Uji konkurensi: beberapa upload paralel; observasi latensi.
- Uji kegagalan node: stop `minio2`; pastikan operasi tetap berjalan; dokumentasikan perilaku saat dua node stop.

## Keamanan
- Jangan menyimpan kredensial di repo; gunakan env.
- TTL presigned pendek; batasi ukuran file untuk demonstrasi.
- Nonaktifkan listing publik; semua operasi melalui Django.

## Next Step
- Jika rencana ini sesuai, saya akan mulai implementasi Fase 1–3 menggunakan Django monolith dan menyiapkan skrip inisialisasi. Anda bisa memilih apakah presigned upload diaktifkan atau tetap server-side saja untuk kesederhanaan.