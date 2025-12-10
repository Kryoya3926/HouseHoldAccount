from django.shortcuts import render, reverse
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView, ListView, FormView
from .models import AccountBook, Category
from .forms import BookForm, BookSearchForm, CSVUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
import io
import pandas as pd
import numpy as np

class BookListView(ListView):
    model=AccountBook
    template_name='book/book_list.html'
    ordering=['-date']
    paginate_by=5

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

class BookDataImport(LoginRequiredMixin, FormView):
    template_name="book/import.html"
    success_url=reverse_lazy("book:book_list")
    form_class=CSVUpdateForm

    def form_valid(self, form):
        #データの読み込み
        csvfile=io.TextIOWrapper(form.cleaned_data["file"], encoding="cp932")

        df=pd.read_csv(csvfile,
                       encoding="SHIFT-JIS", #文字コード
                       usecols=[0,1,2,3,], #使用する列
                       names=["date", "category", "money_amount", "memo"],) #カラム名

        #datetimeに変換
        df["date"]=pd.to_datetime(df["date"], format="%Y/%m/%d")

        df=df.fillna("")
        data_np=np.asarray(df)


        for row in data_np:
            data, created=Category.objects.get_or_create(categories=row[1])

            if data.categories in ("給料","臨時収入"):
                data.categoryType="収入"
            else:
                data.categoryType="出費"

            data.save()

            AccountBook.objects.create(date=row[0], category=data, money_amount=row[2], memo=row[3])

        return super().form_valid(form)

class GraphView(View):
    """
        グラフ表示用のJavaScriptを生成するビュー
    """
    template_name="book/script.js"

    def get(self, request, *args, **kwargs):
        """
            getメソッド呼び出し時にjavascriptを生成
        """

        #指定されたcategoryTypeのCategoryモデルとAccountBookモデル
        accountbook_data=AccountBook.objects.select_related('category')

        #データのプロット
        context={}
        income={}
        outcome={}
        for data in accountbook_data:
            if data.category.categoryType=="収入":
                if not data.category.categories in income.keys():
                    income[data.category.categories]=data.money_amount
                else:
                    income[data.category.categories]+=data.money_amount
            else:
                if not data.category.categories in outcome.keys():
                    outcome[data.category.categories]=data.money_amount
                else:
                    outcome[data.category.categories]+=data.money_amount

        context["categories_income"]=[data for data in income.keys()]
        context["money_amount_income"]=[data for data in income.values()]
        context["categories_outcome"]=[data for data in outcome.keys()]
        context["money_amount_outcome"]=[data for data in outcome.values()]

        return render(request, self.template_name, context, content_type='text/javascript')
