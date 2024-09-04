from django.contrib import admin
from .models import PartOfSpeech, Level, Word


class PartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
    
    def count(self, obj):
        return Word.objects.filter(part_of_speech=obj, part_of_speech__name='名詞').count()
    count.short_description = '登録数'


class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'count')
    
    def count(self, obj):
        return Word.objects.filter(level=obj, level__name='初級').count()
    count.short_description = '登録数'

class WordAdmin(admin.ModelAdmin):
    list_display = ('english', 'japanese', 'part_of_speech', 'phrase', 'level')
    list_filter = ('part_of_speech', 'level',)
    
    fieldsets = (
        ('language', {'fields': ('english', 'japanese')}),
        ('description', {'fields': ('part_of_speech', 'phrase', 'level')}),
    )
    
    search_fields = ('english', 'japanese',)
    
admin.site.register(PartOfSpeech, PartOfSpeechAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Word, WordAdmin)