from django.db import models
from accounts.models import CustomUser
from dictionary.models import Level


class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # ユーザー
    level = models.ForeignKey(Level, on_delete=models.CASCADE) # 対象のレベル
    mode = models.CharField(max_length=10) # モード
    score = models.IntegerField(default=0) # スコア（正解数）
    total_questions = models.IntegerField(default=0) # 問題数のトータル
    current_question_index = models.IntegerField(default=0) # 現在の問題インデックス
    question_ids = models.TextField(blank=0, null=True) # 出題された問題のIDリストをシリアライズして保存
    completed_at = models.DateTimeField(auto_now_add=True) # 完了日時
    is_completed = models.BooleanField(default=False) # 完了しているかどうか
    is_paused = models.BooleanField(default=False) # 中断データがあるか
    
    class Meta:
        db_table = 'user_progress'
        verbose_name = 'ユーザー進行状況'
        verbose_name_plural = 'ユーザー進行状況'
    
    def __str__(self):
        return f"{self.user.username} - {self.level.name} - {self.mode}: {self.score}/{self.total_questions}"
