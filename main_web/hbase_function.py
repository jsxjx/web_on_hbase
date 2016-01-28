#coding=utf-8

import happybase
import time

class HBASE_interface():

    def __init__(self):
        pass

    def connect_hbase(self):
        print u"%s 连接数据库：" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        connection = happybase.Connection(host='10.210.180.43',
                                         port=9090,
                                         timeout = None,
                                         autoconnect=True,
                                         compat='0.94',
                                         )
        print u"%s 连接数据库完毕：" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #print connection.tables()

    # 开始创建数据表
    def create_table(self, table_name):
        print u"%s 连接数据库：" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        connection = happybase.Connection(host='10.210.180.43',
                                         port=9090,
                                         timeout = None,
                                         autoconnect=True,
                                         compat='0.94',
                                         )
        print u"%s 连接数据库完毕：" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        connection.create_table(
            table_name,
            {'c1': dict(max_versions=1, compression='GZ'),
             'c2': dict(max_versions=1, compression='GZ'),
             'c3': dict(max_versions=1, compression='GZ'),
            }
        )
