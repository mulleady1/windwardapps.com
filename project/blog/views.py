from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import BlogEntry


class BlogListView(ListView):
    model = BlogEntry
    template_name = 'blog/list.html'


class BlogDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/detail.html'
