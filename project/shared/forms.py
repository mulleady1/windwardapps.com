from django import forms
from django.conf import settings
import requests


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BaseForm, self).__init__(*args, **kwargs)

    def send_email(self, data):
        if settings.DEBUG:
            print(data)
            return requests.Response()

        res = requests.post(
            settings.EMAIL_API_URL,
            auth=('api', settings.EMAIL_API_KEY),
            data=data)

        return res
