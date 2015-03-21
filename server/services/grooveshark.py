# -*- coding: utf8 -*-

import os
import json
import uuid
import binascii
import hashlib
import requests
import services


GS_CLIENTS = {
    'htmlshark': {
        'token': 'nuggetsOfBaller',
        'revision': '20130520'
    },
    'jsqueue': {
        'token': 'chickenFingers',
        'revision': '20130520'
    }
}

GS_SERVICE_URL = 'https://grooveshark.com/more.php'
GS_CROSSDOMAIN_URL = 'http://grooveshark.com/crossdomain.xml'
GS_COUNTRY = {"CC1":"16384","CC3":"0","ID":"15","CC2":"0","CC4":"0"}


class GSSession(object):
    
    id = None
    uuid = None
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GSSession, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class GSService(services.BaseService):

    session = None
    _CM_TOKEN = None
    _SLUG_NAME = 'gs'

    def __init__(self, auto=False):

        self.session = GSSession()
        if not self.session.id and not self.session.uuid:
            print "new!"
            self.session.id = binascii.b2a_hex(os.urandom(16))
            self.session.uuid = str(uuid.uuid1())

        if auto:
            self.connect()

    def _get_hearders(self):
        return {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'text/plain',
            'Accept-Language': 'en-us:en;q=0.5',
            'Accept-Charset': 'utf-8;q=0.7:*;q=0.7',
            'Accept-Encoding': 'gzip:deflate',
            'Referer': 'http://grooveshark.com/',
            'Origin': 'http://grooveshark.com',
            'Host': 'grooveshark.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.39 Safari/537.36'
        }

    def _prepare_post(self, method, params, client='htmlshark'):
        data = {}
        data['header'] = {}

        data['header']['client'] = client
        data['header']['clientRevision'] = GS_CLIENTS[client]['revision']
        data['header']['privacy'] = 0
        data['header']['session'] = self.session.id
        data['header']['country'] = GS_COUNTRY

        if self._CM_TOKEN:
            data['header']['token'] = self._gen_token_hash(method, client)

        data['uuid'] = self.session.uuid
        data['method'] = method

        
        data['parameters'] = params
        return data

    def _get_secret_key(self):
        md5 = hashlib.md5()
        md5.update(self.session.id)
        return md5.hexdigest()

    def _gen_token_hash(self, method, client):
        r6ch = binascii.b2a_hex(os.urandom(3))
        tkn = '%s:%s:%s:%s' % (method, self._CM_TOKEN, GS_CLIENTS[client]['token'], r6ch)
        return r6ch + hashlib.sha1(tkn).hexdigest()

    def _call(self, method, data, client='htmlshark'):
        _data = self._prepare_post(method, data, client)
        return requests.post(GS_SERVICE_URL, headers=self._get_hearders(), 
            data=json.dumps(_data))

    def _get_stream_key(self, song_id):
        data = {
            'mobile': 'false', 
            'prefetch': 'false', 
            'type': 0,
            'country': GS_COUNTRY,
            'songID': song_id
        }
        r = self._call('getStreamKeyFromSongIDEx', data)
        print r.headers
        print r.content, "STREAMKEY"
        return r.json().get('result')

    def _request_stream(self, song_id):
        stream_key = self._get_stream_key(song_id)
        if stream_key:
            data = {
                    'streamKey':stream_key['streamKey'],
                    'ip':stream_key['ip'],
                    'streamServerID': stream_key['streamServerID']
                }

            headers = self._get_hearders()
            uri = 'http://%s/stream.php?streamKey=%s' % (data['ip'], data['streamKey'])

            headers['Host'] = data['ip']
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

            r = requests.post(uri, headers=headers, 
                data=json.dumps(data))
            if r.status_code == requests.codes.ok:
                return r.content
        return None

    def connect(self):
        data = {'secretKey': self._get_secret_key()}
        rcall = self._call('getCommunicationToken', data)
        if rcall.status_code == requests.codes.ok:
            if rcall.content:
                self._CM_TOKEN = rcall.json().get('result')

    def is_conected(self):
        return self._CM_TOKEN is not None

    def search(self, query):
        data = {'query': query, 'type': 'Songs', 'ppOverride': 'false', 'guts':0}
        rcall = self._call('getResultsFromSearch', data)

        if rcall.status_code == requests.codes.ok:
            result = rcall.json()
            return self._song_response(result.get('result').get('result'))
        return []

    def _get_media_file(self, gs_song_id):
        """"
            gs_song_id --> Grooveshark Song ID
        """
        #data = {
        #    'client': 'jsqueue'
        #}
        #rcall = self._call('getCountry', data, 'jsqueue')
        #print rcall.content, "xx"

        return self._request_stream(gs_song_id)
        

if __name__ == '__main__':

    gs = GSService()
    gs.connect()

    #gs.search('fito paez')

    print gs.download('25076477')

