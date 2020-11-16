from django.http import HttpResponse
from django.test import TestCase

# Create your tests here.


class ContactFormTestCase(TestCase):
    def test_contact_form(self):
        res: HttpResponse = self.client.post('/contact', {
            'name': 'name name',
            'email': 'email@email.com',
            'message': 'hi',
            'h-captcha-response': 'test captcha'
        })
        self.assertEqual(res.status_code, 400)
