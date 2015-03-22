# -*- coding: utf-8 -*-

from controllers import HomeController
from tornado.web import url


urls = [
    url(
        '/',
        HomeController,
        name='home'
    ),
]

