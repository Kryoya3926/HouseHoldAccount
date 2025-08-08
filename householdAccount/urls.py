from django.urls import path
from . import views

app_name='book'
urlpatterns=[
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/add/', views.BookCreateView.as_view(), name='book_add'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
]
