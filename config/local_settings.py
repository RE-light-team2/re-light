import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

# Application definition
print("Debug mode")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '!6rz8gx38ci27@(2pqu#wz8crc1$(0wc4+2is=u@n8do2^vn$$'

ALLOWED_HOSTS = ['localhost']

# settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'remote.enter.light@gmail.com'
EMAIL_HOST_PASSWORD = 'kogyokakmlattdal'
DEFAULT_FROM_EMAIL = 'remote.enter.light@gmail.com'
EMAIL_USE_TLS = True

DEBUG = True  # ローカルでDebugできるようになります
