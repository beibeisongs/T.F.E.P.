# encoding=utf-8
# Author: MJUZY
# Date: 2018-7-22
# Description: Used to Recovery the Faces Scoring Process


import os


def go_Through_Files(path):

    AccountFileNumber = 0  # To show the number of the Account being read

    for dirpath, dirnames, filenames in os.walk(path):  # <Sample>: dirpath = 'C:\\用户的文件\\浙江省\\杭州市\\1000637114'
        for filepath in filenames:  # <Sample>: filepath = '1000637114.json'

            path_Divided = dirpath.split('\\')
            get_user_id = path_Divided[4]

            path = os.path.join(dirpath, filepath)
            path_Divided = str(path).split('.')

            if (filepath == get_user_id + ".json"):

                print("账号：", get_user_id)

                AccountFileNumber += 1
                print("这是第 %i 个账号" % (AccountFileNumber))

                if (AccountFileNumber >= start_pt) and (AccountFileNumber <= end_pt):

                    if (os.path.exists(dirpath + "\\" + get_user_id + "\\" + "Face_Scores.json")):
                        print("Face_Scores.json Existing ! ")
                    else:
                        print("No Existing ! ")

                break


print("请输入要处理的文件所属省份：")

# province = input()
province = "湖北省"

print("请输入要处理的文件所属城市：")

# city = input()
city = "武汉市"

start_pt = 58000
end_pt = 130000

print("Ready to go ! ")

path = "G:\\用户的文件\\" + str(province) + "\\" + str(city)


if __name__ == "__main__":

    go_Through_Files(path)
