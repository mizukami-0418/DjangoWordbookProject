from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path, include
from error import views

# カスタムエラーハンドラ
handler404 = 'error.views.custom_404'
handler500 = 'error.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('contact/', include('contact.urls')),
    path('dictionary/', include('dictionary.urls')),
    path('flashcard/', include('flashcard.urls')),
]