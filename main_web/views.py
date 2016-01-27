# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def storing_data(request):

    return HttpResponse("已完成数据存入")
