# encoding=utf-8
# Date: 2018-7-30
# Author: MJUZY

import urllib3
import urllib.request
import json

import math
import csv
import json
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt


def Export2Csv(userid, emotion, score, text, csvname_output):

    csvFile2 = open(csvname_output, 'a+', newline='')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile2)

    datas = [userid, emotion, score, text]

    writer.writerow(datas)

    csvFile2.close()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http=urllib3.PoolManager()

def get_access_token():

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=7ahYM0PqmFVk3m99GBTpFI8H&client_secret=ySpEpNTllL9z2Gkah1oXfFhC6GeTizwG'
    req = urllib.request.urlopen(host)
    res = req.read().decode('utf-8')
    res = json.loads(res)

    return res


def get_content(text):

    access_token = get_access_token()
    print(access_token)
    access_token = access_token["access_token"]
    print(access_token)

    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=" + access_token  # API
    data = {}
    data["text"] = text

    try:
        data=json.dumps(data)
        request = http.request('POST', url, body=data, headers={'Content-Type': 'application/json'})
        result = request.data
        result = json.loads(result)
        emotion = result['items'][0]['sentiment']
        prob=0
        if emotion == 0:
            prob = result['items'][0]['negative_prob']
        if emotion == 1:
            prob = None
        if emotion == 2:
            prob = result['items'][0]['positive_prob']

        return emotion, prob

    except Exception as e:
        print('a', str(e))

        return "NULL", "NULL"


def getDate(item_time):

    divided = item_time.split(' ')
    month = divided[1]
    day = divided[2]
    year = divided[5]

    return day, month, year


def getElements(item2):

    userid = item2[0]
    idstr = item2[1]

    day, month, year = getDate(item2[2])

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

    return score, text, userid


def goThroughCSV(csv_name, csvname_output):

    userid_temp = ""

    scores_record = []
    emotion_record = []

    users_num_passed = 0

    line_i = 0
    with open(csv_name, "r") as csvfile:
        reader2 = csv.reader(csvfile)  # 读取csv文件，返回的是迭代类型
        for item2 in reader2:
            line_i += 1
            print("现在的行数是：", line_i)

            if (line_i >= start_pt) and (line_i <= end_pt):

                score, text, userid = getElements(item2)
                if text != "NULL":

                    emotion, prob = get_content(text)
                    if emotion == 2:    # Positive
                        emotion = prob
                    if emotion == 0:    # Nagative
                        emotion = (-1) * prob
                    if emotion == 1:
                        emotion = 0

                    Export2Csv(userid, emotion, score, text, csvname_output)
                    """
                    if line_i == 1:
                        userid_temp = userid

                        users_num_passed += 1

                        scores_record.append(0)
                        scores_record[users_num_passed - 1] = score
                        emotion_record.append(0)
                        emotion_record[users_num_passed - 1] = emotion

                    elif userid == userid_temp:
                        emotion_record[users_num_passed - 1] += emotion

                    elif userid_temp != userid:

                        emotion_record[users_num_passed - 1] /= emotion_record[users_num_passed - 1] / users_num_passed

                        userid_temp = userid

                        users_num_passed += 1

                        scores_record.append(0)
                        scores_record[users_num_passed - 1] = score

                        emotion_record.append(0)
                        emotion_record[users_num_passed - 1] = emotion
                    """
            elif (line_i > end_pt):
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

    start_pt = 50838
    end_pt = 230000

    csvname_output = "22_27_emotion.csv"

    csv_name = "22_27.csv"
    goThroughCSV(csv_name, csvname_output)
