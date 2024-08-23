# contact/models.py

from django.db import models
from accounts.models import CustomUser

class Inquiry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='メールアドレス')
    subject = models.CharField(max_length=200, verbose_name='件名')
    context = models.TextField(verbose_name='問い合わせ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')

    class Meta:
        db_table = 'contact'
        verbose_name_plural = 'お問い合わせ'

    def __str__(self):
        return self.subject
