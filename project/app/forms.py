from django import forms
from shared.forms import BaseForm


class ContactForm(BaseForm):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

class LoginForm(BaseForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
