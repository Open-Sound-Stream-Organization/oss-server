"""
Django settings for oss_server project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import secrets
from pathlib import Path
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if 'DJANGO_DEBUG' in os.environ:
    DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "ToBeRead"
if DEBUG:
    SECRET_KEY = 'TotallyNotSecureKeyButItsJustForDebugging'
else:
    secret_key_path = Path('../secret_key.txt')
    if not secret_key_path.is_file() or os.path.getsize(secret_key_path) < 32:
        secret_key_file = secret_key_path.open('w')
        secret_key_file.write(secrets.token_urlsafe(128))
        secret_key_file.close()
    with secret_key_path.open('r') as f:
        SECRET_KEY = f.read().strip()

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if 'DJANGO_HOST' in os.environ:
    ALLOWED_HOSTS += [ os.environ['DJANGO_HOST'] ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'repertoire',
    'tastypie',
    'tastypie_swagger',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oss_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'web_interface/oss-web/build')],
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

WSGI_APPLICATION = 'oss_server.wsgi.application'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
        }
    }
if 'USE_POSTGRESQL' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'ossdb', # set in docker-compose.yml
            'PORT': 5432 # default postgres port
        }
    }




# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "web_interface/oss-web/build/static"),
]

MEDIA_ROOT = 'media/'
MEDIA_URL = 'files/'

TASTYPIE_ABSTRACT_APIKEY = True

TASTYPIE_SWAGGER_API_MODULE_LIST = (
    {'path': 'repertoire.api.v1',
     'obj': 'v1_api',
     'func_name': ''},
)

TASTYPIE_SWAGGER_IGNORE_PATTERN_LIST = ['.DS_Store']
TASTYPIE_SWAGGER_SERVER_URL = 'http://127.0.0.1:8000'
TASTYPIE_SWAGGER_OPEN_API_INFO = {
  "title": "Open Stream Server API",
  "description": "This is a sample server for a pet store.",
  "termsOfService": "http://example.com/terms/",
  "contact": {
    "name": "API Support",
    "url": "http://www.example.com/support",
    "email": "support@example.com"
  },
  "license": {
    "name": "MIT License",
    "url": "https://raw.githubusercontent.com/Open-Sound-Stream-Organization/oss-server/master/LICENSE"
  },
  "version": "1.0.1"
}
TASTYPIE_SWAGGER_INDEX_TITLE = ''
TASTYPIE_SWAGGER_DOCS_DIR = 'api_doc'

#Tastypie settings
API_LIMIT_PER_PAGE = 200
TASTYPIE_ALLOW_MISSING_SLASH = True


#Data upload limit of 100MB

DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600