# encoding = utf-8
# Date: 2018-05-05
# Function: Export Faces Data to Excels


import os

import json
import xlrd
import xlwt
from  xlutils.copy import copy

def write_excel_exist(r_id, excel_path, created_at, lng, lat, street_address, gender, female_score, male_score, get_user_id):

    old_excel = xlrd.open_workbook(excel_path, formatting_info=True)

    # 将操作文件对象拷贝，变成可写的excel对象
    new_excel = copy(old_excel)

    # 获得第一个sheer的对象
    ws = new_excel.get_sheet(0)

    ws.write(r_id, 0, lng)
    ws.write(r_id, 1, lat)
    ws.write(r_id, 2, created_at)
    ws.write(r_id, 3, gender)
    ws.write(r_id, 4, street_address)
    ws.write(r_id, 5, female_score)
    ws.write(r_id, 6, male_score)
    ws.write(r_id, 7, get_user_id)

    new_excel.save(excel_path)


def create_document(export_file_path):

    if os.path.exists(export_file_path) == False:
        os.mkdir(export_file_path)


def Export(r_id, created_at, lng, lat, street_address, gender, female_score, male_score, get_user_id):

    export_file_path = "C:\\ExportFacesInfo"
    create_document(export_file_path)
    create_document(export_file_path + "\\" + get_user_id)

    excel_path = export_file_path + "\\" + get_user_id + "\\" + get_user_id + ".xls"
    if os.path.exists(excel_path) == False:
        book = xlwt.Workbook()  # 创建一个Excel表对象
        sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)

        sheet.write(0, 0, lng)
        sheet.write(0, 1, lat)
        sheet.write(0, 2, created_at)
        sheet.write(0, 3, gender)
        sheet.write(0, 4, street_address)
        sheet.write(0, 5, female_score)
        sheet.write(0, 6, male_score)
        sheet.write(0, 7, get_user_id)

        book.save(excel_path)

    else:
        write_excel_exist(r_id, excel_path, created_at, lng, lat, street_address, gender, female_score, male_score, get_user_id)


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

    get_address_Stp1 = rline["url_objects"]
    get_address_Stp2 = get_address_Stp1[0]
    get_address_Stp3 = get_address_Stp2["object"]["object"]
    get_address_Stp4 = get_address_Stp3["address"]
    street_address = get_address_Stp4["street_address"]

    return created_at, lng, lat, street_address


def getScore(score_path):

    error = "OK"

    try:
        print("The score_path is : " + score_path)
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


def ExportFaceInfo(belonger, dirpath, get_user_id):

    created_at, lng, lat, street_address = getAccountInfo(dirpath, get_user_id)

    for i in range(len(belonger)):

        belonger_i = belonger[i]

        score_path = dirpath + "\\" + str(belonger_i) + "\\" + "Face_Score.json"

        error, gender, female_score, male_score = getScore(score_path)

        if error == "OK":

            Export(i, created_at, lng, lat, street_address, gender, female_score, male_score, get_user_id)


def get_Belonger_list(_results_jsonpath):
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

    for dirpath, dirnames, filenames in os.walk(accounts_documents_path):
        for filepath in filenames:

            get_user_id = dirpath.replace(accounts_documents_path + "\\", "")  # <Sample>: get_user_id = '18811860'

            if filepath == get_user_id + ".json":  # <sample>: 18811860.json

                AccountFileNumber += 1
                print("这是第 %i 个账号" % (AccountFileNumber))
                print("这个账号是：" + get_user_id)

                # To Find the ID Information more Easily !
                print()

                if AccountFileNumber >= start_pt:

                    if os.path.exists(dirpath + "\\" + get_user_id + "_results.json") == True:

                        print("_results.json ok ! ")

                        _results_jsonpath = dirpath + "\\" + get_user_id + "_results.json"

                        error, belonger = get_Belonger_list(_results_jsonpath)
                        if error == "OK":
                            ExportFaceInfo(belonger, dirpath, get_user_id)
                        else:
                            break
                    else:
                        exit(code=0)


if __name__ == "__main__":

    city = "武汉市"
    province = "湖北省"

    start_pt = 0

    accounts_documents_path = "C:\\用户的文件\\" + province + "\\" + city

    goThoughFiles(accounts_documents_path)