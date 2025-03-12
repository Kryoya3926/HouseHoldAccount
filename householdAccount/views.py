from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.utils import timezone
from .models import AccountBook

class BookListView(View):
    def get(self,request,*args,**kwargs):
        context={}
        #家計簿の情報を取得
        hhAccount=AccountBook.objects.order_by('date')
        context['hhAccount']=hhAccount
        return render(request, "book/book_list.html", context)

book_list=BookListView.as_view()
