# coding:UTF-8
# 对文件夹下的所有raw.dat译码GMT、EGT
import os
import struct
import time
import csv
import numpy

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
        if ICD_ONE_LOGIC <> ICD_ZERO_LOGIC:
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

class MERGE_DECODE_LIST():

    def __init__(self):
        pass

    def open_csv_and_merge(self, filedata, csv_file_name, plane_config, num_logic):
        wqar_decode = WQAR_DECODE()
        list_all_para = []
        #读取csv逻辑参数列表，解码大量逻辑参数
        f = open(csv_file_name,'rb')
        reader = csv.reader(f)
        #对参数ID号统一排序
        if num_logic == "logic":
            if plane_config == 256 :
                para_id_number = 645
            else:
                para_id_number = 797
        else:
            para_id_number = 1

        for row in reader:
            if reader.line_num == 1:
                continue
            #读取csv参数列表，解码数值参数
            if num_logic == 'number':
                list_single_para = wqar_decode.frame(plane_config, filedata,
                                                 ICD_MSB=int(row[2]),
                                                 ICD_LSB=int(row[3]),
                                                 ICD_WORD=int(row[4]),
                                                 ICD_SUBF=int(row[5]),
                                                 ICD_SUPF=int(row[6]),
                                                 ICD_RES=float(row[9]),
                                                ICD_SIGN=row[1])
                list_single_para.insert(0, row[7])
            #读取csv参数列表，解码逻辑值值参数
            elif num_logic == 'logic':
                list_single_para = wqar_decode.frame_logic(plane_config, filedata,
                                                        ICD_MSB = int(row[1]),
                                                        ICD_LSB = int(row[2]),
                                                        ICD_WORD = int(row[3]),
                                                        ICD_SUBF = int(row[4]),
                                                        ICD_SUPF = int(row[5]),
                                                        ICD_ONE_LOGIC = row[6],
                                                        ICD_ZERO_LOGIC = row[7])
                list_single_para.insert(0, '')
            para_name = str(para_id_number) + ':' + row[0]
            list_single_para.insert(0, para_name)
            list_all_para.append(list_single_para)
            para_id_number = para_id_number + 1
        return list_all_para


    def all_decode_list(self, dir_path, output_funciton):

        allstarttime = time.clock()
        merge_decode_list = MERGE_DECODE_LIST()

        #单位电脑路径
        path = dir_path
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
            single_path = path + '/' + file + '/' + 'raw.dat'
            if os.path.exists(single_path):
                file_object = open(single_path,'rb')
                filedata = file_object.read()
                file_object.close()
            else:
                print u"raw不存在，退出此文件夹：" + file
                continue

            if file[0:6] in WQAR512_SERISE_list:
                starttime = time.clock()
                #读取csv参数列表，解码大量数值参数
                list_number = merge_decode_list.open_csv_and_merge(filedata,
                                                                   '737-7 numeric.csv',
                                                                   512,
                                                                   'number')

                #读取csv逻辑参数列表，解码大量逻辑参数
                list_logic = merge_decode_list.open_csv_and_merge(filedata,
                                                                  '737-7 LOGIC.csv',
                                                                  512,
                                                                  'logic')
                list_number.extend(list_logic)
                list_all_para = list_number

            if file[0:6] in WQAR256_SERISE_list:
                starttime = time.clock()
                #读取csv参数列表，解码大量数值参数
                list_number = merge_decode_list.open_csv_and_merge(filedata,
                                                                   '737-3C NUM.csv',
                                                                   256,
                                                                   'number')

                #读取csv逻辑参数列表，解码大量逻辑参数
                list_logic = merge_decode_list.open_csv_and_merge(filedata,
                                                                  '737-3C LOGIC.csv',
                                                                  256,
                                                                  'logic')
                list_number.extend(list_logic)
                list_all_para = list_number


            list_all_para_turn = map(list, zip(*list_all_para))


            output_funciton(list_all_para_turn, file)

        allendtime = time.clock()
        print u"全参数译码总耗时：%s" % (allendtime - allstarttime)

    def save_to_csv(self, list_all_para_turn, file):
        numpy_arr = numpy.array(list_all_para_turn)
        xlsx_start_time = time.clock()
        #df_s = DataFrame(numpy_arr)
        #df_s.to_excel(file + '.xlsx', sheet_name='Sheet1')
        numpy.savetxt(file + '.csv', numpy_arr, fmt="%s", delimiter=",")
        xlsx_end_time = time.clock()
        print u"%s 保存时间：%f" % (file, xlsx_end_time - xlsx_start_time)

'''
if __name__=="__main__":
    decode_list = MERGE_DECODE_LIST()
    decode_list.all_decode_list(decode_list.save_to_csv)
'''