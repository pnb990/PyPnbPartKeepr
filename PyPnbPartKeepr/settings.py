"""
Django settings for PyPnbPartKeepr project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')

class Cfg(object):
    def __init__(self,pathList):
        self.cfg = {
                'DB_NAME'           : 'partkeeprpsqldb',
                'DB_USER'           : 'partkeeprpsqluser',
                'DB_PASS'           : 'PartKeeprPsqlPass',
                'DB_HOST'           : '127.0.0.1',
                'DB_PORT'           : '5432',
                'EMAIL_HOST'        : 'localhost',
                'EMAIL_PORT'        : 25,
                'EMAIL_USER'        : None,
                'EMAIL_PASS'        : None,
                'EMAIL_USE_TLS'     : False,
                'EMAIL_USE_SSL'     : False,
                'SECRET_KEY'        : 'CHANGE_ME!!!!',
                'HTTPS_ENABLED'     : False,
                'DEBUG'             : False,
                'DEBUG_TOOLBAR'     : False,
                'DEBUG_NO_CACHES'   : False,
                'ALLOWED_HOSTS'     : [],
                }
        for filename in pathList:
            if os.path.isfile(filename):
                try:
                    print("Load:",filename)
                    self.cfg.update(json.load(open(filename)))
                except json.decoder.JSONDecodeError as e:
                    print("*"*80)
                    print("* filename",filename,e)
                    print("*"*80)
                    sys.exit(1)
        self.verbose = set() if self.cfg['DEBUG'] else None

    def __getattr__(self,name):
        if name in os.environ:
            return os.environ[name]
        val = self.cfg[name]
        if self.verbose != None and name not in self.verbose:
            print("cfg",name,'=',val)
            self.verbose.add(name)
        return self.cfg[name]


cfg = Cfg([ os.path.join(BASE_DIR,'PyPnbPartKeepr.conf.json'), '/etc/PyPnbPartKeepr.conf.json' ])


DB_NAME = cfg.DB_NAME
DB_USER = cfg.DB_USER
DB_PASS = cfg.DB_PASS
DB_HOST = cfg.DB_HOST
DB_PORT = cfg.DB_PORT

EMAIL_HOST          = cfg.EMAIL_HOST
EMAIL_PORT          = cfg.EMAIL_PORT
EMAIL_HOST_USER     = cfg.EMAIL_USER
EMAIL_HOST_PASSWORD = cfg.EMAIL_PASS
EMAIL_USE_TLS       = cfg.EMAIL_USE_TLS
EMAIL_USE_SSL       = cfg.EMAIL_USE_SSL

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# The SECRET_KEY is provided via an environment variable in OpenShift
SECRET_KEY          = cfg.SECRET_KEY

#see later for https
HTTPS_ENABLED       = cfg.HTTPS_ENABLED

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG               = cfg.DEBUG
DEBUG_TOOLBAR       = cfg.DEBUG_TOOLBAR
DEBUG_NO_CACHES     = cfg.DEBUG_NO_CACHES

ALLOWED_HOSTS       = cfg.ALLOWED_HOSTS







SECURE_HSTS_INCLUDE_SUBDOMAINS  =HTTPS_ENABLED
SECURE_HSTS_PRELOAD             =HTTPS_ENABLED
SECURE_HSTS_SECONDS             =3600
SECURE_SSL_REDIRECT             =HTTPS_ENABLED
SESSION_COOKIE_SECURE           =HTTPS_ENABLED
CSRF_COOKIE_SECURE              =HTTPS_ENABLED
SECURE_REFERRER_POLICY          ='same-origin'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'phone_field',
    'bootstrap4',
    'PnbPartKeepr',
    'mptt',
]
    #'view_breadcrumbs',
    #'django_bootstrap_breadcrumbs',
if DEBUG:
    # need pip install django-extensions
    INSTALLED_APPS.append('django_extensions')

if DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

if DEBUG_TOOLBAR:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')


if DEBUG_NO_CACHES:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


ROOT_URLCONF = 'PyPnbPartKeepr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'PyPnbPartKeepr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#        'ENGINE'    : 'django.db.backends.mysql',
        'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
        'NAME'      : DB_NAME,
        'USER'      : DB_USER,
        'PASSWORD'  : DB_PASS,
        'HOST'      : DB_HOST,
        'PORT'      : DB_PORT,
        'OPTIONS': {
#            'init_command': "SET storage_engine=MyISAM;SET sql_mode='STRICT_TRANS_TABLES'",
#            'init_command': 'SET storage_engine=INNODB',
        }
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


#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

BREADCRUMBS_HOME_LABEL = "Home"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

STATIC_URL          = '/static/'
MEDIA_URL           = '/media/'

LOGIN_URL           = 'login'
LOGIN_REDIRECT_URL  = 'home'

