import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "storage",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "demo_minio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]

WSGI_APPLICATION = "demo_minio.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio1:9000")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minioadmin")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "demo-bucket")
MINIO_REGION = os.getenv("MINIO_REGION", "us-east-1")
PRESIGN_TTL = int(os.getenv("PRESIGN_TTL", "300"))
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
