import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'

PORT = 8080
HOST = '127.0.0.1'
SERVER = 'wsgiref'
