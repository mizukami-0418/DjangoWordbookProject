from django.shortcuts import render, get_object_or_404, redirect
from dictionary.models import Word, Level
from django.http import HttpResponse


# 難易度セレクト
def select_level(request):
    if request.method == 'POST':
        level_id = request.POST.get('level')
        
        request.session['level_id'] = level_id
        return redirect('select_mode')
    else:
        # データベースからLevelオブジェクトを全て取得
        levels = Level.objects.all()
    return render(request, 'flashcard/select_level.html', {'levels': levels})


# モードセレクト
def select_mode(request):
    # セッションからlevel_idを取得
    level_id = request.session.get('level_id')
    if not level_id:
        return redirect('select_level')
    
    if request.method == 'POST':
        mode = request.POST.get('mode')
        
        request.session['mode'] = mode
        return redirect('select_num_questions')
    
    # データベースからlevel_idに対応するLevelオブジェクトを取得
    level = get_object_or_404(Level, id=level_id)
    
    return render(request, 'flashcard/select_mode.html', {'level': level})


# 問題数セレクト
def select_num_questions(request):
    level_id = request.session.get('level_id')
    mode = request.session.get('mode')
    if not level_id and mode:
        return redirect('select_level')
    
    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions'))
        
        request.session['num_questions'] = num_questions
        return HttpResponse(num_questions)
    
    level = get_object_or_404(Level, id=level_id)
    
    return render(request, 'flashcard/select_num_questions.html', {'level': level, 'mode': mode})
