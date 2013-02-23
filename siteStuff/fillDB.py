from bier.models import Kiosk, BierPreisListe
def fillIt():
    k1 = Kiosk(name='Lecker,Lecker',address='kleppingstrasse 3 dortmund',owner='guenther')
    k1.save()
    k2 = Kiosk(name='Grosse Tueten',address='vosskuhle dortmund',owner='henriette')
    k2.save()
    k3 = Kiosk(name='Guter Kiosk',address='brueggstrasse dortmund',owner='harkan')
    k3.save()
    k4 = Kiosk(name='Der Kiosk',address='muensterstrasse dortmund',owner='hans werner')
    k4.save()
    
    b1 = BierPreisListe(kiosk=k1, name='Hansa', price='80',date='2013-02-01')
    b1.save()
    b2 = BierPreisListe(kiosk=k1, name='Paderberg', price='99',date='2012-07-15')
    b2.save()
    b3 = BierPreisListe(kiosk=k2, name='gerolsteinerMitSchuss', price='120',date='2011-08-30')
    b3.save()