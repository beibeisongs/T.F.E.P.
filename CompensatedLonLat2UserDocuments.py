# encoding=utf-8
# Date: 2018-8-1
# Author: MJUZY


import json
import csv
import os


def GetPicNum(rline):
    try:
        getid_pic_ids = rline["pic_ids"]
        nid = len(getid_pic_ids)
    except:
        nid = -1
    return nid


def Export2CSV(lon, lat, get_user_id, outputCSV_dirpath):
    CSVPath = outputCSV_dirpath + "\\" + get_user_id + "\\" + get_user_id + ".csv"
    csvFile2 = open(CSVPath, 'a+', newline='')  # 设置newline，否则两行之间会空一行

    writer = csv.writer(csvFile2)
    datas = [lon, lat]
    writer.writerow(datas)

    csvFile2.close()


def GetLonLat(rline):
    geo = rline["geo"]
    coordinates = geo["coordinates"]

    lon = coordinates[1]
    lat = coordinates[0]
    return lon, lat


def judgeExist(get_user_id, outputCSV_dirpath):
    if os.path.exists(outputCSV_dirpath + "\\" + get_user_id):
        return True
    else:
        return False


def getUserID(rline):
    get_user_id = rline["user"]["id"]
    return get_user_id


def goThroughJson(json_source_path, outputCSV_dirpath, start_pt, end_pt, process_i):
    f1 = open(json_source_path, encoding='utf-8')
    for line in f1.readlines():
        rline = json.loads(line)
        get_user_id = str(getUserID(rline))  # <Sample>: '3965394195'

        user_exist = judgeExist(get_user_id, outputCSV_dirpath)
        if user_exist:
            pic_num = GetPicNum(rline)
            if (pic_num == 0) or (pic_num ==1):
                process_i += 1
                if (process_i >= start_pt):
                    lon, lat = GetLonLat(rline)
                    Export2CSV(lon, lat, get_user_id, outputCSV_dirpath)
                    print("process_i : ", process_i, get_user_id, "OK !")
    return process_i


def composeJsonPath(dirpath, filepath):
    path = dirpath + "\\" + filepath
    return path


def GetCity(filepath):

    city = str(filepath).split(".")
    city = city[0]

    return city


def GetProvince(dirpath):

    try:
        province = str(dirpath).split("\\")
        province = province[4]
    except:
        province = -1

    return province


def GetDate(dirpath):

    try:
        date = str(dirpath).split("\\")
        date = date[3]
        date = date.split('-')

        year = date[0]
        month = date[1]
        day = date[2]
    except:
        year = -1
        month = -1
        day = -1

    return year, month, day


def walkPath(disk_walkedpath, province, city, year, month, outputCSV_dirpath, start_pt, end_pt):

    process_i = 0

    for dirpath,dirnames,filenames in os.walk(disk_walkedpath):
        for filepath in filenames:

            # pass    # <Sample>: dirpath = 'E:\\sina\\data\\2014-07-01\\上海市' filepath = '上海市.json'
            get_year, get_month, get_day = GetDate(dirpath)
            print(get_day)
            get_province = GetProvince(dirpath)
            get_city = GetCity(filepath)
            if (get_year == year) and (get_month == month):
                if (get_province == province) and (get_city == city):
                        # print("Ok ! ")
                        json_source_path = composeJsonPath(dirpath, filepath)
                        process_i = goThroughJson(json_source_path, outputCSV_dirpath, start_pt, end_pt, process_i)


if __name__ == "__main__":

    disk_walkedpath = "E:\\sina\\data"

    outputCSV_dirpath = "D:\\实验室项目资料\\T.F.E.P.源码\\ForCompensated"

    province = "浙江省"
    city = "杭州市"

    year = "2014"
    month = "07"

    start_pt = 0
    end_pt = 0

    walkPath(disk_walkedpath, province, city, year, month, outputCSV_dirpath, start_pt, end_pt)
