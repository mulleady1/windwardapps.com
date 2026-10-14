from django.contrib import admin

from .models import BlogEntry, Subscriber


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'headline', 'pub_date', 'created_by')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-pub_date',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribe_date', 'unsubscribe_date')
