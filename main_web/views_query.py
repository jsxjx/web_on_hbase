#coding=utf-8
# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from hbase_function import HBASE_interface
import json

def single_para_query(request):
    hbase_interface = HBASE_interface()
    if request.method == 'POST':
        post_index = request.POST['firstname']
    else:
        post_index = 1

    tablename = 'B-1527_20160125052953'
    cf_name = 'c1:1328'
    cf_set = ['c1:1328']
    result_scan_dict = hbase_interface.query_table(tablename,cf_set)
    result_list = []
    for key, value in result_scan_dict.items():
        single = {'index' : key, 'value' : value[cf_name]}
        result_list.append(single)
    result_json = json.dumps(result_list)
    return HttpResponse(result_json)

def ajax_single_para(request):
    hbase_interface = HBASE_interface()


    post_index = request.GET.get('stencil_name', None)
    index = post_index.encode('utf-8')
    tablename = 'B-1527_20160125052953'
    cf_str = 'c1:' + index
    cf_set = ['c1:' + index]
    result_scan_dict = hbase_interface.query_table(tablename,cf_set)
    result_list = []
    for key, value in result_scan_dict.items():
        single = {'index' : key, 'value' : value[cf_str]}
        result_list.append(single)
    result_json = json.dumps(result_list)
    return HttpResponse(result_json)

def query_single_para_html(request):
    return render(request, 'query_single_para_html.html')