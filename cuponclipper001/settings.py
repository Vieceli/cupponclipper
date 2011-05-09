# Django settings for cuponclipper001 project.

import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

#redirects
DEFAULT_CITY_SLUG = 'cupons/goiania'
LOGIN_URL = "/conta/login/"
LOGIN_REDIRECT_URL = "/"
AUTH_PROFILE_MODULE = 'contas.MeuUser'
CUSTOM_USER_MODEL = 'contas.MeuUser'
#extra configuracoes
ENABLE_SSL = False
FORCE_SCRIPT_NAME = ''

#informacoes site
SITE_NAME = 'Cupon Clipper Brasil'
META_KEYWORDS = 'Descontos, Cupons, Gratuito,Compra,Coletiva'
META_DESCRIPTION = 'Site de cupons'
SESSION_COOKIE_AGE = 7776000 # the number of seconds in 90 days

#configura email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'veiodruida@gmail.com'
EMAIL_HOST_PASSWORD = 'cogumelos1206'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


ADMINS = (
  ('Jhoni', 'veiodruida@gmail.com'),
  ('Miltinho Brandao', 'miltinho@gmail.com'),
  ('Marinho Brandao', 'marinho@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cuponclipper',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '1234',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}



# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"


TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

try:
    from local_settings import *
except ImportError:
    pass

MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT_PATH, 'estatico')
STATIC_URL = '/estatico/'

DJBOLETO_MEDIA_URL = "/media/boletosimg/"

GEOIP_PATH = os.path.join(PROJECT_ROOT_PATH, 'geoip')

ADMIN_MEDIA_PREFIX = '/admin-media/'



# Make this unique, and don't share it with anybody.
SECRET_KEY = 'uffvc26@(wkl&y9$m%vepurbo8h$8h(2+bkcfkja7^4v!08-(p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cuponclipper001.SSLMiddleware.SSLRedirect',
)

ROOT_URLCONF = 'cuponclipper001.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT_PATH,'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'cupon',
    'contas',
    'checkout',
    'boleto',
)

AUTHENTICATION_BACKENDS = (
    # this is the default backend, don't forget to include it!
    'cuponclipper001.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    # this is what you're adding for using Twitter
#    'massivecoupon.socialregistration.auth.TwitterAuth',
    #'massivecoupon.socialregistration.auth.FacebookAuth', # Facebook
#    'massivecoupon.socialregistration.auth.OpenIDAuth', # OpenID
)
