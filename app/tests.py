from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils.timezone import now

from .models import BlogEntry, Subscriber

CONTACT = {'name': 'Ada', 'email': 'ada@example.com', 'message': 'hi', 'h-captcha-response': 'tok'}


class PagesTestCase(TestCase):
    def test_pages_render(self):
        for path in ['/', '/about', '/services', '/vendor-profile', '/news', '/login']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)


class ContactFormTestCase(TestCase):
    def test_missing_fields_are_rejected(self):
        res = self.client.post('/contact', {'name': 'Ada'})
        self.assertEqual(res.status_code, 400)
        self.assertIn('email', res.json()['errors'])

    @patch('app.views.verify_captcha', return_value={'success': True})
    def test_valid_submission(self, _verify):
        res = self.client.post('/contact', CONTACT)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()['success'])

    @override_settings(CAPTCHA_ENFORCE=True)
    @patch('app.views.verify_captcha', return_value={'success': False})
    def test_failed_captcha_is_rejected_when_enforced(self, _verify):
        res = self.client.post('/contact', CONTACT)
        self.assertEqual(res.status_code, 400)


class NewsTestCase(TestCase):
    def setUp(self):
        for title, offset in [('Old', -1), ('Future', 1)]:
            BlogEntry.objects.create(
                title=title, slug=title.lower(), content='...',
                pub_date=now() + timedelta(days=offset), created_date=now(),
            )

    def test_list_hides_future_entries(self):
        res = self.client.get('/news')
        self.assertContains(res, 'Old')
        self.assertNotContains(res, 'Future')

    def test_detail(self):
        self.assertEqual(self.client.get('/news/old').status_code, 200)
        self.assertEqual(self.client.get('/news/nope').status_code, 404)


class SubscribeTestCase(TestCase):
    def test_subscribe_then_duplicate_then_unsubscribe(self):
        res = self.client.post('/news/subscribe', {'email': 'ada@example.com'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Subscriber.objects.count(), 1)

        res = self.client.post('/news/subscribe', {'email': 'ada@example.com'})
        self.assertEqual(res.status_code, 400)

        res = self.client.get('/news/unsubscribe?email=ada@example.com')
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(Subscriber.objects.get().unsubscribe_date)

        self.assertEqual(self.client.get('/news/unsubscribe').status_code, 400)
