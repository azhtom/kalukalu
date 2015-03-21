# -*- coding: utf8 -*-

import os


DEBUG = True
XSRF_COOKIES = False

BASE_PATH = os.path.dirname(__file__)

CACHE_PATH = os.path.join(BASE_PATH, 'cache/')
CACHE_URL = '/cache/'

SERVICES = {
	'gs': 'grooveshark.GSService'
}