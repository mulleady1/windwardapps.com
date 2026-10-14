import logging

import requests
from django import forms
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    def send_email(self, data):
        """Deliver an email through the configured API. Skipped when none is configured."""
        if not settings.EMAIL_API_URL:
            logger.warning('EMAIL_API_URL is not set; not sending "%s" to %s', data['subject'], data['to'])
            return None

        return requests.post(
            settings.EMAIL_API_URL,
            auth=('api', settings.EMAIL_API_KEY),
            data=data,
            timeout=10,
        )


class ContactForm(BaseForm):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        return super().send_email({
            'from': 'Windward Apps <noreply@windwardapps.com>',
            'to': [settings.CONTACT_EMAIL],
            'subject': 'Contact request for windwardapps.com',
            'html': render_to_string('app/email/contact.html', self.cleaned_data),
        })


class LoginForm(BaseForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SubscribeForm(BaseForm):
    email = forms.EmailField()

    def send_email(self):
        return super().send_email({
            'from': 'Windward Apps <newsletter@windwardapps.com>',
            'to': self.cleaned_data['email'],
            'subject': 'Thanks for subscribing!',
            'html': render_to_string('app/email/subscribe-success.html', self.cleaned_data),
        })
