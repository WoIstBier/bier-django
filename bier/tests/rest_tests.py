# -*- coding: utf-8 -*-
from django.test import TestCase
#import json
import logging
from django.conf import settings
import os
import json
#import sys
log = logging.getLogger(__name__)

prefix = '/bier/rest/'

def get_image_path_from_response(resp):
    image_response = json.loads(resp.content)
    img = image_response.get('image')
    print(img)
    path = os.path.abspath(os.path.join(settings.MEDIA_ROOT,img))
    print(path)
    return path

def get_kiosk_id():
    from bier.models import Kiosk
    kiosk = Kiosk.objects.all()[:1].get()
    print(str(kiosk))
    return kiosk.id

def post_image(client,kioskId):
    from PIL import Image as PIL
    from StringIO import StringIO
        
    file_obj = StringIO()
    image = PIL.open('./bier/fixtures/test.jpeg')
    image.save(file_obj, 'jpeg')
    file_obj.name = 'test.jpg'
    file_obj.seek(0)

    resp = client.post(prefix + 'image/', {'kiosk':str(kioskId), 'image': file_obj})
    return resp

class ImageTests(TestCase):
    fixtures = ['test_data.json']

    def test_non_existing_image(self):
        kioskId = get_kiosk_id()
        resp = post_image(self.client, kioskId)
        self.assertEqual(resp.status_code, 201)
        #path = get_image_path_from_response(resp)

        #get some kioskdetails for that kiosk
        resp = self.client.get(prefix + 'kioskDetails/' + str(kioskId) + '/')
        self.assertEqual(resp.status_code, 200)
        #and the image list
        resp = self.client.get(prefix + 'image/?kiosk=' + str(kioskId))
        self.assertEqual(resp.status_code, 200)

        # #log.info(path)
        # filename = os.path.basename(path).decode('utf-8').encode("latin-1")
        # #filename.decode('utf-8').encode("latin-1")
        # log.info('filename is ' + repr(filename))
        # #os.remove(unicode(path))
        # filename = os.path.splitext(filename)[0]

        # filename = filename + '640x480_q85_crop-smart.jpg'
        # folder = os.path.dirname(path).decode('utf-8').encode("latin-1")
        # log.info('folder  is ' + repr(folder))
        # #log.info('Removing ' +  os.join(folder, filename))
        # path = folder + '/' +filename
        # log.info('Removing ' +  folder + '/' +filename)
        # os.remove(path.decode('utf-8').encode("latin-1"))

        # #get some kioskdetails for that kiosk
        # resp = self.client.get(prefix + 'kioskDetails/' + str(kioskId) + '/')
        # self.assertEqual(resp.status_code, 200)
        # #and the image list
        # resp = self.client.get(prefix + 'image/?kiosk=' + str(kioskId))
        # self.assertEqual(resp.status_code, 200)
        #now remove the image and its thumbs
        #folder = os.path.dirname(path)
        #log.info('Folder_ : ' + folder )
        #filename = os.path.basename(path)
        #os.remove(unicode(path))
        #filename = os.path.splitext(filename)[0]
        #log.info('name is: ' + filename )
        #log.info(settings.THUMBNAIL_ALIASES[0].get('medium'))
        
    #     #os.listdir(folder)

    #     #print('asdasdas ')
    #     folder = unicode(folder)
    #     log.info(sys.getfilesystemencoding())
    #     log.info(os.listdir(u'/home/mackaiver/workspace/bier_server/images'))
    #     log.info('asdasdasdasd')
    #     # for f in os.listdir(folder):
    #     #     pass
    #             #log.info(str(f))
    #         # for imgFile in os.listdir(folder):
    #         #     file_path = os.path.join(folder, imgFile)
    #         #     if imgFile.startswith(filename):
    #         #         pass




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
 

