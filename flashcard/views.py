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
        return HttpResponse(mode)
    
    # データベースからlevel_idに対応するLevelオブジェクトを取得
    level = get_object_or_404(Level, id=level_id)
    
    return render(request, 'flashcard/select_mode.html', {'level': level})
