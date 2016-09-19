# -*- coding: utf-8 -*-
from django.test import TestCase
#import json

prefix = '/bier/rest/'


class ViewTests(TestCase):

    def test_radian_conversion(self):
        import woistbier_rest.views as v
        print('Test radian conversion')
        #testing for value 0
        angle_in_radians = v.radians(0)
        self.assertEqual(angle_in_radians, 0)

        #test for value 90
        angle_in_radians = v.radians(90)
        #self.assertEqual(angle_in_radians, 3.1415/2.0)
        self.assertAlmostEqual(angle_in_radians, 3.1415/2.0, places=4)
