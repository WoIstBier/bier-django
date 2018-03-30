import logging
import json
from django.test import TestCase

prefix = '/bier/rest/'
log = logging.getLogger(__name__)

FIXTURES = ['dump_13_11_2016.json']



def get_kiosk_id():
    from woistbier_rest.models import Kiosk
    kiosk = Kiosk.objects.all()[:1].get()
    return kiosk.id

# def post_kiosk(client, number):
#     return client.post(prefix + 'kiosk/', {'street': 'Musterstrasse', 'city': 'Musterstadt', 'zip_code': '12345',
#                                            'number': number, 'geo_lat': '51.51', 'geo_long': '7.51'})
#



# #TODO: all of this should be replaced by temp folder inpython 3.5
# def remove_files_with_prefix_in_folder(prefix, folder):
#     for t in os.listdir(folder):
#         if t.startswith(prefix):
#             os.remove(os.path.join(folder,t))


class CommentTests(TestCase):
    fixtures = FIXTURES

    def post_kiosk(self, street='Markstraße', number=137):
        '''
        Helper method to add a kiosk via post request.
        '''
        response_from_server = self.client.post('/bier/rest/kiosk/', {'street':
            street, 'city': 'Musterstadt', 'zip_code': '12345',
            'number': number, 'geo_lat': '51.51', 'geo_long': '7.51'})

        log.info(response_from_server.data)
        return response_from_server



    def post_comment(self, kiosk_id, username, text):
        '''
        Helper methods that adds a comment to a kiosk with the passed kiosk_id
        '''
        comment =  {'kiosk': kiosk_id,
                            'name': username,
                            'comment': text}
        response_from_server = self.client.post('/bier/rest/comment/', comment)

        log.info(response_from_server.data)
        return response_from_server

    def test_post_multiple_comments(self):
        #post a new empty kiosk
        resp = self.post_kiosk(street='Geilstraße', number=140)
        self.assertEqual(resp.status_code, 201)
        kiosk_id = json.loads(resp.content.decode())['id']

        log.info('kiosk_id: {}'.format(kiosk_id))

        #post a new comment with a username and a text
        username = 'Horst der Borst'
        text = 'Welch schoener kommentar ereilt mich da? Oh neine es ist siegliende mit ihrem Netz! Gott bewahre'
        resp = self.post_comment(kiosk_id, username, text)
        self.assertEqual(resp.status_code, 201)

        #post another comment
        username = 'Der geilere Borst'
        text = 'Noch mehr schöne Kommentare? Oh neine es ist siegliende mit ihrer Armbrust! Gott bewahre.'
        resp = self.post_comment(kiosk_id, username, text)
        self.assertEqual(resp.status_code, 201)

        #at this point two comments should have been succesufully posted
        #get the comments for that new kiosk
        resp = self.client.get(prefix + 'comment/?kiosk={}'.format(kiosk_id))
        self.assertEqual(resp.status_code, 200)
        #list should contain 2 elements
        comments_list = json.loads(resp.content.decode())
        self.assertEquals(len(comments_list), 2)


    def test_post_umlaut_comments(self):
        #post a new empty kiosk
        resp = self.post_kiosk(street='Geilstraße', number=142)
        self.assertEqual(resp.status_code, 201)

        kiosk_id = json.loads(resp.content.decode())['id']

        #post a new comment with a username and a text
        username = 'Klaüs die Mäus'
        text = 'Welch schöner kommentar ereilt mich da? Äh Wat? Das Örtliche! ßßßß'
        resp = self.post_comment(kiosk_id, username, text)
        self.assertEqual(resp.status_code, 201)

        comment = json.loads(resp.content.decode())
        log.info(comment)
        self.assertEquals(comment.get('name'), username)
        self.assertEquals(comment.get('comment'), text)


    def test_too_long_username(self):
        #post a new empty kiosk
        resp = self.post_kiosk(street='Geilstraße', number=145)
        self.assertEqual(resp.status_code, 201)

        kiosk_id = json.loads(resp.content.decode())['id']
        #post another with a really long username this should fail with code 400
        username = 'Klaüs die Mäus ist ein marzahn der königsgesselschaft. Der König folgt ihn treu.' \
                   ' Was immer der Hunnen planen'
        text = 'Ein plathhalter Text. Extra für Sieglinde!'
        resp = self.post_comment(kiosk_id, username, text)
        self.assertEqual(resp.status_code, 400)

    def test_too_long_text(self):

        #post a new empty kiosk
        resp = self.post_kiosk(street='Geilstraße', number=145)
        self.assertEqual(resp.status_code, 201)

        kiosk_id = json.loads(resp.content.decode())['id']
        #post comment  with a really long text this should fail with code 400
        username = 'Klaüsi!'
        text = "Siegfried hieß der wack're Recke, und er kämpfte gut," \
               "hatte eine dicke Haut vom Bad im Drachenblut!" \
               "Siegfried hatte einen Schatz gar groß und meisterlich," \
               "den hatte er geraubt vom alten Zwergenkönig Alberich!" \
               "Kriemhild hieß die holde Maid, das merke bitte sehr" \
               "ihre Brüder hießen Gunther, Gernot, Gieselher!" \
               "Siegfried hielt bei Bruder Gunther um die Kriemhild an," \
               "und so fing ganz froh und munter ihre große Liebe an!" \
               "Gunter liebte eine Frau, die starke Brunhild sehr," \
               "und da musste jetzt der große Held, der Siegfried her!" \
               "Siegfried half dem Gunther wohl, der konnte siegreich sein" \
               "und dann führte König Gunther seine starke Brunhild heim!"
        resp = self.post_comment(kiosk_id, username, text)
        #
        self.assertEqual(resp.status_code, 400)


class KioskTests(TestCase):
    fixtures = FIXTURES

    def post_kiosk(self, street='Markstraße', number=137):
        '''
        Helper method to add a kiosk via post request.
        '''
        response_from_server = self.client.post('/bier/rest/kiosk/', {'street':
            street, 'city': 'Musterstadt', 'zip_code': '12345',
            'number': number, 'geo_lat': '51.51', 'geo_long': '7.51'})

        log.info(response_from_server.data)
        return response_from_server

    def test_post_kiosk(self):
        #post a kiosk and check the return code
        resp = self.post_kiosk()
        self.assertEqual(resp.status_code, 201)

        #check if its really there. That means getting the id of the kiosk in the response
        #and make a get reqeust for it. this wont reutrn a kiosk but a kioskdetailthingy
        kiosk = json.loads(resp.content.decode())
        kiosk_id = kiosk['id']
        resp = self.client.get(prefix + 'kioskDetails/{}/'.format(kiosk_id))
        self.assertEqual(resp.status_code, 200)
        #get the kiosk from the detaisl dict thingy
        kiosk = json.loads(resp.content.decode()).get('kiosk')
        self.assertEqual(kiosk['id'], kiosk_id)


    def test_post_invalid_number(self):
        #post a kiosk with an incalid number check the return code
        resp = self.post_kiosk(street='Markstraße', number='asdasdad')
        self.assertEqual(resp.status_code, 400)

    def test_invalid_street(self):
        #post a kiosk with too long of a street name (ma 150 chars)
        long_street_name = 'acab_'*31
        resp = self.post_kiosk(street=long_street_name, number=12)
        self.assertEqual(resp.status_code, 400)


class ImageTests(TestCase):
    fixtures =FIXTURES

    def post_kiosk(self, street='Markstraße', number=137):
        '''
        Helper method to add a kiosk via post request.
        '''
        response_from_server = self.client.post('/bier/rest/kiosk/', {'street':
            street, 'city': 'Musterstadt', 'zip_code': '12345',
            'number': number, 'geo_lat': '51.51', 'geo_long': '7.51'})

        log.info(response_from_server.data)
        return response_from_server

    def post_image(self, kiosk_id):
        with open('./woistbier_rest/fixtures/unittest_test_image_4311.jpeg', 'rb') as f:
            resp = self.client.post(prefix + 'image/', {'kiosk': kiosk_id, 'image': f})
        return resp

    def test_list(self):
        #post a new empty kiosk
        resp = self.post_kiosk(number=137)
        kiosk = json.loads(resp.content.decode())
        kiosk_id = kiosk['id']

        #post a few images to the kiosk
        N = 5
        for i in range(0, N):
            self.post_image(kiosk_id)


        log.info('Calling images for kiosk id: {}'.format(kiosk_id))
        resp = self.client.get('/bier/rest/image/?kiosk={}'.format(kiosk_id))
        data = json.loads(resp.content.decode())
        log.info('N is: {}, there are {} images'.format(N, len(data)))
        self.assertTrue(len(data) == N)

    def test_image_endpoint(self):
        resp = self.post_kiosk(number=32)
        kiosk = json.loads(resp.content.decode())
        kiosk_id = kiosk['id']

        log.info('Calling images for kiosk id: {}'.format(kiosk_id))
        resp = self.client.get('/bier/rest/image/?kiosk={}'.format(kiosk_id))
        data = json.loads(resp.content.decode())
        self.assertEqual(data, [])

        self.post_image(kiosk_id)
        resp = self.client.get('/bier/rest/image/?kiosk={}'.format(kiosk_id))
        data = json.loads(resp.content.decode())
        self.assertEqual(len(data), 1)


    def test_image_in_kioskdetails(self):
        resp = self.post_kiosk(number=322)
        kiosk = json.loads(resp.content.decode())
        kiosk_id = kiosk['id']

        for i in range(5):
            self.post_image(kiosk_id)

        resp = self.client.get('/bier/rest/image/?kiosk={}'.format(kiosk_id))
        images = json.loads(resp.content.decode())

        resp = self.client.get('/bier/rest/kioskDetails/{}/'.format(kiosk_id))
        kiosk_details = json.loads(resp.content.decode())

        log.info(images)
        log.info(kiosk_details['images'])
        self.assertCountEqual(kiosk_details['images'], images)

    # test if the imagelist in the (images/?kiosk=bla) view is the same as the one deliverd
    # in the kioskdetail view and the kiosklistitem
    # def test_imagelists(self):
    #     #post a new empty kiosk
    #     resp = self.post_kiosk(number=137)
    #     kiosk = json.loads(resp.content.decode())
    #     kiosk_id = kiosk['id']
    #     #post a number of images
    #     for num in range(1, 6):
    #         self.post_image( kiosk_id)
    #         resp = self.client.get(prefix + 'image/?kiosk='.format(kiosk_id))
    #         images_from_view = json.loads(resp.content.decode())
    #         #log.info(str(images_from_view))
    #         #thers should be the posted amount of images in here
    #         self.assertTrue(len(images_from_view) == num)
    #
    #         resp = self.client.get(prefix + 'kioskDetails/' + kiosk_id + '/')
    #         self.assertEqual(resp.status_code, 200)
    #         #get the kiosk from the detaisl dict thingy
    #         images_from_kiosk = json.loads(resp.content.decode()).get('images')
    #         for kiosk_image, image_from_view in zip(images_from_view, images_from_kiosk):
    #             log.info('comparing: {} and {}'.format(kiosk_image, image_from_view))
    #             self.assertEqual(kiosk_image, image_from_view, 'Image lists in the image and the kioskdetails view were not the same')
    #
    #         resp = self.client.get(prefix + 'kioskList/?radius=1000')
    #         kioskListItems = json.loads(resp.content.decode())
    #         #lets find the kiosk with the id we just posted
    #         for listitem in kioskListItems:
    #             i = listitem.get('kiosk').get('id')
    #             if str(i) == str(kiosk_id):
    #                 self.assertTrue(listitem.get('image') is not None, 'thumb was none!')
    #                 break

    # def test_missing_images(self):
    #     resp = self.post_kiosk(number=145)
    #     kiosk = json.loads(resp.content.decode())
    #     kiosk_id = kiosk['id']
    #
    #     resp = self.post_image(kiosk_id)
    #     image_response = json.loads(resp.content.decode())
    #     log.info(image_response)
    #
    #     img = image_response['image']
    #     path = os.path.abspath(os.path.join(settings.MEDIA_ROOT,img))
    #     log.info(path)
    #
    #     self.fail()
    #     #get some kioskdetails for that kiosk
    #     resp = self.client.get(prefix + 'kioskDetails/{}/'.format(kiosk_id))
    #     self.assertEqual(resp.status_code, 200)
    #
    #     log.info(resp.data)
    #     #and the image list
    #     resp = self.client.get(prefix + 'image/?kiosk={}'.format(kiosk_id))
    #     self.assertEqual(resp.status_code, 200)
    #
    #     #now remove the generated image files
    #     folder = os.path.dirname(path)
    #     filename = os.path.basename(path)
    #     filename = os.path.splitext(filename)[0]
    #     remove_files_with_prefix_in_folder(filename, folder)
    #     #and try to load views again
    #     resp = self.client.get(prefix + 'kioskDetails/{}/'.format(kiosk_id))
    #     self.assertEqual(resp.status_code, 200)
    #     resp = self.client.get(prefix + 'image/?kiosk={}'.format(kiosk_id))
    #     self.assertEqual(resp.status_code, 200)


'''
A testcase to check wether the limits imposed on beerprice are working
'''
class BeerPriceTests(TestCase):
    fixtures =FIXTURES

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


class URLTests(TestCase):
    '''
    A test to check some URLs that have to exist
    '''
    fixtures = FIXTURES

    #test for valid url responses like 404
    def test_valid_urls(self):
        kiosk_id = get_kiosk_id()
        resp = self.client.get(prefix + 'kioskDetails/')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(prefix + 'kioskDetails/' + str(kiosk_id) + '/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(prefix + 'beer/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(prefix + 'beerprice/')
        self.assertEqual(resp.status_code, 200)
        # resp = self.client.get(prefix + 'beerPrice/?kiosk=' + str(kiosk_id))
        # self.assertEqual(resp.status_code, 200)

        resp = self.client.get(prefix + 'image/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(prefix + 'kioskList/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(prefix + 'comment/')
        self.assertEqual(resp.status_code, 200)

        #test for 404 response
        resp = self.client.get(prefix + 'nonexsitingurl/')
        log.info('REsp code is : ' + str(resp.status_code))
        self.assertEqual(resp.status_code, 404)
