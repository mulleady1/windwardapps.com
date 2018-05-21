from django import forms
from django.template.loader import render_to_string
from django.conf import settings

from shared.forms import BaseForm


class ContactForm(BaseForm):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        data = {
            'from': 'Windward Apps <noreply@windwardapps.com>',
            'to': [settings.CONTACT_EMAIL],
            'subject': 'Contact request for windwardapps.com',
            'html': render_to_string('app/email/contact.html', self.cleaned_data)
        }

        return super().send_email(data)


class LoginForm(BaseForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
