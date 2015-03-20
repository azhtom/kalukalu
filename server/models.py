# -*- coding: utf-8 -*-

from redisco import models, containers as cont


class Genere(models.Model):

    name        = models.Attribute(required=True)

    @staticmethod
    def create(name):
        generes = Genere.objects.filter(name=name)
        if not generes:
            genere = Genere()
            genere.name = name
            genere.save()
        else: genere  = generes[0]
        return genere

class Artist(models.Model):

    name        = models.Attribute(required=True)
    bio         = models.Attribute()
    created_at  = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create(name):
        artists = Artist.objects.filter(name=name)
        if not artists:
            artist = Artist()
            artist.name = name
            artist.save()
        else: artist = artists[0]
        return artist


class Album(models.Model):

    name        = models.Attribute(required=True)
    year        = models.Attribute()
    covert      = models.Attribute()

    artist      = models.ReferenceField(Artist)

    @staticmethod
    def create(name, artist):
        l = cont.TypedList('artists', 'Artist')
        l.extend(Album.objects.filter(artist=artist, 
            name=name.lower()))
        print l
        if not l:
            print "preee"
            album = Album(artist=artist)
            album.name = name

            print artist.id, "AAA"

            album.artist = artist
            album.save()
        else: album = l[0]
        return album

class Song(models.Model):

    source_id   = models.Attribute(required=True)
    title       = models.Attribute(required=True)
    description = models.Attribute()
    duration    = models.IntegerField()
    covert      = models.Attribute()
    cache_name  = models.Attribute()

    artist      = models.ReferenceField(Artist, required=True)
    album       = models.ReferenceField(Album)
    genere      = models.ReferenceField(Genere, required=True)
    
    # GS or YT slug
    service     = models.Attribute(required=True)

    created_at  = models.DateTimeField(auto_now_add=True)

