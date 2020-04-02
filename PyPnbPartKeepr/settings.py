"""
Django settings for PyPnbPartKeepr project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')


DB_NAME = os.getenv('DB_NAME',      'partkeepradmindb'   )
DB_USER = os.getenv('DB_USERNAME',  'PartKeeprPsqlUser' )
DB_PASS = os.getenv('DB_USERPASS',  'PartKeeprPsqlPass' )
DB_HOST = os.getenv('DB_HOSTNAME',  '127.0.0.1'     )
DB_PORT = os.getenv('DB_HOSTPORT',  '5432'          )


EMAIL_HOST          = os.environ.get('EMAIL_HOST','localhost')
EMAIL_PORT          = os.environ.get('EMAIL_PORT',25)
EMAIL_HOST_USER     = os.environ.get('EMAIL_USER',None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS',None)
EMAIL_USE_TLS       = (os.environ.get('EMAIL_TLS','False') == 'True')
EMAIL_USE_SSL       = (os.environ.get('EMAIL_SSL','False') == 'True')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# The SECRET_KEY is provided via an environment variable in OpenShift
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',
        'CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead).')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG           = (os.environ.get('DEBUG',          'False') == 'True')
DEBUG_TOOLBAR   = (os.environ.get('DEBUG_TOOLBAR',  'False') == 'True')
DEBUG_NO_CACHES = (os.environ.get('DEBUG_NO_CACHES','False') == 'True')

ALLOWED_HOSTS   = os.environ.get('ALLOWED_HOSTS',[])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mptt',
    'bootstrap4',
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

if DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

