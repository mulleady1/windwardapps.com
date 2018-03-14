from django.urls import path

from .views import ContactView, LoginView

urlpatterns = [
    path('', ContactView.as_view(), name='index'),
    path('contact', ContactView.as_view(), name='contact'),
    path('login', LoginView.as_view(), name='login'),
]
