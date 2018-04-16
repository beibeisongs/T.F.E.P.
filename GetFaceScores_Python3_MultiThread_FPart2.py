#!/usr/bin/env python
# encoding = utf-8
# Author: MUJZY
# Date: 2018-04-05
# Description: Use Face++ to analyse the Face Scores


import requests

import os.path

from PIL import Image

import json
from json import JSONDecoder

import base64

import os
import os.path
import sys

from Resize_JPG import ResizeImage
from Resize_JPG import Calculate_JPGsize

import time
import threading


def write_Score(response, f1, belonger):

    data = {}

    data = response
    data["Belonger"] = belonger

    a = json.dumps(data)
    b = str(a) + "\n"

    f1.write(b)

    f1.close()


def open_Json_File_To_Write(path_to_write):

    judgeExisting = True
    judgeExisting = os.path.exists(path_to_write)

    if not judgeExisting:
        f1 = open(path_to_write, mode='w')
    else:
        f1 = open(path_to_write, mode='a')
    return f1


def Get_TheFaceScore(belongerFace_JPG_Wholepath):

    """
    def use_base64_img(filename):
        with open(filename, 'rb') as f:
            img_base64 = base64.b64encode(f.read())

        return img_base64
    """

    fname = belongerFace_JPG_Wholepath

    data = {"api_key": key, "api_secret": secret, "return_attributes": "gender,beauty,age"}

    files = {"image_file": open(fname, "rb")}

    response = requests.post(http_url, data=data, files=files)

    """
    b64Getted = use_base64_img(fname)

    b64Getted = str(b64Getted)

    data = {"api_key": key, "api_secret": secret, "image_base64": b64Getted, "return_attributes": "gender,beauty,age"}

    response = requests.post(
        http_url,
        data=data,
        headers={
            'Authorization': 'APPCODE ' + key,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
    ).json()

    """

    return response


def get_theMaxPic(belonger, belonger_sub_face_name, dirpath, get_user_id):

    belongerFace_JPG_Wholepath = dirpath + "\\" + get_user_id + "\\" + belonger  # <Attention>: 这里已经包含了文件后缀“.jpg”
    belonger_size = Calculate_JPGsize(belongerFace_JPG_Wholepath)
    temp_size = belonger_size
    temp_name = belonger
    temp_whole_path = belongerFace_JPG_Wholepath

    for i in range(0, len(belonger_sub_face_name)):

        belongerSubFace_JPG_Wholepath = dirpath + "\\" + get_user_id + "\\" + belonger_sub_face_name[i]  # <Attention>: 这里已经包含了文件后缀“.jpg”
        belonger_subface_size = Calculate_JPGsize(belongerSubFace_JPG_Wholepath)

        if (belonger_subface_size[0] * belonger_subface_size[1]) > (temp_size[0] * temp_size[1]):
            temp_size = belonger_subface_size
            temp_name = belonger_sub_face_name[i]
            temp_whole_path = belongerSubFace_JPG_Wholepath

    return temp_size, temp_name, temp_whole_path


def get_JsonResultsSource_Belonger(json_results_source_wholepath):

    f1 = open(json_results_source_wholepath, mode='r')

    for line in f1.readlines():

        rline = json.loads(line)
        belonger = rline["Belonger"]  # <Sample>: <type 'list'>: [u'011f0bd4jw1ek0s5x0uysj20qo0zkwn2_extraction_1', u'011f0bd4jw1ekdf0acjsmj218g0xcduc_extraction_1']
        belonger_sub_face_name = rline["Belonger_sub_face_name"]

    return belonger, belonger_sub_face_name


def start_SubThread(belonger, belonger_sub_face_name, dirpath, get_user_id):

    class myThread(threading.Thread):

        def __init__(self, belonger, belonger_sub_face_name, dirpath, get_user_id):

            threading.Thread.__init__(self)

            self.belonger = belonger
            self.belonger_sub_face_name = belonger_sub_face_name
            self.dirpath = dirpath
            self.get_user_id = get_user_id

            self.flag = True

        def run(self):
            getScoreWholeProcess(self.belonger, self.belonger_sub_face_name, self.dirpath, self.get_user_id)
            self.flag = False

    Thread1 = myThread(belonger, belonger_sub_face_name, dirpath, get_user_id)

    Thread1.start()

    return Thread1


def getScoreWholeProcess(belonger, belonger_sub_face_name, dirpath, get_user_id):

    # <Attention>: 下面指令筛选出了主人的脸中相对最大的那张脸
    size, belonger, belongerFace_JPG_Wholepath = get_theMaxPic(belonger, belonger_sub_face_name,
                                                               dirpath, get_user_id)

    if (size[0] < 48) | (size[1] < 48):
        ResizeImage(belongerFace_JPG_Wholepath, belongerFace_JPG_Wholepath, 80, 80)

    response = Get_TheFaceScore(belongerFace_JPG_Wholepath)

    req_con = response.content.decode('utf-8')

    req_dict = JSONDecoder().decode(req_con)

    print(req_dict)

    json_FaceScore_TheWholePath = dirpath + "\\" + get_user_id + "\\" + "Face_Scores.json"

    f1 = open_Json_File_To_Write(json_FaceScore_TheWholePath)

    write_Score(req_dict, f1, belonger)


"""
Attention:
    The codes following are the Main Thread.
"""

key = "-z-GWFLRS9algPAaExP51KCpKIGmH-jJ"
secret = "Ft-p-NQ5wNg6bWK_apS4jaMD37FHqzgG"
http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"

print("请输入想要处理的省份")
# province = input()
province = "湖北省"

print("请输入想要处理的地级市")
# city = input()
city = "武汉市"

start_pt = 0

path = "D:\\用户的文件\\" + province + "\\" + city

Threads = []  # 这是一个用于存放myThreads的List

Threads_i = 0  # 这个变量指代这是第几个被创建的线程

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


                        json_results_source_wholepath = dirpath + "\\" + get_user_id + "\\" + "Results.json"

                        try:
                            belonger, belonger_sub_face_name = get_JsonResultsSource_Belonger(json_results_source_wholepath)

                            mark2 = True

                            while mark2 == True:

                                    Threads_i += 1

                                    if Threads_i < 5:  # <Tip>: 我只允许同时存在4条子线程

                                        # 开启多线程，每个账号一个线程
                                        Threads.append(start_SubThread(belonger, belonger_sub_face_name, dirpath, get_user_id))

                                    else:  # 当轮到第五个线程时，就开始检索前面的线程看有哪一个执行完了，就被join掉
                                        mark = True

                                        while (mark == True):

                                            time.sleep(1)

                                            for i in range(0, 4):  # 即遍历Threads[0、1、2、3]的flag变量是True还是False，true为仍在运行，false为停止运行

                                                try:
                                                    if Threads[i].flag == False:
                                                        Threads[i] = start_SubThread(belonger, belonger_sub_face_name, dirpath, get_user_id)

                                                        mark = False

                                                        break
                                                except:

                                                    print("In Loop: Jump to Next Time ! ")
                                                    break

                                    mark2 = False  # <Description>: 从而退出While循环，进入下一个账号的分析统计

                            break

                        except:

                            print("No Face ! ")

                            break




