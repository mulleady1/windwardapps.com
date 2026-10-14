import logging

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.edit import FormView

from .forms import ContactForm, LoginForm, SubscribeForm
from .http import JsonErrorResponse, JsonSuccessResponse
from .models import BlogEntry, Subscriber

logger = logging.getLogger(__name__)


class AjaxFormView(FormView):
    """FormView that answers with JSON instead of redirecting or re-rendering."""

    def form_valid(self, form):
        return JsonSuccessResponse()

    def form_invalid(self, form):
        return JsonErrorResponse({'errors': form.errors})


# --- Marketing pages --------------------------------------------------------

def verify_captcha(token):
    """Ask hCaptcha whether a token is valid. Returns the decoded response."""
    response = requests.post(
        'https://hcaptcha.com/siteverify',
        data={'secret': settings.CAPTCHA_SECRET, 'response': token},
        timeout=10,
    )
    return response.json()


class IndexView(AjaxFormView):
    form_class = ContactForm
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['captcha_key'] = settings.CAPTCHA_KEY
        return context

    def form_valid(self, form):
        token = self.request.POST.get('h-captcha-response', '')
        try:
            result = verify_captcha(token)
        except (requests.RequestException, ValueError):
            logger.exception('hCaptcha verification failed')
            result = {'success': False}
        logger.debug('hCaptcha response: %s', result)

        if settings.CAPTCHA_ENFORCE and not result.get('success'):
            return JsonErrorResponse({'msg': 'The captcha check failed. Please try again.'})

        form.send_email()
        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'app/login.html'
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is None:
            return JsonErrorResponse({'msg': 'Invalid credentials.'})

        login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


# --- News -------------------------------------------------------------------

class NewsListView(ListView):
    template_name = 'app/news/list.html'

    def get_queryset(self):
        """Published entries only; nothing dated in the future."""
        return BlogEntry.objects.filter(pub_date__lte=now()).order_by('-pub_date')


class NewsDetailView(DetailView):
    model = BlogEntry
    template_name = 'app/news/detail.html'


class SubscribeView(AjaxFormView):
    form_class = SubscribeForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        subscriber = Subscriber.objects.filter(email=email).first()

        if subscriber is None:
            Subscriber.objects.create(email=email)
        elif subscriber.unsubscribe_date is None:
            form.add_error('email', 'You are already subscribed :)')
            return self.form_invalid(form)
        else:
            subscriber.unsubscribe_date = None
            subscriber.save()

        # Confirmation emails are intentionally not sent; the list drew too much spam signup.
        return super().form_valid(form)


def unsubscribe(request):
    email = request.GET.get('email')
    subscriber = Subscriber.objects.filter(email=email).first() if email else None
    if subscriber is None:
        return HttpResponseBadRequest()

    subscriber.unsubscribe_date = now()
    subscriber.save()
    return render(request, 'app/news/unsubscribe-success.html')
