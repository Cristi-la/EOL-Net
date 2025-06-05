import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-q)5s(qmbut89m0zvk(6s)+^3_f!cl24a#$$362=g9ju$0bh!+u'

DEBUG = True

if DEBUG:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage", # Use this for development
            # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage", # Uncomment for production
        },
    }

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    'import_export',

    # EOL-Net apps
    'apps.eol',
    'apps.api',
]

API_THROTTLE_RATES = {
    "anon": "10/min",
    "default": "100/min",
    "ha": "1000/min",
}
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        "apps.api.permissions.TokenPermission",
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": (
        "apps.api.throttles.DynamicScopeRateThrottle",
    ),

    "DEFAULT_THROTTLE_RATES": API_THROTTLE_RATES,
    "DEFAULT_PAGINATION_CLASS": "apps.api.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 1000,
}


SIMPLE_JWT = {
    # Make JWT valid for 1 year:
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    # We’ll use our token_key claim to look up DB metadata if needed.
    "USER_ID_CLAIM": "user_id",  
    "USER_ID_FIELD": "id",
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'EOL-Net API',
    "DESCRIPTION": "API for managing Vendors, Products, and Software lifecycles (EOL/EOS).",   
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,

    # "SECURITY_SCHEMAS": [
    #     {
    #         'type': 'http',
    #         'scheme': 'header',
    #         'name': 'Authorization',
    #         'description': 'JWT token for authentication. Format: `Bearer <token>`',
    #     },
    # ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True



STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


