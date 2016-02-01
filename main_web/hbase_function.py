#coding=utf-8

import happybase
import time
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