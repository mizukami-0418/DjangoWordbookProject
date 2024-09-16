from django.shortcuts import render, get_object_or_404, redirect
from dictionary.models import Word, Level
from django.http import Http404, HttpResponse
from django.contrib import messages
from .models import UserProgress
import random
import json

# 「最初から」か「続きから」を選択する
def select_quiz(request):
    user_progress = UserProgress.objects.filter(user=request.user,is_completed=False).first()
    
    # POSTリクエスト
    if request.method == 'POST':
        # POStリクエストからquiz_mode(newかcontinue)を取得
        selection = request.POST.get('quiz_mode')
        
        # 「最初から」を選んだ場合、新しくクイズを開始する
        if selection == 'new':
            return redirect('select_level')
        # 「前回の続きから」はuser_progress.idからデータを取得し、再開する
        elif selection == 'continue':
            user_progress_data = UserProgress.objects.filter(user=request.user, is_completed=False).all()
            return render(request, 'flashcard/show_paused_data.html', {'user_progress_data': user_progress_data})
            # return redirect('quiz_restart', progress_id=user_progress.id)
        else:
            messages.error(request, 'エラーが発生しました。最初からお願いします。')
            return redirect('select_quiz')
    # GETリクエストの場合は、フォームを表示する
    return render(request, 'flashcard/select_quiz.html', {'user_progress': user_progress})


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


# セッションデータ取得用ヘルパー関数
def get_quiz_session_data(request):
    level_id = request.session.get('level_id')
    mode = request.session.get('mode')
    num_questions = request.session.get('num_questions')
    
    level = get_object_or_404(Level, id=level_id)
    
    return level, mode, num_questions


# モードセレクト
def select_mode(request):
    # ヘルパー関数を使用し、levelを取得
    level, _, _ = get_quiz_session_data(request)
    # 入力確認
    if level is None:
        messages.error(request, 'エラーが発生しました。最初からお願いします')
        return redirect('select_level')
    
    # POSTリクエスト
    if request.method == 'POST':
        # 英訳か和訳のモードを取得し、セッションに保持する
        mode = request.POST.get('mode')
        request.session['mode'] = mode
        return redirect('select_num_questions')
    
    # GETリクエスト
    return render(request, 'flashcard/select_mode.html', {'level': level})

# 問題数セレクト
def select_num_questions(request):
    # ヘルパー関数で難易度とモードを取得
    level, mode, _ = get_quiz_session_data(request)
    if not(level and mode):
        messages.error(request, 'エラーが発生しました。再度選択してください')
        return redirect('select_level')
    
    # POSTリクエスト
    if request.method == 'POST':
        # ポストデータの問題数を取得
        num_questions = request.POST.get('num_questions')
        # num_questionsのバリデーション
        if num_questions is None or not num_questions.isdigit() or int(num_questions) <= 0:
            messages.error(request, 'エラーが発生しました。再度問題数を選択してください')
            # もう一度問題数セレクトを表示
            return render(request, 'flashcard/select_num_questions.html', {'level': level, 'mode': mode})
        # 正常な場合は、セッションに保存しリダイレクト
        request.session['num_questions'] = int(num_questions)
        return redirect('quiz')
    
    # GETリクエスト
    return render(request, 'flashcard/select_num_questions.html', {'level': level, 'mode': mode})

# 単語帳クイズの初期設定を行う関数
def quiz(request):
    # ヘルパー関数を使用し、データを取得
    level, mode, num_questions = get_quiz_session_data(request)
    if not (level and mode and num_questions):
        messages.error(request, 'エラーが発生しました。難易度選択からお願いします')
        return redirect('select_level')
    
    words = Word.objects.filter(level_id=level.id) # 選択した難易度の単語を全て抽出
    # 抽出した単語が選択した出題数より少ない場合、エラーにならないための処理
    total_questions = min(num_questions, words.count())
    # total_questionsの数だけ、wordsからidで取得
    questions = random.sample(list(words.values_list('id', flat=True)), total_questions)
    question_index = 0
    score = 0
    # 途中経過保存用UserProgressモデルを作成
    user_progress = UserProgress.objects.create(
        user=request.user,
        level=level,
        mode=mode,
        score=score,
        total_questions=total_questions,
        current_question_index=question_index,
        question_ids=json.dumps(questions),
    )
    # questionsからインデックスをquestion_indexでidを取得
    question_id = questions[question_index]
    # Wordモデルからquestion_idで問題を取得
    current_question = Word.objects.get(id=question_id)
    
    context = {
        'current_question': current_question,
        'user_progress': user_progress,
    }
    
    return render(request, 'flashcard/quiz.html', context)

# 現在の問題を取得するヘルパー関数
def get_current_question(request, progress_id):
    user_progress = get_object_or_404(UserProgress, id=progress_id, user=request.user, is_completed=False)
    questions = json.loads(user_progress.question_ids)
    question_id = questions[user_progress.current_question_index]
    current_question = get_object_or_404(Word, id=question_id)
    
    return user_progress, current_question

# 中断データで再開
def quiz_restart(request, progress_id):
    # get_current_questionで進捗状況と現在の問題を取得
    user_progress, current_question = get_current_question(request, progress_id)
    
    context = {
        'current_question': current_question,
        'user_progress': user_progress,        
    }
    
    return render(request, 'flashcard/quiz.html', context)


# 回答の正誤を判定する関数
def check_answer(request, progress_id):
    # get_current_questionで進捗状況と現在の問題を取得
    user_progress, current_question = get_current_question(request, progress_id)
    answer = request.POST.get('answer').strip().lower() #POSTリクエストからanswerを取得
    # 問題の解答を取得
    correct_answer = current_question.english if user_progress.mode == 'en' else current_question.japanese.split(',')
    if request.method == 'POST':
        # 英訳モード
        if user_progress.mode == 'en':
            if answer == correct_answer:
                messages.success(request, '正解！！！！')
                user_progress.score += 1 # 正解数を１加算
            else:
                messages.error(request, '残念')
        else: # 和訳モード
            if any(answer == correct_answer_japanese.strip() for correct_answer_japanese in correct_answer):
                messages.success(request, '正解！！！！')
                user_progress.score += 1 # 正解数を１加算
            else:
                messages.error(request, '残念')
                
        user_progress.current_question_index += 1 # 問題番号を1加算
        
        # 問題数の確認
        # current_question_indexが総出題数以上
        if user_progress.current_question_index >= user_progress.total_questions:
            user_progress.is_completed = True
            user_progress.is_paused = False
            user_progress.save()
            return render(request, 'flashcard/last_check_answer.html', {'user_progress':user_progress, 'current_question': current_question})
        else:
            user_progress.save()
            return render(request, 'flashcard/check_answer.html', {'user_progress': user_progress, 'current_question': current_question})
    
    # POSTリクエスト以外は404エラーを返す
    else:
        raise Http404('Page Not Found')

# クイズ中断用関数
def pause_quiz(request, progress_id):
    user_progress = get_object_or_404(UserProgress, id=progress_id, user=request.user)
    
    if not user_progress.is_completed:
        # user_progressを保存する
        user_progress.is_paused = True
        user_progress.save()

    messages.success(request, '途中経過を保存しました')
    return redirect('user_home')


def result(request, progress_id):
    user_progress = get_object_or_404(UserProgress, id=progress_id)
    correct_answer_rate = int( user_progress.score / user_progress.total_questions * 100)
    context = {
        'correct_answer_rate':correct_answer_rate,
        'user_progress': user_progress,
    }
    
    return render(request, 'flashcard/result.html', context)



'''
2024/9/16 コードはオッケー。UI変更のため一旦コメントアウトし保存
# 問題数セレクト
def select_num_questions(request):
    # ヘルパー関数で難易度とモードを取得
    level, mode, _ = get_quiz_session_data(request)
    if not(level and mode):
        messages.error(request, 'エラーが発生しました。再度選択してください')
        return redirect('select_level')
    
    # POSTリクエスト
    if request.method == 'POST':
        # ポストデータの問題数を取得
        num_questions = request.POST.get('num_questions')
        # num_questionsのバリデーション
        if num_questions is None or not num_questions.isdigit() or int(num_questions) <= 0:
            messages.error(request, 'エラーが発生しました。再度問題数を選択してください')
            # もう一度問題数セレクトを表示
            return render(request, 'flashcard/select_num_questions.html', {'level': level, 'mode': mode})
        # 正常な場合は、セッションに保存しリダイレクト
        request.session['num_questions'] = int(num_questions)
        return redirect('select_quiz')
    
    # GETリクエスト
    return render(request, 'flashcard/select_num_questions.html', {'level': level, 'mode': mode})


# 「最初から」か「続きから」を選択する
def select_quiz(request):
    # ヘルパー関数を使用し、level他を取得
    level, mode, num_questions = get_quiz_session_data(request)
    if not (level and mode and num_questions):
        messages.error(request, 'エラーが発生しました。最初からお願いします')
        return redirect('select_level')
    
    user_progress = UserProgress.objects.filter(user=request.user, level=level, mode=mode, total_questions=num_questions, is_completed=False).first()
    
    # POSTリクエスト
    if request.method == 'POST':
        # POStリクエストからquiz_mode(newかcontinue)を取得
        selection = request.POST.get('quiz_mode')
        
        # 「最初から」を選んだ場合、新しくクイズを開始する
        if selection == 'new':
            return redirect('quiz')
        # 「前回の続きから」はuser_progress.idからデータを取得し、再開する
        elif selection == 'continue':
            user_progress_data = UserProgress.objects.filter(user=request.user, level=level, mode=mode, total_questions=num_questions, is_completed=False).all()
            return render(request, 'flashcard/show_paused_data.html', {'user_progress_data': user_progress_data})
            # return redirect('quiz_restart', progress_id=user_progress.id)
        else:
            messages.error(request, 'エラーが発生しました。最初からお願いします。')
            return redirect('select_level')
    # GETリクエストの場合は、フォームを表示する
    context = {
        'level': level,
        'mode': mode,
        'num_questions': num_questions,
        'user_progress': user_progress,
    }
    return render(request, 'flashcard/select_quiz.html', context)
'''