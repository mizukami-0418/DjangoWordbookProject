from django.db import models

class Word(models.Model):
    # 英語の単語
    english = models.CharField(max_length=255)
    
    # 日本語の意味
    japanese = models.CharField(max_length=255)
    
    # 品詞
    part_of_speech = models.CharField(max_length=50)
    
    # 成句や例文
    phrase = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.english} ({self.part_of_speech}): {self.japanese} - {self.phrase}"
