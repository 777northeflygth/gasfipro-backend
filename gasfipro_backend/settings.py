"""
Django settings for gasfipro_backend project.
"""

from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# ✅ SEGURIDAD (Variables de Entorno para Azure)
# ============================================================
# En Azure, estas variables se configuran en "Configuración > Variables de entorno"
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-for-dev')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Permite el dominio de Azure, localhost, etc.
# En Azure configura ALLOWED_HOSTS="gasfipro-api.azurewebsites.net,localhost,127.0.0.1"
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# Azure necesita esto para que el panel de admin y los formularios funcionen bajo HTTPS
CSRF_TRUSTED_ORIGINS = [
    'https://*.azurewebsites.net',
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # allauth + dj-rest-auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    # Local
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ✅ Añadido para servir estáticos en Azure (opcional)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'gasfipro_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'gasfipro_backend.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ============================================================
# ✅ ARCHIVOS ESTÁTICOS Y MEDIA
# ============================================================
STATIC_URL = 'static/'
# ✅ Azure necesita saber dónde guardar los estáticos para el admin
STATIC_ROOT = BASE_DIR / 'staticfiles' 

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================================
# ✅ CORS (Para que el frontend en Azure pueda hacer peticiones)
# ============================================================
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() == 'true'
# Si usas CORS_ALLOW_ALL_ORIGINS=False en Azure, debes agregar el dominio de tu frontend:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://gasfipro-bvaageg3aydngqge.chilecentral-01.azurewebsites.net", # URL de tu frontend en Azure
]

# Límite de archivos
DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024

# ============================================================
# ✅ CONFIGURACIÓN DE DJANGO-ALLAUTH Y GOOGLE
# ============================================================
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_ADAPTER = 'api.adapters.CustomSocialAccountAdapter'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'https://www.googleapis.com/auth/calendar',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
            'prompt': 'consent',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APPS': [
            {
                # ✅ CORREGIDO: Eliminamos las claves reales por seguridad
                'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
                'secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
                'key': '',
            },
        ],
    }
}

ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_STORE_TOKENS = True

# ============================================================
# ✅ DJANGO REST FRAMEWORK Y JWT
# ============================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': None,
    'JWT_AUTH_REFRESH_COOKIE': None,
    'USER_DETAILS_SERIALIZER': 'dj_rest_auth.serializers.UserDetailsSerializer',
    'SESSION_LOGIN': False,
    'TOKEN_MODEL': None,
}

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
