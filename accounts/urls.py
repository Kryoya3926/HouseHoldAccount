from django.urls import path
from . import views

app_name='accounts'
urlpatterns=[
    path('profile/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('profile/update/<int:pk>', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('create/',views.UserCreate.as_view(),name='user_create'),
]
