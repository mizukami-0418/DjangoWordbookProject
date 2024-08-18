# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .forms import UserCreationForm

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    # リスト画面の表示項目とフィルター機能をもつ項目
    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    list_filter = ('email', 'username','is_staff', 'is_superuser')

    # ユーザー選択時に表示されるフィールド
    fieldsets = (
        ('ユーザー情報', {'fields': ('email', 'username')}),
        ('権限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # 管理者画面でのユーザー作成時のフィールドを設定
    add_fieldsets = (
        ('ユーザー作成', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username') # 検索するフィールド
    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)