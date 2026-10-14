from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contact', views.IndexView.as_view(), name='contact'),
    path('about', TemplateView.as_view(template_name='app/about.html'), name='about'),
    path('services', TemplateView.as_view(template_name='app/services.html'), name='services'),
    path('vendor-profile', TemplateView.as_view(template_name='app/vendorprofile.html'), name='vendorprofile'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('news', views.NewsListView.as_view(), name='news-list'),
    path('news/subscribe', views.SubscribeView.as_view(), name='subscribe'),
    path('news/unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('news/<slug:slug>', views.NewsDetailView.as_view(), name='news-detail'),
]
