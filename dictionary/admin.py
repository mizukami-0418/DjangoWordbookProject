from django.contrib import admin
from .models import Word


class WordAdmin(admin.ModelAdmin):
    list_display = ('english', 'japanese', 'part_of_speech', 'phrase', 'level')
    list_filter = ('part_of_speech', 'level')
    
    fieldsets = (
        ('language', {'fields': ('english', 'japanese')}),
        ('description', {'fields': ('part_of_speech', 'phrase', 'level')}),
    )
    
    search_fields = ('english', 'japanese')
    
admin.site.register(Word)