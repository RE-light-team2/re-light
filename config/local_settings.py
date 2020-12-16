import os

SECRET_KEY = '!6rz8gx38ci27@(2pqu#wz8crc1$(0wc4+2is=u@n8do2^vn$$'  # 追加

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True

# local環境用のテストに必要なセッティングかも
