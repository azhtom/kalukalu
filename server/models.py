# -*- coding: utf-8 -*-

from redisco import models, containers as cont


class Genere(models.Model):

    name        = models.Attribute(required=True)


class Artist(models.Model):

    name        = models.Attribute(required=True)
    bio         = models.Attribute()


class Album(models.Model):

    name        = models.Attribute(required=True)
    year        = models.Attribute()
    covert      = models.Attribute()

    artist      = models.ReferenceField('Artist', related_name='artist')

    @staticmethod
    def create(name, artist_id):
        albums = Album.objects.filter(artist_id=artist_id, 
            name=name.lower())
        if not albums:
            album = Album()
            album.name = name
            album.artist_id = artist_id
            album.save()
        else: album = albums.first()
        return album


class Song(models.Model):

    source      = models.Attribute(required=True)
    title       = models.Attribute(required=True)
    description = models.Attribute()
    duration    = models.IntegerField()
    cache_name  = models.Attribute()
    tags        = models.ListField(unicode)

    artist      = models.ReferenceField(Artist, required=True)
    album       = models.ReferenceField(Album, required=True)
    genere      = models.ReferenceField(Genere, required=True)
    
    # GS or YT slug
    service     = models.Attribute(required=True)

    created_at  = models.DateTimeField(auto_now_add=True)

