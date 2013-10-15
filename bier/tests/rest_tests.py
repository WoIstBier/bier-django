# -*- coding: utf-8 -*-
import os
import logging
import json
from django.test import TestCase
from django.conf import settings

prefix = '/bier/rest/'
log = logging.getLogger(__name__)

def get_image_path_from_response(resp):
    image_response = json.loads(resp.content)
    img = image_response.get('image')
    #print(img)
    path = os.path.abspath(os.path.join(settings.MEDIA_ROOT,img))
    #print(path)
    return path

def get_kiosk_id():
    from bier.models import Kiosk
    kiosk = Kiosk.objects.all()[:1].get()
    print(str(kiosk))
    return kiosk.id

def post_kiosk(client, number):
    return client.post(prefix + 'kiosk/', {'street': 'Musterstrasse', 'city': 'Musterstadt', 'zip_code': '12345', 
                                                    'number': number, 'geo_lat': '51.51', 'geo_long': '7.51'})

def post_image(client,kioskId):
    #from PIL import Image as PIL
    #from StringIO import StringIO
    
    with open('./bier/fixtures/unittest_test_image_4311.jpeg', 'r') as f:
        #read_data = f.read()
        resp = client.post(prefix + 'image/', {'kiosk':str(kioskId), 'image': f})

    #file_obj = StringIO()
    #image = PIL.open('./bier/fixtures/test.jpeg')
    #image.save(f, 'jpeg')
    #file_obj.name = 'test.jpg'
    #file_obj.seek(0)

    return resp

def remove_files_with_prefix_in_folder(prefix, folder):
    #log.info('path is: ' + str(folder))
    #log.info('name is: ' + filename )
    for t in os.listdir(folder):
        #log.info(str(t))
        if t.startswith(prefix):
            #log.info('removing file: ' + os.path.join(folder,t))
            os.remove(os.path.join(folder,t))

class KioskTests(TestCase):
    fixtures  = ['test_data.json']

    def test_post_kiosk(self):
        #post a kiosk and check the return code
        resp = post_kiosk(self.client, 42)
        self.assertEqual(resp.status_code, 201)
        #check if its really there. That means getting the id of the kiosk in the response
        #and make a get reqeust for it. this wont reutrn a kiosk but a kioskdetailthingy
        kiosk = json.loads(resp.content)
        resp = self.client.get(prefix + 'kioskDetails/' + str(kiosk.get('id')) + '/')
        self.assertEqual(resp.status_code, 200)
        #get the kiosk from the detaisl dict thingy
        kiosk = json.loads(resp.content).get('kiosk')
        self.assertTrue(kiosk.get('id') > 0)


class ImageTests(TestCase):
    fixtures = ['test_data.json']
    # test if the imagelist in the (images/?kiosk=bla) view is the same as the one deliverd in the kioskdetail view 
    def test_imagelists(self):
        #post a new empty kiosk
        resp = post_kiosk(self.client, 137)
        kiosk = json.loads(resp.content)
        kiosk_id = str(kiosk.get('id'))
        #post a number of images
        for num in range(1,6):
            post_image(self.client, kiosk_id)
            resp = self.client.get(prefix + 'image/?kiosk=' + kiosk_id)
            images_from_view = json.loads(resp.content)
            #log.info(str(images))
            #thers should be the posted amount of images in here
            self.assertTrue(len(images_from_view) == num )
            
            resp = self.client.get(prefix + 'kioskDetails/' + kiosk_id + '/')
            self.assertEqual(resp.status_code, 200)
            #get the kiosk from the detaisl dict thingy
            images_from_kiosk = json.loads(resp.content).get('images')
            self.assertItemsEqual(images_from_view, images_from_kiosk, 'Image lists in the image and the kioskdetails view were not the same')
            #log.info(str(images))






    def test_post_images(self):
        #post a kiosk and get the list of images for its id. This list should be empty for a new kiosk
        resp = post_kiosk(self.client, 137)
        kiosk = json.loads(resp.content)

        resp = self.client.get(prefix + 'image/?kiosk=' + str(kiosk.get('id')))
        images = json.loads(resp.content)
        self.assertEquals(images, [])
        #now post an image to the kiosk and check if the list contains 1 image
        post_image(self.client, kiosk.get('id'))
        resp = self.client.get(prefix + 'image/?kiosk=' + str(kiosk.get('id')))
        images = json.loads(resp.content)
        #log.info(str(images))
        self.assertTrue(len(images) == 1 )


    def test_missing_images(self):
        kioskId = get_kiosk_id()
        #post an image and save the path to it
        resp = post_image(self.client, kioskId)
        path = get_image_path_from_response(resp)

        #get some kioskdetails for that kiosk
        resp = self.client.get(prefix + 'kioskDetails/' + str(kioskId) + '/')
        self.assertEqual(resp.status_code, 200)
        #and the image list
        resp = self.client.get(prefix + 'image/?kiosk=' + str(kioskId))
        self.assertEqual(resp.status_code, 200)

        #now remove the generated image files
        folder = os.path.dirname(path)
        filename = os.path.basename(path)
        filename = os.path.splitext(filename)[0]
        remove_files_with_prefix_in_folder(filename, folder)
        #and try to load views again
        resp = self.client.get(prefix + 'kioskDetails/' + str(kioskId) + '/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(prefix + 'image/?kiosk=' + str(kioskId))
        self.assertEqual(resp.status_code, 200)

    def test_cleanup_images(self):

        path = os.path.join(os.path.abspath(settings.MEDIA_ROOT), 'images')
        #now remove the generated image files
        log.info('Removing files in folder: ' +str(path))
        remove_files_with_prefix_in_folder('unittest_test_image_4311', path)



'''
A testcase to check wether the limits imposed on beerprice are working
'''
class BeerPriceTests(TestCase):
    fixtures = ['test_data.json']

    #a function for a valid beer
    def test_post_beer_price(self):
        kioskId = get_kiosk_id()
        response = self.client.post(prefix + 'beerprice/', {'kiosk': kioskId, 'size': '0.33', 'beer': '8',  'price': '100' })
        msg = 'POST request was unsuccessful for some reason. expected: ' + str(201) + ' response: ' + str(response.status_code) + str(response)
        self.assertEqual(response.status_code, 201, msg)

    def test_post_invalid_beer_price(self):
        kioskId = get_kiosk_id()

        #price too low
        response = self.client.post(prefix + 'beerprice/', {'kiosk': kioskId, 'size': '0.33', 'beer': '6',  'price': '5' })
        msg = 'POST request was succesful. rice was too low expected: ' + str(400) + ' response: ' + str(response.status_code) + str(response)
        self.assertEqual(response.status_code, 400, msg)
        #price too high
        response = self.client.post(prefix + 'beerprice/', {'kiosk': kioskId, 'size': '0.7', 'beer': '6',  'price': '405' })
        msg = 'POST request was succesful. Price was too damn high expected' + str(400) + ' response: ' + str(response.status_code) + str(response)
        self.assertEqual(response.status_code, 400, msg)


'''
A test to check wether the throttling of the rest api works
'''
class RestThrottleTests(TestCase):
    fixtures = ['test_data.json']
    
    #post one kiosk with street and number to the db
    def post_kiosk(self, street, number):
        resp = self.client.post(prefix + 'kiosk/', {'street': 
            street, 'city': 'Musterstadt', 'zip_code': '12345', 
            'number': number, 'geo_lat': '51.51', 'geo_long': '7.51'})
        return resp.status_code
    
    def test_kiosk_addition_throttle(self):
        print('throttle test add kiosk 1 ')
        import time
        from bier.models import Kiosk
        #lets get a count of kioske 
        number = Kiosk.objects.count()
        statuscode = 201
        i = 1
        starttime = time.time()
        #lets have a loop posting kioske and sleep for a bit each time
        while statuscode is 201 and i <= 15:
            statuscode = self.post_kiosk('langestraße', i)
            # time.sleep(0.1)
            i = i + 1
        #elapsed time should be below the limit set by the throttle
        elapsed = time.time() - starttime
        #print('last statuscode was: ' +  str(statuscode))
        number = Kiosk.objects.count() - number
        if(number > 10 and  elapsed < 60):
            self.fail('Too many kiosks posted. Elapsed time was: ' + str(elapsed) + ' and ' + str(number) + ' kiosk have been posted')
        self.assertEqual(statuscode, 429 , 'Expected a too many requests statuscode (429) but its: '  + str(statuscode) + '      ' + str(number) + ' kiosks have been posted')
        #we cant test the exact number of posted kioske here. Since other tests also post stuff.
        #self.assertEqual(number, 10)
 

