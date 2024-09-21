from django.contrib import admin
from .models import UserProgress, UserWordStatus, UserReviewProgress

# Register your models here.
admin.site.register(UserProgress)
admin.site.register(UserWordStatus)
admin.site.register(UserReviewProgress)