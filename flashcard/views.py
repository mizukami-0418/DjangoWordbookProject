from django.shortcuts import render, get_object_or_404, redirect
from dictionary.models import Word, Level
from django.http import HttpResponse


def select_level(request):
    if request.method == 'POST':
        level_id = request.POST.get('level')
        return HttpResponse(level_id)
    else:
        levels = Level.objects.all()
    return render(request, 'flashcard/select_level.html', {'levels': levels})