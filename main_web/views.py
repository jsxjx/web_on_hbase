# coding:utf-8
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from decode_all_function import MERGE_DECODE_LIST
from models import save_decode_list_to_hbase

import time
import socket

def home(request):
    return render(request, 'home.html')

def storing_data(request):

    allstarttime = time.clock()
    decode_list = MERGE_DECODE_LIST()

    computer_name = socket.getfqdn(socket.gethostname())
    if computer_name == "wxjd-61222177.cq.airchina.com.cn":
        #单位电脑路径
        dir_path = r'G:\QAR_DATA\append_upload'
    else:
        #服务器电脑路径
        dir_path = '/opt/QAR_DATA/hbase_append_upload'
    decode_list.all_decode_list(dir_path, save_decode_list_to_hbase)
    #decode_list.all_decode_list(dir_path, decode_list.save_to_csv)

    allendtime = time.clock()
    print u"全参数译码总耗时：%s" % (allendtime - allstarttime)

    return HttpResponse("已完成数据存入")
