from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    # path('mode_choice', views.mode_choice, name='mode_choice'),　一旦コメントアウト
    # path('search_japanese', views.search_japanese, name='search_japanese'),
    # path('search_english', views.search_english, name='search_english'),
]
