from django.urls import path
from . import views


urlpatterns = [
    path('', views.select_level, name='select_level'),
]
