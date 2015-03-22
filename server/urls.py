# -*- coding: utf-8 -*-

from controllers import SearchController, PlaySongController, CacheController
from tornado.web import url


urls = [
    url(
        '/(.*)/search',
        SearchController,
        name='search_service'
    ),
    url(
        '/(.*)/play-song/(.*)',
        PlaySongController,
        name='play_song_service'
    ),
    url(
        '/discover',
        DiscoverController,
        name='discover_service'
    ),
    url(
        '/cache/(.*)',
        CacheController,
        name='cache_service'
    ),
]