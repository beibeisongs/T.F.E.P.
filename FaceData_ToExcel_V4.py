# encoding = utf-8
# Date: 2018-05-05
# Function: Export Faces Data to Excels


import os

import json
import xlrd
import xlwt
from  xlutils.copy import copy


def Export(excel_i, excel_path, book, sheet, line_i, created_at, lng, lat, street_address, gender, female_score, male_score, get_user_id):

    sheet.write(line_i % 1000, 0, lng)
    sheet.write(line_i % 1000, 1, lat)
    sheet.write(line_i % 1000, 2, created_at)
    sheet.write(line_i % 1000, 3, gender)
    sheet.write(line_i % 1000, 4, street_address)
    sheet.write(line_i % 1000, 5, female_score)
    sheet.write(line_i % 1000, 6, male_score)
    sheet.write(line_i % 1000, 7, get_user_id)

    print("line_i : ", line_i)

    if (line_i != 0) and ((line_i + 1) % 1000 == 0):

        excel_i += 1
        excel_path = "InfoB" + str(excel_i) + ".xls"

        book.save(excel_path)

        book = xlwt.Workbook()  # 创建一个Excel表对象
        sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)


    line_i += 1

    return book, sheet, line_i, excel_i


def getAccountInfo(dirpath, get_user_id):

    account_json_path = dirpath + "\\" + get_user_id + ".json"
    f1 = open(account_json_path, encoding='utf-8')
    line = f1.readline()
    rline = json.loads(line)

    created_at = rline["created_at"]
    geo = rline["geo"]
    coordinates = geo["coordinates"]
    lng = coordinates[1]
    lat = coordinates[0]

    try:
        get_address_Stp1 = rline["url_objects"]
        get_address_Stp2 = get_address_Stp1[0]
        get_address_Stp3 = get_address_Stp2["object"]["object"]
        get_address_Stp4 = get_address_Stp3["address"]
        street_address = get_address_Stp4["street_address"]
    except:
        street_address = "None"

    # print("created_at : ", created_at)

    return created_at, lng, lat, street_address


def getScore(score_path):

    error = "OK"

    try:

        f1 = open(score_path, encoding='utf-8')
        for line in f1.readlines():
            rline = json.loads(line)
            faces = rline["faces"]
            faces_0 = faces[0]
            attributes = faces_0["attributes"]

            gender = attributes["gender"]
            gender = gender["value"]
            print("The gender is : " + gender)

            beauty = attributes["beauty"]
            female_score = beauty["female_score"]
            male_score = beauty["male_score"]

            return error, gender, female_score, male_score
    except:
        error = "ERROR"
        gender = 0
        female_score = 0
        male_score = 0

        return error, gender, female_score, male_score


def ExportFaceInfo(excel_i, excel_path, book, sheet, line_i, belonger, dirpath, get_user_id):

    created_at, lng, lat, street_address = getAccountInfo(dirpath, get_user_id)

    score_path = dirpath + "\\" + get_user_id + "\\" + "Face_Scores.json"

    error, gender, female_score, male_score = getScore(score_path)

    if error == "OK":
        book, sheet, line_i, excel_i = Export(excel_i, excel_path, book, sheet, line_i, created_at, lng, lat, street_address, gender, female_score, male_score, get_user_id)

    return book, sheet, line_i, excel_i

def get_Belonger(_results_jsonpath):
    error = "OK"
    try:
        f1 = open(_results_jsonpath, encoding='utf-8')
        for line in f1.readlines():
            rline = json.loads(line)
            belonger = rline["Belonger"]

        return error, belonger
    except:
        error = "ERROR"
        belonger = []

        return error, belonger


def goThoughFiles(accounts_documents_path):

    AccountFileNumber = 0  # To show the number the Account being read

    line_i = 0  # To record the number of the Excel Line

    excel_i = 0  # The excel number saved
    excel_path = "InfoB" + str(excel_i) + ".xls"

    book = xlwt.Workbook()  # 创建一个Excel表对象
    sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)

    for dirpath, dirnames, filenames in os.walk(accounts_documents_path):
        for filepath in filenames:

            get_user_id = dirpath.replace(accounts_documents_path + "\\", "")  # <Sample>: get_user_id = '18811860'

            if filepath == get_user_id + ".json":  # <sample>: 18811860.json

                AccountFileNumber += 1
                print("这是第 %i 个账号" % (AccountFileNumber), "这个账号是：" + get_user_id)

                if (AccountFileNumber >= start_pt) and (AccountFileNumber <= end_pt):

                    if os.path.exists(dirpath + "\\" + get_user_id + "\\" + "Results.json") == True:

                        # print("Results.json ok ! ")

                        _results_jsonpath = dirpath + "\\" + get_user_id + "\\" + "Results.json"

                        error, belonger = get_Belonger(_results_jsonpath)
                        if error == "OK":
                            book, sheet, line_i, excel_i = ExportFaceInfo(excel_i, excel_path, book, sheet, line_i, belonger, dirpath, get_user_id)
                        else:
                            break
                    else:
                        excel_path = "InfoB" + str(excel_i + 1) + ".xls"
                        book.save(excel_path)

    excel_path = "InfoB" + str(excel_i + 1) + ".xls"
    book.save(excel_path)



if __name__ == "__main__":

    city = "武汉市"
    province = "湖北省"

    # start_pt = 4
    # end_pt = 6
    start_pt = 30760
    end_pt = 140000

    accounts_documents_path = "D:\\用户的文件\\" + province + "\\" + city

    goThoughFiles(accounts_documents_path)