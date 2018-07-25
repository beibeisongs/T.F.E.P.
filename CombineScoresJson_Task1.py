#!/usr/bin/env python
# encoding = utf-8
# Author: MUJZY
# Date: 2018-04-05
# Description: Use Face++ to analyse the Face Scores


import json
from json import JSONDecoder

import os
import os.path


def get_JsonScoresSource_Belonger(json_results_source_wholepath):

    f1 = open(json_results_source_wholepath, mode='r')

    try:

        for line in f1.readlines():

            rline = json.loads(line)

            belonger = rline["Belonger"]  # <Sample>: <type 'list'>: [u'011f0bd4jw1ek0s5x0uysj20qo0zkwn2_extraction_1', u'011f0bd4jw1ekdf0acjsmj218g0xcduc_extraction_1']

            get_faces = rline["faces"]
            get_faces_dic = get_faces[0]
            get_attributes = get_faces_dic["attributes"]
            get_gender = get_attributes["gender"]
            get_gender_value = get_gender["value"]

            get_age = get_attributes["age"]
            get_age_value = get_age["value"]

            get_beauty = get_attributes["beauty"]
            get_female_score = get_beauty["female_score"]
            get_male_score = get_beauty["male_score"]

    except:
        belonger = -1
        get_gender_value = -1
        get_age_value = -1
        get_female_score = -1
        get_male_score = -1

    return belonger, get_gender_value, get_age_value, get_female_score, get_male_score


if __name__ == "__main__":

    print("请输入想要处理的省份")
    # province = input()
    province = "浙江省"

    print("请输入想要处理的地级市")
    # city = input()
    city = "杭州市"

    start_pt = 0
    end_pt = 230000

    path = "D:\\用户的文件\\" + province + "\\" + city

    AccountFileNumber = 0  # To show the number the Account being read

    C_array = []

    JsonPathToWrite = "Combine_Result.json"
    f1 = open(JsonPathToWrite, mode='w')

    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:  # <Sample>: filepath = '1982819117.json'

            path_Divided = dirpath.split('\\')
            if len(path_Divided) >= 5:
                get_user_id = path_Divided[4]

                path = os.path.join(dirpath, filepath)
                path_Divided = str(path).split('.')

                if (filepath == get_user_id + ".json"):

                    print("账号：", get_user_id)

                    AccountFileNumber += 1
                    print("这是第 %i 个账号" % (AccountFileNumber))

                    if (AccountFileNumber >= start_pt) and (AccountFileNumber <= end_pt):

                        if os.path.exists(dirpath + "\\" + "Ext_Step_Ok") == True:

                            if os.path.exists(dirpath + "\\" + get_user_id + "\\" + "Results.json") == True:

                                print("Results.json Existing !")
                                print("-----------------------")

                                if os.path.exists(dirpath + "\\" + get_user_id + "\\" + "Face_Scores.json"):

                                    json_scores_source_wholepath = dirpath + "\\" + get_user_id + "\\" + "Face_Scores.json"

                                    belonger, get_gender_value, get_age_value, get_female_score, get_male_score = get_JsonScoresSource_Belonger(json_scores_source_wholepath)

                                    if get_male_score != -1:

                                        data = {}
                                        data["belonger"] = belonger
                                        data["gender"] = get_gender_value
                                        data["age"] = get_age_value
                                        data["female_score"] = get_female_score
                                        data["male_score"] = get_male_score
                                        data["id"] = get_user_id

                                        a = json.dumps(data)
                                        b = str(a) + '\n'  # 注意！！！一定要换行！！！换行！！！！
                                        print("Written : ", b)

                                        judgeExisting = os.path.exists(JsonPathToWrite)

                                        if not judgeExisting:
                                            f1.write(b)
                                        else:
                                            f1 = open(JsonPathToWrite, mode='a')
                                            f1.write(b)

                                        break

                    elif (AccountFileNumber > end_pt): exit(0)

                    break
