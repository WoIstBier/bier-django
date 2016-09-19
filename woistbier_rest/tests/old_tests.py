# -*- coding: utf-8 -*-
from django.test import TestCase
import json

prefix = '/bier/rest/'



'''
This function looks up for some proper index
for which you can get positive response (<100, 200)

Return value is the first index that fits the requirements
'''
def get_proper_response_index(testcase, suffix):
        i = 1
        resp = testcase.client.get(prefix + suffix + '/' + str(i), follow = 1)

        while resp.status_code is not 200 and i < 100:
            if resp.status_code is 405:
                break
            i+=1
            resp = testcase.client.get(prefix + suffix + '/' + str(i), follow = 1)

        return i


'''
Check different status codes and JSON content delivered
for TESTCASE with given SUFFIX
'''
def basic_status_code(testcase, suffix):
    resp1 = testcase.client.get(prefix + suffix)
    testcase.assertEqual(resp1.status_code, 301, 'Server redirect did not give a proper response statuscode! expected: ' + str(301) + ' response: ' + str(resp1.status_code))

    resp1 = testcase.client.get(prefix + suffix, follow = 1)
    testcase.assertEqual(resp1.status_code, 200, 'URL = ' + prefix+suffix + 'Server redirect did not give a proper response statuscode! expected: ' + str(200) + ' response: ' + str(resp1.status_code))

    resp2 = testcase.client.get(prefix + suffix + '/')
    testcase.assertEqual(resp1.status_code, 200, 'Server redirect did not give a proper response statuscode! expected: ' + str(200) + ' response: ' + str(resp2.status_code))
    testcase.assertJSONEqual(resp1.content, resp2.content, 'The request redirect was not a proper redirect. The two responses are not equal.')

    resp2 = testcase.client.get(prefix + suffix + '/', {'ignore_text': 'ignore', 'ignore_num': 123})
    testcase.assertEqual(resp2.status_code, 200, 'The given ignore keys have not been ignored by the server! The two responses are not equal.')
    testcase.assertJSONEqual(resp1.content, resp2.content, 'The given ignore keys have not been ignored by the server! The two responses are not equal.')

class kioskListTests(TestCase):

    fixtures = ['test_data.json']

    def test_status_codes(self):
        print(str(1))
        basic_status_code(self, 'kioskList')

        resp1 = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.5 , 'geo_long': 7.5, 'radius': 5})
        self.assertEqual(resp1.status_code, 200)

        resp2 = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.5 , 'geo_long': 7.5, 'radius': 5, 'ignore_text': 'ignore', 'ignore_num': 123})
        msg = 'The given ignore keys have not been ignored by the API!'
        self.assertEqual(resp2.status_code, 200, msg)
        msg += 'The two responses are not equal.'
        self.assertJSONEqual(resp1.content, resp2.content, msg)

        resp1 = self.client.get(prefix + 'kioskList/', {'beer': 'Hansa'})
        self.assertEqual(resp1.status_code, 200)

        resp1 = self.client.get(prefix + 'kioskList/', {'geo_lat': '5a1.5' , 'geo_long': '7b.5', 'radius': 'c5'})
        self.assertEqual(resp1.status_code, 400)


    '''
    parameters for non existing beers. or lookup kiosks at tatooine
    '''
    def test_distance_and_empty_response(self):
        print(str(2))
        resp = self.client.get(prefix + 'kioskList/', {'geo_lat': 0.2 , 'geo_long': -176.5, 'radius': 5})
        self.assertEqual(resp.content, '[]', 'We got a kiosk on Baker Island!')

        #request with a non-existent beer
        response  = self.client.get(prefix + 'kioskList/', {'beer': 'gibtsnichtbier'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')

        #mos espa coordinates tunisia
        response  = self.client.get(prefix + "kioskList/", {'geo_lat': 33.994296, 'geo_long': 7.842677})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]', 'We got a kiosk on tatooine!')

        #test radius too small
        response  = self.client.get(prefix + "kioskList/?radius=0.01&geo_lat=51.53533&geo_long=7.48700")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')

    def test_response_content(self):
        print(str(3))
        None_notallowed = ['kiosk', 'distance']
        None_allowed    = ['beerPrice', 'image']

        resp = self.client.get(prefix + 'kioskList/', {'geo_lat': 51.53 , 'geo_long': 7.45, 'radius': 5})
        self.assertTrue(resp, "Response from KioskList was empty FFS")

        kiosk_list = json.loads(resp.content)
        for kiosk in kiosk_list:
            self.assertGreaterEqual(5, kiosk.get('distance'), 'The distance is greater than the given radius!')
            for key in None_notallowed:
                self.assertTrue(kiosk.has_key(key), "The key " + key + " wasn't found in the response.")
                self.assertNotEqual(kiosk.get(key), None)
                self.assertNotEqual(kiosk.get(key), '')

            for key in None_allowed:
                self.assertTrue(kiosk.has_key(key), "The key " + key + " wasn't found in the response.")

        resp = self.client.get(prefix + 'kioskList/', {'beer': 'Hansa'})

        cont_dict = json.loads(resp.content)
        for kiosk in cont_dict:
            self.assertTrue(kiosk.get('beerPrice').get('beer_name').__contains__('Hansa')  )
#             self.assertTrue( (kiosk.get('beerPrice.beer_name')).__contains__('Hansa'))


class KioskDetailsTests(TestCase):
    fixtures = ['test_data.json']

    def test_status_codes(self):
        print(str(4))
        proper_id = get_proper_response_index(self, 'kioskDetails')
        basic_status_code(self, 'kioskDetails/' + str(proper_id))

        resp1 = self.client.get(prefix + 'kioskDetails/' + str(proper_id - 1) + '/')
        self.assertEqual(resp1.status_code, 404)

    def test_response_content(self):
        print(str(5))
        resp = self.client.get(prefix + 'kioskDetails/' + str(get_proper_response_index(self, 'kioskDetails')) + '/')

        cont_dict = json.loads(resp.content)

        for key in ['images', 'beerPrices', 'comments', 'kiosk']:
            self.assertTrue(cont_dict.has_key(key), "The key " + key + " wasn't found in the response.")

        msg = 'The given response does not contain a kiosk.'
        self.assertNotEqual(cont_dict.get('kiosk'), '[]', msg)
        self.assertNotEqual(cont_dict.get('kiosk'), None, msg)



class BeerTests(TestCase):
    fixtures = ['test_data.json']

    def test_status_codes(self):
        print(str(6))
        basic_status_code(self, 'beer')

'''
A testcase to check various limits on the beerprice models
'''
class BeerPriceTests(TestCase):

    fixtures = ['test_data.json']

    def test_status_codes(self):
        print(str(7))
        basic_status_code(self, 'beerprice')

        resp = self.client.post(prefix + 'beerprice/', {'kiosk': '12312312321321', 'size': '0.7', 'beer': '7',  'price': '128' })
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(400) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 400, msg)

        resp = self.client.post(prefix + 'beerprice/', {'size': '0.7', 'beer': '7',  'price': '128' })
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(400) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 400, msg)

    def test_edit_beerprice(self):
        print(str(17))
        proper_beer_id = get_proper_response_index(self, 'beer')
        proper_kiosk_id = get_proper_response_index(self, 'kiosk')
        proper_beerprice_id = get_proper_response_index(self, 'beerprice')
        data=json.dumps({'kiosk': str(proper_kiosk_id), 'size': '0.7', 'beer': str(proper_beer_id),  'price': '128' })
        #print('kiosk id: ' + str(proper_kiosk_id) + '  beerprice id' + str(proper_beerprice_id) + ' beer id : ' + str(proper_beer_id))

        resp = self.client.put(prefix + 'beerprice/' + str(proper_beerprice_id) + '/', data, content_type='application/json')
        msg = 'PUT request was unsuccessful for some reason. expected: ' + str(200) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 200, msg)

        before_dict = json.loads(resp.content)
        self.assertEqual(str(before_dict.get('size')), '0.7')
        self.assertEqual(str(before_dict.get('price')), '128')

        data=json.dumps({'kiosk': str(proper_kiosk_id), 'size': '1.0', 'beer': str(proper_beer_id),  'price': '110' })
        resp = self.client.put(prefix + 'beerprice/' + str(proper_beerprice_id)  + '/', data, content_type='application/json')
        msg = 'PUT request was unsuccessful for some reason. expected: ' + str(200) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 200, msg)

        before_dict = json.loads(resp.content)
        self.assertEqual(str(before_dict.get('size')), '1.0')
        self.assertEqual(str(before_dict.get('price')), '110')

    def test_post_beerprice(self):
        print(str(8))
        from woistbier_rest.models import BeerPrice
        proper_beer_id = get_proper_response_index(self, 'beer')
        proper_kiosk_id = get_proper_response_index(self, 'kiosk')

        resp = self.client.post(prefix + 'beerprice/', {'kiosk': str(proper_kiosk_id), 'size': '0.7', 'beer': str(proper_beer_id),  'price': '128' })
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 201, msg)

        cont_dict = json.loads(resp.content)

        b = BeerPrice.objects.get(pk = cont_dict.get('id'))

        keys = ['id', 'size',  'price', 'score']

        for key in keys:
            self.assertEqual(str(cont_dict.get(key)), str(getattr(b, key)))

#         b_created = str(getattr(b, 'created'))[:10] + 'T' + str(getattr(b, 'created'))[11:23] + 'Z'
#         b_modified = str(getattr(b, 'modified'))[:10] + 'T' + str(getattr(b, 'modified'))[11:23] + 'Z'
#
#         self.assertEqual(cont_dict.get('created'), b_created)
#         self.assertEqual(cont_dict.get('modified'), b_modified)

        self.assertEqual(cont_dict.get('kiosk'), proper_kiosk_id, 'The beerprice was not posted to the given kiosk!')
        self.assertEqual(cont_dict.get('beer'), proper_beer_id, 'The beerprice was not posted with the given beer!')

        resp = self.client.post(prefix + 'beerprice/', {'size': '0.5', 'beer': str(proper_beer_id - 1), 'kiosk': str(proper_kiosk_id), 'price': '78'})
        msg = 'POST request with a beer not existing was successful. expected: ' + str(400) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 400, msg)

        resp = self.client.post(prefix + 'beerprice/', {'size': '0.5', 'beer': str(proper_beer_id), 'kiosk': str(proper_kiosk_id), 'price': '1'})
        msg = 'POST request with a beer price of one cent was successful. expected: ' + str(400) + ' response: ' + str(resp.status_code) + str(resp)
        #self.assertEqual(resp.status_code, 400, msg)


class KioskTests(TestCase):
    fixtures = ['test_data.json']

    def test_status_codes(self):
        print(str(9))
        basic_status_code(self, 'kiosk')

    def test_post_kiosk(self):
        print(str(10))
        from woistbier_rest.models import Kiosk
        resp = self.client.post(prefix + 'kiosk/', {'street': 'Musterstrasse', 'city': 'Musterstadt', 'zip_code': '12345',
                                                    'number': '123', 'geo_lat': '51.51', 'geo_long': '7.51'})
        self.assertEqual(resp.status_code, 201, 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(resp.status_code)+ str(resp))

        cont_dict = json.loads(resp.content)
        k = Kiosk.objects.get(pk = cont_dict.get('id'))

        keys = ['street', 'number', 'zip_code', 'city', 'name', 'description', 'owner', 'geo_lat', 'geo_long', 'is_valid_address']

        for key in keys:
            expectedValue = None
            responseValue = None
            try:
                expectedValue = float(cont_dict.get(key))
                responseValue = float(getattr(k, key))
            except  (ValueError, TypeError):
                expectedValue = str(cont_dict.get(key))
                responseValue = str(getattr(k, key))

            self.assertEqual(expectedValue, responseValue)

#         k_created = str(getattr(k, 'created'))[:10] + 'T' + str(getattr(k, 'created'))[11:23] + 'Z'
#         self.assertEqual(cont_dict.get('created'), k_created)

        resp = self.client.post(prefix + 'kiosk/', {'street': 'Musterstrasse', 'city': 'Musterstadt', 'zip_code': '12345',
                                                    'number': '123', 'geo_lat': '51.51', 'geo_long': '7.51'})
        self.assertEqual(resp.status_code, 400, 'POST request with duplicate data was successfull.')


class ImageTests(TestCase):
    fixtures = ['test_data.json']

    def test_status_code(self):
        print(str(11))
        basic_status_code(self, 'image')

        from PIL import Image as PIL
        from StringIO import StringIO

        file_obj = StringIO()
        image = PIL.open('./woistbier_rest/fixtures/unittest_test_image_4311.jpeg')
        image.save(file_obj, 'jpeg')
        file_obj.name = 'test.jpg'
        file_obj.seek(0)
        resp = self.client.post(prefix + 'image/', {'kiosk':'123123123123123', 'image': file_obj})
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(400) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 400, msg)

        resp = self.client.post(prefix + 'image/', {'image': file_obj})
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(400) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 400, msg)

    def test_post_image(self):
        print(str(12))
        from PIL import Image as PIL
        from StringIO import StringIO

        file_obj = StringIO()
        image = PIL.open('./woistbier_rest/fixtures/unittest_test_image_4311.jpeg')
        image.save(file_obj, 'jpeg')
        file_obj.name = 'test.png'
        file_obj.seek(0)

        proper_kiosk_id = get_proper_response_index(self, 'kiosk')
        resp = self.client.post(prefix + 'image/', {'kiosk':str(proper_kiosk_id), 'image': file_obj})
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(resp.status_code) + str(resp)
        self.assertEqual(resp.status_code, 201, msg)

        image_response = json.loads(resp.content)
        #this is either a list if it contains more than one image. or its a dict.
        self.assertFalse(isinstance(image_response, list), "Posting an image returned more than one image")
        keys = ['kiosk', 'image']
        for key in keys:
            self.assertTrue(image_response.has_key(key), "The key " + key + " wasn't found in the response.")
        #self.assertEqual(resp.status_code, 200)
    def test_response_content(self):
        print(str(13))
        keys = ['kiosk', 'thumbnail_url', 'gallery_url']

        resp = self.client.get(prefix + 'image/')
        self.assertTrue(resp, "Response from imageList was empty FFS")

        image_list = json.loads(resp.content)
        for img in image_list:
            for key in keys:
                self.assertTrue(img.has_key(key), "The key " + key + " wasn't found in the response.")

    def test_regression_7_6(self):
        print(str(14))
        resp = self.client.get(prefix + 'image/')
        self.assertTrue(resp, "Response from imageList was empty FFS")

        image_list = json.loads(resp.content)
        id_set = set()
        for img in image_list:
            id_set.add(img.get("kiosk"))
        self.assertTrue(len(id_set) > 1, "Only images for 1 kiosk returned")

class CommentTests(TestCase):
    fixtures = ['test_data.json']

    def test_status_code(self):
        print(str(15))
        basic_status_code(self, 'comment')
        resp = self.client.post(prefix + 'comment/', {'kiosk':'123123123123123123', 'name': 'TestName', 'comment': 'test. test. 123.'})
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(400) + ' response: ' + str(resp.status_code)+ str(resp)
        self.assertEqual(resp.status_code, 400, msg)


        resp = self.client.post(prefix + 'comment/', {'name': 'TestName', 'comment': 'test. test. 123.'})
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(400) + ' response: ' + str(resp.status_code)+ str(resp)
        self.assertEqual(resp.status_code, 400, msg)

    def test_post_comment(self):
        print(str(16))
        from woistbier_rest.models import Comment
        proper_kiosk_id = get_proper_response_index(self, 'kiosk')

        resp = self.client.post(prefix + 'comment/', {'kiosk':str(proper_kiosk_id), 'name': 'TestName', 'comment': 'test. test. 123.'})
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(resp.status_code)+ str(resp)
        self.assertEqual(resp.status_code, 201, msg)

        cont_dict = json.loads(resp.content)
        c = Comment.objects.get(pk = cont_dict.get('id'))

        keys = ['id', 'name', 'comment']

        for key in keys:
            self.assertEqual(str(cont_dict.get(key)),str(getattr(c, key)))





#         c_created = str(getattr(c, 'created'))[:10] + 'T' + str(getattr(c, 'created'))[11:23] + 'Z'
#         self.assertEqual(cont_dict.get('created'), c_created)
