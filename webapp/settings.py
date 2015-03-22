# -*- coding: utf8 -*-

import os


DEBUG = True
XSRF_COOKIES = False

BASE_PATH = os.path.dirname(__file__)

# WEBAPP
STATIC_PATH = os.path.join(BASE_PATH, 'static')
STATIC_URL = '/static/'

TEMPLATE_PATH = os.path.join(BASE_PATH, 'templates')

LANG = 'es-PE'


# KALUKALU SERVER
KLU_SERVER = 'http://localhost:8888/'