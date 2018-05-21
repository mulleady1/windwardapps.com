from django import forms
from django.template.loader import render_to_string

from shared.forms import BaseForm


class SubscribeForm(BaseForm):
    email = forms.EmailField()

    def send_email(self):
        data = {
            'from': 'Windward Apps <newsletter@windwardapps.com>',
            'to': self.cleaned_data['email'],
            'subject': 'Thanks for subscribing!',
            'html': render_to_string('blog/email/subscribe-success.html', self.cleaned_data)
        }

        return super().send_email(data)
