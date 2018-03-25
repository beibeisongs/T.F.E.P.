#!/usr/bin/env python
# encoding = utf-8
# Author: MUJZY
# Date: 2018-03-19


import os


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


def go_Through_PicsFile(province, city, start_pt):

    path = "E:\\用户的文件\\" + str(province) + "\\" + str(city)

    AccountFileNumber = 0  # To show the number the Account being read

    for dirpath, dirnames, filenames in os.walk(path):

            for filepath in filenames:

                get_user_id = dirpath.replace(path + "\\", "")  # <Sample>: '18811860'

                if filepath == get_user_id + ".json":   # <sample>: 18811860.json

                    if os.path.exists(dirpath + "\\" + get_user_id + "_results.json") == True:

                        AccountFileNumber += 1;
                        print("这是第 %d 个 账号" % AccountFileNumber)
                        print(get_user_id)
                        print()
                        break

                    elif os.path.exists(dirpath + "\\" + get_user_id + "_results.json") == False:
                        print("No _Results.json File ! ")


print("请输入要处理的文件所属省份：")

# province = input()
province = "湖北省"

print("请输入要处理的文件所属城市：")

# city = input()
city = "武汉市"

print("请输入选择处理的账号起点序号")
# start_pt = input()
start_pt = 30760

print("Ready to go ! ")

go_Through_PicsFile(province, city, start_pt)