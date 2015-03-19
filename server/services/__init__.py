# -*- coding: utf8 -*-

from models import Song

song_id     = models.Attribute(required=True)
    title       = models.Attribute(required=True)
    description = models.Attribute()
    duration    = models.IntegerField()
    covert      = models.Attribute()

    artist      = models.ReferenceField(Artist)
    album       = models.ReferenceField(Album)
    genere      = models.ReferenceField(Genere)
    
    # GS or YT slug
    service     = models.Attribute(required=True)

    created_at  = models.DateTimeField(auto_now_add=True)


 
class BaseService(object):

    def _prepare_song(self, _song):

        title = _song['SongName']
        song_id = _song['SongID']
        covert = _song['Covert']

        artist_id = _song['ArtistID']
        album_name = _song['ArtistID']

        songs = Song.objects.filter(song_id=song_id)

        if songs:


        return {
            'name': song.title,
            'artist_id': song['ArtistID'],
            'song_id': song['SongID']
        }

    def _song_response(self, results):
        return map(self._prepare_song, results)

