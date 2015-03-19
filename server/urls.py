# -*- coding: utf-8 -*-

from controllers import SearchHandler, DownloadHandler
from tornado.web import url


urls = [
    url(
        '/(.*)/search',
        SearchHandler,
        name='search_service'
    ),
    url(
        '/(.*)/download/(.*)',
        DownloadHandler,
        name='download_service'
    ),
]