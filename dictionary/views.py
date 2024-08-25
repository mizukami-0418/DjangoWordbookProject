from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Word

# モード選択
@login_required
def mode_choice(request):
    return render(request, 'dictionary/mode_choice.html')

# 単語検索機能
@login_required
def search(request):
    query = request.GET.get('query', '')  # 検索クエリを取得
    results = []
    
    if query:
        # 英語または日本語で検索
        results = Word.objects.filter(
            Q(english__icontains=query) | Q(japanese__icontains=query)
        )
    
    return render(request, 'dictionary/search.html', {'results': results, 'query': query})

# 英和辞典
@login_required
def search_english(request):
    query = request.GET.get('query', '')  # 検索クエリを取得
    language = request.GET.get('language', 'ja')  # 言語指定を取得
    results = []
    
    if query:
        # 日本語で検索
        results = Word.objects.filter(
            Q(japanese__icontains=query)
        )
    # 初回表示時に空の状態でレンダリングする場合は以下のように設定
    else:
        return render(request, 'dictionary/search_english.html', {'results': results, 'query': query})
    
    
    return render(request, 'dictionary/search_result.html', {'results': results, 'query': query, 'language': language})
    


# 和英辞典
@login_required
def search_japanese(request):
    query = request.GET.get('query', '')  # 検索クエリを取得
    language = request.GET.get('language', 'en')  # 言語指定を取得
    results = []
    
    if query:
        # 英語で検索
        results = Word.objects.filter(
            Q(english__icontains=query)
        )
        # 初回表示時に空の状態でレンダリングする場合は以下のように設定
    else:
        return render(request, 'dictionary/search_japanese.html', {'results': results, 'query': query})
    
    return render(request, 'dictionary/search_result.html', {'results': results, 'query': query, 'language': language})
