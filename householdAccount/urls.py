from django.urls import path
from . import views

app_name='householdAccount'
urlpatterns=[
    path('', views.book_list, name='book_list'),
]
