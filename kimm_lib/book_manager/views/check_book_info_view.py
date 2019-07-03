from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from book_manager.forms import *
from book_manager.models.book import Book
from book_manager.models.bookinfo import BookInfo
from book_manager.models.category import Category
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check

import datetime

class CheckBookInfoView(DetailView):
    template_name ='book_manager/check_bookinfo.html'
    model = BookInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        bookinfo = BookInfo.objects.get(id = id)
        context['title'] = bookinfo.title
        context['id'] = bookinfo.id
        return context

    def post(self, request, *args, **kwargs):
        bookinfo = BookInfo.objects.get(id = self.kwargs['pk'])
        records = Book.objects.filter(bookinfo = bookinfo, disposal_date__isnull = True)
        if records.first() is not None:
            return redirect(to = '/book_manager/error_bookinfo')
        else :
            bookinfo.delete_date = datetime.date.today()
            bookinfo.save()
            return redirect(to ='/book_manager/complete_bookinfo')

    def get(self, request, **kwargs):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
