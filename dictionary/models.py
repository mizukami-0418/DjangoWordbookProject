from django.db import models

class Word(models.Model):
    LEVEL_SELECT = {
        'Beginner': '初級(中学)',
        'Intermediate': '中級(高校)',
        'Advanced': '上級(大学,社会人)',
        'Expert': '特級(それ以上)',
    }
    
    PART_OF_SPEECH_SELECT = {
        '名詞': '名詞',
        '形容詞': '形容詞',
        '代名詞': '代名詞',
        '副詞': '副詞',
        '動詞': '動詞',
        '自動詞': '自動詞',
        '他動詞': '他動詞',
        '自動詞・他動詞': '自動詞、他動詞',
        '助動詞': '助動詞',
        '前置詞': '前置詞',
        '接続詞': '接続詞',
        '間投詞': '間投詞',
    }
    
    english = models.CharField(max_length=255, verbose_name='英語') # 英語
    japanese = models.CharField(max_length=255, verbose_name='日本語') # 日本語
    part_of_speech = models.CharField(max_length=50, choices=PART_OF_SPEECH_SELECT, verbose_name='品詞') # 品詞
    phrase = models.TextField(blank=True, null=True, verbose_name='成句') # 成句や例文
    level = models.CharField(max_length=20, choices=LEVEL_SELECT, verbose_name='難易度', null=True) # 難易度
    
    class Meta:
        db_table = 'word'
        verbose_name_plural = '単語'
    
    def __str__(self):
        return self.english
