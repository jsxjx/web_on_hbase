#coding=utf-8

from hbase_function import HBASE_interface
from hbase_function import LIST_to_STR
from aircraft_config import AC_WQAR_CONFIG

class Second_Storing:

    def __init__(self):
        self.hb_if = HBASE_interface()
        self.list_str = LIST_to_STR()
        self.ac_config = AC_WQAR_CONFIG()
        pass

    def merge_GMT_time(self, table_name):
        GMT_model_256 = [89, 90, 91]
        GMT_model_512 = [96, 97, 98]
        hb_if = self.hb_if
        list_str = self.list_str
        ac_config = self.ac_config

        # 飞机构型判断
        ac_number = table_name[0:6]
        if ac_number in ac_config.WQAR256_SERISE_list:
            model = GMT_model_256
        elif ac_number in ac_config.WQAR512_SERISE_list:
            model = GMT_model_512
        else:
            print '无此机号：' + table_name[0:6]
            return
        #连接数据库中的表
        table = hb_if.table(table_name)
        self.GMT_storing_to_c2(table_name, model)
        print table_name, table


    def GMT_storing_to_c2(self, table_name, model):
        hb_if = self.hb_if
        list_str = self.list_str
        ac_config = self.ac_config
        cf_set = hb_if.list_make_columns_family('c1', model)
        table = hb_if.table(table_name)
        result_scan_dict = hb_if.query_table(table_name,cf_set)
        #print result_scan_dict
        result_list = []
        para_name_dic = result_scan_dict['00000']
        #print para_name_dic
        GMT_time = ''
        list_GMT_time = []
        for key, value in result_scan_dict.items():
            #print key, value
            if key == "00000":
                list_GMT_time.append('$GMT TIME')
                table.put(key, {'c2:1': '$GMT TIME'})
                continue
            #时间单位的列表
            if key == "UNITS":
                print value
                table.put(key, {'c2:1': 'HH:MM:SS'})
                continue
            if value[cf_set[0]] == '':
                list_GMT_time.append(GMT_time)
                table.put(key, {'c2:1': GMT_time})
                continue

            for key2, value2 in value.items():
                value[key2] = (str(int(float(value2)))).zfill(2)
            seq = ':'
            GMT_time = seq.join([value[cf_set[0]], value[cf_set[1]], value[cf_set[2]]])
            list_GMT_time.append(GMT_time)
            table.put(key, {'c2:1': GMT_time})



'''
second_storing = Second_Storing()
second_storing.merge_GMT_time()
'''




