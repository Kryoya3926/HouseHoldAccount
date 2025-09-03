from django.shortcuts import render, reverse
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView, ListView
from .models import AccountBook
from .forms import BookForm, BookSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class BookListView(ListView):
    model=AccountBook
    template_name='book/book_list.html'

    def get_queryset(self):
        form=BookSearchForm(self.request.GET or None)
        self.form=form

        queryset=super().get_queryset()
        if form.is_valid():
            key_word=form.cleaned_data.get('key_word')
            if key_word:
                for word in key_word.split():
                    queryset=queryset.filter(Q(category__categories__icontains=word)|Q(category__categoryType__icontains=word)|Q(memo__icontains=word)) #Categoryモデルの中のcategoriesを指定
        return queryset

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['form']=self.form
        return context

book_list=BookListView.as_view()

class BookDetailView(DetailView):
    model=AccountBook
    template_name="book/book_detail.html"

book_detail=BookDetailView.as_view()

class BookCreateView(LoginRequiredMixin, CreateView):
    model=AccountBook
    form_class=BookForm
    template_name='book/book_add.html'

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('book:book_list')

class BookUpdateView(UpdateView):
    model=AccountBook
    form_class=BookForm
    template_name='book/book_update.html'

    def get_success_url(self):
        return reverse('book:book_detail', args=(self.object.id,))

class BookDeleteView(DeleteView):
    model=AccountBook
    template_name='book/book_delete.html'
    def get_success_url(self):
        return reverse('book:book_list')
