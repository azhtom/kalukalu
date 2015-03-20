# -*- coding: utf-8 -*-

import os
import tornado
import settings
import redisco

from urls import urls
from tornado.options import define, options, parse_command_line


global_settings = dict((setting.lower(), getattr(settings, setting))
                       for setting in dir(settings) if setting.isupper())


class Application(tornado.web.Application):

    def __init__(self, handlers=None, default_host='', transforms=None,
                 **settings):
        super(Application, self).__init__(handlers, default_host, transforms,
                                          **settings)

        redisco.connection_setup(host='localhost', port=6379, db=10)


if __name__ == '__main__':
    define('host', default='127.0.0.1', help='host address to listen on')
    define('port', default=8888, type=int, help='port to listen on')

    parse_command_line()
    application = Application(urls, **global_settings)
    application.listen(options.port, options.host, xheaders=True)

    tornado.ioloop.IOLoop.instance().start()

