# contact/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InquiryForm


@login_required
def contact_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)  # 一旦保存を延期
            inquiry.user = request.user  # ログインしているユーザーをセット
            inquiry.save()  # 保存
            messages.success(request, 'お問い合わせを送信しました')
            return redirect('detail')
    else:
        form = InquiryForm()
    return render(request, 'contact/contact.html', {'form': form})
