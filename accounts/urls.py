from django.urls import path
from . import views
from .views import CustomPasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/', views.user_home, name='user_home'),
    path('user/edit/', views.user_edit, name='edit'),
    path('user/detail/', views.user_detail, name='detail'),
    path('user/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('user/password_change/done', views.password_change_done, name='password_change_done'),
]