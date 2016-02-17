# coding:utf-8
from django.db import models

# Create your models here.
import happybase
import time
from hbase_function import HBASE_interface

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

    #建立分表，并向分表中插入数据
    hbase_interface.create_table(file[0:21])
    table = connection.table(file[0:21])
    print table
    happybase_start_time = time.clock()
    b = table.batch()
    counter_list_all_para = len(list_all_para_turn)
    counter_list_columns = len(list_all_para_turn[0])

    # 按python list 标号从零开始改为从一开始，以符合数据库设计
    counter_list_columns_app_1 = counter_list_columns + 1
    for i in range(0, counter_list_all_para):
        #print u"第 %s 行"%i
        str_i = str(i).zfill(5)
        dic_j = {}
        for j in range(1, counter_list_columns_app_1):
            str_value = str(list_all_para_turn[i][j-1]) #对应在list中的下标要减一
            dic_j['c1:'+ str(j)] = str_value

        table.put(str_i, dic_j)

    #b.send()

    happybase_end_time = time.clock()
    print u"存入耗时： %s"%(happybase_end_time - happybase_start_time)