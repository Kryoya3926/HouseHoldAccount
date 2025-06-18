from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.views.generic import DetailView, UpdateView, CreateView
from django.shortcuts import resolve_url
from .forms import UserUpdateForm, UserCreateForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception=True

    def test_func(self):
        user=self.request.user
        return user.pk==self.kwargs['pk'] or user.is_superuser

class UserDetail(OnlyYouMixin, DetailView):
    model=User
    template_name='accounts/user_detail.html'

class UserUpdate(OnlyYouMixin, UpdateView):
    model=User
    form_class=UserUpdateForm
    template_name='accounts/user_form.html'

    def get_success_url(self):
        return resolve_url('accounts:user_detail', pk=self.kwargs['pk'])

class UserCreate(CreateView):
    template_name="registration/user_create.html"
    form_class=UserCreateForm
    success_url=reverse_lazy('login')
