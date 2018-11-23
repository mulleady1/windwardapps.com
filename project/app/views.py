from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

from .forms import ContactForm, LoginForm
from shared.http import JsonErrorResponse
from shared.views import AjaxFormView


class IndexView(AjaxFormView):
    form_class = ContactForm
    template_name = 'app/index.html'

    def form_valid(self, form):
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
