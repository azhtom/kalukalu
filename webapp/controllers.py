# -*- coding: utf8 -*-

import tornado.web
import json


class HomeController(tornado.web.RequestHandler):

    def get(self):

        data = {
            'klu_server': self.settings.get('klu_server')
        }

        self.render('home.html', data=data)

