from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('contact/', include('contact.urls')),
    path('dictionary/', include('dictionary.urls')),
    path('flashcard/', include('flashcard.urls')),
]