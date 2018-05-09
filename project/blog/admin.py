from django.contrib import admin

from .models import BlogEntry


class BlogEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(BlogEntry, BlogEntryAdmin)
