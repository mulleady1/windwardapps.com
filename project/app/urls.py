from django.urls import path

from .views import IndexView, LoginView, LogoutView, about, services, vendorprofile

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact', IndexView.as_view(), name='contact'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('about', about, name='about'),
    path('services', services, name='services'),
    path('vendor-profile', vendorprofile, name='vendorprofile'),
]
