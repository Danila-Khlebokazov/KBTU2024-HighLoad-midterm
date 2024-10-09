# CORE -------------------------
from pathlib import Path

import environ

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env.str("SECRET_KEY", "secret")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["*"])
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", False)
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

USE_X_FORWARDED_HOST = True

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

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

AUTH_USER_MODEL = "authentication.User"

# MIDDLEWARE -------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# APPS -------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # three-party
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "debug_toolbar",
    # local
    "apps.core",
    "apps.authentication",
]

# STATIC AND DATA -------------------------
STATIC_URL = "static/"
STATIC_ROOT = "/app/var/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("POSTGRES_DB", "midka"),
        "HOST": env.str("POSTGRES_HOST", "localhost"),
        "PORT": env.str("POSTGRES_PORT", "5432"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
    },
    "readonly": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("POSTGRES_DB", "midka"),
        "HOST": env.str("POSTGRES_HOST_2", "localhost"),
        "PORT": env.str("POSTGRES_PORT", "5432"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
    },
}

DATABASE_ROUTERS = ['config.db_utils.CustomDatabaseRouter']

# CACHE AND SESSION
# -----------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    }
}

SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 1209600

# REST FRAMEWORK
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "exceptions.core_exception_handler",
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": ("apps.authentication.backends.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# SPECTACULAR_SETTINGS
# -----------------------------------------------------------------------------
SITE_URL = env.str("SITE_URL", "http://localhost")

SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "TITLE": "E-commerce service API",
    "DESCRIPTION": "E-commerce service",
    "SERVERS": [{"url": SITE_URL}],
    "SWAGGER_UI_SETTINGS": {
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 4,
        "filter": True,
        "persistAuthorization": True,
    },
}

# NOTIFICATION CENTER SETTINGS
# -----------------------------------------------------------------------------
NOTIFICATION_CENTER_RABBITMQ = env.str(
    "NOTIFICATION_CENTER_RABBITMQ", "amqp://guest:guest@localhost:5672/"
)

# DEBUG TOOLBAR SETTINGS
# -----------------------------------------------------------------------------
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda _: True,
}
