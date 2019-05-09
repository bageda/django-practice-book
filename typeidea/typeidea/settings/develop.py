from .base import *


DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qx',
        'USER': 'qx',
        'PASSWORD': 'q0520305x',
        'HOST': '127.0.0.1',   #将postgresql端口映射到本机
        'PORT': '5432',
    }
}
