# -*- coding: utf8 -*-

import utils
import settings
import importlib
import tornado.web
import json

from models import Song


class JsonResponse(tornado.web.RequestHandler):
    """
        Request handler where requests and responses speak JSON.
        From: https://gist.github.com/mminer/5464753
    """
    def prepare(self):
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message) # Bad Request
 
        # Set up response dictionary.
        self.response = dict()
 
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
 
    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'
 
        self.response = kwargs
        self.write_json()
 
    def write_json(self):
        output = json.dumps(self.response)
        self.write(output)


class DiscoverController(JsonResponse):

    def get(self):

        self.response = []
        return self.write_json()
    

class SearchController(JsonResponse):

    def get(self, slug):
        servname = settings.SERVICES.get(slug)
        if servname:
            q = self.get_argument('q')
            remote = self.get_argument('remote', 0)

            service = utils.get_service_class(servname)()

            if remote == '1':
                service.connect()
                result = service.search(q)
            else:
                result = service.search_in_cache(q)
                if not result:
                    service.connect()
                    service.search(q)
                    result = service.search_in_cache(q)

            self.response['songs'] = result
            return self.write_json()
        else:
            return self.write_error(404)


class PlaySongController(JsonResponse):

    def get(self, slug, song_id):
        
        servname = settings.SERVICES.get(slug)
        if servname:
            service = utils.get_service_class(servname)()
            service.connect()

            result = service.get_song(song_id)

            self.response = result
            return self.write_json()
        else:
            return self.write_error(404)


class CacheController(tornado.web.RequestHandler):

    def get(self, file_name):

        full_path = '%s%s' % (settings.CACHE_PATH, file_name)

        buf_size = 4096
        self.set_header('Content-Type', 'audio/mpeg')
        self.set_header('Content-Disposition', 'attachment; filename=' + file_name)
        with open(full_path, 'r') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()

            