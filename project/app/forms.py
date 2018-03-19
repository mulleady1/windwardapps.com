from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from shared.forms import BaseForm


class ContactForm(BaseForm):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        html = render_to_string('app/email/contact.html', self.cleaned_data)
        send_mail(
            'Contact request for windwardapps.com',
            None,
            'noreply@windwardapps.com',
            [settings.CONTACT_EMAIL],
            fail_silently=False,
            html_message=html
        )


class LoginForm(BaseForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
