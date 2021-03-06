"""
Django settings for usaid project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x5$p1g&$ezsv*y0e9datzesr^lpnz#n)yk!p%((_njib7r+9y8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrapform',

    'general',
    'boleta',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'usaid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                os.path.join(BASE_DIR, 'general', 'templates'),
                os.path.join(BASE_DIR, 'boleta', 'templates'),
                ],
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

WSGI_APPLICATION = 'usaid.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

os.environ["ODBCSYSINI"] = "/home/BiDSS"


DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'DB_A0641C_USAID',                      # Or path to database file if using sqlite3.
        'USER': 'DB_A0641C_USAID_admin',                      # Not used with sqlite3.
        'PASSWORD': 'Motagua2016',                  # Not used with sqlite3.
        'HOST': 'sqlserverdatasource',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '1433',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
                'host_is_server': False,
                'dsn': 'sqlserverdatasource',
        },
    }
}
DATABASE_NAME = 'DB_A0641C_USAID'
DATABASE_HOST = 'sqlserverdatasource'
DATABASE_PORT = '1433'
DATABASE_USER = 'DB_A0641C_USAID_admin'
DATABASE_PASSWORD = 'Motagua2016'
DATABASE_OPTIONS = {
        'host_is_server': False,
        'dsn': 'sqlserverdatasource',
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = '/assets/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)