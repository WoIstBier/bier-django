'''
Created on 23.02.2013

@author: DerDans
'''
import urllib
import urllib2
from django.utils import simplejson as json
 
def get_geo(address):
    address = urllib.quote(address)
#    url = "http://maps.google.com/maps/geo?q=%s&output=json&oe=utf8&sensor=true_or_false&key=12345" % (address)
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (address)
    data = urllib2.urlopen(url)
    obj = json.loads( data.read() )
    if obj['Status']['code'] == 200:
        data = obj['Placemark'][0]['Point']['coordinates']
    else:
        raise Exception('Invalid address')
    return data