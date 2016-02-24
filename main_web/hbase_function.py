#coding=utf-8

import happybase
import time
import csv
from collections import OrderedDict

class HBASE_interface():

    def __init__(self):
        self.connect_hbase = self.connection_hbase()

    def connection_hbase(self):
        print u"%s 连接数据库" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        connection = happybase.Connection(host='10.210.180.43',
                                         port=9090,
                                         timeout = None,
                                         autoconnect=True,
                                         compat='0.94',
                                         )
        print u"%s 连接数据库完毕" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return connection
        #print connection.tables()

    def table(self, table_name):
        connection = self.connect_hbase
        table = connection.table(table_name)
        return table

    # 开始创建数据表
    def create_table(self, table_name):
        connection = self.connect_hbase
        connection.create_table(
            table_name,
            {'c1': dict(max_versions=1, compression='GZ'),
             'c2': dict(max_versions=1, compression='GZ'),
             'c3': dict(max_versions=1, compression='GZ'),
            }
        )
        print u"%s 已创建表：%s" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), table_name)

    def delete_table(self, table_name):
        connection = self.connect_hbase
        connection.delete_table(table_name, True)
        print u"%s 已删除表：%s" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), table_name)

    def query_table(self, table_name, family_colunm):
        connection = self.connect_hbase
        table = connection.table(table_name)
        scan_result = table.scan(columns = family_colunm)
        ordered_columns_dict = OrderedDict(scan_result)
        return ordered_columns_dict

    def list_query_tablenames(self):
        table_name = 'tablename_index'
        table = self.table(table_name)
        list_table_name = []
        for key, value in table.scan():
            list_table_name.append(key)
        return list_table_name

    def list_make_columns_family(self, str_cf_name, list_model):
        list_result = []
        for item in list_model:
            list_result.append(str_cf_name + ':' + str(item))
        return list_result



class LIST_to_STR():

    def __init__(self):
        pass

    def int_to_str(self, original_list):
        list_int_to_str = []
        for item in original_list:
            list_int_to_str.append(str(item))
        sep = ','
        str_list = sep.join(list_int_to_str)
        print u"列表转换成逗号分割的字符串：" + str_list
        return str_list

    def str_to_int(self, original_str):
        sep = ','
        list_str_to_list = original_str.split(sep)
        print u"逗号分割的字符串转换成列表："
        print list_str_to_list
        return list_str_to_list

    def opencsv(self, csv_file_name):
        #读取csv逻辑参数列表，解码大量逻辑参数
        f = open(csv_file_name,'rb')
        reader = csv.reader(f)
        list_index = []
        for row in reader:
            para_id_number = reader.line_num - 1
            para_id_name = str(para_id_number) + ':' + row[0]
            list_index.append(para_id_name)

        return list_index

    def make_para_id_list(self):
        csv_name_list = ['737-3C ALL.csv', '737-7 ALL.csv']
        list_WQAR256_para_index = []
        list_WQAR512_para_index = []

        list_WQAR256_para_index = list_WQAR256_para_index + self.opencsv(csv_name_list[0])
        list_WQAR512_para_index = list_WQAR512_para_index + self.opencsv(csv_name_list[1])

        return list_WQAR256_para_index, list_WQAR512_para_index

class Echarts_option():

    def __init__(self):
        pass

    def str_to_obj(self, option_string):
        list_1 = option_string.split(";")
        print list_1
        echarts_config_option = [{},{},{}]
        for index in range(3):
            if list_1[index] <> "":
                list_2 = list_1[index].split(",")
                print  list_2
                for item in list_2:
                    print item
                    id_type = item.split("_")
                    print id_type
                    echarts_config_option[index][id_type[0]] = id_type[1]
        print echarts_config_option
        '''
        #去除列表中空的项--未完成
        for item_index in range(3):
            print echarts_config_option[item_index]
            if not echarts_config_option[item_index] is None:
                echarts_config_option.pop(item_index)
        '''

        return echarts_config_option

    def judge_logic_echart(self, list_option):
        list_echart_index_of_logic = []
        list_to_str = LIST_to_STR()
        list_WQAR256_para_index, list_WQAR512_para_index = list_to_str.make_para_id_list()
        for index in range(3):

            for key, value in list_option[index].items():
                print "key,value"
                print key,value
                if key in list_WQAR512_para_index:
                    if list_WQAR512_para_index.index(key) >= 796:
                        list_echart_index_of_logic.append(index)
                        break
                elif key in list_WQAR256_para_index:
                    if list_WQAR256_para_index.index(key) >= 644:
                        list_echart_index_of_logic.append(index)
                        break

        return list_echart_index_of_logic
