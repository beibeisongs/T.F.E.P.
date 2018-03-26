#!/usr/bin/env python
# encoding = utf-8
# Author: MUJZY
# Date: 2018-03-22
# Description: Find the Account Owner.


import json
import sys

import os
import glob

import numpy
import matplotlib.pyplot as plt

import dlib
from PIL import Image
from skimage import io

from FaceSizeComparasion import GetSelected

import threading
import time


def compose_Data_toWrite(Max_Number, desc_link_jpgname, total_list, sum_SubFaceNames):

    data = {}

    if total_list == []:
        data["Attention"]  = "No Face !"
    else:
        data[desc_link_jpgname[Max_Number]] = total_list[Max_Number]    # <Sample>: "3b9adb14jw1ekd7mc8oe0j20f00qoaar_extraction_1": 7.0
        data["Belonger"] = desc_link_jpgname[Max_Number]    # <Sample>: "Belonger": "3b9adb14jw1ekd7mc8oe0j20f00qoaar_extraction_1"
        data["Belonger_sub_face_name"] = sum_SubFaceNames[Max_Number]

    return data


def write_ResultJson(Max_Number, desc_link_jpgname, document_path, total_list, sum_SubFaceNames):

    data = compose_Data_toWrite(Max_Number, desc_link_jpgname, total_list, sum_SubFaceNames)

    f1 = open(document_path + "\\" + "Results.json", mode='w')
    print("Opening JSON ! ")

    a = json.dumps(data)
    b = str(a + '\n')

    print("Writing JSON ! ")
    f1.write(b)

    print("Finish writing JSON ! ")


def getMaxTot(total_list):

    Max_Number_def = 0  # 点明这个Maz_Number是这个define中的

    temp = 0
    for i in range(0, len(total_list)):

        if total_list[i] > temp:

            Max_Number_def = i
            temp = total_list[i]

    return Max_Number_def   # 返回的值为total_list中最大值的下标


def Construct_Candidates_List(filenames, document_path):

    descriptors = []    # descriptor这个列表每个元素一次储存每个人脸的特征矩阵，后面计算欧式距离时会用到
    desc_link_jpgname = []  # 记录对应的人脸特征矩阵的所属JPG文件名

    for i in range(0, len(filenames)):

        path_jpg = document_path + "\\" + filenames[i]  # <Sample>: path_jpg = C:\\用户的文件\\湖北省\\武汉市\\1982819117\\1982819117\\762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2.jpg

        try:
            img = io.imread(path_jpg)

            # 人脸检测
            # 因为都是已经截好的图片，所以人脸数量必然是一
            dets = detector(img, 1)

            for k, d in enumerate(dets):

                # 关键点检测
                shape = sp(img, d)

                # 描述子提取，128D向量
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                print("face_descriptor : Ok ! ")

                # 转换成numpy，array
                d_test = numpy.array(face_descriptor)

                # descriptor这个列表每个元素一次储存每个人脸的特征矩阵，后面计算欧式距离时会用到
                descriptors.append(d_test)
                # 记录对应的人脸特征矩阵的所属JPG文件名
                desc_link_jpgname.append(filenames[i])  # <Attention>: 每个元素是字符串 <Sample>: 762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2.jpg

        except:
            # <Description>: 有可能出现图片加载不了的错误
            print("Not able to Load ! ")

    return descriptors, desc_link_jpgname


def analysor(document_path, get_user_id):   # <Sample>: document_path = 'C:\\用户的文件\\湖北省\\武汉市\\1982819117\\1982819117'

    for dirpath, dirnames, filenames in os.walk(document_path): # <Sample>: dirpath = 'C:\\用户的文件\\湖北省\\武汉市\\1982819117\\1982819117'

        # 先把filenames中的所有截出来的人脸当成候选人脸构成一个列表
        print("Start Constructing A Condidates List ! ")

        descriptors, desc_link_jpgname = Construct_Candidates_List(filenames, document_path)

        total_list = [] # 用来储存每一张脸撞脸的总次数

        # subFaceNames = []    # 用来记录与该脸为同一张脸的对应的JPG Name  # <Sample>: 762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2

        sum_SubFaceNames = []   # 将每一张脸的Sub Faces集合为一个List

        face_i = -1 # 该变量指代现在遍历到的人脸在desc_link_jpgname这个list中的下标

        for filepath in desc_link_jpgname:  # <Sample>: filepath = '762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2.jpg'
                                    # <Sample>: filenames = <class 'list'>: ['762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_1.jpg', '762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2.jpg', '762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_3.jpg', '762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_4.jpg', '762f6b2djw1ei0keq5ft2j20hs0vkact_extraction_1.jpg', '762f6b2djw1ei0keq5ft2j20hs0vkact_extraction_2.jpg', '762f6b2djw1ei0keq5ft2j20hs0vkact_extraction_3.jpg', '762f6b2djw1ei0kf1id0nj20hs0vkdiq_extraction_1.jpg', '762f6b2djw1ei0kf1id0nj20hs0vkdiq_extraction_2.jpg', '762f6b2djw1ei0kf1id0nj20hs0vkdiq_extraction_3.jpg', '762f6b2djw1eiihfi1jitj20c00hs75k_extraction_1.jpg', '762f6b2djw1ej7q49u3qpj20c00hsdhs_extraction_1.jpg', '762f6b2djw1ej7q4aye61j20c00hsgn9_extraction_1.jpg', '762f6b2djw1ej7q4bw25dj20c00hsgnb_extraction_1.jpg', '762f6b2djw1ejjgu54qsuj21w02iob2a_extraction_1.jpg']

            subFaceNames = []  # 用来记录与该脸为同一张脸的对应的JPG Name  # <Sample>: 762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2

            face_i += 1

            print("Enter Faces Document ! ")
            print(filepath)

            path_jpg = dirpath + "\\" + filepath    # <Sample>: path_jpg = 'C:\\用户的文件\\湖北省\\武汉市\\1982819117\\1982819117\\762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2.jpg'

            get_picID_stp1 = filepath.split("_e")
            pic_id = get_picID_stp1[0]  # <Sample>: pic_id = 762f6b2djw1ei0kepm85pj20hs0vkdir

            # 现在开始统计每张脸在这个账号中出现的次数
            i = -1

            tot = 0

            for des_i in descriptors:   # <Description>: des_i是每个人脸的特征矩阵

                i += 1

                # 出自同一只照片的人脸会被跳过，不进行欧式距离的比较，因为同一个照片的人脸不可能是同一个人
                # <Attention>: desc_link_jpgname[i]是对应des_i这个特征矩阵所指代的人脸
                if desc_link_jpgname[i].find(pic_id) == -1: # 返回值为-1，说明不是出自同一张照片

                    # 下面计算欧式距离
                    dist_ = numpy.linalg.norm(des_i - descriptors[face_i])   # <Description>: des_i 是每一个候选人的人脸特征矩阵

                    # 统计撞脸次数被储存到total_list 列表中
                    if dist_ < 0.384:   # <Tip>: 一般欧氏距离小于0.384就可以认为是同一张脸了，值越小说明是同一张脸的可能性越大

                        tot += 1
                        print("tot + 1 ! ")

                        subFaceNames.append(desc_link_jpgname[i])

            # <Attention>: 注意！有可能出现total_list是[]的情况

            total_list.append(tot)

            sum_SubFaceNames.append(subFaceNames)

        print("total_list : ", total_list)

        Max_Number = getMaxTot(total_list)   # 返回的值为total_list中最大值的下标

        write_ResultJson(Max_Number, desc_link_jpgname, document_path, total_list, sum_SubFaceNames)


def start_SubThread(document_path, get_user_id):

    class myThread(threading.Thread):

        def __init__(self, document_path, get_user_id):

            threading.Thread.__init__(self)

            self.document_path = document_path
            self.get_user_id = get_user_id

            self.flag = True    # True表示该线程正在运行

        def run(self):

            print("Run ! ")

            analysor(self.document_path, self.get_user_id)

            self.flag = False   # False表示线程结束

    Thread1 = myThread(document_path, get_user_id)

    Thread1.start()

    return Thread1


def go_Through_PicsFile(province, city, start_pt):

    path = "E:\\用户的文件\\" + str(province) + "\\" + str(city) # <Sample>: 'C:\\用户的文件\\湖北省\\武汉市'

    AccountFileNumber = 0  # To show the number the Account being read

    Threads = []    # 这是一个用于存放myThreads的List

    Threads_i = 0   # 这个变量指代这是第几个被创建的线程

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

                    mark2 = True

                    while mark2 == True:

                        if os.path.exists(dirpath + "\\" + "Ext_Step_Ok") == True:   # 即存在标记文件夹，则进行下面的操作

                            print(" Ext_Step_Ok ! ")

                            Threads_i += 1

                            if Threads_i < 5:   # <Tip>: 我只允许同时存在4条子线程

                                # 开启多线程，每个账号一个线程
                                Threads.append(start_SubThread(dirpath + "\\" + get_user_id, get_user_id))

                            else:   # 当轮到第五个线程时，就开始检索前面的线程看有哪一个执行完了，就被join掉
                                mark = True

                                while (mark == True):

                                    time.sleep(1)

                                    for i in range(0, 4):   # 即遍历Threads[0、1、2、3]的flag变量是True还是False，true为仍在运行，false为停止运行

                                        try:
                                            if Threads[i].flag == False:

                                                Threads[i] = start_SubThread(dirpath + "\\" + get_user_id, get_user_id)

                                                mark = False

                                                break
                                        except:
                                            print("In Loop: Jump to Next Time ! ")
                                            break

                            mark2 = False    # <Description>: 从而退出While循环，进入下一个账号的分析统计

                        else:
                            print("  No Ext_Step_Ok ! ")
                            mark2 = True
                            time.sleep(10)
                            print(" Try again ! ")

                break   # 因为只要满足了filepath == get_user_id + ".json":  # <sample>: 18811860.json
                        # 就应该跳出循环，进入下一个账号了

"""
prepare_detector
~~~~~~~~~~~~~~~~
This function is used to get all the detectors ready.
"""


def prepare_detector(predictor_path, face_rec_model_path):

    # 1、加载正脸检测器
    detector = dlib.get_frontal_face_detector()
    print("prepare_detector Ok!")
    # 2、加载人脸关键点检测器
    sp = dlib.shape_predictor(predictor_path)
    print("prepare_detector Ok!")
    # 3、加载人脸识别模型
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    print("prepare_detector Ok!")

    return detector, sp, facerec


"""
prepare_path_etc
~~~~~~~~~~~~~~~~
This function is used to introduce the data of two essential models, by its location in the hardware.
And the two models are located in the same documents with Face_Exist_Statistics_Test5.py.
"""


def prepare_path_etc():

    # 1、人脸关键点检测器
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    # 2、人脸识别模型：
    face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"

    return predictor_path, face_rec_model_path


"""
Attention:
    The codes following are the Main Thread of this program.
"""


predictor_path, face_rec_model_path = prepare_path_etc()

detector, sp, facerec = prepare_detector(predictor_path, face_rec_model_path)

print("请输入要处理的文件所属省份：")

# province = input()
province = "湖北省"

print("请输入要处理的文件所属城市：")

# city = input()
city = "武汉市"

print("请输入选择处理的账号起点序号")
# start_pt = input()
start_pt = 30760     # <Attention>: 注意！这个账号中是一定有Ext_Step_Ok文件夹的，所以如果后面遇到No Ext_Step_Ok ! 则一定是Faces_Extraction_MultiThread_Test2.py还没有将人脸提取出来

print("Ready to go ! ")

go_Through_PicsFile(province, city, start_pt)