# encoding=utf-8
# Date: 2018-7-20
# Author: MJUZY


import os
from shutil import copy

import json

from Resize_JPG import ResizeImage
from Resize_JPG import Calculate_JPGsize


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
        belonger = -1
        belonger_sub_face_name = -1

    return belonger, belonger_sub_face_name


def move(path, get_user_id, dirpath):

    old_json_path = path

    json_results_source_wholepath = dirpath + "\\" + get_user_id + "\\" + "Results.json"

    belonger, belonger_sub_face_name = get_JsonResultsSource_Belonger(json_results_source_wholepath)

    if belonger != -1:

        new_path, account_lib, extracted_lib = create_libs(get_user_id)

        # <Attention>: 下面指令筛选出了主人的脸中相对最大的那张脸
        size, belonger, belongerFace_JPG_Wholepath = get_theMaxPic(belonger, belonger_sub_face_name, dirpath, get_user_id)

        if (size[0] < 48) | (size[1] < 48):
            ResizeImage(belongerFace_JPG_Wholepath, belongerFace_JPG_Wholepath, 80, 80)

        copy(belongerFace_JPG_Wholepath, extracted_lib)


def create_libs(get_user_id):

    new_path = "D:\\用户的文件\\" + str(province) + "\\" + str(city)
    judgeExisting = os.path.exists(new_path)
    if not judgeExisting:
        os.makedirs(new_path)

    account_lib = new_path + "\\" + get_user_id
    judgeExisting = os.path.exists(account_lib)
    if not judgeExisting:
        os.makedirs(account_lib)

    extracted_lib = account_lib + "\\" + get_user_id
    judgeExisting = os.path.exists(extracted_lib)
    if not judgeExisting:
        os.makedirs(extracted_lib)

    return new_path, account_lib, extracted_lib


def move_process(province, city):

    path = "E:\\用户的文件\\" + str(province) + "\\" + str(city)

    AccountFileNumber = 0  # To show the number the Account being read

    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:

            get_user_id = dirpath.replace(path + "\\", "")  # <Sample>: '18811860'

            if filepath == get_user_id + ".json":  # <sample>: 18811860.json

                print(get_user_id)

                AccountFileNumber += 1
                print("这是第 %i 个账号" % (AccountFileNumber))

                if (AccountFileNumber >= start_pt) and (AccountFileNumber <= end_pt):

                    move(dirpath + "\\" + get_user_id + ".json", get_user_id, dirpath)

                elif (AccountFileNumber > end_pt): exit(0)


if __name__ == "__main__":

    print("请输入要处理的文件所属省份：")

    # province = input()
    province = "广东省"

    print("请输入要处理的文件所属城市：")

    # city = input()
    city = "广州市"

    print("请输入选择处理的账号起点序号")
    # start_pt = input()
    start_pt = 0    # <Attention>: 注意！这个账号中是一定有Ext_Step_Ok文件夹的，所以如果后面遇到No Ext_Step_Ok ! 则一定是Faces_Extraction_MultiThread_Test2.py还没有将人脸提取出来

    end_pt = 130000

    print("Ready to go ! ")

    move_process(province, city)
