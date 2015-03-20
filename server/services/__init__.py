# -*- coding: utf8 -*-

from models import Song, Album, Genere, Artist


class BaseService(object):

    def _prepare_song(self, _song):

        title = _song['SongName']
        source_id = _song['SongID']
        covert = _song['CoverArtFilename']

        artist_name = _song['ArtistName']
        album_name = _song['AlbumName']

        songs = Song.objects.filter(source_id=source_id)
        song = Song(title=title, source_id=source_id, covert=covert)

        if not songs:
            artist = Artist.create(name=artist_name)
            
            album = Album.create(name=album_name, artist=artist)

            genere = Genere(name="Unknown")
            Genere.create(genere)

            song.artist = artist
            song.album = album
            song.genere = genere
            song.genere = self._SLUG_NAME

            song.save()

        else: song = songs[0]

        return {
            'title': song.title,
            'artist_name': song.artist.name,
            'artist_id': song.artist.id,
            'song_id': song.id
        }

    def _song_response(self, results):
        return map(self._prepare_song, results)

