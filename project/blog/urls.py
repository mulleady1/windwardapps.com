from django.urls import path

from .views import BlogListView, BlogDetailView, SubscribeView, unsubscribe

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('/subscribe', SubscribeView.as_view(), name='subscribe'),
    path('/unsubscribe', unsubscribe, name='unsubscribe'),
    path('/<slug:slug>', BlogDetailView.as_view(), name='blog-detail'),
]
