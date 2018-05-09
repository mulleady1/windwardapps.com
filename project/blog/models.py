from django.db import models
from django.contrib.auth.models import User


class BlogEntry(models.Model):
    title = models.CharField(max_length=200)
    headline = models.CharField(max_length=400, blank=True, null=True)
    content = models.CharField(max_length=100000)
    slug = models.SlugField()
    image_url = models.URLField(blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField()
