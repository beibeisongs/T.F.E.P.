# encoding=utf-8
# Date: 2018-11-13
# Author: MJUZY


import json
from keras.preprocessing import image
from keras.models import load_model
import numpy as np
import os


def makeUpDetection(belonger_facepath, dirpath, get_user_id):
    img = image.load_img(belonger_facepath,
                         target_size=(224, 224))

    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)  # shape = <class 'tuple'>: (1, 224, 224, 3)
    img_tensor /= 255.

    result = model.predict(img_tensor)
    result_array0 = result[0]

    result_names = ["Original", "Made up"]

    if result_array0[0] >= result_array0[1]:
        answer = result_names[0]
    else:
        answer = result_names[1]

    f1 = open(dirpath + "\\" + "makeup_result.json", mode='w')
    data = {}
    data["makeup_result"] = answer

    a = json.dumps(data)
    b = str(a + '\n')
    f1.write(b)
    f1.close()

    return


def readResultJson(reJsonPath):
    try:
        f1 = open(reJsonPath, encoding="utf-8")
        for line in f1.readlines():
            rline = json.loads(line)
            belonger_jpgname = rline["Belonger"]
            return belonger_jpgname
    except:
        belonger_jpgname = 'z'
        return belonger_jpgname


def go_Through_PicsFile(province, city, path):

    AccountFileNumber = 0  # To show the number the Account being read
    for dirpath, dirnames, filenames in os.walk(path):

            path_Divided = dirpath.split('\\')
            if len(path_Divided) == 5:
                get_user_id = path_Divided[4]
                if AccountFileNumber >= start_pt:
                    if os.path.exists(dirpath + "\\" + get_user_id):
                        reJsonPath = dirpath + "\\" + get_user_id + "\\" + "Results.json"
                        if os.path.exists(reJsonPath):

                            belonger_jpgname = readResultJson(reJsonPath)
                            if belonger_jpgname != 'z':
                                belonger_facepath = dirpath + "\\" + get_user_id + "\\" + belonger_jpgname
                                makeUpDetection(belonger_facepath, dirpath, get_user_id)
                            else:
                                print("Info: No face ! ")
                else:
                    print("jump ! ")

                print("账号：", get_user_id)
                AccountFileNumber += 1
                print("这是第 %i 个账号\n" % (AccountFileNumber))


if __name__ == "__main__":
    model = load_model("D:/Py35_Pro_ifMakeup_Classification/VGG16FineTune_2_MakeupDetection.h5")
    model.summary()

    province = "湖北省"
    city = "武汉市"
    path = "F:\\用户的文件\\" + str(province) + "\\" + str(city)

    start_pt = 30759
    # start_pt = 1
    print("Info : Ready to go ! ")

    go_Through_PicsFile(province, city, path)
