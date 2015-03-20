# -*- coding: utf8 -*-

import re

from models import Song, Album, Genere, Artist


class BaseService(object):

    def _song_to_json(self, song):
        return {
            'song_id': song.id,
            'duration': song.duration,
            '_id': song.source,
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

            tags = list(set([t for t in tags if len(t) > 2]))

            song.tags = tags
            song.service = self._SLUG_NAME
            song.duration = int(float(duration))
            song.source = source_id

            print song.is_valid()
            print song.save()

        return self._song_to_json(song)

    def _song_response(self, results):
        return map(self._prepare_song, results)

    def search_in_cache(self, query):
        """
            Search on local database
            TODO: improved search algorithm
        """
        #rtists = Artist.objects.filter(name=query)

        #for artist in artists:
        #    _results += Song.objects.filter(artist_id=artist.id)

        #if not _results:
        words = re.sub("[^\w]", " ", query.lower()).split()
        _songs = []

        for word in words:
            if not _songs:
                _songs = Song.objects.filter(tags=word)
            else:
                _songs = _songs.filter(tags=word)

        return map(self._song_to_json, _songs)