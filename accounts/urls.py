from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/', views.user_home, name='user_home'),
    path('user/edit/', views.user_edit, name='edit'),
    path('user/detail/', views.user_detail, name='detail'),
]