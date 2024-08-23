# contact/forms.py

from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['subject', 'context']
        labels = {
            'subject': '件名',
            'context': '問い合わせ内容',
        }
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': '件名'}),
            'context': forms.Textarea(attrs={'placeholder': 'お問い合わせ内容をご記入ください'}),
        }
