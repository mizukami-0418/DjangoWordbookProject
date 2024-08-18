from django import forms
from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='ユーザー名')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワード確認', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'confirm_password')
        
    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('パスワード不一致')
        return cd['confirm_password']


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)

class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='ユーザー名')
    email = forms.EmailField(label='メールアドレス')
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード確認', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('パスワード不一致')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user