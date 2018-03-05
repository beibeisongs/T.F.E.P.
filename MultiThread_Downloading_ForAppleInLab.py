# encoding=utf-8
# Date: 2018-3-5
# Author: MUJZY


import re
import json

import urllib
import urllib.request
import urllib3
import requests

import os
import time
import socket
import threading

def create_Disk_File(province,city):
    path2 = "F:\\用户的文件\\"+str(province)+"\\"+str(city)
    judgeExisting = os.path.exists(path2)
    if not judgeExisting:
        print(str(path2) + '创建成功！')
        os.makedirs(path2)
    return

def get_province_city_path_ToRead(province,city,input_year,input_month):
    path_json_source = "F:\\Fast_Prepared_Json\\"+str(province)+"\\"+str(city)+"\\"+input_year+"\\"+input_month
    return path_json_source

def compose_Path_ToWrite_json(province,city,get_id):
    path_to_write = "F:\\用户的文件\\"+str(province)+"\\"+str(city)+"\\"+str(get_id)
    judgeExisting = os.path.exists(path_to_write)
    if not judgeExisting:
        # print(str(path_to_write) + '创建成功！')
        os.makedirs(path_to_write)
    path_to_write_json = path_to_write+"\\"+str(get_id)+".json"
    return path_to_write_json

def get_Userid(path):
    path_Divided = path.split('\\')
    # print(path_Divided)
    get_id= path_Divided[6].split('.')
    get_id = get_id[0]
    # print(get_id)
    return get_id

def compose_Json_Path_ToRead(path_json_source,get_id):
   json_path_to_read =  path_json_source+"\\"+str(get_id)+".json"
   return json_path_to_read

def read_Json_Source(json_path_to_read,pic_num_least,province,city,get_id,shushu):
    f1 = open(json_path_to_read,encoding='utf-8')
    pic_num = len(f1.readlines())
    if pic_num>int(pic_num_least)+1:
        # 现在构造得到要写入的json文件的位置
        path_to_write_json = compose_Path_ToWrite_json(province, city, get_id)
        f2 = open(json_path_to_read,encoding='utf-8')
        for line in f2.readlines():
            rline = json.loads(line)
            # 现在得到构造好的网址
            get_composed_url = rline["se_get_large_url"]
            # 现在开始写入json文件
            write_Json_data(path_to_write_json, rline)
            # 现在开始准备下载图片
            # 先得到pic_id的序列
            get_the_JPG_id = get_The_JPG_Id(get_composed_url)
            # 再构造jpg要下载到的位置
            the_path_to_download_jpg = compose_JPG_Dowmload_Path(province, city, get_the_JPG_id, get_id)
            # 再下载图片
            shushu = Download_Pics(the_path_to_download_jpg,get_composed_url,shushu)
    return shushu

def open_Json_File_To_Write(path_to_write):
    judgeExisting = True
    judgeExisting = os.path.exists(path_to_write)
    if not judgeExisting:
        f1 = open(path_to_write,mode='w')
    else:
        f1 = open(path_to_write,mode='a')
    return f1

def write_Json_data(path_to_write_json,rline):
    f1 = open_Json_File_To_Write(path_to_write_json)
    a = json.dumps(rline)
    b = str(a)+"\n"
    f1.write(b)
    return

def get_The_JPG_Id(get_composed_url):
    composed_url_Divided = str(get_composed_url).split('/')
    composed_url_Divided = composed_url_Divided[4].split(".")
    get_the_JPG_id = composed_url_Divided[0]
    return get_the_JPG_id

def compose_JPG_Dowmload_Path(province,city,get_the_JPG_id,get_id):
    path = "F:\\用户的文件\\"+str(province)+"\\"+str(city)+"\\"+str(get_id)+"\\"+str(get_the_JPG_id)+".jpg"
    return path

def Download_Pics(the_path_to_download_jpg,get_composed_url,shushu):
    class SubThread():
        shushu = 0  # 初始化为0
        def sub_Thread_Download(the_path_to_download_jpg,get_composed_url,shushu,sub_thread1):
            try:
                shushu = shushu+1
                print("现在下载的图片数目是:")
                print(shushu)

                """
                <The temporary function>: To avoid downloading the repeated JPG
                path2 = the_path_to_download_jpg    # download to this path
                judgeExisting = os.path.exists(path2)
                if judgeExisting:
                    print("Exist!!!")
                else:
                """

                """
                <Another orders for the same funtion>
                socket.setdefaulttimeout(10)
                urllib.request.urlretrieve(get_composed_url,the_path_to_download_jpg)
                """
                resp = requests.get(get_composed_url, timeout=6)
                f = open(the_path_to_download_jpg, 'wb')
                f.write(resp.content)
                f.close()

                if shushu%30==0:
                    print("休息一下")
                    time.sleep(3)
            except:

                mark_state = True

                n_error_times = 0   # 记录报错次数

                while mark_state:

                    n_error_times += 1

                    print("下载超时或出错了。。")
                    # time.sleep(1)
                    print("现在重新连接。。")
                    try:
                        resp = requests.get(get_composed_url, timeout=6)
                        f = open(the_path_to_download_jpg, 'wb')
                        f.write(resp.content)
                        f.close()
                    except :
                        mark_state = True

                    if n_error_times % 30 == 0:

                        time.sleep(1)
                        n_error_times = 0
                        print()

                    judgeExisting = os.path.exists(the_path_to_download_jpg)
                    if judgeExisting:
                        mark_state = False

                if shushu % 30 == 0 :
                    print("休息一下")
                    time.sleep(3)

            sub_thread1.shushu = shushu

    class GetShushu():
        shushu = 0  # 初始化为0

    sub_thread1 = SubThread()
    sub_thread1.shushu = shushu

    t = threading.Thread(target=SubThread.sub_Thread_Download,name=None,args=(the_path_to_download_jpg,get_composed_url,sub_thread1.shushu,sub_thread1))
    t.start()
    t.join()

    get_shushu1 = GetShushu()
    get_shushu1.shushu = sub_thread1.shushu

    return get_shushu1.shushu

def gothrough_Source(path_json_source,province,city,pic_num_least):
    shushu = 0
    """
    为了能够看到下载进度，在此先计算账户总数
    """

    for dirpath, dirnames, filenames in os.walk(path_json_source):
        for filepath in filenames:
            path = os.path.join(dirpath, filepath)
            # 现在开始得到文件名上的userid
            get_id = get_Userid(path)

            # 现在开始读取json数据源
            json_path_to_read = compose_Json_Path_ToRead(path_json_source,get_id)
            shushu = read_Json_Source(json_path_to_read,pic_num_least,province,city,get_id,shushu)

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
input_province = "湖北省"
input_city = "武汉市"
input_year = "2014"
input_month = "10"
pic_num_least = 1

# 现在开始遍历文件夹并进行用户json文件的读取、过滤、再写入以及下载图片
create_Disk_File(input_province,input_city)

path_json_source = get_province_city_path_ToRead(input_province,input_city,input_year,input_month)

gothrough_Source(path_json_source,input_province,input_city,pic_num_least)

print("Ok!")
mark = input()

