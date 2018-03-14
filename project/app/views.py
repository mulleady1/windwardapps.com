from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate

from .forms import ContactForm, LoginForm
from shared.http import JsonErrorResponse
from shared.views import AjaxFormView

class ContactView(AjaxFormView):
    form_class = ContactForm
    template_name = 'app/index.html'

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'app/login.html'
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(form)
        if user is None:
            return JsonErrorResponse({ 'msg': 'Invalid credentials.' })

        return super(LoginView, self).form_valid(form)
