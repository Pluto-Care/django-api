from pathlib import Path
from decouple import config
from django.core.mail import get_connection

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_BASE_DIR = BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    'SECRET_KEY', default='django-insecure$&!9x6t7m7q2^q1l7c@z5@2!&1!v1c7zq^r#_b2z9#q^w3q9z')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# Custom Settings

FORGET_PASSWORD_LINK_TIMEOUT = 30  # minutes

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'logs',

    'users',
    'users.users_sessions',
    'users.users_totp',
    'users.users_forgot_password',
    'users.users_app_tokens',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "core.middlewares.APIRequestFormatMiddleware",
    "users.users_app_tokens.middlewares.AppTokenMiddleware",
    "core.middlewares.RequestOriginMiddleware",
    "users.users_sessions.middlewares.SessionMiddleware",
    "logs.middlewares.APILogMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# DRF

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.error_handling.drf_exception.drf_exception_handler',
}

# Security

CORS_ALLOWED_ORIGINS = [config('FRONTEND_URL')]
CSRF_TRUSTED_ORIGINS = [config('FRONTEND_URL')]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

# Set the origins that API will respond to.
# To set all origins, use value ['*']
ALLOW_ORIGINS = [config('FRONTEND_URL')]


# Database
def get_database():
    if config('DB_HOST', default=None) is None or config('DB_HOST', default=None) == '':
        Path(str(PROJECT_BASE_DIR) +
             "/db").mkdir(parents=True, exist_ok=True)
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': PROJECT_BASE_DIR / 'db' / 'db.sqlite3',
            }
        }
    else:
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME'),
                'USER': config('DB_USERNAME'),
                'PASSWORD': config('DB_PASSWORD'),
                'HOST': config('DB_HOST'),
                'PORT': config('DB_PORT'),
            }
        }


# If no database is provided, use sqlite3
DATABASES = {
    'logs_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_BASE_DIR / 'db' / 'logs.sqlite3',
    },
    **get_database()
}

DATABASE_ROUTERS = ["core.database_router.DatabaseRouter"]

# Email
# https://docs.djangoproject.com/en/5.0/topics/email/

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


def getEmailConnection():
    if config('SMTP_USE_TLS') == 'True':
        return get_connection(
            host=config('SMTP_HOST'),
            port=config('SMTP_PORT'),
            username=config('SMTP_USER'),
            password=config('SMTP_PASSWORD'),
            use_tls=True,
        )
    else:
        return get_connection(
            host=config('SMTP_HOST'),
            port=config('SMTP_PORT'),
            username=config('SMTP_USER'),
            password=config('SMTP_PASSWORD'),
            use_ssl=True,
        )


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
