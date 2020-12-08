import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

# Application definition
print("Debug mode")

SECRET_KEY = '!6rz8gx38ci27@(2pqu#wz8crc1$(0wc4+2is=u@n8do2^vn$$'

ALLOWED_HOSTS = ['localhost']

DEFAULT_CHARSET = "utf-8"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


DEBUG = True  # ローカルでDebugできるようになります

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
