# Flask Monolithic Starter Kit

Boilerplate aplikasi web monolitik dengan Flask, SQLite, Bootstrap 5, dan Alpine.js.

## Spesifikasi

| Komponen | Teknologi |
|----------|-----------|
| Backend Framework | Flask 3.0+ |
| Database | SQLite + Flask-SQLAlchemy |
| Migrasi | Flask-Migrate |
| Dependency Manager | Poetry |
| Environment | python-dotenv |
| Frontend CSS | Bootstrap 5 (CDN) |
| Frontend JS | Alpine.js (CDN) |

## Struktur File

```
.
├── .env              # Konfigurasi environment
├── app.py            # Aplikasi Flask utama
├── models.py         # Definisi model database
├── seeds.py          # CLI command untuk seeder
├── pyproject.toml    # Konfigurasi Poetry
└── templates/
    └── index.html   # Template HTML
```

## Instalasi

### 1. Install Dependencies

```bash
poetry install
```

### 2. Aktivasi Virtual Environment

```bash
poetry shell
```

## Konfigurasi Database

### 3. Inisialisasi Folder Migrasi

```bash
flask db init
```

### 4. Buat File Migrasi

```bash
flask db migrate -m "Initial migration"
```

### 5. Eksekusi Migrasi ke Database

```bash
flask db upgrade
```

## Pengisian Data Awal

### 6. Jalankan Seeder

```bash
flask seed-db
```

Command ini akan menambahkan 3 user dummy ke tabel `users`:
- johndoe (john@example.com)
- janedoe (jane@example.com)
- bobsmith (bob@example.com)

## Menjalankan Server

### 7. Jalankan Aplikasi

```bash
flask run
```

Server akan berjalan di `http://localhost:5000`

## Endpoint API

### GET /api/users

Mengembalikan semua user dalam format JSON.

**Response:**
```json
[
  {"id": 1, "username": "johndoe", "email": "john@example.com"},
  {"id": 2, "username": "janedoe", "email": "jane@example.com"},
  {"id": 3, "username": "bobsmith", "email": "bob@example.com"}
]
```

## Konfigurasi Environment (.env)

```bash
FLASK_APP=app.py
FLASK_DEBUG=1
DATABASE_URL=sqlite:///app.db
```

- `FLASK_APP`: Nama file aplikasi Flask
- `FLASK_DEBUG`: 1 untuk development, 0 untuk production
- `DATABASE_URL`: URL koneksi database SQLite

## Perintah CLI Tersedia

| Perintah | Deskripsi |
|---------|-----------|
| `flask db init` | Inisialisasi folder migrasi |
| `flask db migrate` | Buat file migrasi |
| `flask db upgrade` | Eksekusi migrasi ke database |
| `flask db downgrade` | Rollback migrasi terakhir |
| `flask seed-db` | Isi database dengan data dummy |
| `flask run` | Jalankan server Flask |

## Troubleshooting

### ERROR: ModuleNotFoundError: No module named 'flask'

Pastikan virtual environment sudah diaktifkan:

```bash
poetry shell
```

### ERROR: No application found

Pastikan `FLASK_APP` sudah diset di file `.env`:

```bash
FLASK_APP=app.py
```

### ERROR: table users already exists

Hapus file database dan buat ulang:

```bash
rm app.db
flask db migrate -m "Recreate"
flask db upgrade
flask seed-db
```

## Fitur

- MVC Architecture dengan Flask
- RESTful API endpoint
- Database migration dengan Flask-Migrate
- CLI custom command untuk seeder
- Responsive UI dengan Bootstrap 5
- Dynamic data fetching dengan Alpine.js (tanpa reload halaman)
- Konfigurasi environment dengan .env

## Lisensi

MIT License