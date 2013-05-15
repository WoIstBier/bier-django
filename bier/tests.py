# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client
urlprefix = '/bier/rest/'
class KioskListTest(TestCase):
    fixtures = ['test_data.json']
    client = Client()
    def test_return_code(self):
        response  = self.client.get(urlprefix + "kioskList/")
        self.assertEqual(response.status_code , 200)
        response  = self.client.get(urlprefix + "kioskList")
        self.assertEqual(response.status_code , 301)
    
    def test_bad_parameter(self):
        response  = self.client.get(urlprefix + "kioskList/?geo_lat=123a.23434")
        self.assertEqual(response.status_code, 400)
        response  = self.client.get(urlprefix + "kioskList/?geo_long=123.23434a")
        self.assertEqual(response.status_code, 400)
        
    def test_empty_result_parameter(self):
        '''test parameters for non existing beers. or lookup kiosks at tatoine'''
        response  = self.client.get(urlprefix + "kioskList/?beer=gibtsjagarnichtbier")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')
        #mos espa coordinates tunisia
        response  = self.client.get(urlprefix + "kioskList/?geo_lat=33.994296&geo_long=7.842677")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')
        #test radius too small
        response  = self.client.get(urlprefix + "kioskList/?radius=0.01&geo_lat=51.53533&geo_long=7.48700")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')
        
    def test_beer_parameter(self):
        '''test if only kiosk with the right beers are returned'''
        response  = self.client.get(urlprefix + "kioskList/?beer=kronen")
        self.assertEqual(response.status_code, 200)
        #there has to be an entry having kronen beer.
        self.assertNotEqual(response.content, '[]')
