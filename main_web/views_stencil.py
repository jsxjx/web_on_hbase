#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from hbase_function import HBASE_interface
from hbase_function import LIST_to_STR
from aircraft_config import AC_WQAR_CONFIG
import json


def storing_stencil(request):
    return render(request, 'storing_stencil_html.html')

def storing_stencil_ajax(request):
    #前端传入参数
    ata = request.GET.get('stencil_ATA', None)
    name = request.GET.get('stencil_name', None)
    para_256 = request.GET.get('stencil_256_para', None)
    para_512 = request.GET.get('stencil_512_para', None)
    creator = request.GET.get('stencil_creator', None)
    #对传入进行解码
    name_decode = name.encode('utf-8')
    creator_decode = creator.encode('utf-8')
    para_256_decode = para_256.split(',')
    para_512_decode = para_512.split(',')
    #防输错设计，前端多输入了，号，列表中有空值即去掉
    while '' in para_256_decode:
        para_256_decode.remove('')
    while '' in para_512_decode:
        para_512_decode.remove('')
    #存入数据库
    '''
    stencil.objects.create(configuration = conf, ATA = ata, \
                          stencil_name = name_decode, list_para = para_decode)
    '''
    hb_if = HBASE_interface()
    list_str = LIST_to_STR()
    table = hb_if.table('stencil_config')
    str_stencil_name = name_decode
    str_para_256 = list_str.int_to_str(para_256_decode)
    str_para_512 = list_str.int_to_str(para_512_decode)

    dict_cf_data = {'c1:NAME': str_stencil_name,
                    'c1:WQAR512_IDC': str_para_512,
                    'c1:WQAR256_IDC': str_para_256,
                    'c1:ATA': ata,
                    'c1:creator':creator_decode,
                    'c1:ECHARTS_256':';;',
                    'c1:ECHARTS_512':';;'}

    cf_set = ['c1:NAME']
    dict = hb_if.query_table('stencil_config', cf_set)
    table_max_index = len(dict.items())
    print "table max index: %s"  % table_max_index
    rowkey = (str(table_max_index + 1)).zfill(3)
    print rowkey
    print dict_cf_data
    table.put(rowkey, dict_cf_data)
    #回传前端，反馈结果
    para_256_post = ','.join(para_256_decode)
    para_512_post = ','.join(para_512_decode)
    text = '<br>已录入<br>模版：' + str(name_decode) + \
           '<br>参数256：' + str(para_256_post) + \
            '<br>参数512：' + str(para_512_post) + \
           '<br>章节：' + str(ata)
    return HttpResponse(text)

def stencil_list(request):
    hb_if = HBASE_interface()
    list_str = LIST_to_STR()
    table = hb_if.table('stencil_config')
    tablename = "stencil_config"
    cf_set = ['c1:NAME',
              'c1:ATA',
              'c1:creator',
              ]
    result_scan_dict = hb_if.query_table(tablename,cf_set)
    result_list = []
    for key, value in result_scan_dict.items():
        print key, value
        single = {'index' : key,
                  'NAME' : value['c1:NAME'],
                  'ATA':value['c1:ATA'],
                  'creator':value['c1:creator'],
                  }
        result_list.append(single)
    result_json = json.dumps(result_list)
    return render(request, 'stencil_list.html',{'result_json': result_json})

def edit_stencil(request, stencil_index_number):
    hb_if = HBASE_interface()
    list_str = LIST_to_STR()
    tablename = "stencil_config"
    table = hb_if.table(tablename)
    result_scan_dict = table.row(stencil_index_number)
    print result_scan_dict
    result_list = [result_scan_dict]
    result_json = json.dumps(result_list)

    print result_scan_dict['c1:WQAR256_IDC']
    print result_scan_dict['c1:WQAR512_IDC']

    list_WQAR256_model = list_str.str_to_int(result_scan_dict['c1:WQAR256_IDC'])
    list_WQAR512_model = list_str.str_to_int(result_scan_dict['c1:WQAR512_IDC'])
    list_WQAR256_para_index, list_WQAR512_para_index = list_str.make_para_id_list()
    result_list_256_id = []
    result_list_512_id = []
    for each_id_number in list_WQAR256_model:
        result_list_256_id.append(list_WQAR256_para_index[int(each_id_number)])
    for each_id_number in list_WQAR512_model:
        result_list_512_id.append(list_WQAR512_para_index[int(each_id_number)])

    print result_list_256_id,result_list_512_id

    return render(request, 'edit_stencil.html',{'result_json': result_json,
                                                'result_json_256':result_list_256_id,
                                                'result_json_512':result_list_512_id,
                                                'stencil_index_number':stencil_index_number})

def stencil_echarts(request):

    stencil_index_number = request.GET.get('stencil_index_number', None)
    post_string_256 = request.GET.get('post_string_256', None)
    post_string_512 = request.GET.get('post_string_512', None)
    rowkey = (str(stencil_index_number)).zfill(3)
    print rowkey
    hb_if = HBASE_interface()
    list_str = LIST_to_STR()
    table = hb_if.table('stencil_config')
    dict_cf_data = {'c1:ECHARTS_256': post_string_256,
                    'c1:ECHARTS_512': post_string_512
                    }
    table.put(rowkey, dict_cf_data)





    return HttpResponse("已录入")