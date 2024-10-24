import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_DIR = str(Path(os.path.join(BASE_DIR, ".env")))

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DEBUG_TOOLBAR=(bool, False),
    EMKOPO_UAT=(bool, False),
    EMKOPO_SIT=(bool, True),
    EMKOPO_PROD=(bool, False),
    DATABASE_SQLITE_ENABLED=(bool, False),
    SMTP_PORT=(int, 25),
    EMKOPO_BOOTSTRAP=(int, 4),
    EMKOPO_PAGINATION=(int, 20)
)

environ.Env.read_env(ENV_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEVELOPER = env.str("DEVELOPER")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")
DEBUG_TOOLBAR = env("DEBUG_TOOLBAR")
DATABASE_SQLITE_ENABLED = env("DATABASE_SQLITE_ENABLED")
APP_NAME = env.str("DJANGO_APP_NAME")
SMTP_PORT = env("SMTP_PORT")

EMKOPO_SIT = env("EMKOPO_SIT")
EMKOPO_UAT = env("EMKOPO_UAT")
EMKOPO_PROD = env("EMKOPO_PROD")
EMKOPO_BOOTSTRAP = env("EMKOPO_BOOTSTRAP")
EMKOPO_PAGINATION = env("EMKOPO_PAGINATION")
EMKOPO_ADMIN = env.str("EMKOPO_ADMIN")
EMKOPO_LOAN_ID_PREFIX = env.str("EMKOPO_LOAN_ID_PREFIX")
EMKOPO_ORG_ACRONYM = env.str("EMKOPO_ORG_ACRONYM")
EMKOPO_ORG_NAME = env.str("EMKOPO_ORG_NAME")
EMKOPO_NEW_LOAN_MSG = env.str("EMKOPO_NEW_LOAN_MSG")
EMKOPO_NEW_TOP_UP_MSG = env.str("EMKOPO_NEW_TOP_UP_MSG")
EMKOPO_NEW_TAKEOVER_MSG = env.str("EMKOPO_NEW_TAKEOVER_MSG")
EMKOPO_UTUMISHI_SYSNAME = env.str("EMKOPO_UTUMISHI_SYSNAME")
EMKOPO_TERMS_SERVICE_URL = env.str("EMKOPO_TERMS_SERVICE_URL")
ESS_UTUMISHI_API = env.str("ESS_UTUMISHI_API")
ESS_SIGNATURE = env.str("ESS_SIGNATURE")
ESS_PUBLIC_KEY = env.str("ESS_PUBLIC_KEY")
EMKOPO_PRIVATE_KEY = env.str("EMKOPO_PRIVATE_KEY")
EMKOPO_PRODUCT_DECOMMISSION_API = env.str("EMKOPO_PRODUCT_DECOMMISSION_API")

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'rest_framework',
    'drf_yasg',
    'emkopo_api.apps.AppConfig',
    'emkopo_dashboard.apps.AppConfig',
    'emkopo_auth.apps.AppConfig',
    'emkopo_product.apps.AppConfig',
    'emkopo_loan.apps.AppConfig',
]

MIDDLEWARE = [
    'emkopo_api.middlewares.CacheRequestBodyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'emkopo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'emkopo.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Keep JSON for other endpoints
        'rest_framework_xml.parsers.XMLParser',  # Add XMLParser for XML support
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Keep JSON for other endpoints
        'rest_framework_xml.renderers.XMLRenderer',  # Add XMLRenderer for XML support
    ]
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOG_DIR = os.path.join(BASE_DIR, '.logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Log all levels (DEBUG and above)
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'emkopo.log'),
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'emkopo_error.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',  # Only log INFO level and above to console in production
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],  # Write logs to file and console
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'error_file'],  # Log errors separately
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file', 'error_file'],  # Log security errors
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = env.str("DJANGO_LOGIN_REDIRECT_URL")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
