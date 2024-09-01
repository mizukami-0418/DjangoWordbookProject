from django.shortcuts import render, get_object_or_404, redirect
from dictionary.models import Word, Level
from django.http import HttpResponse
import random


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
        return redirect('quiz')
    
    level = get_object_or_404(Level, id=level_id)
    
    return render(request, 'flashcard/select_num_questions.html', {'level': level, 'mode': mode})


# 単語帳クイズ
def quiz(request):
    level_id = request.session.get('level_id')
    mode = request.session.get('mode')
    num_questions = request.session.get('num_questions')
    level = get_object_or_404(Level, id=level_id)
    
    if not level_id and mode and num_questions:
        return redirect('select_level')
    
    words = Word.objects.filter(level_id=level_id) # 選択した難易度の単語を全て抽出
    # 抽出した単語が選択した出題数より少ない場合、エラーにならないための処理
    total_questions = min(num_questions, words.count())
    
    # セッションに問題番号がない場合は新規で保存
    if 'question_index' not in request.session:
        # 抽出した単語の中から問題数分のidをランダムで取得
        question_ids = random.sample(list(words.values_list('id', flat=True)), total_questions)
        # 各データをセッションに保存
        request.session['question_index'] = 0 # 最初の問題番号を0にする
        request.session['score'] = 0 # 正解数を0に設定
        request.session['question_ids'] = question_ids # 抽出したid
        
    # 現在の問題indexを取得
    question_index = request.session['question_index']
    
    # 問題番号が問題数以上になれば全て終了
    if question_index >= total_questions:
        return redirect('result')
    
    # idから問題の単語を抽出する
    question_id = request.session['question_ids'][question_index]
    current_question = Word.objects.get(id=question_id)
    
    if request.method == 'POST':
        # ユーザーの回答を両端の空白を削除し、小文字に変換する
        answer = request.POST.get('answer').strip().lower()
        correct_answer = current_question.english if mode == 'en' else current_question.japanese
        if answer == correct_answer:
            # 正解数を１加算
            request.session['score'] += 1
        # 問題番号を1加算
        request.session['question_index'] += 1
        
        return redirect('quiz')

    return render(request, 'flashcard/quiz.html', {'current_question': current_question, 'mode': mode, 'question_index': question_index, 'level': level})
    
    
def result(request):
    score = request.session.get('score')
    total_questions = request.session.get('num_questions')
    correct_answer_rate = int(score / total_questions * 100)
    
    request.session.flush()
    
    return render(request, 'flashcard/result.html', {
        'score': score, 'total_questions': total_questions, 'correct_answer_rate':correct_answer_rate
    })