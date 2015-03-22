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

    def __init__(self):
        self.id = binascii.b2a_hex(os.urandom(16))
        self.uuid = str(uuid.uuid1())

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GSSession, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class GSService(services.BaseService):

    session = None
    _CM_TOKEN = None
    _SLUG_NAME = 'gs'

    def __init__(self):
        self.session = GSSession()

    def _headers(self):
        """
            Headers for Grooveshark Requests
        """
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

    def _prepare_call(self, method, params, client='htmlshark'):
        """
            Header and parameters vars
        """
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
        """
            Session ID to MD5
        """
        md5 = hashlib.md5()
        md5.update(self.session.id)
        return md5.hexdigest()

    def _gen_token_hash(self, method, client):
        """
            Grooveshark Token
            ==================

            Generate 6 random hex characters.
            Create a SHA1 hash:
            METHOD + ':' + COMUNICATION_TOKEN + ':' + CLIENT_TOKEN + RANDOM CHARACTERS
            Returns:
                RANDOM CHARACTERS + SHA1 HASH
        """
        r6ch = binascii.b2a_hex(os.urandom(3))
        tkn = '%s:%s:%s:%s' % (method, self._CM_TOKEN, GS_CLIENTS[client]['token'], r6ch)
        return r6ch + hashlib.sha1(tkn).hexdigest()

    def _call(self, method, data, client='htmlshark'):
        _data = self._prepare_call(method, data, client)
        return requests.post(GS_SERVICE_URL, headers=self._headers(), 
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

            headers = self._headers()
            uri = 'http://%s/stream.php?streamKey=%s' % (data['ip'], data['streamKey'])

            headers['Host'] = data['ip']
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

            r = requests.post(uri, headers=headers, 
                data=json.dumps(data))
            if r.status_code == requests.codes.ok:
                return r.content
        return None

    def _get_media_file(self, gs_song_id):
        """"
            gs_song_id --> Grooveshark Song ID
        """
        return self._request_stream(gs_song_id)

    def connect(self):
        """
            Connect to Grooveshark to receive a token.
            If result is None, it will be impossible to use the gs api.
        """
        data = {'secretKey': self._get_secret_key()}
        rcall = self._call('getCommunicationToken', data)
        if rcall.status_code == requests.codes.ok:
            if rcall.content:
                self._CM_TOKEN = rcall.json().get('result')

    def search(self, query):
        data = {'query': query, 'type': 'Songs', 'ppOverride': 'false', 'guts':0}
        rcall = self._call('getResultsFromSearch', data)

        if rcall.status_code == requests.codes.ok:
            result = rcall.json()
            return self._song_response(result.get('result').get('result'))
        return []

    def is_conected(self):
        return self._CM_TOKEN is not None
        
