#!/usr/bin/env python
# encoding = utf-8
# Author: MUJZY
# Date: 2018-03-19
# Description: Use MultiThread to Extract the Faces in the JPG Files


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


def save_Extraction_Face_JPG(img_path, left, top, right, bottom,
                             compose_sub_spec_face_jpg_path):

    img = Image.open(str(img_path))
    print("save_Extraction_Face_JPG Ok!")

    """
    plt.figure("Beauty")
    plt.subplot(1,2,1),plt.title("Origin")
    plt.imshow(img),plt.axis('off')
    """

    box = (left, top, right, bottom)
    roi = img.crop(box)

    roi.save(compose_sub_spec_face_jpg_path)

    """
    plt.subplot(1, 2, 1), plt.title('Roi')
    # 注意！！！最后一个参数是控制要腾出多少个位置展示图片，如1，2，1就是展示在第一个位置
    # 而1，2，2则是则是将图片展示在第二个位置上
    plt.imshow(roi), plt.axis('off')
    path = compose_extraction_face_jpg_path
    plt.savefig(path)
    """


def start_Save_Extracted_JPG(face_number, pic_id, path_jpg, d, document_path):

    # 这里是人脸提取后的保存功能部分
    face_number += 1
    print("这是第 %d 张图片" % face_number)

    the_candidate_name = str(pic_id) + '_extraction_' + str(face_number)

    compose_sub_spec_face_jpg_path = document_path + "\\" + the_candidate_name + ".jpg"  # <Sample>: path = D:\\用户的文件\\广东省\\广州市\\18811860\\18811860\\....jpg

    # 读取人脸区域的坐标
    left, right, top, bottom = d.left(), d.right(), d.top(), d.bottom()
    print("脸部坐标：（%d,%d）,(%d,%d)" % (left, top, right, bottom))

    save_Extraction_Face_JPG(img_path=path_jpg, left=left,
                             top=top, right=right, bottom=bottom,
                             compose_sub_spec_face_jpg_path=compose_sub_spec_face_jpg_path)

    return face_number


"""
extract_Face_InsideJPG(path_jpg, pic_id, descriptors, candidates_names
                        candidates_weight_dictionary, detector, sp, facerec.
                            sub_spec_face_file_path, candidates_names_face_side_score_list)
Description for Function:
    作用：读取path_jpg所指的那张JPG文件，并提取出里面的所有人脸，并作需要的数据记录。
Samples and Descriptions <variable>:
    face_number{int} = 
    <face_number>: 作用：记录该照片中人脸的数目
    scores{array, double} = 
    <scores>: 作用： score越大，说明越接近正脸
    side_rate{list} = 
    <side_rate>: 作用：储存各张脸的正脸率
    num_of_faces{int} = 
    <num_of_faces>: 作用：储存该照片的人脸个数
    side_rate_i{int} = 
    <side_rate_i>: 作用：side_rate_i会在每单次循环后+ 1，从而使正脸率对应该照片中的那个脸
"""


def extract_Face_InsideJPG(path_jpg, pic_id, detector, document_path,):

    face_number = 0
    print("extract_Face_InsideJPG Ok!")

    try:
        img = io.imread(path_jpg)
        print("extract_Face_InsideJPG Ok!")

        """
        side_rate = []
        # scores值越大越接近正脸
        dets, scores, idx = detector.run(img, 1)
        for i, d in enumerate(dets):
            # print("Detection {}, dets{},score: {}, face_type:{}".format(i, d, scores[i], idx[i]))
            side_rate.append(scores[i])  # 越先被遍历的在数组中的下标越小
        """

        # 人脸检测
        dets = detector(img, 1)
        print("extract_Face_InsideJPG Ok!")

        # print("Number of faces detected:{}".format(len(dets)))

        # 记录每张脸的大小
        faceSizeList = []

        for k, d in enumerate(dets):    # <Samples>: d = {rectangle}[(451, -62) (913, 451)]
            """
            <Samples>:
                left = d.left() # <Samples>: {int}451   <Description>: 人脸左边距离图片左边界的距离
                right = d.right()   # <Samples>: {int}913   <Description>: 人脸右边距离图片左边界的距离
                top = d.top()   # <Samples>: {int}-62   <Description>: 人脸上边距离图片上边界的距离
                bottom = d.bottom() # <Samples>: {int}451   <Description>: 人脸下边距离图片上边界的距离
            """
            SIZE1 = (d.right() - d.left()) * (d.bottom() - d.top()) # <Sample>: {int}
            faceSizeList.append(SIZE1)

        faceSizeList = GetSelected(faceSizeList)    # <Description>: faceSizeList中最后不是0的那些元素所对应的对象就是被选中的
        print("extract_Face_InsideJPG Ok!")

        # 得到人脸个数的变量
        num_of_faces = len(dets)
        print("extract_Face_InsideJPG Ok!")

        if num_of_faces > 0 :

            # 初始化一个_i来对应side_rate这个list的指针位置，从而获取这张脸的正脸率：即：score来进行比较
            side_rate_i = 0

            for k, d in enumerate(dets):

                if faceSizeList[side_rate_i] != 0:

                    face_number = start_Save_Extracted_JPG(face_number, pic_id, path_jpg, d, document_path)
                    print("extract_Face_InsideJPG Ok!")

                    side_rate_i = side_rate_i + 1
    except:

        print("Not able to Load!")


def createFacesDocument(path, get_user_id):

    temp = get_user_id + ".json"
    path = path.replace(temp, get_user_id)

    judgeExisting = os.path.exists(path)
    if not judgeExisting :
        os.makedirs(path)

    print("createFacesDocument Ok!")

    return path # <Sample>: path = D:\\用户的文件\\广东省\\广州市\\18811860\\18811860


"""
compose_ReadJPG_Path(path, get_user_id, pic_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Description for Function::
    作用：返回的path值，是要读的JPG文件的完整路径
Samples：
    path(2nd) = 'D:\\用户的文件\\广东省\\广州市\\18811860\\011f0bd4jw1ek0s5pr3r3j20xc18g7ht.jpg'
"""


def compose_ReadJPG_Path(path, get_user_id, pic_id):

    get_user_id = str(get_user_id) + ".json"
    pic_JPG_filename = str(pic_id) + ".jpg"
    path = path.replace(get_user_id, pic_JPG_filename)
    print("compose_ReadJPG_Path Ok!")

    return path  # 这个path就是要读的JPG的完整路径


"""
get_Pic_id(rline)
~~~~~~~~~~~~~~~~~
Discription for Function:
    作用：返回pic_id，pic_id是该用户账号中该jpg文件的编号，如果出现异常，则pic_id = 'F'或'E'。
"""


def get_Pic_id(rline, UMARK, line_i):

    try:
        get_se_url = rline["se_get_large_url"]  # 注意：该path后面有斜杠
        print("get_Pic_id Ok!")

        if line_i != 1 :

            if get_se_url != UMARK :

                str_divided1 = str(get_se_url).split("e/")
                str_divided2 = str(str_divided1[1]).split(".")
                pic_id = str_divided2[0]
                return pic_id  # 注意：它是没有“.jpg”后缀的
            else :
                return "E"
    except:
        pic_id = "F"

        return pic_id


def avoid_Repeated_JSON(path):

    f1 = open(path, encoding='utf-8')
    rline = json.loads(f1.readline())
    UMARK = rline["se_get_large_url"]   # <Function>: 储存该文件夹的第一行的"se_get_large_url"

    print("avoid_Repeated_JSON Ok!")

    return UMARK


"""
read_JsonFiles(path, get_user_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Samples:
    path = 'D:\\用户的文件\\广东省\\广州市\\18811860\\18811860.json'
    get_user_id = '18811860'
    f1 = <_io.TextIOWrapper name='D:\\用户的文件\\广东省\\广州市\\18811860\\18811860.json' mode='r' encoding='utf-8'>
    new_json_filepath = 'D:\\用户的文件\\广东省\\广州市\\18811860\\18811860_results.json'
    sub_spec_face_file_path = 'D:\\用户的文件\\广东省\\广州市\\18811860\\'
    pic_id = '011f0bd4jw1ek0s5pr3r3j20xc18g7ht'
    path_jpg = 'D:\\用户的文件\\广东省\\广州市\\18811860\\011f0bd4jw1ek0s5pr3r3j20xc18g7ht.jpg'
    candidates_names = 
    descritptors = 
    candidates_weight_dictionary = 
    candidates_names_face_side_score_list = 
Description:
    descriptors = <class 'list'>: 该列表储存各候选人脸的描述子
    candidates_names = <class 'list'>: 该列表储存各候选人脸对应的jpg文件名
    candidates_weight_dictionary = <class 'list'>: 该列表储存各候选人的“代表性脸”的权重总和
    candidates_names_facesidescore_list = <class 'dict'>: 该字典，以pic_id为键值，键值映射的值为正脸率（即：后面的变量：score），作用：查询score，然后进行正脸率的比较
"""


def read_JsonFiles(path, get_user_id, dirpath):

    UMARK = avoid_Repeated_JSON(path)

    f1 = open(path, encoding='utf-8')
    print("read_JsonFiles Ok!")

    # 新建一个文件夹，来放置所有提取出来的人脸，该文件夹以该账号作为文件名
    # <Sample>: path = D:\\用户的文件\\广东省\\广州市\\18811860\\18811860
    document_path = createFacesDocument(path, get_user_id)
    print("read_JsonFiles Ok!")

    line_i = 0

    for line in f1.readlines():

        line_i += 1

        # rline加载每一整条的JSON信息
        rline = json.loads(line)

        # 得到该pic_id
        pic_id = get_Pic_id(rline, UMARK, line_i)  # 注意：它是没有“.jpg”后缀的
        print("read_JsonFiles Ok!")

        if pic_id != "F":   # 即没有捕捉到异常

            # 构造要读的jpg文件的完整路径：
            path_jpg = compose_ReadJPG_Path(path, get_user_id, pic_id)  # 这个path就是要读的JPG的完整路径
            print("read_JsonFiles Ok!")

            # 现在开始检测并记录该图片中的人脸
            extract_Face_InsideJPG(path_jpg, pic_id, detector, document_path)
            print("read_JsonFiles Ok!")

        if pic_id == "E" : break  # 即发现有重复的JPG文件指向，所以退出该for循环

    # 结束该账号的人脸提取，并创建一个“Ext_Ok”文件夹，以标记该账号已经完成人脸提取
    dirpath = dirpath + "\\" + "Ext_Step_Ok"  # <Sample>: D:\\用户的文件\\广东省\\广州市\\18811860\\Ext_Step_Ok

    # To solve the problem following : FileExistsError: [WinError 183] 当文件已存在时，无法创建该文件。: 'D:\\用户的文件\\湖北省\\武汉市\\2813127262\\Ext_Step_Ok'
    if not os.path.exists(dirpath):

        os.makedirs(dirpath)
    else:
        print("Already Existing Ext_Step_Ok ! ")


"""
go_Through_PicsFile(province, city)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Samples:
    province = '广东省'
    city = '广东省'
    path = 'D:\\用户的文件\\广东省\\广州市'
    dirpath = 'D:\\用户的文件\\广东省\\广州市\\18811860'
    dirnames = <class 'list'>: []
    filenames = <class 'list'>: ['011f0bd4jw1ek0s5pr3r3j20xc18g7ht.jpg', '...', '18811860.json']
    path_Divided = <class 'list'>: ['18811860', 'json']
    get_user_id = '18811860'
    path(2nd) = 'D:\\用户的文件\\广东省\\广州市\\18811860\\18811860.json'
"""


def go_Through_PicsFile(province, city):

    path = "D:\\用户的文件\\" + str(province) + "\\" + str(city)

    AccountFileNumber = 0  # To show the number the Account being read

    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:

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

                        read_JsonFiles(dirpath + "\\" + get_user_id + ".json", get_user_id, dirpath)

                        break

                    elif (AccountFileNumber > end_pt):
                        exit(0)

                    break


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
province = "广东省"

print("请输入要处理的文件所属城市：")

# city = input()
city = "广州市"

start_pt = 150001
end_pt = 190000

print("Ready to go ! ")

go_Through_PicsFile(province, city)
