from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import BaseFormView, FormView
from django.contrib.auth import authenticate

from .forms import ContactForm, LoginForm

class AjaxFormView(BaseFormView):
    def get(self, form):
        return HttpResponseNotAllowed(['POST'])

class JsonSuccessResponse(JsonResponse):
    def __init__(self, data={}, **kwargs):
        data['success'] = True
        super().__init__(data, **kwargs)

class JsonErrorResponse(JsonResponse):
    status_code = 400

    def __init__(self, data={}, **kwargs):
        data['success'] = False
        super().__init__(data, **kwargs)


def index(request):
    return render(request, 'app/index.html')

class ContactView(AjaxFormView):
    form_class = ContactForm

    def form_valid(self, form):
        #form.send_email()
        return JsonSuccessResponse()

    def form_invalid(self, form):
        return JsonErrorResponse()

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'app/login.html'
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(form)
        if user is None:
            return JsonErrorResponse({ 'msg': 'Invalid credentials.' })
