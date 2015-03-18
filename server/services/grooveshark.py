# -*- coding: utf8 -*-

import os
import json
import uuid
import binascii
import hashlib
import requests


GS_SALT = 'chickenFingers'
GS_SERVICE_URL = 'https://grooveshark.com/more.php'
GS_CROSSDOMAIN_URL = 'http://grooveshark.com/crossdomain.xml'
GS_COUNTRY = {'ID': 57, 'CC1': 72057594037927940, 'CC2': 0, 'CC3': 0, 'CC4': 0, 'DMA': 0, 'IPR': 0}


class GSService(object):

    __session_id = None
    __UUID = None
    __CM_TOKEN = None

    def __init__(self):
        self.__session_id = binascii.b2a_hex(os.urandom(16))
        self.__UUID = uuid.uuid1().hex
        self.connect()

    def __get_hearders(self):
        return {
            'Accept': 'text/html:application/xhtml+xml:application/xml;q=0.9:*/*;q=0.8',
            'Content-Type': 'text/html; charset=UTF-8',
            'Accept-Language': 'en-us:en;q=0.5',
            'Accept-Charset': 'utf-8;q=0.7:*;q=0.7',
            'Accept-Encoding': 'gzip:deflate',
            'Referer': 'http://grooveshark.com',
            'Origin': 'http://grooveshark.com',
            'Host': 'grooveshark.com',
            'User-Agent': 'Mozilla/5.0 Windows; U; Windows NT 5.1; de; rv:1.9.0.19) Gecko/2010031422 Firefox/3.0.19'
        }

    def __prepare_post(self, method, params):
        data = {}
        data['header'] = {}
        data['header']['country'] = GS_COUNTRY
        
        data['header']['client'] = 'jsqueue'
        data['header']['clientRevision'] = '20130520'
        data['header']['privacy'] = 0
        data['header']['session'] = self.__session_id

        if self.__CM_TOKEN:
            data['header']['token'] = self.__gen_token_hash(method)

        data['UUID'] = self.__UUID
        data['method'] = method
        data['parameters'] = params
        return data

    def __get_secret_key(self):
        md5 = hashlib.md5()
        md5.update(self.__session_id)
        return md5.hexdigest()

    def __gen_token_hash(self, method):
        r6ch = binascii.b2a_hex(os.urandom(3))
        tkn = '%s:%s:%s:%s' % (method, self.__CM_TOKEN, GS_SALT, r6ch)
        return r6ch + hashlib.sha1(tkn).hexdigest()

    def __call(self, method, data):
        _data = self.__prepare_post(method, data)
        return requests.post(GS_SERVICE_URL, headers=self.__get_hearders(), 
            data=json.dumps(_data))

    def __get_stream_key(self, song_id):
        data = {
            'mobile':'false', 
            'prefetch':'false', 
            'songID': song_id,
            'country': GS_COUNTRY
        }
        r = self.__call('getStreamKeyFromSongIDEx', data)
        print r.content
        return r.json()

    def __request_stream(self, song_id):
        stream_key = self.__get_stream_key(song_id)
        data = {
                'streamKey':stream_key['streamKey'],
                'ip':stream_key['ip'],
                'streamServerID': stream_key['streamServerID']
            }

        headers = self.__get_hearders()
        uri = 'http://%s/stream.php' % data['ip']

        headers['Host'] = data['ip']
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        r = requests.post(uri, headers=headers, 
            data=json.dumps(data))
        print r.content

    def __prepare_song(self, song):
        return {
            'name': song['SongName'],
            'artist_id': song['ArtistID'],
            'song_id': song['SongID']
        }

    def __song_response(self, results):
        return map(self.__prepare_song, results)

    def connect(self):
        data = {'secretKey': self.__get_secret_key()}
        rcall = self.__call('getCommunicationToken', data)
        if rcall.status_code == requests.codes.ok:
            if rcall.content:
                self.__CM_TOKEN = rcall.json().get('result')

    def search(self, query):
        data = {'query': query, 'type': 'Songs', 'ppOverride': 'false', 'guts':0}
        rcall = self.__call('getResultsFromSearch', data)
        if rcall.status_code == requests.codes.ok:
            result = rcall.json()
            return self.__song_response(result.get('result').get('result'))
        return None

    def download(self, song_id):
        self.__request_stream(song_id)
        data = {}

        return data


if __name__ == '__main__':
    gs = GSService()
    gs.download(24306654)