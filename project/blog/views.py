from django.http import HttpResponseBadRequest
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from shared.views import AjaxFormView
from .models import BlogEntry, Subscriber
from .forms import SubscribeForm

class BlogListView(ListView):
    model = BlogEntry
    template_name = 'blog/list.html'


class BlogDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/detail.html'

class SubscribeView(AjaxFormView):
    form_class = SubscribeForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            subscriber = Subscriber.objects.get(email=email)
            if subscriber.unsubscribe_date is None:
                form.errors['email'] = ['You are already subscribed :)']
                return super().form_invalid(form)
            subscriber.unsubscribe_date = None
            subscriber.save()
        except ObjectDoesNotExist:
            Subscriber.objects.create(email=email)

        form.send_email()
        return super(SubscribeView, self).form_valid(form)


def unsubscribe(request):
    try:
        subscriber = Subscriber.objects.get(email=request.GET['email'])
    except ObjectDoesNotExist:
        return HttpResponseBadRequest()

    subscriber.unsubscribe_date = now()
    subscriber.save()
    return render(request, 'blog/unsubscribe-success.html')
