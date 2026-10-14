import logging

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.edit import FormView

from . import throttle
from .forms import ContactForm, LoginForm, SubscribeForm
from .models import BlogEntry, Subscriber

logger = logging.getLogger(__name__)


def client_ip(request):
    """nginx sets X-Forwarded-For; the first address is the client."""
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    return forwarded.split(',')[0].strip() or request.META.get('REMOTE_ADDR', '')


def verify_captcha(token):
    """Ask hCaptcha whether a token is valid. Returns the decoded response."""
    response = requests.post(
        'https://hcaptcha.com/siteverify',
        data={'secret': settings.CAPTCHA_SECRET, 'response': token},
        timeout=10,
    )
    return response.json()


class GuardedFormView(FormView):
    """A public form that answers htmx with template partials and screens out abuse.

    A submission passes through, in order: the honeypot (bots get a fake success),
    a per-IP and a site-wide rate limit, and the captcha when enforcement is on.
    Subclasses set `form_partial`, `success_partial`, `throttle_scope`, and
    implement `handle(form)` for the real work.
    """

    form_partial = ''
    success_partial = ''
    throttle_scope = ''
    ip_limit = 5
    global_limit = 30

    def form_valid(self, form):
        if form.is_bot:
            logger.info('%s: honeypot filled, ignoring submission', self.throttle_scope)
            return self.success()

        ip = client_ip(self.request)
        if not throttle.allow(f'{self.throttle_scope}:ip:{ip}', self.ip_limit) or \
           not throttle.allow(f'{self.throttle_scope}:all', self.global_limit):
            form.add_error(None, 'Too many submissions right now. Please try again in an hour.')
            return self.render_form(form, status=429)

        if settings.CAPTCHA_ENFORCE:
            try:
                result = verify_captcha(self.request.POST.get('h-captcha-response', ''))
            except (requests.RequestException, ValueError):
                logger.exception('hCaptcha verification failed')
                result = {'success': False}
            if not result.get('success'):
                form.add_error(None, 'The captcha check failed. Please try again.')
                return self.render_form(form, status=422)

        return self.handle(form)

    def form_invalid(self, form):
        return self.render_form(form, status=422)

    def render_form(self, form, status=200):
        return render(self.request, self.form_partial, self.get_context_data(form=form), status=status)

    def success(self):
        return render(self.request, self.success_partial, self.get_context_data())

    def handle(self, form):
        raise NotImplementedError


# --- Marketing pages --------------------------------------------------------

class IndexView(GuardedFormView):
    form_class = ContactForm
    template_name = 'app/index.html'
    form_partial = 'app/index.html#contact-form'
    success_partial = 'app/index.html#contact-success'
    throttle_scope = 'contact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['captcha_key'] = settings.CAPTCHA_KEY
        return context

    def handle(self, form):
        form.send_email()
        return self.success()


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
            form.add_error(None, 'Invalid username or password.')
            return self.form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


# --- News -------------------------------------------------------------------

class NewsletterMixin:
    """Pages that show the newsletter signup need a blank form and the captcha key."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('form', SubscribeForm())
        context['captcha_key'] = settings.CAPTCHA_KEY
        return context


class NewsListView(NewsletterMixin, ListView):
    template_name = 'app/news/list.html'

    def get_queryset(self):
        """Published entries only; nothing dated in the future."""
        return BlogEntry.objects.filter(pub_date__lte=now()).order_by('-pub_date')


class NewsDetailView(NewsletterMixin, DetailView):
    model = BlogEntry
    template_name = 'app/news/detail.html'


class SubscribeView(GuardedFormView):
    form_class = SubscribeForm
    template_name = 'app/news/base.html#subscribe-form'
    form_partial = 'app/news/base.html#subscribe-form'
    success_partial = 'app/news/base.html#subscribe-success'
    throttle_scope = 'subscribe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['captcha_key'] = settings.CAPTCHA_KEY
        return context

    def handle(self, form):
        email = form.cleaned_data['email']
        subscriber = Subscriber.objects.filter(email=email).first()

        if subscriber is None:
            Subscriber.objects.create(email=email)
        elif subscriber.unsubscribe_date is None:
            form.add_error('email', 'You are already subscribed :)')
            return self.render_form(form, status=422)
        else:
            subscriber.unsubscribe_date = None
            subscriber.save()

        # Confirmation emails are intentionally not sent; the list drew too much spam signup.
        return self.success()


def unsubscribe(request):
    email = request.GET.get('email')
    subscriber = Subscriber.objects.filter(email=email).first() if email else None
    if subscriber is None:
        return HttpResponseBadRequest()

    subscriber.unsubscribe_date = now()
    subscriber.save()
    return render(request, 'app/news/unsubscribe-success.html')
