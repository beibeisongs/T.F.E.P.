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

    try:

        for line in f1.readlines():

            rline = json.loads(line)
            belonger = rline["Belonger"]  # <Sample>: <type 'list'>: [u'011f0bd4jw1ek0s5x0uysj20qo0zkwn2_extraction_1', u'011f0bd4jw1ekdf0acjsmj218g0xcduc_extraction_1']
            belonger_sub_face_name = rline["Belonger_sub_face_name"]
    except:
        belonger_sub_face_name = -1
        belonger = -1

    return belonger, belonger_sub_face_name


"""
Attention:
    The codes following are the Main Thread.
"""

key = "-z-GWFLRS9algPAaExP51KCpKIGmH-jJ"
secret = "Ft-p-NQ5wNg6bWK_apS4jaMD37FHqzgG"
http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"

print("请输入想要处理的省份")
# province = input()
province = "广东省"

print("请输入想要处理的地级市")
# city = input()
city = "广州市"

start_pt = 0
end_pt = 2

path = "C:\\用户的文件\\" + province + "\\" + city

AccountFileNumber = 0  # To show the number the Account being read

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

                            if not os.path.exists(dirpath + "\\" + get_user_id + "\\" + "Face_Scores.json"):

                                json_results_source_wholepath = dirpath + "\\" + get_user_id + "\\" + "Results.json"

                                belonger, belonger_sub_face_name = get_JsonResultsSource_Belonger(json_results_source_wholepath)

                                if belonger != -1:

                                    # <Attention>: 下面指令筛选出了主人的脸中相对最大的那张脸
                                    size, belonger,  belongerFace_JPG_Wholepath = get_theMaxPic(belonger, belonger_sub_face_name, dirpath, get_user_id)

                                    if (size[0] < 48) | (size[1] < 48):

                                        ResizeImage(belongerFace_JPG_Wholepath, belongerFace_JPG_Wholepath, 80, 80)

                                    response = Get_TheFaceScore(belongerFace_JPG_Wholepath)

                                    req_con = response.content.decode('utf-8')

                                    req_dict = JSONDecoder().decode(req_con)

                                    print(req_dict)

                                    json_FaceScore_TheWholePath = dirpath + "\\" + get_user_id + "\\" + "Face_Scores.json"

                                    f1 = open_Json_File_To_Write(json_FaceScore_TheWholePath)

                                    write_Score(req_dict, f1, belonger)

                                    print("!!! Finished A Compensate Process !!! ")

                                    break

                    elif (AccountFileNumber > end_pt): exit(0)

                    break
