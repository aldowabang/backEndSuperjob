# SuperJob API

Backend API untuk platform lowongan kerja sekelas Glints, dibangun menggunakan **FastAPI** + **PostgreSQL** + **SQLAlchemy**.

> Referensi Video: [https://www.youtube.com/watch?v=6H5gQXzN6vQ](https://www.youtube.com/watch?v=6H5gQXzN6vQ)

---

## Struktur Project

```
superjob-api/
├── app/
│   ├── main.py              # Inisialisasi FastAPI & menyatukan semua router
│   ├── database.py          # SessionLocal, Base Model, & get_db dependency
│   ├── core/
│   │   └── security.py      # JWT, Password Hashing (Bcrypt), OAuth2 scheme
│   ├── models/              # Tabel SQLAlchemy (ORM)
│   │   ├── __init__.py      # Import semua model agar Base mengenali tabelnya
│   │   ├── user.py          # User & Profile (One-to-One)
│   │   ├── company.py       # Company (One-to-One dengan User/Employer)
│   │   ├── job.py           # Job & Pivot tabel job_skills (Many-to-Many)
│   │   ├── application.py   # Application & ApplicationHistory
│   │   ├── master.py        # City, Skill, JobType, WorkModel
│   │   └── notification.py  # Notification
│   ├── schemas/             # Pydantic models (Validasi Request & Response)
│   │   ├── auth_schema.py   # Login & Token schema
│   │   ├── user_schema.py   # Register, Profile, Company schema
│   │   └── job_schema.py    # Job create & response schema
│   ├── crud/                # Logika Query Database
│   │   ├── user_crud.py     # CRUD User, Profile, Company
│   │   └── job_crud.py      # CRUD Job & Skills
│   └── api/
│       └── v1/
│           ├── api.py       # Router utama yang menggabungkan semua endpoint
│           └── endpoints/
│               ├── auth.py  # Register & Login
│               ├── users.py # Setup Company Profile
│               └── jobs.py  # Post & List Jobs
├── .env                     # Environment variables (DATABASE_URL, SECRET_KEY)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Daftar Endpoint API

### Base URL: `/api/v1`

| Method | Endpoint               | Deskripsi                          | Auth       |
|--------|------------------------|------------------------------------|------------|
| GET    | `/`                    | Welcome message & status           | ❌ Tidak   |
| POST   | `/api/v1/auth/register`| Registrasi user baru               | ❌ Tidak   |
| POST   | `/api/v1/auth/login`   | Login (OAuth2, return JWT token)   | ❌ Tidak   |
| POST   | `/api/v1/users/company`| Setup profil perusahaan (Employer) | ✅ Bearer  |
| POST   | `/api/v1/jobs/`        | Post lowongan kerja baru           | ✅ Bearer  |
| GET    | `/api/v1/jobs/`        | Lihat semua lowongan aktif         | ❌ Tidak   |

### Detail Endpoint:

#### 1. `POST /api/v1/auth/register`
- Request Body: `{ email, password (min 8 char), role: "seeker"/"employer" }`
- Otomatis membuat profil kosong dengan nama dari email
- Response: data user (id, email, role, created_at)

#### 2. `POST /api/v1/auth/login`
- Menggunakan OAuth2 Password Flow (`username` diisi email)
- Response: `{ access_token, token_type: "bearer" }`
- Token berlaku 24 jam (HS256 JWT)

#### 3. `POST /api/v1/users/company`
- **Hanya Employer** yang bisa membuat profil perusahaan
- Request: `{ name, description?, city_id, logo_url? }`
- Setiap employer hanya bisa punya 1 perusahaan (One-to-One)

#### 4. `POST /api/v1/jobs/`
- **Hanya Employer** dengan perusahaan terdaftar yang bisa posting
- Request: `{ title, description, salary_min?, salary_max?, city_id, job_type_id, work_model_id, skill_ids[] }`

#### 5. `GET /api/v1/jobs/`
- Menampilkan semua lowongan dengan `is_open = True`
- Termasuk data relasi (company, city, job_type, work_model, skills)

---

## Model Database (10 Tabel)

| No | Tabel                  | Deskripsi                                    |
|----|------------------------|----------------------------------------------|
| 1  | `users`                | Data user (email, password hash, role)       |
| 2  | `profiles`             | Profil user (nama, phone, bio, CV URL)       |
| 3  | `companies`            | Profil perusahaan employer                   |
| 4  | `jobs`                 | Lowongan kerja                               |
| 5  | `job_skills`           | Pivot table Many-to-Many (Job ↔ Skill)       |
| 6  | `applications`         | Lamaran kerja (user melamar ke job)          |
| 7  | `application_histories`| Riwayat perubahan status lamaran             |
| 8  | `cities`               | Master data kota                             |
| 9  | `skills`               | Master data skill/keahlian                   |
| 10 | `job_types`            | Master data tipe kerja (Full-time, Part-time)|
| 11 | `work_models`          | Master data model kerja (Remote, On-site)    |
| 12 | `notifications`        | Notifikasi untuk user                        |

---

## Cara Menjalankan

```bash
# 1. Clone project
git clone <repository-url>
cd superJobApi

# 2. Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database PostgreSQL
# Pastikan PostgreSQL berjalan dan buat database:
# CREATE DATABASE superjobdb;

# 5. Buat file .env
# DATABASE_URL=postgresql://user:password@localhost:5432/superjobdb
# SECRET_KEY=your-secret-key
# ALGORITHM=HS256

# 6. Jalankan server
uvicorn app.main:app --reload

# 7. Akses API docs
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

---

## Catatan Refleksi — Eksplorasi IDE & AI Coding

Berikut catatan refleksi setelah menggunakan AI coding tools untuk membangun project SuperJob API ini:

### 1. Fitur AI yang Paling Membantu
- **Scaffold endpoint otomatis** — AI sangat cepat dalam membuat boilerplate FastAPI: router, schema, CRUD, dan model sekaligus. Yang biasanya memakan waktu 1-2 jam bisa selesai dalam hitungan menit.
- **Penjelasan logika kode** — AI membantu menjelaskan konsep seperti OAuth2 Password Flow, JWT token, dan relationship SQLAlchemy (One-to-One, Many-to-Many) dengan bahasa yang mudah dipahami.
- **Auto-complete dan suggestions** — IDE + AI mempercepat penulisan kode repetitif seperti schema Pydantic dan CRUD functions.

### 2. Bagian yang TIDAK Bisa Diserahkan ke AI
- **Desain arsitektur database** — Keputusan seperti "apakah user-company itu One-to-One atau One-to-Many" harus dipahami sendiri berdasarkan business logic.
- **Validasi business rules** — AI bisa membuat kode yang berjalan, tapi belum tentu sesuai kebutuhan bisnis. Contoh: AI mungkin lupa bahwa employer harus punya company sebelum posting job.
- **Keamanan dan error handling** — AI kadang menggunakan default yang tidak aman (seperti `SECRET_KEY` hardcoded). Developer harus review dan pastikan semua variabel sensitif di `.env`.

### 3. Risiko jika Hasil AI Langsung Dipakai Tanpa Review
- **Bug tersembunyi** — Contoh nyata: AI lupa import `CompanyCreate` di `user_crud.py`, yang menyebabkan `NameError` saat runtime. Kode terlihat benar di mata, tapi error saat dijalankan.
- **Schema tidak lengkap** — `CompanyResponse` awalnya hanya mengembalikan `user_id`, padahal client butuh data lengkap (name, description, dll). Ini bisa menyebabkan frontend tidak berfungsi.
- **Keamanan terancam** — Jika tidak di-review, API key, database credentials, atau secret key bisa ikut ter-commit ke repository publik.
- **Asumsi keliru** — AI mengasumsikan tabel master (cities, skills, job_types, work_models) sudah terisi data, padahal belum ada seeder atau endpoint untuk mengisinya.
- **Kode yang "bekerja" belum tentu "benar"** — Kode hasil AI perlu diverifikasi apakah sesuai dengan requirement spesifik project, bukan hanya apakah bisa jalan tanpa error.

---

## Teknologi yang Digunakan

| Teknologi      | Fungsi                              |
|----------------|-------------------------------------|
| FastAPI        | Web framework (async, auto-docs)    |
| SQLAlchemy     | ORM untuk database PostgreSQL       |
| PostgreSQL     | Database relasional                 |
| Pydantic       | Validasi data request/response      |
| Bcrypt         | Hashing password                    |
| python-jose    | JWT (JSON Web Token) authentication |
| Uvicorn        | ASGI server                         |


