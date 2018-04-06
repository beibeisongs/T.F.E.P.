#!/usr/bin/env python
# encoding = utf-8
# Author: MUJZY
# Date: 2018-04-06
# Description: Export the JSON DATA to the database of mysql


import os
import json
import pymysql


def getInfo(rline):

    get_geo_Stp1 = rline["geo"]["coordinates"]
    latitude = get_geo_Stp1[0]
    lngtitude = get_geo_Stp1[1]

    time = rline["created_at"]

    get_address_Stp1 = rline["url_objects"]
    get_address_Stp2 = get_address_Stp1[0]
    get_address_Stp3 = get_address_Stp2["object"]["object"]
    get_address_Stp4 = get_address_Stp3["address"]
    street_address = get_address_Stp4["street_address"]

    return latitude, lngtitude, time, street_address


def insertUserInfo(c, conn, name, latitude, lngtitude, time, street_address):

    order = "INSERT INTO faces_scores VALUES (" + "'" + name + "'" + ',' + \
            "NULL" + "," + \
            "NULL" + "," + \
            "NULL" + "," + \
            "NULL" + "," + \
            str(latitude) + "," + \
            str(lngtitude) + "," + \
            "'" + time + "'" + "," + \
            "'" + street_address + "'" + \
            ");"

    c.execute(order)
    conn.commit()

    print("Finish export one Info ! ")


def inserFaceSoresIntoTable(c, conn, name, gender, age, female_score, male_score):

    order = "INSERT INTO faces_scores VALUES (" + "'" + name + "'" + ',' + \
                                                "'" + gender + "'"+ "," + \
                                                str(age) + "," + \
                                                str(female_score) + "," + \
                                                str(male_score) + "," + \
                                                "NULL" + "," + \
                                                "NULL" + "," + \
                                                "NULL" + "," + \
                                                "NULL" + \
                                            ");"
    c.execute(order)
    conn.commit()

    print("Finish export one Face_datas ! ")


def get_FaceScores(rline):

    get_faceScores_Stp1 = rline["faces"]
    get_faceScores_Stp2 = get_faceScores_Stp1[0]    # <Attention>: 下标0是一个字典
    get_faceScores_Stp3 = get_faceScores_Stp2["attributes"] # <Attention>: 这里又嵌套了一个字典

    get_gender_Stp1 = get_faceScores_Stp3["gender"]
    gender = get_gender_Stp1["value"]

    get_age_Stp1 = get_faceScores_Stp3["age"]
    age = get_age_Stp1["value"]

    get_beauty_Stp1 = get_faceScores_Stp3["beauty"]
    female_score = get_beauty_Stp1["female_score"]
    male_score = get_beauty_Stp1["male_score"]

    return gender, age, female_score, male_score


def exportUserInfo(c, conn, json_originalSource_wholepath, get_user_id):

    name = str(get_user_id)

    f1 = open(json_originalSource_wholepath)

    line_temp = f1.readline()
    rline_temp = json.loads(line_temp)
    latitude_tp, lngtitude_tp, time_tp, street_address_tp = getInfo(rline_temp)
    insertUserInfo(c, conn, name, latitude_tp, lngtitude_tp, time_tp, street_address_tp)

    for line in f1.readlines():

        rline = json.loads(line)

        latitude, lngtitude, time, street_address = getInfo(rline)

        if street_address != street_address_tp:

            insertUserInfo(c, conn, name, latitude, lngtitude, time, street_address)

            street_address_tp = street_address

def exportFaceScoresDatas(c, conn, json_FaceScores_wholepath, get_user_id):

    name = str(get_user_id)

    f1 = open(json_FaceScores_wholepath, encoding='utf-8')

    line = f1.readline()
    rline = json.loads(line)
    gender, age, female_score, male_score = get_FaceScores(rline)

    print("Show First Part Datas : " + str(gender) + " " + str(age) + " " + str(female_score) + " " + str(male_score))

    inserFaceSoresIntoTable(c, conn, name, gender, age, female_score, male_score)


def connectToDatabase():

    print("Now start connecting the database...")

    # connect to the database
    conn = pymysql.connect(db='Faces', user='root', passwd='270127', host='localhost', charset="utf8")
    c = conn.cursor()

    print("Finishing connecting to the database Faces ! ")

    return c, conn


if __name__ == '__main__':

    print("请输入想要处理的省份")
    # province = input()
    province = "湖北省"

    print("请输入想要处理的地级市")
    # city = input()
    city = "武汉市"

    start_pt = 0

    path = "C:\\用户的文件\\" + province + "\\" + city

    c, conn = connectToDatabase()

    AccountFileNumber = 0  # To show the number the Account being read

    for dirpath, dirnames, filenames in os.walk(path):

        for filepath in filenames:  # <Sample>: filepath = '1982819117.json'

            get_user_id = dirpath.replace(path + "\\", "")  # <Sample>: get_user_id = '18811860'

            if filepath == get_user_id + ".json":  # <sample>: 18811860.json
                                                     # <sample>: dirpath = C:\用户的文件\湖北省\武汉市\1000270434
                AccountFileNumber += 1
                print("这是第 %i 个账号" % (AccountFileNumber))
                print("这个账号是：" + get_user_id)

                if AccountFileNumber >= start_pt:

                    if os.path.exists(dirpath + "\\" + "Ext_Step_Ok") == True:

                        if os.path.exists(dirpath + "\\" + get_user_id + "\\" + "Results.json") == True:

                            print("Results.json Existing !")
                            print("-----------------------")

                            json_originalSource_wholepath = dirpath + "\\" + get_user_id + ".json"
                            json_FaceScores_wholepath = dirpath + "\\" + get_user_id + "\\" + "Face_Scores.json"

                            try:
                                exportFaceScoresDatas(c, conn, json_FaceScores_wholepath, get_user_id)

                                exportUserInfo(c, conn, json_originalSource_wholepath, get_user_id)
                            except:
                                print("Next !")