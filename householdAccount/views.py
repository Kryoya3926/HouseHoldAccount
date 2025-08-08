from django.shortcuts import render, reverse
from django.views.generic import View, DetailView, CreateView, UpdateView
from .models import AccountBook
from .forms import BookForm
from django.contrib.auth.mixins import LoginRequiredMixin

class BookListView(View):
    def get(self, request, *args, **kwargs):
        context={}
        #家計簿の情報を取得
        hhAccount=AccountBook.objects.order_by('date')
        context['hhAccount']=hhAccount
        return render(request, "book/book_list.html", context)

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
