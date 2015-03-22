# -*- coding: utf8 -*-

import re
import uuid
import settings

from models import Song, Album, Genere, Artist


class BaseService(object):

    def _song_to_json(self, song):
        return {
            'song_id': song.id,
            'duration': song.duration,
            'title': song.title.title(),
            'artist': {
                'id': song.artist.id,
                'name': song.artist.name.title()
            },
            'album': {
                'id': song.album.id,
                'name': song.album.name.title(),
            }
        }

    def _prepare_song(self, _song):

        title = _song['SongName']
        source_id = _song['SongID']
        duration = _song['EstimateDuration']

        artist_name = _song['ArtistName']
        album_name = _song['AlbumName'] or u'unknown'

        artist = Artist.objects.get_or_create(name=artist_name.lower())
        album = Album.create(name=album_name.lower(), artist_id=artist.id)
        genere = Genere.objects.get_or_create(name=u'unknown')

        song = Song.objects.get_or_create(title=title.lower(),
                artist_id=artist.id,
                album_id=album.id,
                genere_id=genere.id)

        if not song.source:
            tags = []
            tags += re.sub("[^\w]", " ", artist.name.lower()).split()
            tags += re.sub("[^\w]", " ", album.name.lower()).split()
            tags += re.sub("[^\w]", " ", title.lower()).split()

            song.tags = tags
            song.service = self._SLUG_NAME
            song.duration = int(float(duration))
            song.source = source_id

            song.is_valid()
            song.save()

        return self._song_to_json(song)

    def _song_response(self, results):
        return map(self._prepare_song, results)

    def _save_song_in_cache(self, song):
        binary_song = self._get_media_file(song.source)
        if binary_song:
            cache_name = str(uuid.uuid4()) + '.mp3'

            full_path = '%s%s' % (settings.CACHE_PATH, cache_name)
            _file = open(full_path, 'wb')
            _file.write(binary_song)
            _file.close()

            song.cache_name = cache_name
            song.save()

    def search_in_cache(self, query):
        """
            Search on local database
            TODO: improved search algorithm
        """
        words = re.sub("[^\w]", " ", query.lower()).split()
        songs = Song.objects.filter(tags=words[0])

        results = [sg for sg in songs if (len(list(set(words) - set(sg.tags))) + .0) / len(sg.tags) == 0]

        return map(self._song_to_json, results)

    def get_song(self, song_id):
        """
            Search song and stored in cache
        """
        song = Song.objects.get_by_id(song_id)

        if song:
            if not song.cache_name:
                self._save_song_in_cache(song)
            result = self._song_to_json(song)
            result['media_url'] = '%s%s' % (settings.CACHE_URL, song.cache_name)
            return result
        return []

