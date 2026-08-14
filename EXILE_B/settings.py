import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ENVIRONMENT
# ============================================================

env = environ.Env(
    DEBUG=(bool, False)
)

# Local : lecture du fichier .env
# Render : utilise directement les variables d'environnement
environ.Env.read_env(str(BASE_DIR / ".env"))


# ============================================================
# CORE SETTINGS
# ============================================================

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1"]
)


# ============================================================
# SUPABASE
# ============================================================

SUPABASE_URL = env("SUPABASE_URL", default="")

SUPABASE_KEY = env("SUPABASE_KEY", default="")


# ============================================================
# DATABASE
# ============================================================
#
# DATABASE_URL doit maintenant pointer vers
# Supabase PostgreSQL.
#
# Exemple :
#
# DATABASE_URL=postgresql://postgres.xxxxx:mot_de_passe@....pooler.supabase.com:5432/postgres
#
# Django utilise automatiquement PostgreSQL si DATABASE_URL
# est présente.
#

DATABASES = {
    "default": env.db("DATABASE_URL")
}


# ============================================================
# CORS
# ============================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://exile-backend-9q6o.onrender.com",
    "https://exoe.netlify.app",
    "https://exoe.vercel.app",
    "https://exoe-neat4e0ph-exile-team1.vercel.app",
    "https://exoe-grznqf1hw-exile-team1.vercel.app",
    "https://exoe-9vi19nbq0-exile-team1.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True


# ============================================================
# AUTHENTICATION
# ============================================================

AUTH_USER_MODEL = "users.CustomUser"


# ============================================================
# INSTALLED APPS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",

    "users",
    "API",
    "accueil",
    "demande",
    "evenement",
    "abonnement",
    "profil",
    "activities",
    "badges",

    "drf_spectacular",
    "drf_spectacular_sidecar",

    "corsheaders",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",
}


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# STATIC & MEDIA
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# ============================================================
# URL / WSGI
# ============================================================

ROOT_URLCONF = "EXILE_B.urls"

WSGI_APPLICATION = "EXILE_B.wsgi.application"


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",

        "OPTIONS": {
            "min_length": 8
        },
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"