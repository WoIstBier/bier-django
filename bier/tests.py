"""
These will pass when you run "manage.py test".
"""

from django.test import TestCase

from django.test import Client

import json



prefix = '/bier/rest/'



def get_proper_response_index(testcase, suffix):
        i=1
        resp = testcase.client.get(prefix + suffix + '/' + str(i), follow = 1)
       
        while resp.status_code is not 200:
            if resp.status_code is 405:
                break
            i+=1
            resp = testcase.client.get(prefix + suffix + '/' + str(i), follow = 1)

        return i
    
def basic_status_code(testcase, suffix):
    resp1 = testcase.client.get(prefix + suffix)
    testcase.assertEqual(resp1.status_code, 301, 'Server redirect did not give a proper response statuscode! expected: ' + str(301) + ' response: ' + str(resp1.status_code))
    resp1 = testcase.client.get(prefix + suffix, follow = 1)
    testcase.assertEqual(resp1.status_code, 200, 'Server redirect did not give a proper response statuscode! expected: ' + str(200) + ' response: ' + str(resp1.status_code))
    resp2 = testcase.client.get(prefix + suffix + '/')
    testcase.assertEqual(resp1.status_code, 200, 'Server redirect did not give a proper response statuscode! expected: ' + str(200) + ' response: ' + str(resp1.status_code))
    testcase.assertJSONEqual(resp1.content, resp2.content, 'The request redirect was not a proper redirect. The two responses are not equal.')
    resp2 = testcase.client.get(prefix + suffix + '/', {'ignore_text': 'ignore', 'ignore_num': 123})
    testcase.assertEqual(resp2.status_code, 200, 'The given ignore keys have not been ignored by the server! The two responses are not equal.')
    testcase.assertJSONEqual(resp1.content, resp2.content, 'The given ignore keys have not been ignored by the server! The two responses are not equal.')
class kioskListTests(TestCase):
    def test_status_codes(self):
        basic_status_code(self, 'kioskList')

        resp1 = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.5 , 'geo_long': 7.5, 'radius': 5})
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.5 , 'geo_long': 7.5, 'radius': 5, 'ignore_text': 'ignore', 'ignore_num': 123})
        self.assertEqual(resp2.status_code, 200, 'The given ignore keys have not been ignored by the API!')
        self.assertJSONEqual(resp1.content, resp2.content, 'The given ignore keys have not been ignored by the API! The two responses are not equal.')
        
        resp2 = self.client.get(prefix + 'kioskList/', {'geo_lat': '5a1.5' , 'geo_long': '7b.5', 'radius': 'c5'})
        self.assertEqual(resp2.status_code, 400)
        
#         response  = self.client.get(urlprefix + "kioskList/?geo_lat=123a.23434")
#         self.assertEqual(response.status_code, 400)
#         response  = self.client.get(urlprefix + "kioskList/?geo_long=123.23434a")
#         self.assertEqual(response.status_code, 400)
        
    ''' parameters for non existing beers. or lookup kiosks at tatoine'''
    def test_distance_and_empty_response(self):
        resp = self.client.get(prefix + 'kioskList/', {'geo_lat': 0.2 , 'geo_long': -176.5, 'radius': 5})
        self.assertEqual(resp.content, '[]', 'We got a Kiosk on Baker Island!')
        response  = self.client.get(prefix + "kioskList/?beer=gibtsjagarnichtbier")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')
        #mos espa coordinates tunisia
        response  = self.client.get(prefix + "kioskList/?geo_lat=33.994296&geo_long=7.842677")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')
        #test radius too small
        response  = self.client.get(prefix + "kioskList/?radius=0.01&geo_lat=51.53533&geo_long=7.48700")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')
        #self.assertNotEqual(resp.content, '[]', 'The kioskList returned an empty response for Baker Island!')

    def test_response_content(self):
          
        None_notallowed = ['kioskName', 'kioskStreet', 'kioskCity', 'kioskPostalCode', 'kioskNumber', 'distance']
        None_allowed    = ['beerName', 'beerBrew', 'beerSize', 'beerPrice', 'thumb_path']
          
        resp = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.5 , 'geo_long': 7.5, 'radius': 5})
          
        cont_dict = eval(resp.content.replace('null', 'None'))[1]   
        #print(cont_dict)
        self.assertGreaterEqual(5, cont_dict.get('distance'), 'The distance is greater than the given radius!')
          
        
        cont_dict = json.loads(resp.content)[1]
        
        #self.assertGreaterEqual(5, cont_dict.get('distance'), 'The distance is greater than the given radius!')
        
        for key in None_notallowed:
            self.assertTrue(cont_dict.has_key(key), "The key " + key + " wasn't found in the response.")
            self.assertNotEqual(cont_dict.get(key), None)
            self.assertNotEqual(cont_dict.get(key), '')
          
        for key in None_allowed:
            self.assertTrue(cont_dict.has_key(key), "The key " + key + " wasn't found in the response.") 

        resp = self.client.get(prefix + 'kioskList/', {'beer': 'Hansa'})
        
#         BeerPrice.objects.filter()
#        TODO: filter the kiosk by brand an compare to given response
        
class KioskDetailsTests(TestCase):
    fixtures = ['test_data.json']
    def get_proper_response_index(self):
        i=1
        resp = self.client.get(prefix + 'kioskDetails/' + str(i) + '/')
           
        while resp.status_code == 404 and i < 20:
            i+=1
            resp = self.client.get(prefix + 'kioskDetails/' + str(i) + '/')
        return i
     
    def test_status_codes(self):
        resp1 = self.client.get(prefix + 'kioskDetails/' + str(self.get_proper_response_index()) + '/')
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(prefix + 'kioskDetails/' + str(self.get_proper_response_index()) + '/', {'ignore_text': 'ignore', 'ignore_num': '123'})
        self.assertEqual(resp2.status_code, 200)
        self.assertJSONEqual(resp1.content, resp2.content, 'The given ignore keys have not been ignored by the server! The two given responses are not equal.')
        proper_id = get_proper_response_index(self, 'kioskDetails')
        
        basic_status_code(self, 'kioskDetails/' + str(proper_id))
        
        resp1 = self.client.get(prefix + 'kioskDetails/' + str(proper_id - 1) + '/')
        self.assertEqual(resp1.status_code, 404)
        
    def test_response_content(self):
        resp = self.client.get(prefix + 'kioskDetails/' + str(get_proper_response_index(self, 'kioskDetails')) + '/')
        
        cont_dict = json.loads(resp.content)

        for key in ['image', 'beerPrice', 'comments', 'kiosk']:
            self.assertTrue(cont_dict.has_key(key), "The key " + key + " wasn't found in the response.")
             
        self.assertNotEqual(cont_dict.get('kiosk'), '[]', 'The given response does not contain a kiosk.')
        self.assertNotEqual(cont_dict.get('kiosk'), 'None', 'The given response does not contain a kiosk.')
        
        
        
class BeerTests(TestCase):
    fixtures = ['test_data.json']
    def test_status_codes(self):
        resp1 = self.client.get(prefix + 'beer/')
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(prefix + 'beer/', {'ignore_text': 'ignore', 'ignore_num': '123'})
        self.assertEqual(resp2.status_code, 200)
        self.assertJSONEqual(resp1.content, resp2.content, 'The given ignore keys have not been ignored by the server! The two given responses are not equal.')
        basic_status_code(self, 'beer')
        
        
        
class BeerPriceTests(TestCase):    
    def test_status_codes(self):
        basic_status_code(self, 'beerprice')
        
    def test_post_beerprice(self):
        from bier.models import BeerPrice
        proper_beer_id = get_proper_response_index(self, 'beer')
        proper_kiosk_id = get_proper_response_index(self, 'kiosk')
        
        resp = self.client.post(prefix + 'beerprice/', {'size': '0.5', 'beer': str(proper_beer_id), 'kiosk': str(proper_kiosk_id), 'price': '78', 'score': '156'})
        self.assertEqual(resp.status_code, 201, 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(resp.status_code))
        
        cont_dict = json.loads(resp.content) 
        b = BeerPrice.objects.filter(pk = cont_dict.get('id'))
        
        keys = ['beer_name', 'beer_location', 'beer_brand', 'id', 'size', 'kiosk', 'beer', 'price', 'score', 'created', 'modified']
        
        for key in keys:
            self.assertEqual(cont_dict.get(key), b.eval(key))
        
        self.assertEqual(cont_dict.get('kiosk'), proper_kiosk_id, 'The beerprice was not posted to the given kiosk!')
        self.assertEqual(cont_dict.get('beer'), proper_beer_id, 'The beerprice was not posted with the given beer!')
            
        resp = self.client.post(prefix + 'beerprice/', {'size': '0.5', 'beer': str(proper_beer_id - 1), 'kiosk': str(proper_kiosk_id), 'price': '78', 'score': '156'})
        self.assertEqual(resp.status_code, 400, 'POST request with a beer not existing was successful. expected: ' + str(400) + ' response: ' + str(resp.status_code))
        
        resp = self.client.post(prefix + 'beerprice/', {'size': '0.5', 'beer': str(proper_beer_id), 'kiosk': str(proper_kiosk_id), 'price': '1', 'score': '2'})
        self.assertEqual(resp.status_code, 400, 'POST request with a beer price of one cent was successful. expected: ' + str(400) + ' response: ' + str(resp.status_code))
        
class KioskTests(TestCase):
    def test_status_codes(self):
        basic_status_code(self, 'kiosk')
        
    def test_post_kiosk(self):
        from bier.models import Kiosk
        resp = self.client.post(prefix + 'kiosk/', {'street': 'Musterstra\u00dfe', 'city': 'Musterstadt', 'zip_code': '12345', 
                                                    'number': '123', 'geo_lat': '51.51', 'geo_long': '7.51'})
        self.assertEqual(resp.status_code, 201, 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(resp.status_code))
        
        cont_dict = json.loads(resp.content)
        k = Kiosk.objects.filter(pk = cont_dict.get('id'))
        
        keys = ['street', 'number', 'zip_code', 'city', 'name', 'description', 'owner', 'geo_lat', 'geo_long', 'is_valid_address', 'created']
        
        for key in keys:
            self.assertEqual(cont_dict.get(key), k.eval(key))
            
        resp = self.client.post(prefix + 'kiosk/', {'street': 'Musterstra\u00dfe', 'city': 'Musterstadt', 'zip_code': '12345', 
                                                    'number': '123', 'geo_lat': '51.51', 'geo_long': '7.51'})
        self.assertEqual(resp.status_code, 400, 'POST request with duplicate data was successfull.')
        
class ImageTests(TestCase):
    def test_status_code(self):
        basic_status_code(self, 'image')
        
    def test_post_image(self):
        from bier.models import Image
        resp = self.client.post(prefix + 'image/', {'path': 'C:/Users/Philipp/workspace/bierserver/media/do-test.gif'})
        self.assertEqual(resp.status_code, 201, 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(resp.status_code))
        
        cont_dict = json.loads(resp.content)
        i = Image.objects.filter(pk = cont_dict.get('id'))
        
        keys = ['imageUrl', 'thumbUrl', 'id', 'image', 'thumbnail']
        
        for key in keys:
            self.assertEqual(cont_dict.get(key), i.eval(key))
        
        resp = self.client.get(cont_dict.get('thumbUrl'))
        self.assertEqual(resp.status_code, 200)
        
class CommentTests(TestCase):
    def test_status_code(self):
        basic_status_code(self, 'comment')
        
    def test_post_comment(self):
        from bier.models import Comment
        resp = self.client.post(prefix + 'comment/', {'name': 'TestName', 'comment': 'test. test. 123.'})
        self.assertEqual(resp.status_code, 201, 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(resp.status_code))
        
        cont_dict = json.loads(resp.content)
        k = Comment.objects.filter(pk = cont_dict.get('id'))
        
        keys = ['id', 'name', 'comment', 'created']
        
        for key in keys:
            self.assertEqual(cont_dict.get(key), k.eval(key))
        
        
