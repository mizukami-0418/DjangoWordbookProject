from django.urls import path
from . import views


urlpatterns = [
    path('', views.select_level, name='select_level'),
    path('select_mode', views.select_mode, name='select_mode'),
    path('select_num_questions', views.select_num_questions, name='select_num_questions'),
    path('select_quiz', views.select_quiz, name='select_quiz'),
    path('quiz', views.quiz, name='quiz'),
    path('quiz/restart/<int:progress_id>/', views.quiz_restart, name='quiz_restart'),
    path('check_answer/<int:progress_id>/', views.check_answer, name='check_answer'),
    path('result/<int:progress_id>/', views.result, name='result'),
    path('pause_quiz/<int:progress_id>/', views.pause_quiz, name='pause_quiz'),
]
