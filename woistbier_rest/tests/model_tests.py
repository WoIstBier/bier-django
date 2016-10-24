# -*- coding: utf-8 -*-
from django.test import TestCase
import json
from woistbier_rest.models import Kiosk, BeerPrice, Beer

prefix = '/bier/rest/'


#create a dummy kiosk
def create_dummy_kiosk(street='musterstraße', number=123, city='Dortmund' ):
    kiosk = Kiosk()
    kiosk.street = street
    kiosk.number = number
    kiosk.city = city
    kiosk.save()
    return kiosk


def create_dummy_beer(name='Geiles Bier', brew='Pils', location='Dortmund'):
    beer = Beer(name=name, brew=brew, location=location)
    beer.save()
    return beer


'''
Tests for the kioskmodel.
'''


class KioskModelTest(TestCase):

    #suppose the admin want sto change the addres of the kiosk. The name should change as well
    def test_kiosk_save(self):
        #create a new kiosk isntance and save it to the db
        #kiosk = self.post_kiosk_and_get_resulting_kiosk('TestStraße', 12)
        kiosk = create_dummy_kiosk(street='Bierstraße', number=123)
        self.assertEqual(kiosk.name, 'Bierstraße' + ' ' + str(123))

        #now change street name and number
        kiosk.name = 'Dem Horst Sein Kiosk'
        kiosk.save()

        self.assertEqual(kiosk.name, 'Dem Horst Sein Kiosk')


class BeerPriceTest(TestCase):

    def test_save_beerprice(self):
        #create a dummy object
        kiosk = create_dummy_kiosk()
        beer = create_dummy_beer()

        beer_price = BeerPrice()
        beer_price.beer = beer
        beer_price.price = 120
        beer_price.size = 0.5
        beer_price.kiosk = kiosk
        beer_price.save()

        self.assertEquals(beer_price.score, beer_price.price/beer_price.size,
                          'Score not correctly computed. Its '+str(beer_price.score)
                          + ' but it should be  ' + str(beer_price.price/beer_price.size))
