from django.contrib import admin

from .models import BlogEntry, Subscriber


class BlogEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(Subscriber)
