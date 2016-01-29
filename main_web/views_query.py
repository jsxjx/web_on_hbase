# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from hbase_function import HBASE_interface
import json

def ajax_single_para(request):
    hbase_interface = HBASE_interface()
    post_index = request.GET.get('column_index', None)
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

def table_list(request):
    hbase_interface = HBASE_interface()
    tablename = "tablename_index"
    cf_set = ['c1:Aircraft_Identification',
              'c1:updata_Date',
              'c1:updata_Time']
    result_scan_dict = hbase_interface.query_table(tablename,cf_set)
    result_list = []
    for key, value in result_scan_dict.items():
        single = {'index' : key,
                  'Aircraft_Identification' : value['c1:Aircraft_Identification'],
                  'updata_Date':value['c1:updata_Date'],
                  'updata_Time':value['c1:updata_Time'],}
        result_list.append(single)
    result_json = json.dumps(result_list)
    return render(request, 'table_list.html',{'result_json': result_json})