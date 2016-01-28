# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from hbase_function import HBASE_interface
# coding:UTF-8
# 对文件夹下的所有raw.dat译码GMT、EGT
import os
import struct
import time
import csv
import numpy
from pandas import DataFrame

class WQAR_DECODE():

    def __init__(self):
        pass

    def SUPF_binary_decode(self, filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES):
        worddata = filedata[count+ICD_number:count+ICD_number+2]
        #到达末尾则不再算超帧数
        if worddata == '':
            return False
        int_word1 = struct.unpack("<h", worddata)[0]

        int_word1 = int_word1 >> (ICD_LSB-1)
        Remove_MSB = 2 ** (ICD_MSB - ICD_LSB + 1) -1
        int_word1 = int_word1 & Remove_MSB
        float_word1 = int_word1
        return float_word1

    def binary_decode(self, filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN):
        worddata = filedata[count+ICD_number:count+ICD_number+2]
        #print headworddata
        int_word1 = struct.unpack("<h", worddata)[0]
        #print hex(headword & 0xFFFF) , headword
        SIGN = int_word1 >> (ICD_MSB - 1)
        SIGN = SIGN & 1

        int_word1 = int_word1 >> (ICD_LSB-1)
        Remove_MSB = 2 ** (ICD_MSB - ICD_LSB + 1) -1
        int_word1 = int_word1 & Remove_MSB
        if ICD_SIGN == 'S':
            if SIGN == 0:
                float_word1 = int_word1 * ICD_RES
            else:
                float_word1 = - ( 2 ** (ICD_MSB - ICD_LSB + 1) - int_word1 )
                float_word1 = float_word1 * ICD_RES
        elif ICD_SIGN == "":
            float_word1 = int_word1 * ICD_RES
        return float_word1

    def frame(self, frame_number, filedata, ICD_MSB, ICD_LSB, ICD_WORD, ICD_SUBF, ICD_SUPF, ICD_RES, ICD_SIGN):
        ICD_number = (ICD_WORD-1) *2
        list_para = []
        #print type(filedata)
        #print len(filedata)
        for count in range(0, len(filedata), frame_number*2):
            headworddata = filedata[count:count + 2]
            #print headworddata
            headword = struct.unpack("<h", headworddata)[0]
            sycword_list = [583, 1464, 2631, 3512, -32185]
            if headword in sycword_list:
                #print "headword: %d" % headword
                if ICD_SUPF == 0:
                    if ICD_SUBF == 0:
                        float_word1 = self.binary_decode(filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN)
                        list_para.append(float_word1)
                    else:
                        if ICD_SUBF == (sycword_list.index(headword) + 1 ):
                            float_word1 = self.binary_decode(filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN)
                            list_para.append(float_word1)
                        else:
                            list_para.append("")
                elif ICD_SUPF <> 0:
                    if frame_number == 512 :
                        SUPF_word = self.SUPF_binary_decode(filedata,
                                                            (int(count/(4*frame_number*2)))*4*frame_number*2,
                                                            (499-1)*2, 9, 12, 1)
                    else:
                        SUPF_word = self.SUPF_binary_decode(filedata,
                                                            (int(count/(4*frame_number*2)))*4*frame_number*2 + 2*frame_number*2,
                                                            (256-1)*2, 9, 12, 1)
                    SUPF_word = SUPF_word +1
                    #print "SUPF_word: %d" % SUPF_word
                    if ICD_SUBF == 0:
                        if SUPF_word == ICD_SUPF:
                            float_word1 = self.binary_decode(filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN)
                            list_para.append(float_word1)
                        else:
                            list_para.append("")
                    elif ICD_SUBF <> 0:
                        if SUPF_word == ICD_SUPF:
                            #print SUPF_word
                            #print sycword_list.index(headword) + 1
                            if ICD_SUBF == (sycword_list.index(headword) + 1 ):
                                float_word1 = self.binary_decode(filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN)
                                list_para.append(float_word1)
                            else:
                                list_para.append("")
                        else:
                            list_para.append("")

        return list_para

    def logic_binary_decode(self, filedata, count, ICD_number, \
                            ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC):

        worddata = filedata[count+ICD_number:count+ICD_number+2]
        #print headworddata
        int_word1 = struct.unpack("<h", worddata)[0]
        int_word1 = int_word1 >> (ICD_LSB-1)
        Remove_MSB = 2 ** (ICD_MSB - ICD_LSB + 1) -1
        int_word1 = int_word1 & Remove_MSB
        result = 1
        if ICD_ONE_LOGIC <> "CODED":
            if int_word1 == 1:
                result = ICD_ONE_LOGIC
            elif int_word1 == 0:
                result = ICD_ZERO_LOGIC
        else:
            result = int_word1

        return result

    def frame_logic(self, frame_number, filedata, ICD_MSB, ICD_LSB, ICD_WORD, ICD_SUBF, ICD_SUPF,\
                    ICD_ONE_LOGIC, ICD_ZERO_LOGIC):

        ICD_number = (ICD_WORD-1) *2
        list_para = []
        #print type(filedata)
        #print len(filedata)
        for count in range(0, len(filedata), frame_number*2):
            headworddata = filedata[count:count + 2]
            #print headworddata
            headword = struct.unpack("<h", headworddata)[0]
            sycword_list = [583, 1464, 2631, 3512, -32185]
            if headword in sycword_list:
                #print "headword: %d" % headword
                if ICD_SUPF == 0:
                    if ICD_SUBF == 0:
                        float_word1 = self.logic_binary_decode(filedata, count, ICD_number, \
                                                         ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC)
                        list_para.append(float_word1)
                    else:
                        if ICD_SUBF == (sycword_list.index(headword) + 1 ):
                            float_word1 = self.logic_binary_decode(filedata, count, ICD_number, \
                                                         ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC)
                            list_para.append(float_word1)
                        else:
                            list_para.append("")
                elif ICD_SUPF <> 0:
                    if frame_number == 512 :
                        SUPF_word = self.SUPF_binary_decode(filedata, \
                                                            (int(count/(4*frame_number*2)))*4*frame_number*2,
                                                            (499-1)*2, 9, 12, 1)
                    else:
                        SUPF_word = self.SUPF_binary_decode(filedata, \
                                                            (int(count/(4*frame_number*2)))*4*frame_number*2 + 2*frame_number*2,
                                                            (256-1)*2, 9, 12, 1)

                    SUPF_word = SUPF_word +1
                    #print "SUPF_word: %d" % SUPF_word
                    if ICD_SUBF == 0:
                        if SUPF_word == ICD_SUPF:
                            float_word1 = self.logic_binary_decode(filedata, count, ICD_number, \
                                                         ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC)
                            list_para.append(float_word1)
                        else:
                            list_para.append("")
                    elif ICD_SUBF <> 0:
                        if SUPF_word == ICD_SUPF:
                            #print SUPF_word
                            #print sycword_list.index(headword) + 1
                            if ICD_SUBF == (sycword_list.index(headword) + 1 ):
                                float_word1 = self.logic_binary_decode(filedata, count, ICD_number, \
                                                         ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC)
                                list_para.append(float_word1)
                            else:
                                list_para.append("")
                        else:
                            list_para.append("")

        return list_para






import happybase
# 多线程库
from multiprocessing import Pool


# Create your views here.
def index(request):
    return render(request, 'index.html')

def storing_data(request):

    connection = happybase.Connection(host='10.210.180.43',
                                     port=9090,
                                     timeout = None,
                                     autoconnect=True,
                                     compat='0.94',
                                     )
    allstarttime = time.clock()
    wqar_decode = WQAR_DECODE()
    hbase_interface = HBASE_interface()
    #单位电脑路径
    path = r'/opt/QAR_DATA/for_one_test'

    #家里电脑路径
    #path = r'F:\TDRS_DATA\WQAR_RAW_DAT'
    dirs = os.listdir(path)
    WQAR512_SERISE_list = ["B-1976","B-1956","B-5803","B-5679","B-1527","B-1738","B-5622","B-1942","B-1959",\
                           "B-5682","B-5297","B-5296","B-5583","B-1768","B-1765","B-1763","B-5582","B-1531"]

    WQAR256_SERISE_list = ["B-2612","B-2613","B-2700","B-5201","B-5202","B-5203","B-5214","B-5217","B-5220",\
                           "B-5325","B-5327","B-5329","B-5390","B-5392","B-5398","B-5426","B-5443","B-5477",\
                           "B-5486","B-5496","B-5198","B-2649"]


    #file_output=file("GMT_EGT.txt","a+")
    for file in dirs:
        #初始化缓存列表
        list_single_para = []
        list_all_para = []
        if file[0:6] in WQAR512_SERISE_list:
            starttime = time.clock()
            single_path = path + '/' + file + '/' + 'raw.dat'
            if os.path.exists(single_path):
                file_object = open(single_path,'rb')
                filedata = file_object.read()
                file_object.close()

                #读取csv参数列表，解码大量数值参数
                with open('737-7 numeric.csv','rb') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if reader.line_num == 1:
                            continue

                        list_single_para = wqar_decode.frame(512, filedata, \
                                                         ICD_MSB=int(row[2]),\
                                                         ICD_LSB=int(row[3]), \
                                                         ICD_WORD=int(row[4]),\
                                                         ICD_SUBF=int(row[5]), \
                                                         ICD_SUPF=int(row[6]), \
                                                         ICD_RES=float(row[9]),\
                                                        ICD_SIGN=row[1])
                        list_single_para.insert(0, row[0])
                        list_all_para.append(list_single_para)

                #读取csv逻辑参数列表，解码大量逻辑参数
                with open('737-7 LOGIC.csv','rb') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if reader.line_num == 1:
                            continue

                        list_single_para = wqar_decode.frame_logic(512, filedata,
                                                                ICD_MSB = int(row[1]), \
                                                                ICD_LSB = int(row[2]), \
                                                                ICD_WORD = int(row[3]),\
                                                                ICD_SUBF = int(row[4]),\
                                                                ICD_SUPF = int(row[5]),\
                                                                ICD_ONE_LOGIC = row[6],\
                                                                ICD_ZERO_LOGIC = row[7])
                        list_single_para.insert(0, row[0])
                        list_all_para.append(list_single_para)



        if file[0:6] in WQAR256_SERISE_list:
            starttime = time.clock()
            single_path = path + '/' + file + '/' + 'raw.dat'
            if os.path.exists(single_path):
                file_object = open(single_path,'rb')
                filedata = file_object.read()
                file_object.close()
                #读取csv参数列表，解码大量数值参数
                with open('737-3C NUM.csv','rb') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if reader.line_num == 1:
                            continue

                        list_single_para = wqar_decode.frame(256, filedata, \
                                                         ICD_MSB=int(row[2]),\
                                                         ICD_LSB=int(row[3]), \
                                                         ICD_WORD=int(row[4]),\
                                                         ICD_SUBF=int(row[5]), \
                                                         ICD_SUPF=int(row[6]), \
                                                         ICD_RES=float(row[9]),\
                                                        ICD_SIGN=row[1])
                        list_single_para.insert(0, row[0])
                        list_all_para.append(list_single_para)

                #读取csv逻辑参数列表，解码大量逻辑参数
                with open('737-3C LOGIC.csv','rb') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if reader.line_num == 1:
                            continue

                        list_single_para = wqar_decode.frame_logic(256, filedata,
                                                                ICD_MSB = int(row[1]), \
                                                                ICD_LSB = int(row[2]), \
                                                                ICD_WORD = int(row[3]),\
                                                                ICD_SUBF = int(row[4]),\
                                                                ICD_SUPF = int(row[5]),\
                                                                ICD_ONE_LOGIC = row[6],\
                                                                ICD_ZERO_LOGIC = row[7])
                        list_single_para.insert(0, row[0])
                        list_all_para.append(list_single_para)



        #简单输出结果到csv
        list_all_para_turn = map(list, zip(*list_all_para))

        hbase_interface.create_table(file[0:21])
        table = connection.table(file[0:21])
        print table
        happybase_start_time = time.clock()
        p = Pool()
        b = table.batch()
        counter_list_all_para = len(list_all_para_turn)
        counter_list_columns = len(list_all_para_turn[0])

        for i in range(counter_list_all_para):
            #print u"第 %s 行"%i
            str_i = str(i)
            dic_j = {}
            for j in range(counter_list_columns):
                str_j = str(list_all_para_turn[0][j])
                str_value = str(list_all_para_turn[i][j])
                dic_j['c1:'+ str(j) + '_' + str_j + '_'] = str_value

            table.put(str_i, dic_j)

        #b.send()

        happybase_end_time = time.clock()
        print u"存入耗时： %s"%(happybase_end_time - happybase_start_time)

        numpy_arr = numpy.array(list_all_para_turn)
        df_s = DataFrame(numpy_arr)
        xlsx_start_time = time.clock()
        #df_s.to_excel(file + '.xlsx', sheet_name='Sheet1')
        numpy.savetxt(file + '.csv', numpy_arr, fmt="%s", delimiter=",")
        xlsx_end_time = time.clock()
        print u"%s xlsx保存时间：%f" % (file, xlsx_end_time - xlsx_start_time)
        endtime = time.clock()

    allendtime = time.clock()
    print u"全参数译码总耗时：%s" % (allendtime - allstarttime)

    return HttpResponse("已完成数据存入")
