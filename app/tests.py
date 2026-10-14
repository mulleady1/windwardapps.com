from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils.timezone import now

from .models import BlogEntry, Subscriber

CONTACT = {'name': 'Ada', 'email': 'ada@example.com', 'message': 'hi'}


class FormTestCase(TestCase):
    def setUp(self):
        cache.clear()


class PagesTestCase(TestCase):
    def test_pages_render(self):
        for path in ['/', '/about', '/services', '/vendor-profile', '/news', '/login', '/test']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_pages_load_htmx_not_jquery(self):
        html = self.client.get('/').content.decode()
        self.assertIn('htmx.min.js', html)
        self.assertNotIn('jquery', html)


class ContactFormTestCase(FormTestCase):
    def test_missing_fields_rerender_the_form(self):
        res = self.client.post('/contact', {'name': 'Ada'})
        self.assertEqual(res.status_code, 422)
        self.assertContains(res, 'This field is required', status_code=422)
        self.assertContains(res, 'hx-post="/contact"', status_code=422)

    @patch('app.forms.BaseForm.send_email')
    def test_valid_submission(self, send):
        res = self.client.post('/contact', CONTACT)
        self.assertContains(res, "Thanks! We'll be in touch soon.")
        send.assert_called_once()

    @override_settings(CAPTCHA_ENFORCE=True)
    @patch('app.views.verify_captcha', return_value={'success': False})
    def test_failed_captcha_is_rejected_when_enforced(self, _verify):
        res = self.client.post('/contact', CONTACT)
        self.assertContains(res, 'captcha check failed', status_code=422)

    @override_settings(CAPTCHA_ENFORCE=True)
    @patch('app.views.verify_captcha', return_value={'success': True})
    @patch('app.forms.BaseForm.send_email')
    def test_passed_captcha_goes_through_when_enforced(self, send, _verify):
        res = self.client.post('/contact', CONTACT)
        self.assertContains(res, 'Thanks!')
        send.assert_called_once()

    @override_settings(BAD_EMAILS={'ada@example.com'})
    @patch('app.forms.BaseForm.send_email')
    def test_blocked_sender_is_dropped_silently(self, send):
        res = self.client.post('/contact', CONTACT)
        self.assertContains(res, 'Thanks!')
        send.assert_not_called()

    @patch('app.forms.BaseForm.send_email')
    def test_honeypot_fakes_success_without_sending(self, send):
        res = self.client.post('/contact', {**CONTACT, 'website': 'http://spam.example'})
        self.assertContains(res, 'Thanks!')
        send.assert_not_called()

    @patch('app.forms.BaseForm.send_email')
    def test_rate_limit_per_ip(self, send):
        for _ in range(5):
            self.assertEqual(self.client.post('/contact', CONTACT).status_code, 200)
        res = self.client.post('/contact', CONTACT)
        self.assertContains(res, 'Too many submissions', status_code=429)
        self.assertEqual(send.call_count, 5)

    @patch('app.forms.BaseForm.send_email')
    def test_rate_limit_uses_forwarded_ip(self, send):
        for i in range(5):
            self.client.post('/contact', CONTACT, HTTP_X_FORWARDED_FOR='203.0.113.9')
        blocked = self.client.post('/contact', CONTACT, HTTP_X_FORWARDED_FOR='203.0.113.9')
        other = self.client.post('/contact', CONTACT, HTTP_X_FORWARDED_FOR='198.51.100.4')
        self.assertEqual(blocked.status_code, 429)
        self.assertEqual(other.status_code, 200)


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
        self.assertContains(res, 'hx-post="/news/subscribe"')

    def test_detail(self):
        self.assertEqual(self.client.get('/news/old').status_code, 200)
        self.assertEqual(self.client.get('/news/nope').status_code, 404)


class SubscribeTestCase(FormTestCase):
    def test_subscribe_then_duplicate_then_unsubscribe(self):
        res = self.client.post('/news/subscribe', {'email': 'ada@example.com'})
        self.assertContains(res, "You're on the list")
        self.assertEqual(Subscriber.objects.count(), 1)

        res = self.client.post('/news/subscribe', {'email': 'ada@example.com'})
        self.assertContains(res, 'already subscribed', status_code=422)

        res = self.client.get('/news/unsubscribe?email=ada@example.com')
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(Subscriber.objects.get().unsubscribe_date)

        self.assertEqual(self.client.get('/news/unsubscribe').status_code, 400)

    def test_invalid_email_rerenders_form(self):
        res = self.client.post('/news/subscribe', {'email': 'nope'})
        self.assertContains(res, 'Enter a valid email address', status_code=422)
        self.assertEqual(Subscriber.objects.count(), 0)

    def test_honeypot_does_not_create_subscriber(self):
        res = self.client.post('/news/subscribe', {'email': 'bot@example.com', 'website': 'x'})
        self.assertContains(res, "You're on the list")
        self.assertEqual(Subscriber.objects.count(), 0)

    def test_rate_limit(self):
        for i in range(5):
            self.client.post('/news/subscribe', {'email': f'u{i}@example.com'})
        res = self.client.post('/news/subscribe', {'email': 'u9@example.com'})
        self.assertEqual(res.status_code, 429)
        self.assertEqual(Subscriber.objects.count(), 5)


class LoginTestCase(TestCase):
    def test_bad_credentials_show_error(self):
        res = self.client.post('/login', {'username': 'x', 'password': 'y'})
        self.assertContains(res, 'Invalid username or password')

    def test_good_credentials_redirect_home(self):
        User.objects.create_user('kyle', password='pw')
        res = self.client.post('/login', {'username': 'kyle', 'password': 'pw'})
        self.assertRedirects(res, '/')
