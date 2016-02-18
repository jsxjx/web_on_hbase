# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from hbase_function import HBASE_interface
from hbase_function import LIST_to_STR
from aircraft_config import AC_WQAR_CONFIG
import json

def all_childtable_index_list(request):
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
    return render(request, 'all_childtable_index_list.html',{'result_json': result_json})

def childtable(request, flight_id):
    list = [flight_id]
    json_list = json.dumps(list)

    hbase_interface = HBASE_interface()
    table_name = "stencil_config"
    cf_set = ['c1:WQAR512_IDC',
              'c1:WQAR256_IDC',
              'c1:NAME']
    result_scan_dict = hbase_interface.query_table(table_name, cf_set)
    result_list = []
    for key, value in result_scan_dict.items():
        single = {'index' : key,
                  'NAME' : value['c1:NAME']
                  }
        result_list.append(single)

    return render(request, 'childtable.html', {'json_list': json_list,
                                               'stencil_option': result_list})

def ajax_some_para(request):
    hbase_interface = HBASE_interface()
    list_str = LIST_to_STR()
    post_index = request.GET.get('value_conf', None)
    print post_index
    post_flight_id = request.GET.get('flight_id', None)
    aircraft_id = post_flight_id[0:6]
    # 读取模版表的存储详情
    table_stencil_name = "stencil_config"
    cf_set_stencil = ['c1:WQAR512_IDC',
                      'c1:WQAR256_IDC',
                      'c1:NAME']
    result_scan_dict = hbase_interface.query_table(table_stencil_name,cf_set_stencil)

    dict_stencil_config = result_scan_dict[post_index]
    str_WQAR256 = dict_stencil_config['c1:WQAR256_IDC']
    str_WQAR512 = dict_stencil_config['c1:WQAR512_IDC']
    list_WQAR256 = list_str.str_to_int(str_WQAR256)
    list_WQAR512 = list_str.str_to_int(str_WQAR512)

    # 机号构型判断
    ac_wqar_config = AC_WQAR_CONFIG()
    if aircraft_id in ac_wqar_config.WQAR512_SERISE_list:
        model = list_WQAR512
    elif aircraft_id in ac_wqar_config.WQAR256_SERISE_list:
        model = list_WQAR256
    else:
        return HttpResponse("无此机号")

    tablename = post_flight_id
    cf_set = []

    for item in model:
        cf_set.append('c1:' + str(item))


    result_scan_dict = hbase_interface.query_table(tablename,cf_set)
    result_list = []
    para_name_dic = result_scan_dict['00000']
    for key, value in result_scan_dict.items():
        single = {'index' : key}
        for key_para, value_para in value.items():
            para_name = para_name_dic[key_para]
            single[para_name] = value_para

        result_list.append(single)

    #查询出C2的值
    cf_set_c2 = ['c2:1']
    dict_c2_scan = hbase_interface.query_table(tablename,cf_set_c2)
    dict_c2_para_name = dict_c2_scan['00000']
    list_c1_c2 = []
    i = 0
    for key, value in dict_c2_scan.items():
        single = result_list[i]
        for key_para, value_para in value.items():
            para_name = dict_c2_para_name[key_para]
            single[para_name] = value_para
        list_c1_c2.append(single)
        i = i + 1

    result_json = json.dumps(list_c1_c2)
    return HttpResponse(result_json)