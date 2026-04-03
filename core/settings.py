import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# ----------------------------
# BASE DIRECTORIES
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------------
# ENVIRONMENT
# ----------------------------
def load_env():
    env_dev = BASE_DIR / ".env.dev"
    env_prod = BASE_DIR / ".env.prod"

    if env_dev.exists():
        print("--- Loading Environment: DEV ---")
        load_dotenv(env_dev)
    elif env_prod.exists():
        print("--- Loading Environment: PROD ---")
        load_dotenv(env_prod)
    else:
        print("--- No .env files found. Using System Environment Variables ---")


load_env()

SECRET_KEY = os.getenv("PROJECT_KEY")

IS_PROD = os.getenv("IS_PROD", "False").lower() == "true"

DEBUG = not IS_PROD


# ----------------------------
# SECURITY
# ----------------------------
SECRET_KEY = os.getenv("PROJECT_KEY")


# ----------------------------
# CRSF
# ----------------------------
csrf_env = os.getenv("CSRF_TRUSTED_ORIGINS")

if IS_PROD:

    CSRF_TRUSTED_ORIGINS = [url.strip() for url in csrf_env.split(",") if url.strip()]
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    CORS_ALLOW_ALL_ORIGINS = True


# ----------------------------
# ALLOWED_HOST
# ----------------------------
allowed_host_env = os.getenv("ALLOWED_HOSTS")

if IS_PROD:
    ALLOWED_HOSTS = [url.strip() for url in allowed_host_env.split(",") if url.strip()]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


# ----------------------------
# CORS
# ----------------------------
cors_env = os.getenv("CORS_URLS")

if IS_PROD:
    CORS_ALLOWED_ORIGINS = [url.strip() for url in cors_env.split(",") if url.strip()]
else:
    CORS_ALLOW_ALL_ORIGINS = True

# ----------------------------
# INSTALLED APPS
# ----------------------------
INSTALLED_APPS = [
    "django.contrib.gis",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "core",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------
# URLS & TEMPLATES
# ----------------------------
ROOT_URLCONF = "core.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# ----------------------------
# DATABASE
# ----------------------------
if IS_PROD:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
            "CONN_MAX_AGE": 600,
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }


# ----------------------------
# PASSWORD VALIDATION
# ----------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ----------------------------
# INTERNATIONALIZATION
# ----------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ----------------------------
# STATIC & MEDIA
# ----------------------------
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

if IS_PROD:
    # AWS / Backblaze B2
    AWS_ACCESS_KEY_ID = os.getenv("B2_APP_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("B2_APP_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")
    AWS_S3_REGION_NAME = "us-east-005"
    AWS_S3_ENDPOINT_URL = f"https://s3.{AWS_S3_REGION_NAME}.backblazeb2.com"

    # Update these URLs
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/"
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/static/"

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "querystring_auth": False,
                "default_acl": "public-read",
                "file_overwrite": True,
                "location": "media",
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "querystring_auth": False,
                "default_acl": "public-read",
                "file_overwrite": True,
                "location": "static",
            },
        },
    }

else:
    # Local filesystem
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------
# EMAIL
# ----------------------------
WEBSITE_EMAIL = os.getenv("WEBSITE_EMAIL")
DEFAULT_FROM_EMAIL = (
    f"Infralens (TopMapSolutions) Customer Support <no-reply@{WEBSITE_EMAIL}>"
)

if IS_PROD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("BREVO_HOST")
    EMAIL_PORT = int(os.getenv("BREVO_PORT", 587))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv("BREVO_SMTP_LOGIN")
    EMAIL_HOST_PASSWORD = os.getenv("BREVO_SMTP_PASSWORD")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# -----------------------------
# DJANGO REST FRAMEWORK API
# ------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "100/minute",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ----------------------------
# LOGGING
# ----------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
