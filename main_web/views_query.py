# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from hbase_function import HBASE_interface
import json

def ajax_single_para(request):
    hbase_interface = HBASE_interface()
    post_index = request.GET.get('column_index', None)
    post_flight_id = request.GET.get('flight_id', None)
    # 机号构型判断
    WQAR512_SERISE_list = ["B-1976","B-1956","B-5803","B-5679","B-1527","B-1738","B-5622","B-1942","B-1959",\
                           "B-5682","B-5297","B-5296","B-5583","B-1768","B-1765","B-1763","B-5582","B-1531","B-6496"]

    WQAR256_SERISE_list = ["B-2612","B-2613","B-2700","B-5201","B-5202","B-5203","B-5214","B-5217","B-5220",\
                           "B-5325","B-5327","B-5329","B-5390","B-5392","B-5398","B-5426","B-5443","B-5477",\
                           "B-5486","B-5496","B-5198","B-2649"]
    WQAR256_FUEL_MODEL = [65, 89, 90, 91, 214, 216, 224, 225, 232, 233, 234, 433, 434]
    WQAR512_FUEL_MODEL = [69, 96, 97, 98, 241, 242, 249, 250, 363, 364, 365, 394, 395]
    aircraft_id = post_flight_id[0:6]
    if aircraft_id in WQAR512_SERISE_list:
        model = WQAR512_FUEL_MODEL
    elif aircraft_id in WQAR256_SERISE_list:
        model = WQAR256_FUEL_MODEL
    else:
        return HttpResponse("无此机号")

    index = post_index.encode('utf-8')
    tablename = post_flight_id
    cf_set = []
    for item in model:
        cf_set.append('c1:' + str(item))

    result_scan_dict = hbase_interface.query_table(tablename,cf_set)
    result_list = []
    para_name_dic = result_scan_dict['00000']
    print para_name_dic.items()
    for key, value in result_scan_dict.items():
        single = {'index' : key}
        for key_para, value_para in value.items():
            para_name = para_name_dic[key_para]
            single[para_name] = value_para
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

def table_index(request, flight_id):
    list = [flight_id]
    json_list = json.dumps(list)
    return render(request, 'query_single_para_html.html', {'json_list': json_list})