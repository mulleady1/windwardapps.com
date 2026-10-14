from django.conf import settings
from django.db import models


class BlogEntry(models.Model):
    title = models.CharField(max_length=200)
    headline = models.CharField(max_length=400, blank=True, null=True)
    content = models.TextField()
    slug = models.SlugField()
    image_url = models.CharField(max_length=1000, blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField()

    class Meta:
        # Table names predate the single-app layout; keep them so existing data is untouched.
        db_table = 'blog_blogentry'
        verbose_name_plural = 'blog entries'

    def __str__(self):
        return f'{self.title} - {self.headline}'


class Subscriber(models.Model):
    email = models.EmailField()
    subscribe_date = models.DateTimeField(auto_now=True)
    unsubscribe_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'blog_subscriber'

    def __str__(self):
        return self.email
