from fastapi import FastAPI
from app.database import engine, Base
# Kita perlu import semua models agar Base.metadata.create_all mengenali tabel-tabelnya
from app.models import user, master, company, job, application, notification
from app.api.v1.api import api_router

# Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title="SuperJob API",
    description="Backend API untuk platform lowongan kerja sekelas Glints",
    version="1.0.0"
)

# Perintah untuk membuat tabel di database secara otomatis (Jika belum ada)
# Catatan: Di produksi, kita akan menggunakan Alembic untuk ini.
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Welcome to SuperJob API",
        "docs": "/docs",
        "status": "Active"
    }

app.include_router(api_router, prefix="/api/v1")