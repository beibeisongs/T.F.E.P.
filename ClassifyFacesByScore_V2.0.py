#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Function:Classify the Faces by score in region width for 5 points
# Description:Used for files part One
# Date:2018-04-28

from PIL import Image

import json
import sys

import os


def copy_Operation(jpg_path, destination):

    im = Image.open(jpg_path)
    im.save(destination)

    print("Copy Ok ! ")


def get_ScoreRegion(female_score):
    score_level = int(int(female_score) / 5) * 5
    print("score_level : " + "up_" + str(score_level))
    score_level_filename = "up_" + str(score_level)

    return score_level_filename


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


def copyJPGs(belonger, dirpath):

        score_path = dirpath + "\\" + "Face_Scores.json"

        error, gender, female_score, male_score = getScore(score_path)

        if error == "OK":

            score_level_filename = get_ScoreRegion(female_score)

            if gender == "Female":

                jpg_path = dirpath + "\\" + str(belonger)
                print("jpg_path : " + jpg_path)
                destination = "D:\\用户的文件\\ScoreRegions_female\\" + score_level_filename + "\\" + str(belonger)
                print("destination : " + destination)

                copy_Operation(jpg_path, destination)

            elif gender == "Male":

                jpg_path = dirpath + "\\" + str(belonger)
                print("jpg_path : " + jpg_path)
                destination = "D:\\用户的文件\\ScoreRegions_male\\" + score_level_filename + "\\" + str(belonger)
                print("destination : " + destination)

                copy_Operation(jpg_path, destination)
        else:
            print("Mo Scores ! ")

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


def go_Through_PicsFile(province, city, start_pt):

    path = "D:\\用户的文件\\" + str(province) + "\\" + str(city)  # <Sample>: 'C:\\用户的文件\\湖北省\\武汉市'

    AccountFileNumber = 0  # To show the number the Account being read

    for dirpath, dirnames, filenames in os.walk(path):  # <Sample>: dirpath = 'C:\\用户的文件\\湖北省\\武汉市\\1982819117'

        for filepath in filenames:  # <Sample>: filepath = '1982819117.json'

            get_user_id = dirpath.replace(path + "\\", "")  # <Sample>: get_user_id = '18811860'

            if filepath == get_user_id + ".json":  # <sample>: 18811860.json

                AccountFileNumber += 1
                print("这是第 %i 个账号" % (AccountFileNumber))
                print("这个账号是：" + get_user_id)

                # To Find the ID Information more Easily !
                print()

                if AccountFileNumber >= start_pt:

                    if os.path.exists(dirpath + "\\" + get_user_id + "\\" + "Results.json") == True:

                        print("Results.json ok ! ")

                        _results_jsonpath = dirpath + "\\" + get_user_id + "\\" + "Results.json"

                        error, belonger = get_Belonger(_results_jsonpath)
                        if error == "OK":
                            copyJPGs(belonger, dirpath + "\\" + get_user_id)
                        else:
                            break
                    else:
                        print("No Results.json ! ")


def createScoreRegionDocuments_m():
    path = "D:\\用户的文件\\ScoreRegions_male"
    if os.path.exists(path) == False:
        os.makedirs(path)

    for i in range(0, 21):
        leveldocument_path = path + "\\" + "up_" + str(i * 5)
        if os.path.exists(leveldocument_path) == False:
            os.makedirs(leveldocument_path)

def createScoreRegionDocuments_f():
    path = "D:\\用户的文件\\ScoreRegions_female"
    if os.path.exists(path) == False:
        os.makedirs(path)

    for i in range(0, 21):
        leveldocument_path = path + "\\" + "up_" + str(i * 5)
        if os.path.exists(leveldocument_path) == False:
            os.makedirs(leveldocument_path)


if __name__ == "__main__":

    print("请输入要处理的文件所属省份：")

    # province = input()
    province = "湖北省"

    print("请输入要处理的文件所属城市：")

    # city = input()
    city = "武汉市"

    print("请输入选择处理的账号起点序号")
    # start_pt = input()
    start_pt = 0

    print("Ready to go ! ")

    createScoreRegionDocuments_m()
    createScoreRegionDocuments_f()

    go_Through_PicsFile(province, city, start_pt)