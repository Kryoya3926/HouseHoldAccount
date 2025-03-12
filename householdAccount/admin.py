from django.contrib import admin

# Register your models here.
from .models import Category, AccountBook
admin.site.register(AccountBook)
admin.site.register(Category)
