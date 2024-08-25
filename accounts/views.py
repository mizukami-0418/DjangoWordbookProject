from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, '登録完了')
            return redirect('user_home')
        else:
            messages.error(request, '登録失敗')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'ログイン')
                return redirect(reverse('user_home'))
            else:
                messages.error(request, 'ログインできず')
        else:
            messages.error(request, '入力ミスあり')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'ログアウトしました')
    return redirect('home')


@login_required
def user_home(request):
    return render(request, 'accounts/user_home.html')

@login_required
def user_detail(request):
    return render(request, 'accounts/user_detail.html')

@login_required
def user_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'ユーザー情報を更新しました')
            return redirect('detail')
        else:
            messages.error(request, '失敗したので再入力してください')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'accounts/user_edit.html', {'form': form})