# -*- coding: utf-8 -*-

from controllers import SearchHandler, PlaySongHandler, CacheHandler
from tornado.web import url


urls = [
    url(
        '/(.*)/search',
        SearchHandler,
        name='search_service'
    ),
    url(
        '/(.*)/play-song/(.*)',
        PlaySongHandler,
        name='play_song_service'
    ),
    url(
        '/cache/(.*)',
        CacheHandler,
        name='cache_service'
    ),
]