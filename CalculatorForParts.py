#encoding=utf-8

import json
import os

def get_Userid(path):
    path_Divided = path.split('\\')
    #print(path_Divided)
    get_id= path_Divided[6].split('.')
    get_id = get_id[0]
    #print(get_id)
    return get_id

def compose_Json_Path_ToRead(path_json_source,get_id):
   json_path_to_read =  path_json_source+"\\"+str(get_id)+".json"
   return json_path_to_read

def get_province_city_path_ToRead(province,city,input_year,input_month):
    path_json_source = "F:\\Fast_Prepared_Json\\"+str(province)+"\\"+str(city)+"\\"+input_year+"\\"+input_month
    return path_json_source

def read_Json_Source(json_path_to_read,pic_num_least,province,city,get_id):
    f1 = open(json_path_to_read,encoding='utf-8')
    pic_num = len(f1.readlines())
    return pic_num

def gothrough_Source(path_json_source, province, city, pic_num_least):
    total = 0
    """
    为了能够看到下载进度，在此先计算账户总数
    """

    for dirpath, dirnames, filenames in os.walk(path_json_source):
        for filepath in filenames:
            path = os.path.join(dirpath, filepath)
            # 现在开始得到文件名上的userid
            get_id = get_Userid(path)

            # 现在开始读取json数据源
            json_path_to_read = compose_Json_Path_ToRead(path_json_source, get_id)
            pic_num = read_Json_Source(json_path_to_read, pic_num_least, province, city, get_id)
            print(pic_num)
            total = total+pic_num
            print("TOTAL:",total)

"""
print("请输入想要下载的省份或直辖市：")
input_province = input()
print("请输入想要下载的城市：")
input_city = input()
print("请输入想要下载的年份：（2014）")
input_year = input()
print("请输入想要下载的月份：（07）")
input_month = input()
print("请输入想要过滤的图片数目下限：")
pic_num_least = input()
"""
input_province = "广东省"
input_city = "广州市"
input_year = "2014"
input_month = "08"
pic_num_least = 1

path_json_source = get_province_city_path_ToRead(input_province,input_city,input_year,input_month)

gothrough_Source(path_json_source,input_province,input_city,pic_num_least)

print("Ok!")
mark = input()