from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from shared.models import CharFieldWithTextarea


class BlogEntry(models.Model):
    title = models.CharField(max_length=200)
    headline = models.CharField(max_length=400, blank=True, null=True)
    content = CharFieldWithTextarea(max_length=100000)
    slug = models.SlugField()
    image_url = models.CharField(max_length=1000, blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField()

    def __str__(self):
        return '{} - {}'.format(self.title, self.headline)


class Subscriber(models.Model):
    email = models.EmailField()
    subscribe_date = models.DateTimeField(auto_now=True)
    unsubscribe_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.email
