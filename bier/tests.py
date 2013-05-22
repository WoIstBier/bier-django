"""
These will pass when you run "manage.py test".

"""
from django.test import TestCase
from django.test import Client

urlprefix = '/bier/rest/'
prefix = '/bier/rest/'
fixtures = ['test_data.json']
class KioskListTest(TestCase):
    fixtures = ['test_data.json']
    client = Client()
        
    def test_status_codes(self):
        resp1 = self.client.get(prefix + 'kioskList/')
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(prefix + 'kioskList/', {'ignore_text': 'ignore', 'ignore_num': 123})
        self.assertEqual(resp2.status_code, 200, 'The given ignore keys have not been ignored by the server!')
        self.assertJSONEqual(resp1.content, resp2.content)
        
        resp1 = self.client.get(prefix + "kioskList")
        self.assertEqual(resp1.status_code , 301)
        
        resp1 = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.5 , 'geo_long': 7.5, 'radius': 5})
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.5 , 'geo_long': 7.5, 'radius': 5, 'ignore_text': 'ignore', 'ignore_num': 123})
        self.assertEqual(resp2.status_code, 200, 'The given ignore keys have not been ignored by the server!')
        self.assertJSONEqual(resp1.content, resp2.content, 'The given ignore keys have not been ignored by the server! The two given responses are not equal.')
        
        resp2 = self.client.get(prefix + 'kioskList/', {'geo_lat': '5a0' , 'geo_long': '5b0', 'radius': 'c5'})
        self.assertEqual(resp2.status_code, 400)
        
        response  = self.client.get(urlprefix + "kioskList/?geo_lat=123a.23434")
        self.assertEqual(response.status_code, 400)
        response  = self.client.get(urlprefix + "kioskList/?geo_long=123.23434a")
        self.assertEqual(response.status_code, 400)
        
    ''' parameters for non existing beers. or lookup kiosks at tatoine'''
    def test_distance_and_empty_response(self):
        resp = self.client.get(prefix + 'kioskList/', {'geo_lat': 0.2 , 'geo_long': -176.5, 'radius': 5})
        self.assertEqual(resp.content, '[]', 'We got a Kiosk on Baker Island!')
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

    def test_response_content(self):
          
        None_notallowed = ['kioskName', 'kioskStreet', 'kioskCity', 'kioskPostalCode', 'kioskNumber', 'distance']
        None_allowed    = ['beerName', 'beerBrew', 'beerSize', 'beerPrice', 'thumb_path']
          
        resp = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.5 , 'geo_long': 7.5, 'radius': 5})
          
        cont_dict = eval(resp.content.replace('null', 'None'))[1]   
        #print(cont_dict)
        self.assertGreaterEqual(5, cont_dict.get('distance'), 'The distance is greater than the given radius!')
          
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
         
#         resp1 = self.client.get(prefix + 'kioskDetails/' + str(self.get_proper_response_index() - 1) + '/')
#         self.assertEqual(resp1.status_code, 404)
         
    def test_response_content(self):
        resp = self.client.get(prefix + 'kioskDetails/' + str(2) + '/')
         
        cont_dict = eval(resp.content.replace('null', 'None').replace('true', '1'))
         
        for key in ['images', 'beerPrices', 'comments', 'kiosk']:
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
    
