from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate

from .forms import ContactForm, LoginForm

class JsonSuccessResponse(JsonResponse):
    def __init__(self, data={}, **kwargs):
        data['success'] = True
        super(JsonSuccessResponse, self).__init__(data, **kwargs)

class JsonErrorResponse(JsonResponse):
    status_code = 400
    def __init__(self, data={}, **kwargs):
        data['success'] = False
        super(JsonErrorResponse, self).__init__(data, **kwargs)

class AjaxFormView(FormView):
    def form_valid(self, form):
        return JsonSuccessResponse()

    def form_invalid(self, form):
        return JsonErrorResponse({ 'errors': form.errors })


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
