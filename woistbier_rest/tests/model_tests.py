# -*- coding: utf-8 -*-
from django.test import TestCase
import json
from woistbier_rest.models import Kiosk

prefix = '/bier/rest/'

'''
Tests for the kioskmodel. 
'''
class KiokModellTest(TestCase):
    #post one kiosk with street and number to the db
    def post_kiosk_and_get_resulting_kiosk(self, street, number):
        resp = self.client.post(prefix + 'kiosk/', {'street': 
            street, 'city': 'Musterstadt', 'zip_code': '12345', 
            'number': number, 'geo_lat': '51.51', 'geo_long': '7.51'})
        cont_dict = json.loads(resp.content)
        k = Kiosk.objects.get(pk = cont_dict.get('id'))
        return k
    
    #suppose the admin want sto change the addres of the kiosk. The name should change as well
    def test_kiosk_save(self):
        #create a new kiosk isntance and save it to the db
        kiosk = self.post_kiosk_and_get_resulting_kiosk( 'TestStraße', 12)

        self.assertEqual(unicode(kiosk.street).encode('utf-8'), 'TestStraße')
        self.assertEqual(kiosk.number, 12)
        self.assertEqual(unicode(kiosk.name).encode('utf-8'), 'TestStraße' + ' ' + str(12))

        #now change street name and number
        kiosk.street = 'AndereStraße'
        kiosk.number = 32

        self.assertEqual(kiosk.street, 'AndereStraße')
        self.assertEqual(kiosk.number, 32)
        #the kiosk.name will change on calling the save method
        self.assertNotEqual(unicode(kiosk.name).encode('utf-8'), 'AndereStraße' + str(32))
        
        kiosk.save()

        self.assertEqual(kiosk.name, 'AndereStraße' + ' ' + str(32))



