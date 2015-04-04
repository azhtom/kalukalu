# -*- coding: utf8 -*-

import settings


YOUTUBE_API_VERSION = 'v3'


class YouTubeService(BaseService):
    """
        YouTube Service
    """
    def __init__(self):
        pass

    def _get_media_file(self, yt_song_id):
        pass

    def connect(self):
        self.youtube = build(settings.YOUTUBE_API_SERVICE_NAME, 
                        YOUTUBE_API_VERSION,
                        developerKey=settings.DEVELOPER_KEY)

    def search(self, q):
        pass

