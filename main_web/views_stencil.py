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
    #对传入进行解码
    name_decode = name.encode('utf-8')
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
                    'c1:ATA': ata}

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