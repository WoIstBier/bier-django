'''
Created on Mar 30, 2013

@author: mackaiver
'''
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bier.models import Kiosk
import logging
log = logging.getLogger(__name__)
@receiver(pre_save, sender=Kiosk)
def kiosk_signal_handler(sender, **kwargs):
    log.debug("Pre Save method on kiosk model recieved")
    for key, value in kwargs.iteritems():
        log.debug( "kwargs in signal:  %s = %s" % (key, value))