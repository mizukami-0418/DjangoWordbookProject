# contact/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('result/', views.contact_result, name='contact_result'),
]
