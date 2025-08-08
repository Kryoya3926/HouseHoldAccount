from django.forms import ModelForm
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
