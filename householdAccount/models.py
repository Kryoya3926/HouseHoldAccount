"""
 Blogアプリ
 データモデル

 Filename: models.py
 Date: 2025.1.22
 Written by: Ryoya Kurihara

"""
from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    categories=models.CharField(max_length=200)
    categoryType=models.CharField(max_length=50)

    def __str__(self):
        return "{} {}".format(self.categoryType,self.categories)

class AccountBook(models.Model):
    """
    家計簿クラス

    date:日付
    category:カテゴリ
    money_amount:金額
    memo:メモ

    """
    date=models.DateField(default=timezone.now)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    money_amount=models.IntegerField()
    memo=models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{} {}".format(self.date,self.category)
