# encoding=utf-8

import json
import os
import re
import time

def create_Disk_File():
    path2 = "F:\\Fast_Prepared_Json"
    judgeExisting = os.path.exists(path2)
    if not judgeExisting:
        print(str(path2) + '创建成功！')
        os.makedirs(path2)
    return

def judge_If_Goon(province,city,path,input_year,input_month):
    if_goon = False
    try:
        path_Divided = path.split("\\")
        get_date = path_Divided[3]  # 由此得到遍历到的日期

        get_filename_the_last_part = str(path_Divided[5])
        get_filename_the_last_part = get_filename_the_last_part.split(".")
        get_filename_the_last_part_1 = get_filename_the_last_part[0]    #由此得到文件路径所在是哪个市，从而避免重复

        get_filename_province = str(path_Divided[4])    #由此得到文件路径所在是哪个省，从而避免重复

        if province == get_filename_province:
            if city == get_filename_the_last_part_1:
                if_goon = True
    except:
        pass

    return if_goon,get_date

def judge_If_Goon_Date(province,city,path,input_year,input_month):
    if_goon_date = False
    try:
        path_Divided = path.split("\\")
        get_date = path_Divided[3]  # 由此得到遍历到的日期
        get_date_Divided = get_date.split('-')
        get_date_year = get_date_Divided[0]
        get_date_month = get_date_Divided[1]

        if get_date_year == input_year:
            if get_date_month == input_month: if_goon_date = True
    except:
        pass

    return if_goon_date

def get_The_Filepath_Date(province,city,input_year,input_month):
    create_province_city_path_toPlace_Json(province,city,input_year,input_month)
    path2 = "F:\\sina\\data"
    for dirpath,dirnames,filenames in os.walk(path2):
        path = dirpath
        if_goon_date = judge_If_Goon_Date(province, city, path, input_year, input_month)

        if if_goon_date:

            if_file_ex = False
            city_jsonname = city+".json"
            for i in range(0,len(filenames)):
                if city_jsonname == filenames[i] :
                    if_file_ex = True
                    i_ex = i
            if if_file_ex:
                filepath = filenames[i_ex]
                path = os.path.join(dirpath,filepath)

                if_goon,get_date = judge_If_Goon(province,city,path,input_year,input_month)

                if if_goon:
                    #由此得到那个json数据源的路径
                    path_json_source = get_province_city_path_ToRead(province,city,get_date)
                    read_The_Json(path_json_source,province,city,get_date,input_year,input_month)

        else:
            continue

def get_province_city_path_ToRead(province,city,get_date):
    path_json_source = "F:\\sina\\data\\"+str(get_date)+"\\"+str(province)+"\\"+str(city)+".json"
    return path_json_source

def create_province_city_path_toPlace_Json(province,city,input_year,input_month):
    path2 = "F:\\Fast_Prepared_Json\\"+str(province)+"\\"+str(city)+"\\"+input_year+"\\"+input_month
    judgeExisting = os.path.exists(path2)
    if not judgeExisting:
        print(str(path2) + '创建成功！')
        os.makedirs(path2)
    return

def read_The_Json(path_json_source,province,city,get_date,input_year,input_month):
    f1 = open(path_json_source,encoding='utf-8')
    for line in f1.readlines():
        rline = json.loads(line)
        try:
            get_id = rline["user"]["id"]

            #接下来就要得到具体的将json文件写在哪里了
            path_to_write = compose_jsonPath_to_Write(province,city,get_id,input_year,input_month)

            #先构造要写入的Json的Content,同时在这个Function里写入Content
            compose_Content_To_Write(rline,get_id,path_to_write,get_date)
        except:
            continue

def compose_Content_To_Write(rline,get_id,path_to_write,get_date):
    # 得到图片它自身的id序列
    getid_pic_ids = rline["pic_ids"]
    nid = len(getid_pic_ids)
    if nid > 1:
        f1 = open_Json_File_To_Write(path_to_write)
        # nid是图片的数量！！！
        print("得到用户图片的数量：")
        print(nid)

        # 初步构造下载图片的网址
        getori_part1 = compose_pic_Url_part1(rline)

        # 下面依次构造图片的url
        for i in range(0, nid):  # 注意range()函数的第二个参数，要为所需数值+1
            # getid1[i]为当前图片自身的id
            getori1 = getori_part1 + 'e/' + getid_pic_ids[i] + ".jpg"
            geturllarge = getori1
            #print("下面是构造好的url：")
            #print(geturllarge)
            rline["se_get_large_url"] = str(geturllarge)
            #然后写入data的内容
            write_Json_Content(rline,f1,get_date)

def open_Json_File_To_Write(path_to_write):
    judgeExisting = True
    judgeExisting = os.path.exists(path_to_write)
    if not judgeExisting:
        f1 = open(path_to_write,mode='w')
    else:
        f1 = open(path_to_write,mode='a')
    return f1

def compose_pic_Url_part1(rline):
    getori = rline["original_pic"]
    getori1 = str(getori).split('ww')
    getori2 = str(getori1[1]).split('.s')
    getorihoubufen = 'http://ww3.s' + str(getori2[1])
    getori = str(getorihoubufen).split('e/')
    getori1 = getori[0] + 'e/'  # 目前得到的是...jpg前网址的那部分，下面的一步会继续构造

    getori_part1 = getori[0]
    return getori_part1

def write_Json_Content(data,f1,get_date):
    print(get_date)
    a = json.dumps(data)
    b = str(a)+'\n'
    f1.write(b)
    #print("写入成功！")
    #print(b)
    return

def compose_jsonPath_to_Write(province,city,get_id,input_year,input_month):
    path_to_write = "F:\\Fast_Prepared_Json\\"+str(province)+"\\"+str(city)+"\\"+str(input_year)+"\\"+str(input_month)+"\\"+str(get_id)+".json"
    return path_to_write

"""
create_Disk_File()
print("请输入选择的省份：(湖北省)")
input_province = input()
print("请输入选择的城市：（武汉市）")
input_city = input()
print("请输入选择的年份：（2015）")
input_year = input()
print("请输入选择的月份：（01）")
input_month = input()
"""
input_province = "广东省"
input_city = "广州市"
input_year = "2014"
input_month = "08"

#创建路径去放置该城市的用户的文件夹
#create_province_city_path_toPlace_Json(input_province,input_city)

#循环构造要读的json文件
get_The_Filepath_Date(input_province,input_city,input_year,input_month)

print("ok!")

mark = input()




