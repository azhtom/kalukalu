# -*- coding: utf8 -*-

import utils
import settings
import importlib
import tornado.web
import json


class JsonHandler(tornado.web.RequestHandler):
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


class SearchHandler(JsonHandler):

	def get(self, slug):
		
		servname = settings.SERVICES.get(slug)
		if servname:
			q = self.get_argument('q')
			service = utils.get_service_class(servname)
			result = service().search(q)
			self.response['songs'] = result
			return self.write_json()
		else:
			return self.write_error(404)


class DownloadHandler(JsonHandler):

	def get(self, slug, song_id):
		
		servname = settings.SERVICES.get(slug)
		if servname:
			service = utils.get_service_class(servname)
			result = service().download(song_id)
			self.response['url'] = result
			return self.write_json()
		else:
			return self.write_error(404)