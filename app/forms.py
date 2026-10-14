import logging

import requests
from django import forms
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class BaseForm(forms.Form):
    """Public form: no label suffix, a honeypot field, and email delivery."""

    # Bots fill every field they can find. Humans never see this one.
    website = forms.CharField(
        required=False,
        label='Leave this empty',
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'tabindex': '-1'}),
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.order_fields([name for name in self.fields if name != 'website'] + ['website'])

    @property
    def is_bot(self):
        return bool(self.cleaned_data.get('website'))

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
        sender = self.cleaned_data['email']
        if sender.lower() in settings.BAD_EMAILS:
            logger.info('Dropping contact message from blocked sender %s', sender)
            return None

        return super().send_email({
            'from': 'Windward Apps <noreply@windwardapps.com>',
            'to': [settings.CONTACT_EMAIL],
            'subject': 'Contact request for windwardapps.com',
            'html': render_to_string('app/email/contact.html', self.cleaned_data),
        })


class SubscribeForm(BaseForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
