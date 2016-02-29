# coding:utf-8
from django.db import models

# Create your models here.
import happybase
import time,datetime
from hbase_function import HBASE_interface
from second_storing import Second_Storing

def save_decode_list_to_hbase(list_all_para_turn, file):
    hbase_interface = HBASE_interface()
    connection = happybase.Connection(host='10.210.180.43',
                                     port=9090,
                                     timeout = None,
                                     autoconnect=True,
                                     compat='0.94',
                                     )
    # 向索引表中插入数据分表的表头信息
    table_tablename_index = connection.table("tablename_index")
    pro_Aircraft_Identification = file[0:6]
    pro_updata_Date = file[7:11] + '-' + file[11:13] + '-' + file[13:15]
    pro_updata_Time = file[15:17] + ':' + file[17:19] + ':' + file[19:21]
    dic_table_info = {'c1:Aircraft_Identification': pro_Aircraft_Identification,
                      'c1:updata_Date': pro_updata_Date,
                      'c1:updata_Time':pro_updata_Time}

    table_tablename_index.put(file[0:21], dic_table_info)
    # 测试速度时用
    #hbase_interface.delete_table(file[0:21])
    #建立分表，并向分表中插入数据
    hbase_interface.create_table(file[0:21])
    table = connection.table(file[0:21])
    print table
    happybase_start_time = datetime.datetime.now()
    b = table.batch()
    counter_list_all_para = len(list_all_para_turn)
    counter_list_columns = len(list_all_para_turn[0])

    # 按python list 标号从零开始改为从一开始，以符合数据库设计
    counter_list_columns_app_1 = counter_list_columns + 1
    put_table_data = []
    for i in range(0, counter_list_all_para):
        #print u"第 %s 行"%i

        if i == 0:
            str_i = str(i).zfill(5)
        elif i == 1:
            str_i = 'UNITS'
        else:
            str_i = str(i - 1).zfill(5)
        dic_j = {}
        for j in range(1, counter_list_columns_app_1):
            str_value = str(list_all_para_turn[i][j-1]) #对应在list中的下标要减一
            dic_j['c1:'+ str(j)] = str_value

        put_table_data.append([str_i, dic_j])

    print u"%s 开始HBASE插入" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    start_put_time = datetime.datetime.now()
    put_data(file[0:21], put_table_data, counter_list_all_para)
    end_put_time = datetime.datetime.now()
    print u"%s 结束HBASE插入" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print u"插入耗时： %s s" %((end_put_time - start_put_time).seconds)
    #b.send()
    #进行GMT的处理
    second_storing = Second_Storing()
    second_storing.merge_GMT_time(file[0:21])

    happybase_end_time = datetime.datetime.now()
    #print u"存入耗时： %s"%((happybase_end_time - happybase_start_time).seconds)



pool = happybase.ConnectionPool(size=66,
                                host='10.210.180.43',
                                port=9090,
                                timeout = None,
                                autoconnect=True,
                                compat='0.94',)
from multiprocessing import Pool
import os, time, random
def put_data(table_name, list_put_table_data, counter_list_all_para):

    cut_number = (counter_list_all_para//74) + 1
    #cut_number = 1
    print "进程数： %s" % cut_number
    list_cut = div_list(list_put_table_data, cut_number)
    print list_cut[0][0][0], list_cut[0][-1][0]
    #print list_cut[1][0][0], list_cut[1][-1][0]
    p = Pool()
    for i in range(cut_number):
        p.apply_async(threading_put_data, args=(table_name, list_cut[i]))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'


def threading_put_data(table_name, list_put_table_data):
    connection = happybase.Connection(host='10.210.180.43',
                                     port=9090,
                                     timeout = None,
                                     autoconnect=True,
                                     compat='0.94',
                                     )
    table = connection.table(table_name)
    for i in range(0, len(list_put_table_data)):
        table.put(list_put_table_data[i][0], list_put_table_data[i][1])

def div_list(ls,n):
    if not isinstance(ls,list) or not isinstance(n,int):
        return []
    ls_len = len(ls)
    if n<=0 or 0==ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = ls_len/n
        k = ls_len%n
        ### j,j,j,...(前面有n-1个j),j+k
        #步长j,次数n-1
        ls_return = []
        for i in xrange(0,(n-1)*j,j):
            ls_return.append(ls[i:i+j])
        #算上末尾的j+k
        ls_return.append(ls[(n-1)*j:])
        return ls_return
