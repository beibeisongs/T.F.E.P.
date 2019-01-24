# encoding=utf-8
# Date: 2019-01-24
# Author: MJUZY


import dlib
from FaceSizeComparasion import GetSelected
import json
import numpy as np
import os
from PIL import Image
from skimage import io


def save_Extraction_Face_JPG(img_path, left, top, right, bottom,
                             compose_sub_spec_face_jpg_path):
    img = Image.open(str(img_path))
    print("save_Extraction_Face_JPG Ok!")

    box = (left, top, right, bottom)
    roi = img.crop(box)

    roi.save(compose_sub_spec_face_jpg_path)


def start_Save_Extracted_JPG(face_number, pic_id, path_jpg, d, document_path):
    face_number += 1
    print("这是第 %d 张图片" % face_number)

    the_candidate_name = str(pic_id) + '_extraction_' + str(face_number)

    compose_sub_spec_face_jpg_path = document_path + "\\" + the_candidate_name + ".jpg"  # <Sample>: path = D:\\用户的文件\\广东省\\广州市\\18811860\\18811860\\....jpg

    left, right, top, bottom = d.left(), d.right(), d.top(), d.bottom()
    print("脸部坐标：（%d,%d）,(%d,%d)" % (left, top, right, bottom))

    save_Extraction_Face_JPG(img_path=path_jpg, left=left,
                             top=top, right=right, bottom=bottom,
                             compose_sub_spec_face_jpg_path=compose_sub_spec_face_jpg_path)

    return face_number


def extract_Face_InsideJPG(path_jpg, pic_id, detector, document_path, ):
    face_number = 0
    print("extract_Face_InsideJPG Ok!")

    try:
        img = io.imread(path_jpg)
        print("extract_Face_InsideJPG Ok!")

        dets = detector(img, 1)
        print("extract_Face_InsideJPG Ok!")

        faceSizeList = []

        for k, d in enumerate(dets):
            SIZE1 = (d.right() - d.left()) * (d.bottom() - d.top())
            faceSizeList.append(SIZE1)

        faceSizeList = GetSelected(faceSizeList)
        print("extract_Face_InsideJPG Ok!")

        num_of_faces = len(dets)
        print("extract_Face_InsideJPG Ok!")

        if num_of_faces > 0:

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
    if not judgeExisting:
        os.makedirs(path)

    print("createFacesDocument Ok!")

    return path


def compose_ReadJPG_Path(path, get_user_id, pic_id):
    get_user_id = str(get_user_id) + ".json"
    pic_JPG_filename = str(pic_id) + ".jpg"

    path = path.replace(get_user_id, pic_JPG_filename)
    print("compose_ReadJPG_Path Ok!")

    return path


def get_Pic_id(rline, UMARK, line_i):
    try:
        get_se_url = rline["se_get_large_url"]
        print("get_Pic_id Ok!")

        if line_i != 1:
            if get_se_url != UMARK:
                str_divided1 = str(get_se_url).split("e/")
                str_divided2 = str(str_divided1[1]).split(".")
                pic_id = str_divided2[0]

                return pic_id
            else:
                return "E"
        else:
            str_divided1 = str(get_se_url).split("e/")
            str_divided2 = str(str_divided1[1]).split(".")
            pic_id = str_divided2[0]

            return pic_id
    except:
        pic_id = "F"

        return pic_id


def avoid_Repeated_JSON(path, get_user_id, dirpath):
    f1 = open(path, encoding='utf-8')
    try:
        rline = json.loads(f1.readline())

        UMARK = rline["se_get_large_url"]

        print("avoid_Repeated_JSON Ok!")

        return UMARK
    except:
        UMARK = 'E'

        """
        To show the Error ! 
        """
        print("Unicode Error ! ")
        print()
        print()
        print()

        if os.path.exists(dirpath + "\\" + "UnicodeError") is False:
            os.mkdir(dirpath + "\\" + "UnicodeError")

        return UMARK


def read_JsonFiles(path, get_user_id, dirpath):
    UMARK = avoid_Repeated_JSON(path, get_user_id, dirpath)
    if UMARK == 'E':
        return

    f1 = open(path, encoding='utf-8')
    print("read_JsonFiles Ok!")

    document_path = createFacesDocument(path, get_user_id)
    print("read_JsonFiles Ok!")

    line_i = 0

    for line in f1.readlines():

        line_i += 1

        try:
            rline = json.loads(line)
        except:
            """
                    To show the Error ! 
                    """
            print("Unicode Error ! ")
            print()
            print()
            print()

            if os.path.exists(dirpath + "\\" + "UnicodeError") is False:
                os.mkdir(dirpath + "\\" + "UnicodeError")
            break

        pic_id = get_Pic_id(rline, UMARK, line_i)  # 注意：它是没有“.jpg”后缀的
        print("read_JsonFiles Ok!")

        if pic_id != "F":
            path_jpg = compose_ReadJPG_Path(path, get_user_id, pic_id)  # 这个path就是要读的JPG的完整路径
            print("read_JsonFiles Ok!")

            extract_Face_InsideJPG(path_jpg, pic_id, detector, document_path)
            print("read_JsonFiles Ok!")

        if pic_id == "E":
            break

    dirpath = dirpath + "\\" + "Ext_Step_Ok"

    if not os.path.exists(dirpath):

        os.makedirs(dirpath)
    else:
        print("Already Existing Ext_Step_Ok ! ")


# =====================================================================================================================!


def compose_Data_toWrite(Max_Number, desc_link_jpgname, total_list, sum_SubFaceNames):
    data = {}

    if not total_list:
        data["Attention"] = "No Face !"
    else:
        # <Sample>:
        #   "3b9adb14jw1ekd7mc8oe0j20f00qoaar_extraction_1": 7.0
        data[desc_link_jpgname[Max_Number]] = total_list[Max_Number]

        # <Sample>:
        #   "Belonger": "3b9adb14jw1ekd7mc8oe0j20f00qoaar_extraction_1"
        data["Belonger"] = desc_link_jpgname[Max_Number]

        data["Belonger_sub_face_name"] = sum_SubFaceNames[Max_Number]

    return data


def write_ResultJson(Max_Number, desc_link_jpgname, document_path, total_list, sum_SubFaceNames, dirpath, get_user_id):
    data = compose_Data_toWrite(Max_Number, desc_link_jpgname, total_list, sum_SubFaceNames)

    try:
        f1 = open(document_path + "\\" + "Results.json", mode='w')
        print("Opening JSON ! ")
    except:
        # 提前结束该账号的进程
        print("Find Error ! ")

        dirpath = dirpath + "\\" + get_user_id + "\\" + "Error Mark"

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        return

    a = json.dumps(data)
    b = str(a + '\n')

    print("Writing JSON ! ")
    f1.write(b)

    print("Finish writing JSON ! ")


def getMaxTot(total_list):
    # 点明这个Maz_Number 是这个define中的
    Max_Number_def = 0

    temp = 0
    for i in range(0, len(total_list)):

        if total_list[i] > temp:
            Max_Number_def = i
            temp = total_list[i]

    # 返回的值为total_list中最大值的下标
    return Max_Number_def


def Construct_Candidates_List(filenames, document_path):
    # descriptor这个列表每个元素一次储存每个人脸的特征矩阵
    #   后面计算欧式距离时会用到
    descriptors = []

    # 记录对应的人脸特征矩阵的所属JPG文件名
    desc_link_jpgname = []

    for i in range(0, len(filenames)):

        path_jpg = document_path + "\\" + filenames[i]

        try:
            img = io.imread(path_jpg)

            # 人脸检测
            #   因为都是已经截好的图片，所以人脸数量必然是一
            dets = detector(img, 1)

            for k, d in enumerate(dets):
                # 关键点检测
                shape = sp(img, d)

                # 描述子提取，128D向量
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                print("face_descriptor : Ok ! ")

                # 转换成numpy，array
                d_test = np.array(face_descriptor)

                # descriptor这个列表每个元素一次储存每个人脸的特征矩阵，后面计算欧式距离时会用到
                descriptors.append(d_test)

                # 记录对应的人脸特征矩阵的所属JPG文件名
                # <Attention>
                #   每个元素是字符串
                #       <Sample>: 762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2.jpg
                desc_link_jpgname.append(filenames[i])

        except:
            # <Description>
            #   有可能出现图片加载不了的错误
            print("Not able to Load ! ")

    return descriptors, desc_link_jpgname


def analysor(document_path, get_user_id):
    for dirpath, dirnames, filenames in os.walk(document_path):

        # 先把filenames中的所有截出来的人脸当成候选人脸构成一个列表
        print("Start Constructing A Condidates List ! ")

        descriptors, desc_link_jpgname = Construct_Candidates_List(filenames, document_path)

        # 用来储存每一张脸撞脸的总次数
        total_list = []

        # 将每一张脸的Sub Faces集合为一个List
        sum_SubFaceNames = []

        # 该变量指代现在遍历到的人脸在desc_link_jpgname这个list中的下标
        face_i = -1

        for filepath in desc_link_jpgname:

            # 用来记录与该脸为同一张脸的对应的JPG Name
            #   <Sample>: 762f6b2djw1ei0kepm85pj20hs0vkdir_extraction_2
            subFaceNames = []

            face_i += 1

            print("Enter Faces Document ! ")
            print(filepath)

            path_jpg = dirpath + "\\" + filepath

            get_picID_stp1 = filepath.split("_e")

            # <Sample>: pic_id = 762f6b2djw1ei0kepm85pj20hs0vkdir
            pic_id = get_picID_stp1[0]

            # 现在开始统计每张脸在这个账号中出现的次数
            i = -1

            tot = 0

            for des_i in descriptors:  # <Description>: des_i是每个人脸的特征矩阵

                i += 1

                # 出自同一只照片的人脸会被跳过，不进行欧式距离的比较，因为同一个照片的人脸不可能是同一个人
                #   <Attention>: desc_link_jpgname[i]是对应des_i这个特征矩阵所指代的人脸
                #       返回值为-1，说明不是出自同一张照片

                if desc_link_jpgname[i].find(pic_id) == -1:

                    # 下面计算欧式距离
                    dist_ = np.linalg.norm(des_i - descriptors[face_i])  # <Description>: des_i 是每一个候选人的人脸特征矩阵

                    # 统计撞脸次数被储存到total_list 列表中
                    #   一般欧氏距离小于0.384就可以认为是同一张脸了，值越小说明是同一张脸的可能性越大
                    if dist_ < 0.384:
                        tot += 1
                        print("tot + 1 ! ")

                        subFaceNames.append(desc_link_jpgname[i])

            # <Attention>
            #   注意！有可能出现total_list是[]的情况
            total_list.append(tot)

            sum_SubFaceNames.append(subFaceNames)

        print("total_list : ", total_list)

        # 返回的值为total_list中最大值的下标
        Max_Number = getMaxTot(total_list)

        write_ResultJson(Max_Number, desc_link_jpgname, document_path, total_list, sum_SubFaceNames, dirpath,
                         get_user_id)


# =====================================================================================================================!


def Find_Owner_Process(document_path, get_user_id):
    analysor(document_path, get_user_id)


def ifFinishExtractFace(get_user_id, dirpath):
    Ext_Step_Ok_Path = dirpath + "\\" + get_user_id + "\\" + "Ext_Step_Ok"

    if not os.path.exists(Ext_Step_Ok_Path):
        return False
    else:
        return True


def if_Results_Json_Exists(get_user_id, dirpath):
    Results_Json_Path = dirpath + "\\" + get_user_id + "\\" + get_user_id + "\\" + "Results.json"

    if not os.path.exists(Results_Json_Path):
        return False
    else:
        return True


def Having_Unicode_Error(get_user_id, dirpath):
    Unicode_Error_File_Path = dirpath + "\\" + get_user_id + "\\" + "UnicodeError"

    if os.path.exists(Unicode_Error_File_Path):
        return True
    else:
        return False


def go_Through_PicsFile():
    path = dir_disk + ":\\用户的文件\\" + str(province) + "\\" + str(city)

    for dirpath, dirnames, filenames in os.walk(path):

        AccountFileNumber = start_pt

        while AccountFileNumber <= end_pt:
            """
            To show the uid ! 
            """
            get_user_id = dirnames[AccountFileNumber]

            print("UID : ", get_user_id)
            print("Index : ", AccountFileNumber)
            print()
            print()
            print()

            if not Having_Unicode_Error(get_user_id, dirpath):

                Finish_Extract_Flag = False

                if not ifFinishExtractFace(get_user_id, dirpath):
                    try:
                        read_JsonFiles(dirpath + "\\" + get_user_id + "\\" + get_user_id + ".json",
                                       get_user_id,
                                       dirpath + "\\" + get_user_id)

                        Finish_Extract_Flag = True

                    except UnicodeDecodeError:
                        """
                        To show the Error ! 
                        """
                        print("Unicode Error ! ")
                        print()
                        print()
                        print()

                        if os.path.exists(dirpath + "\\" + get_user_id + "\\" + "UnicodeError") is False:
                            os.mkdir(dirpath + "\\" + get_user_id + "\\" + "UnicodeError")
                else:
                    Finish_Extract_Flag = True

                if Finish_Extract_Flag:
                    if not if_Results_Json_Exists(get_user_id, dirpath):

                        Find_Owner_Process(dirpath + "\\" + get_user_id + "\\" + get_user_id,
                                           get_user_id)

            AccountFileNumber += 1

        break


def prepare_detector(predictor_path, face_rec_model_path):
    detector = dlib.get_frontal_face_detector()
    print("prepare_detector Ok!")

    sp = dlib.shape_predictor(predictor_path)
    print("prepare_detector Ok!")

    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    print("prepare_detector Ok!")

    return detector, sp, facerec


def prepare_path_etc():
    predictor_path = "D:/USBei Documents/Dlib_Data/shape_predictor_68_face_landmarks.dat"

    face_rec_model_path = "D:/USBei Documents/Dlib_Data/dlib_face_recognition_resnet_model_v1.dat"

    return predictor_path, face_rec_model_path


if __name__ == "__main__":
    predictor_path, face_rec_model_path = prepare_path_etc()

    detector, sp, facerec = prepare_detector(predictor_path, face_rec_model_path)

    dir_disk = "E"

    province = "上海市"
    city = "上海市"

    start_pt = 0
    end_pt = 3

    go_Through_PicsFile()
