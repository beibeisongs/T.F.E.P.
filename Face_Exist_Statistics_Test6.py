# encoding=utf-8

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


def add_theCandidate_Weight_Value(the_candidate_name, candidates_weight_dictionary, num_of_faces):
    try:
        candidates_weight_dictionary[str(the_candidate_name)] = candidates_weight_dictionary[
                                                                    str(the_candidate_name)] + 1 / num_of_faces
        # print("Great!")
    except:
        candidates_weight_dictionary[str(the_candidate_name)] = 1 / num_of_faces
        # print("Great!")


def save_Extracted_SubFace_JPG(path_jpg, spec_SubFaceJPGPath_ToSave, left, right, top, bottom, d):
    # print("脸部坐标：（%d,%d）,(%d,%d)" % (left, top, right, bottom))

    img = Image.open(str(path_jpg))

    box = (left, top, right, bottom)
    roi = img.crop(box)
    roi.save(spec_SubFaceJPGPath_ToSave)


def start_Save_TheSubFace(path_jpg, face_number, spec_SubFaceJPGPath_ToSave, d):

    # 人脸提取后的保存功能部分
    # print("这是第 %d 张图片" % face_number)

    # 注意：要用来保存的那个文件夹的路径是：spec_SubFaceJPGPath_ToSave

    # plus:读取人脸的区域坐标
    left, right, top, bottom = d.left(), d.right(), d.top(), d.bottom()
    # print("脸部坐标：（%d,%d）,(%d,%d)" % (left, top, right, bottom))

    save_Extracted_SubFace_JPG(path_jpg, spec_SubFaceJPGPath_ToSave, left, right, top, bottom, d)


def create_Sub_Faces_File(compose_sub_spec_face_file_path):
    judgeExisting = os.path.exists(compose_sub_spec_face_file_path)
    if not judgeExisting:
        os.makedirs(compose_sub_spec_face_file_path)


def save_Extraction_Face_JPG(img_path, left, top, right, bottom, compose_sub_spec_face_file_path,
                             compose_sub_spec_face_jpg_path):

    # print("脸部坐标：（%d,%d）,(%d,%d)" % (left, top, right, bottom))

    img = Image.open(str(img_path))

    """
    plt.figure("Beauty")
    plt.subplot(1,2,1),plt.title("Origin")
    plt.imshow(img),plt.axis('off')
    """

    box = (left, top, right, bottom)
    roi = img.crop(box)
    # roi.save(compose_extraction_face_jpg_path)

    # 在此先把这个放置某人所有人脸截图的文件夹给创建了
    create_Sub_Faces_File(compose_sub_spec_face_file_path)
    roi.save(compose_sub_spec_face_jpg_path)

    """

    plt.subplot(1, 2, 1), plt.title('Roi')
    # 注意！！！最后一个参数是控制要腾出多少个位置展示图片，如1，2，1就是展示在第一个位置
    # 而1，2，2则是则是将图片展示在第二个位置上

    plt.imshow(roi), plt.axis('off')

    path = compose_extraction_face_jpg_path
    plt.savefig(path)
    """


def start_Save_Extracted_JPG(face_number, pic_id, path_jpg, d, sub_spec_face_file_path):

    # 这里是人脸提取后的保存功能部分
    face_number += 1
    #print("这是第 %d 张图片" % face_number)

    the_candidate_name = str(pic_id) + '_extraction_' + str(face_number)

    compose_sub_spec_face_file_path = sub_spec_face_file_path + the_candidate_name

    compose_sub_spec_face_jpg_path = compose_sub_spec_face_file_path + "\\" + the_candidate_name + ".jpg"

    # 读取人脸区域的坐标
    left, right, top, bottom = d.left(), d.right(), d.top(), d.bottom()
    # print("脸部坐标：（%d,%d）,(%d,%d)" % (left, top, right, bottom))

    save_Extraction_Face_JPG(img_path=path_jpg, left=left,
                             top=top, right=right, bottom=bottom,
                             compose_sub_spec_face_file_path=compose_sub_spec_face_file_path,
                             compose_sub_spec_face_jpg_path=compose_sub_spec_face_jpg_path)
    return face_number, the_candidate_name


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


def extract_Face_InsideJPG(path_jpg, pic_id, descriptors, candidates_names,
                           candidates_weight_dictionary, detector, sp, facerec,
                           sub_spec_face_file_path, candidates_names_face_side_score_list):
    face_number = 0
    try:
        img = io.imread(path_jpg)

        side_rate = []
        # scores值越大越接近正脸
        dets, scores, idx = detector.run(img, 1)
        for i, d in enumerate(dets):
            # print("Detection {}, dets{},score: {}, face_type:{}".format(i, d, scores[i], idx[i]))
            side_rate.append(scores[i])  # 越先被遍历的在数组中的下标越小

        # 人脸检测
        dets = detector(img, 1)
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

        # 得到人脸个数的变量
        num_of_faces = len(dets)

        # 初始化一个_i来对应side_rate这个list的指针位置，从而获取这张脸的正脸率：即：score来进行比较
        side_rate_i = 0
        for k, d in enumerate(dets):

            if faceSizeList[side_rate_i] != 0:

                # 记录当次欧氏距离的记录列表
                dist = []

                # 2、关键点检测
                shape = sp(img, d)

                # 3、描述子提取，128D向量
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                # 转换为numpy，array
                d_test = numpy.array(face_descriptor)

                # 计算欧氏距离
                # 即先遍历一遍Candidates(遍历一遍已经记录在descriptors数组的数据)
                # 提醒：候选人名单就是传入该def方法的candidates_names数组
                for i in descriptors:
                    dist_ = numpy.linalg.norm(i - d_test)
                    dist.append(dist_)

                # print(candidates_names)

                # 候选人和距离组成一个dict
                c_d = dict(zip(candidates_names, dist))
                cd_sorted = sorted(c_d.items(), key=lambda d: d[1])

                if cd_sorted == []:

                    face_number, the_candidate_name = start_Save_Extracted_JPG(face_number, pic_id, path_jpg, d,
                                                                               sub_spec_face_file_path)

                    # 在candidates_names_face_side_score_list[str(the_candidate_name)]处赋予一个list,list[0]=the_candidate_name,list[1]=side_rate[side_rate_i]                candidates_names_face_side_score_list[str(the_candidate_name)] = []
                    candidates_names_face_side_score_list = insert_TheScoreList(candidates_names_face_side_score_list,
                                                                                the_candidate_name, side_rate, side_rate_i)

                    candidates_names.append(str(the_candidate_name))
                    descriptors.append(d_test)
                    add_theCandidate_Weight_Value(the_candidate_name, candidates_weight_dictionary, num_of_faces)

                else:

                    # 下面是为了DEBUG时能够清晰地显示所需看到的值
                    # cd_sorted_vice_forTest = cd_sorted[0][0]
                    # print(cd_sorted_vice_forTest)
                    cd_sorted_vice_forTest = cd_sorted[0][1]
                    # print(cd_sorted_vice_forTest)

                    if float(cd_sorted_vice_forTest) > 0.38:  # 注意！！！值越小，说明越可能与这张脸是同一个人！！！一般在0.354以下为同一张脸
                        # 但仍需要考虑应带要多少的值排除侧脸影响的效果才能最好

                        face_number, the_candidate_name = start_Save_Extracted_JPG(face_number,
                                                                                   pic_id, path_jpg, d,
                                                                                   sub_spec_face_file_path)

                        # 在candidates_names_face_side_score_list[str(the_candidate_name)]处赋予一个list,list[0]=the_candidate_name,list[1]=side_rate[side_rate_i]                candidates_names_face_side_score_list[str(the_candidate_name)] = []
                        candidates_names_face_side_score_list = insert_TheScoreList(candidates_names_face_side_score_list,
                                                                                    the_candidate_name, side_rate,
                                                                                    side_rate_i)

                        candidates_names.append(str(the_candidate_name))
                        descriptors.append(d_test)
                        add_theCandidate_Weight_Value(the_candidate_name, candidates_weight_dictionary, num_of_faces)

                    else:  # 走到这一步说明是检测到有同一张脸了
                        face_number = face_number + 1
                        the_same_face_jpg_candidate_name = str(cd_sorted[0][0])
                        spec_SubFaceJPGPath_ToSave = sub_spec_face_file_path + the_same_face_jpg_candidate_name + "\\" + str(
                            pic_id) + "_extraction_" + str(face_number) + ".jpg"
                        sub_pic_name = str(pic_id) + "_extraction_" + str(face_number)
                        # 然后现在把这张脸归属保存到对应的人的脸的文件夹中
                        start_Save_TheSubFace(path_jpg, face_number, spec_SubFaceJPGPath_ToSave, d)

                        add_theCandidate_Weight_Value(the_same_face_jpg_candidate_name, candidates_weight_dictionary,
                                                      num_of_faces)
                        # 下面开始判断这张相同的脸和原来的被相同的脸谁的正脸率较大,如果前者较大，则进行键值（the_same_face_jpg_candidate_name）以及score（正脸率）的修改
                        candidates_names_face_side_score_list = correct_Candidates_SideFaceScores_Dictionary(
                            candidates_names_face_side_score_list, the_same_face_jpg_candidate_name, sub_pic_name,
                            side_rate, side_rate_i)

                        # print("\n The person is : ", cd_sorted[0][0])

                    side_rate_i = side_rate_i + 1
    except:
        print("Not able to Load!")
        return candidates_names, descriptors, candidates_weight_dictionary, candidates_names_face_side_score_list

    return candidates_names, descriptors, candidates_weight_dictionary, candidates_names_face_side_score_list


def insert_TheScoreList(candidates_names_face_side_score_list, the_candidate_name, side_rate, side_rate_i):
    list1 = []
    list1.append(str(the_candidate_name))
    list1.append(side_rate[side_rate_i])
    candidates_names_face_side_score_list[str(the_candidate_name)] = list1
    return candidates_names_face_side_score_list


def correct_Candidates_SideFaceScores_Dictionary(candidates_names_face_side_score_list,
                                                 the_same_face_jpg_candidate_name, sub_pic_name, side_rate,
                                                 side_rate_i):

    list1 = candidates_names_face_side_score_list[the_same_face_jpg_candidate_name]

    if list1[1] < side_rate[side_rate_i]:
        list1[1] = side_rate[side_rate_i]
        list[0] = sub_pic_name
        candidates_names_face_side_score_list[str(the_same_face_jpg_candidate_name)] = list1

    return candidates_names_face_side_score_list


def get_TheBelonger_JPGname(candidates_weight_dictionary):
    # 初始化
    get_face_weight_temp = 0
    get_face_name_temp = ''
    belonger_list = []
    for key, value in candidates_weight_dictionary.items():
        get_face_weight = float(value)
        if get_face_weight > get_face_weight_temp:
            get_face_weight_temp = get_face_weight
            get_face_name_temp = key
            belonger_list = []  # 让list重新初始化
            belonger_list.append(get_face_name_temp)
        elif get_face_weight == get_face_weight_temp:
            belonger_list.append(key)

    return belonger_list, get_face_weight_temp, get_face_name_temp


def record_Belongername_WeightDictionary(belonger_list, summarize_belonger_sub_name_list, get_face_weight_temp,
                                         candidates_weight_dictionary, new_json_filepath):
    data = {}
    data = candidates_weight_dictionary
    data["Belonger"] = belonger_list
    data["Belonger_sub_face_name"] = summarize_belonger_sub_name_list
    a = json.dumps(data)
    b = str(a + '\n')
    f1 = open(new_json_filepath, mode='w')
    f1.write(b)


def get_TheMaxSideScore_CandidateSubJpg_Name(belonger_list, candidates_names_face_side_score_list):
    summarize_belonger_sub_name_list = []
    for i in range(0, len(belonger_list)):
        list1 = candidates_names_face_side_score_list[belonger_list[i]]
        belonger_sub_face_name = list1[0]
        belonger_sub_face_side_rate = list1[1]
        summarize_belonger_sub_name_list.append(belonger_sub_face_name)
    return summarize_belonger_sub_name_list


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
    return path  # 这个path就是要读的JPG的完整路径


"""
get_Pic_id(rline)
~~~~~~~~~~~~~~~~~
Discription for Function:
    作用：返回pic_id，pic_id是该用户账号中该jpg文件的编号，如果出现异常，则pic_id = 0。
"""


def get_Pic_id(rline):
    try:
        get_se_url = rline["se_get_large_url"]  # 注意：该path后面有斜杠

        str_divided1 = str(get_se_url).split("e/")
        str_divided2 = str(str_divided1[1]).split(".")
        pic_id = str_divided2[0]
        return pic_id  # 注意：它是没有“.jpg”后缀的
    except:
        pic_id = 0
        return pic_id


"""
create_CandidatesResults_JsonFile(paath, get_user_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Discription for Function:
    作用：创建一个Candidates文件来放置提取出来的用来代表某个特定的人的人脸,并创建一个放置新json文件的路径用来记录该账号的统计信息
Samples：
    path = {str}'D:\\用户的文件\\广东省\\广州市\\18811860\\18811860.json'
    user_id_json_name = '18811860.json'
    new_json_filename = '18811860_results.json'
    new_json_filepath = 'D:\\用户的文件\\广东省\\广州市\\18811860\\18811860_results.json'
    sub_spec_face_file_path = 'D:\\用户的文件\\广东省\\广州市\\18811860\\'
Discription:
    sub_spec_face_file_path = {str}: 作用：此字符串变量用于储存一条未完成构造的路径，该路径的完整路径的作用是：将该账号照片中出现过的每个人的所有脸，都储存在代表这个人的那个文件夹里
"""


def create_CandidatesResults_JsonFile(path, get_user_id):
    user_id_json_name = str(get_user_id) + ".json"

    new_json_filename = str(get_user_id) + "_results" + ".json"
    new_json_file_path = path.replace(user_id_json_name, new_json_filename)

    sub_spec_face_file_path = path.replace(user_id_json_name,
                                           "")  # 注意：这个path是用来准备之后构造从属于同一个人的脸的JPG文件夹的路径，其文件名将会是代表这个人的脸的JPG文件名

    return new_json_file_path, sub_spec_face_file_path


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


def read_JsonFiles(path, get_user_id):

    f1 = open(path, encoding='utf-8')
    # 候选人脸描述子list
    descriptors = []
    # 用来保存候选人即相对应的jpg文件名的list
    candidates_names = []
    # 先创建一个Dictionary记录每一个人的“代表脸”的权重总和
    candidates_weight_dictionary = {}
    # 初始化为一个字典，以pic_id为键值，键值映射的值为正脸率：即：后面的score，这是为了后面查询score然后进行正脸率的比较
    candidates_names_facesidescore_list = {}
    # 创建一个Candidates 文件来放置提取出来的人脸,并创建一个放置新json文件的路径用来记录该账号的统计信息
    new_json_filepath, sub_spec_face_file_path = create_CandidatesResults_JsonFile(path, get_user_id)

    for line in f1.readlines():

        # rline加载每一整条的JSON信息
        rline = json.loads(line)
        # 得到该pic_id
        pic_id = get_Pic_id(rline)  # 注意：它是没有“.jpg”后缀的

        if pic_id != 0:
            # 构造要读的jpg文件的完整路径：
            path_jpg = compose_ReadJPG_Path(path, get_user_id, pic_id)  # 这个path就是要读的JPG的完整路径

            # 现在开始检测并记录该图片中的人脸
            candidates_names, descriptors, candidates_weight_dictionary, candidates_names_face_side_score_list = extract_Face_InsideJPG(
                path_jpg, pic_id, descriptors, candidates_names, candidates_weight_dictionary, detector, sp, facerec,
                sub_spec_face_file_path, candidates_names_facesidescore_list)

    # 现在开始遍历字典从而获取权重最大的那张脸
    belonger_list, get_face_weight_temp, get_face_name_temp = get_TheBelonger_JPGname(candidates_weight_dictionary)
    # 现在开始遍历字典从而获取belonger的人脸中score(正脸率)最大的那张脸截图
    summarize_belonger_sub_name_list = get_TheMaxSideScore_CandidateSubJpg_Name(belonger_list,
                                                                                candidates_names_face_side_score_list)
    # 将得到的微博所有者人脸的JPG文件名和所有人脸的权重字典记录到Json文件
    record_Belongername_WeightDictionary(belonger_list, summarize_belonger_sub_name_list, get_face_weight_temp,
                                         candidates_weight_dictionary, new_json_filepath)
    # Test:
    #print("The weight list of face is :")
    #print(candidates_weight_dictionary)


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

    AccountFileNumber = 0  #To show the number the Account being read

    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:

            path_Divided = filepath.split('.')
            get_user_id = path_Divided[0]

            path = os.path.join(dirpath, filepath)
            path_Divided = str(path).split('.')
            # print(path_Divided)
            if path_Divided[1] == 'json':

                print(get_user_id)
                AccountFileNumber += 1;
                print("这是第 %i 个账号" % (AccountFileNumber))

                read_JsonFiles(path, get_user_id)


"""
prepare_detector
~~~~~~~~~~~~~~~~
This function is used to get all the detectors ready.
"""


def prepare_detector(predictor_path, face_rec_model_path):

    # 1、加载正脸检测器
    detector = dlib.get_frontal_face_detector()
    # 2、加载人脸关键点检测器
    sp = dlib.shape_predictor(predictor_path)
    # 3、加载人脸识别模型
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)

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

go_Through_PicsFile(province, city)
