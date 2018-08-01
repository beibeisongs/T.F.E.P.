# encoding=utf-8
# Date: 2018-7-30
# Author: MJUZY


import os
import math
import csv
import json
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt


def writeCSV(item2, csv_output_name):

    csvFile2 = open(csv_output_name, 'a+', newline='')  # 设置newline，否则两行之间会空一行

    writer = csv.writer(csvFile2)
    datas = item2
    writer.writerow(datas)

    csvFile2.close()


def ExportCompensatedLonLat(userid, findCompensated_dirpath, csv_output_name, female_score, male_score):

    findCompensated_CSVPath = findCompensated_dirpath + "\\" + str(userid) + "\\" + str(userid) + ".csv"
    if os.path.exists(findCompensated_CSVPath):

        line_i = 0
        with open(findCompensated_CSVPath, "r") as csvfile:
            reader2 = csv.reader(csvfile)  # 读取csv文件，返回的是迭代类型
            for item2 in reader2:
                datas = []
                line_i += 1
                print("现在的行数是：", line_i)

                datas.append(userid)
                datas.append(0)
                datas.append(0)
                datas.append(0)
                datas.append(0)
                datas.append(item2[0])
                datas.append(item2[1])
                datas.append(0)
                datas.append(0)
                datas.append(0)
                datas.append(0)
                datas.append(female_score)
                datas.append(male_score)
                writeCSV(datas, csv_output_name)

        csvfile.close()


def getElements(item2):

    userid = item2[0]

    female_score = item2[11]
    male_score = item2[12]

    return female_score, male_score, userid


def goThroughCSV(csv_name, csv_output_name, findCompensated_dirpath):

    userid_temp = ""

    users_num_passed = 0

    line_i = 0
    with open(csv_name, "r") as csvfile:
        reader2 = csv.reader(csvfile)  # 读取csv文件，返回的是迭代类型
        for item2 in reader2:
            line_i += 1
            print("现在的行数是：", line_i)

            if (line_i >= start_pt):

                female_score, male_score, userid = getElements(item2)
                if line_i == 1:
                    userid_temp = userid

                    users_num_passed += 1

                    ExportCompensatedLonLat(userid, findCompensated_dirpath, csv_output_name, female_score, male_score)
                    writeCSV(item2, csv_output_name)

                elif userid == userid_temp:

                    writeCSV(item2, csv_output_name)

                elif userid_temp != userid:
                    ExportCompensatedLonLat(userid, findCompensated_dirpath, csv_output_name, female_score, male_score)
                    writeCSV(item2, csv_output_name)

                    userid_temp = userid

                    users_num_passed += 1

            else:
                break
    """
    print(distances_record)
    print(len(distances_record))
    print(scores_record)
    print(len(scores_record))
    """

    csvfile.close()


if __name__ == "__main__":

    # b = [12, 22, 27, 33, 40, 50, 63, 88]
    b = [16, 22, 27, 33, 40, 50, 63, 88]

    start_pt = 0
    end_pt = 0

    csv_name = "22_27.csv"
    csv_output_name = "22_27_CompensateLonLat.csv"

    findCompensated_dirpath = "D:\\实验室项目资料\\T.F.E.P.源码\\ForCompensated"

    goThroughCSV(csv_name, csv_output_name, findCompensated_dirpath)
