# encoding=utf-8
# Date: 2018-8-3
# Author: MJUZY


import pymysql
import numpy as np
import csv


def writeDatasList(csv_filename, datas_list):
    csvFile2 = open(csv_filename, 'a+', newline='')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile2)

    for row in datas_list:
        writer.writerow(row)

    csvFile2.close()



def SearchedMatched(csv_name, poiid, poitype):
    datas_list = []
    datas_row = []
    line_i = 0
    with open(csv_name, "r") as csvfile:
        reader2 = csv.reader(csvfile)
        for item2 in reader2:
            line_i += 1
            # print("现在的行数是：", line_i)

            poiid_csv = str(item2[3])
            if (len(poiid_csv) == 20):
                if (poiid_csv == poiid):
                    userid, idstr, title, lon, lat, gender, text, street_address, age, score = getWeiboElements(item2)
                    datas_row = [userid, idstr, poiid, title, lon, lat, gender, text, street_address, age, score, poitype]
                    datas_list.append(datas_row)
    return datas_list


def getWeiboElements(item2):

    userid = item2[0]
    idstr = item2[1]

    # day, month, year = getDate(item2[2])

    title = item2[4]

    lon = float(item2[5])
    lat = float(item2[6])

    gender = item2[7]
    if gender == "Female": gender = 'f'
    elif gender == "Male": gender = 'm'

    text = item2[8]

    street_address = item2[9]

    age = item2[10]

    female_score = item2[11]
    male_score = item2[12]
    score = (float(female_score) + float(male_score)) / 2

    return userid, idstr, title, lon, lat, gender, text, street_address, age, score


def createDict(csv_name):

    line_i = 0
    csv_poi_dic = {}
    with open(csv_name, "r") as csvfile:
        reader2 = csv.reader(csvfile)
        for item2 in reader2:
            line_i += 1
            print("现在的行数是：", line_i)

            poiid_csv = str(item2[3])
            if (len(poiid_csv) == 20):
                # print(len(poiid_csv))
                if poiid_csv not in csv_poi_dic.keys():
                    csv_poi_dic[poiid_csv] = poiid_csv
    return csv_poi_dic


def ExportPOIType(csv_name, csv_output_name, csv_poi_dict, cur, conn):
    cur.execute("SELECT * FROM hangzhou_poi;")
    line_ii = 0
    for r in cur.fetchall():
        line_ii += 1
        print("line_ii : ", line_ii)

        r = np.array(r).tolist()
        poiid, poitype = getElement(r)

        if poiid in csv_poi_dict.keys():
            datas_list = SearchedMatched(csv_name, poiid, poitype)
            writeDatasList(csv_output_name, datas_list)


def findMatched(csv_name, cur, conn, csv_output_name):

    csv_poi_dict = createDict(csv_name)
    ExportPOIType(csv_name, csv_output_name, csv_poi_dict, cur, conn)

    conn.close()


def writeCSV(csv_filename, userid, idstr, poiid, title, lon, lat, gender, text, street_address, age, score, poitype):
    csvFile2 = open(csv_filename, 'a+', newline='')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile2)
    datas = [userid, idstr, poiid, title, lon, lat, gender, text, street_address, age, score, poitype]
    writer.writerow(datas)

    csvFile2.close()


def getElement(r):
    poiid = r[0]
    poitype = r[6]

    return poiid, poitype


def connectToDatabase():

    print("Now start connecting the database...")

    # connect to the database
    conn = pymysql.connect(db='weibo_1', user='root', passwd='270127', host='localhost', charset="utf8")
    c = conn.cursor()

    print("Finishing connecting to the database Faces ! ")

    return c, conn


if __name__ == "__main__":

    cur, conn = connectToDatabase()

    csv_name = "22_27_CompensateLonLatPoi.csv"
    csv_output_name = "22_27_POIType_Fast.csv"

    findMatched(csv_name, cur, conn, csv_output_name)
