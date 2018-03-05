#!/usr/bin/python
# -*- coding: latin-1 -*-
# Author: MUJZY
# Date: 2018-01-16


import requests

import json
import base64

import os
import os.path
import sys

from Resize_JPG import ResizeImage
from Resize_JPG import Calculate_JPGsize


def write_Score(response, f1, belonger_id):

    data = {}
    data = response
    data["Belonger"] = belonger_id

    a = json.dumps(data)
    b = str(a)+"\n"

    f1.write(b)
    f1.close()


def open_Json_File_To_Write(path_to_write):

    judgeExisting = True
    judgeExisting = os.path.exists(path_to_write)

    if not judgeExisting:
        f1 = open(path_to_write,mode='w')
    else:
        f1 = open(path_to_write,mode='a')
    return f1


def Get_TheFaceScore(belongerFace_JPG_Wholepath):

    def use_base64_img(filename):
        with open(filename, 'rb') as f:
            img_base64 = base64.b64encode(f.read())
        return img_base64

    fname = belongerFace_JPG_Wholepath # 一定要裁剪后只剩脸的图像才好打分
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

    return response


def get_JsonResultsSource_Belonger(json_results_source_wholepath):

    f1 = open(json_results_source_wholepath, mode='r')

    for line in f1.readlines():
        rline = json.loads(line)
        belonger = rline["Belonger"]    # <Sample>: <type 'list'>: [u'011f0bd4jw1ek0s5x0uysj20qo0zkwn2_extraction_1', u'011f0bd4jw1ekdf0acjsmj218g0xcduc_extraction_1']
        sub_face_for_belonger = rline["Belonger_sub_face_name"] # <Description>: "Belonger_sub_face_name" is the key to the faces of best side_score of the account's belonger
    return belonger, sub_face_for_belonger


"""
Attention:
    The codes following are the Main Thread.
"""

"""
Attention:
    key = "-z-GWFLRS9algPAaExP51KCpKIGmH-jJ"
    secret = "Ft-p-NQ5wNg6bWK_apS4jaMD37FHqzgG"
    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
"""


reload(sys)
sys.setdefaultencoding('utf-8')

key = "-z-GWFLRS9algPAaExP51KCpKIGmH-jJ"
secret = "Ft-p-NQ5wNg6bWK_apS4jaMD37FHqzgG"
http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"

print("请输入想要进行人脸打分的文件的所属省份")
# province = input()
province = "广东省"

print("请输入想要进行人脸打分的文件的所属城市")
# city = input()
city = "广州市"

path = ( "C:\\用户的文件\\" + province + "\\" + city ).encode('utf-8')
path = path.decode('utf-8')

for dirpath, dirnames, filenames in os.walk(path):
    for filepath in filenames:

        str1 = "json"
        str2 = "results"

        if str1 in filepath:
            if str2 in filepath:

                json_results_source_wholepath = dirpath + "\\" + filepath   # <Sample>: # <Sample>: u'D:\\用户的文件\\广东省\\广州市\\18811860\\18811860_results.json'
                belonger, belonger_sub_face = get_JsonResultsSource_Belonger(json_results_source_wholepath)  # 注意 : 这两个变量是一个list

                for belonger_i in range(0, len(belonger)) :  # <Sample>: belonger = <type 'list'>: [u'011f0bd4jw1ek0s5x0uysj20qo0zkwn2_extraction_1', u'011f0bd4jw1ekdf0acjsmj218g0xcduc_extraction_1']

                    belongerFace_JPG_Wholepath = dirpath + "\\" + belonger[belonger_i] + "\\" + belonger_sub_face[belonger_i] + ".jpg"   # <Samples>: dirpath = u'D:\\用户的文件\\广东省\\广州市\\18811860'

                    size = Calculate_JPGsize(belongerFace_JPG_Wholepath)

                    if  (size[0] < 48) | (size[1] < 48) :
                        ResizeImage(belongerFace_JPG_Wholepath, belongerFace_JPG_Wholepath, 80, 80)

                    response = Get_TheFaceScore(belongerFace_JPG_Wholepath)

                    json_FaceScore_TheWholePath = dirpath + "\\" + belonger[belonger_i] + "\\" + "Face_Score.json"

                    f1 = open_Json_File_To_Write(json_FaceScore_TheWholePath)

                    write_Score(response, f1, belonger[belonger_i])
