from bier.models import Kiosk, BeerPrice, Beer
def fillIt():
    k1 = Kiosk(name='Lecker',street='kleppingstraße', number='3', zip_code = '44135', city='dortmund',owner='guenther')
    k1.save()
    k2 = Kiosk(name='Brückstraßen Kiosk',street='Brückstraße', zip_code = '44135', number='39', city='dortmund',owner='guenther')
    k2.save()
    k3 = Kiosk(name='Guter Kiosk',street='Mallinckrodtstr',zip_code = '44145', number='118', city='dortmund',owner='hakan')
    k3.save()
    k4 = Kiosk(name='Ein Kiosk',street='Hauptstr', number='105', city='dortmund',owner='guenther')
    k4.save()
    
    b1 = Beer(name='Hansa', brand='redeberger Gruppe', location='dortmund')
    b2 = Beer(name='Paderbverg', brand='Krombacher', location='dortmund')
    b3 = Beer(name='Kronen Export', brand='Kronen', location='dortmund')
    b4 = Beer(name='Kronen Pils', brand='Kronen', location='dortmund')
    b1.save()
    b2.save()
    b3.save()
    b4.save()
    
    p1 = BeerPrice(kiosk=k1, name=b1 , price='80',date='2013-02-01')
    p2 = BeerPrice(kiosk=k1, name=b2 , price='90',date='2013-02-01')
    p3 = BeerPrice(kiosk=k1, name=b3 , price='70',date='2013-02-01')
    p4 = BeerPrice(kiosk=k2, name=b1 , price='80',date='2013-02-01')
    p5 = BeerPrice(kiosk=k2, name=b3 , price='80',date='2013-02-01')
    p6 = BeerPrice(kiosk=k2, name=b4 , price='80',date='2013-02-01')
    p7 = BeerPrice(kiosk=k3, name=b4 , price='80',date='2013-02-01')
    p8 = BeerPrice(kiosk=k3, name=b1 , price='80',date='2013-02-01')
    p9 = BeerPrice(kiosk=k4, name=b2 , price='80',date='2013-02-01')
    p1.save();
    p2.save();
    p3.save();
    p4.save();
    p5.save();
    p6.save();
    p7.save();
    p8.save();
    p9.save();
    
    
             