# -*- coding: utf-8 -*-

from redisco import models


class Genere(models.Model):

    name        = models.Attribute(required=True)


class Artist(models.Model):

    name        = models.Attribute(required=True)
    bio         = models.Attribute(required=True)
    created_at  = models.DateTimeField(auto_now_add=True)


class Album(models.Model):

    name        = models.Attribute(required=True)
    year        = models.Attribute(required=True)
    covert      = models.Attribute()


class Song(models.Model):

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

