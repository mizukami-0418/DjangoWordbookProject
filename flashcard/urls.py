from django.urls import path
from . import views


urlpatterns = [
    path('', views.select_level, name='select_level'),
    path('select_mode', views.select_mode, name='select_mode'),
]
