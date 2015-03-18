# -*- coding: utf-8 -*-

import services

from tornado.web import url


urls = [
    url(
        '/(.*)/search',
        services.SearchHandler,
        name='search_service'
    ),
    url(
        '/(.*)/download/(.*)',
        services.DownloadHandler,
        name='download_service'
    ),
]