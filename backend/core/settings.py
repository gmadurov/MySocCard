"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from mollie.api.client import Client
from .utils.utils import init_DB

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
# set to false before uploading
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get("DEBUG") == "True" else False
LOCAL = False if os.environ.get("LOCAL") == "False" else True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["localhost", "mamon.esrtheta.nl", "10.0.2.2", ".esrtheta.nl", "host.docker.internal"]

JWT_KEY = os.environ.get("JWT_KEY")

# Application definition

INSTALLED_APPS = [
    ######### self added
    "admin_interface",
    "rest_framework_simplejwt.token_blacklist",
    "purchase.apps.PurchaseConfig",
    "rest_framework_simplejwt",
    "users.apps.UsersConfig",
    "client.apps.ClientConfig",
    "rest_framework",
    "corsheaders",
    "colorfield",
    "storages",
    "django_seed",
    "simple_history",
    ########## default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #### self added
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]
from api.authentication import CORS_ALLOW_ALL_ORIGINS, REST_FRAMEWORK, SIMPLE_JWT, JWT_KEY

JWT_KEY = JWT_KEY

# CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = CORS_ALLOW_ALL_ORIGINS
REST_FRAMEWORK = REST_FRAMEWORK
SIMPLE_JWT = SIMPLE_JWT

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
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
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # new


WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# if LOCAL:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }
#     # start
# else:

# print(os.environ.get("DATABASE_URL", "\n\n\n\n\n\n\n\n\n\\n\n\n\n\n\n\n\nn\n\n"))
# try:
#     DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("POSTGRES_NAME"),
#         "USER": os.environ.get("POSTGRES_USER"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#         "HOST": "postgres",
#         "PORT": 5432,
#     }
# }
# except:
host, port, name, user, password = init_DB(os.environ.get("DATABASE_URL"))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": name,
        "USER": user,
        "PASSWORD": password,
        "HOST": host,
        "PORT": port,
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGES = [("en", "us"), ("nl", "nl")]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_URL = "/static/"
# start
MEDIA_URL = "/mediafiles/"
# STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "mediafiles"
STATIC_ROOT = BASE_DIR / "staticfiles"
### end


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ADMINS = [
    ("Gustavo Maduro", "dev.gam.vollmer@gmail.com"),
    ("webmaster", "webmaster@esrtheta.nl"),
]
MANAGERS = [
    ("Gustavo Maduro", "dev.gam.vollmer@gmail.com"),
    ("webmaster", "webmaster@esrtheta.nl"),
]
# SECURE_SSL_REDIRECT = True
CSRF_TRUSTED_ORIGINS = ["https://*.esrtheta.nl", "http://localhost:8000"]


MOLLIE_API_KEY = os.environ.get("MOLLIE_API_KEY")
MOLLIE_PARTNER_ID = os.environ.get("MOLLIE_PARTNER_ID")
MOLLIE_PROFILE_ID = os.environ.get("MOLLIE_PROFILE_ID")
try:
    mollie_client = Client()
    mollie_client.set_api_key(MOLLIE_API_KEY)
except:
    print("mollie not available")
