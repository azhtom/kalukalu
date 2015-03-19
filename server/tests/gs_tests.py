# -*- coding: utf-8 -*-

import unittest
import redisco

from services.grooveshark import GSService


class GSTest(unittest.TestCase):

    def setUp(self):
        redisco.connection_setup(host='localhost', port=6380, db=10)
        self.gs = GSService()

    def connect_test(self):
        self.assertEqual(self.gs.is_conected(), True)

    def search_test(self):
        result = self.gs.search('blink-182')
        self.assertEqual(type(result), list)

        if result:
            song = result[0]
            self.assertTrue(song is not None)

    def download_test(self):
        #song_id = '24338816'
        #result = self.gs.download(song_id)
        #self.assertTrue(result is not None)
        pass
 
