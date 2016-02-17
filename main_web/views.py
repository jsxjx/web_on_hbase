# coding:utf-8
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from decode_all_function import MERGE_DECODE_LIST
from models import save_decode_list_to_hbase
from second_storing import Second_Storing
import time

def home(request):
    return render(request, 'home.html')

def storing_data(request):

    allstarttime = time.clock()
    decode_list = MERGE_DECODE_LIST()
    #单位电脑路径
    #dir_path = r'G:\QAR_DATA\for_test_wgl'
    #测试路径
    dir_path = r'G:\QAR_DATA\append_upload'
    decode_list.all_decode_list(dir_path, save_decode_list_to_hbase)

    allendtime = time.clock()
    print u"全参数译码总耗时：%s" % (allendtime - allstarttime)
    second_storing = Second_Storing()
    second_storing.merge_GMT_time()
    return HttpResponse("已完成数据存入")
