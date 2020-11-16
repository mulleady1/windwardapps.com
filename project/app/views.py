import logging
import requests
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

from .forms import ContactForm, LoginForm
from shared.http import JsonErrorResponse
from shared.views import AjaxFormView

logger = logging.getLogger(__file__)


class IndexView(AjaxFormView):
    form_class = ContactForm
    template_name = 'app/index.html'

    def form_valid(self, form):
        req: HttpRequest = self.request
        token = req.POST['h-captcha-response']
        logger.debug('token=%s', token)
        params = {
            "secret": "0xDe6629D85B9C59e02DACB04759B81558b72a4d21",
            "response": token
        }

        r = requests.post("https://hcaptcha.com/siteverify", json=params)
        result = r.json()
        logger.debug('hcaptcha response=%s', result)
        if not result['success']:
            return JsonErrorResponse({'error': 'captcha error'})

        form.send_email()
        return super(IndexView, self).form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'app/login.html'
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(
            username=form.data['username'], password=form.data['password'])
        if user is None:
            return JsonErrorResponse({'msg': 'Invalid credentials.'})

        login(self.request, user)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def about(req):
    return render(req, 'app/about.html')


def services(req):
    return render(req, 'app/services.html')


def vendorprofile(req):
    return render(req, 'app/vendorprofile.html')
