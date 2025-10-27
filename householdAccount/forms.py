from django.forms import ModelForm
from django import forms
from .models import AccountBook

class BookForm(ModelForm):
    class Meta:
        model=AccountBook
        fields=("date","category","money_amount","memo")
        labels={
            'date': '日付',
            'category': 'カテゴリー',
            'money_amount': '金額',
            'memo': 'メモ',
        }

class BookSearchForm(forms.Form):
    key_word=forms.CharField(label='検索キーワード', required=False)

class CSVUpdateForm(forms.Form):
    file=forms.FileField(label="CSVファイル", help_text="拡張子がCSVのファイルをアップロードしてください。")
