# encoding=utf-8
# Date: 2018-8
# Author: MJUZY


import csv
import matplotlib.pyplot as plt
import numpy as np


def goThroughGaps(boundary, list_16_22, list_16_22_total, list_16_22_ROG, based_gap):
    n_gap = 0
    element_i = 0
    mark = True

    length = len(list_16_22)

    gap_value = based_gap + boundary * n_gap

    list_16_22_total.append(0)
    list_16_22_ROG.append(0)

    while mark:

        if (list_16_22[element_i] <= gap_value):
            list_16_22_total[n_gap] += 1
            element_i += 1

            if element_i == length:
                list_16_22_ROG[n_gap] = gap_value

                mark = False
                return list_16_22_total, list_16_22_ROG

        else:
            list_16_22_ROG[n_gap] = gap_value
            list_16_22_ROG.append(0)

            n_gap += 1

            list_16_22_total.append(0)
            list_16_22_total[n_gap] = list_16_22_total[n_gap - 1]

            gap_value = gap_value + boundary


def GetElements(item2):
    # id = item2[0]
    # gender = item2[1]
    age = float(item2[2])
    # score = (float(item2[3]) + float(item2[4])) / 2
    ROG = float(item2[8])

    return age, ROG


def readCSV(boundary, csv_name, based_gap):
    line_i = 0
    age_list = []
    ROG_list = []

    list_16_22 = []
    list_16_22_total = []
    list_16_22_ROG = []

    list_22_27 = []
    list_22_27_total = []
    list_22_27_ROG = []

    list_27_33 = []
    list_27_33_total = []
    list_27_33_ROG = []

    list_33_40 = []
    list_33_40_total = []
    list_33_40_ROG = []

    gap = boundary * 1  # Initialize the gap

    with open(csv_name, "r") as csvfile:
        reader2 = csv.reader(csvfile)
        for item2 in reader2:
            line_i += 1
            # print("现在的行数是：", line_i)
            if line_i >= 2:

                age, ROG = GetElements(item2)
                age_list.append(age)
                ROG_list.append(ROG)
        dtype = [('age', float), ('ROG', float)]

        NewTuples = []
        for i in range(len(age_list)):
            NewTuples.append((age_list[i], ROG_list[i]))
        pointsSort = np.array(NewTuples, dtype)
        pointsSort = np.sort(pointsSort, order='ROG')
        # print(pointsSort, '--pointSort')
        # False means it has not been checked
        # True means it has been involved into the Total
        for i in range(len(pointsSort)):
            if (pointsSort[i][0] >= 16) and ( pointsSort[i][0] < 22):
                list_16_22.append(pointsSort[i][1])
            if (pointsSort[i][0] >= 22) and ( pointsSort[i][0] < 27):
                list_22_27.append(pointsSort[i][1])
            if (pointsSort[i][0] >= 27) and ( pointsSort[i][0] < 33):
                list_27_33.append(pointsSort[i][1])
            if (pointsSort[i][0] >= 33) and ( pointsSort[i][0] <= 40):
                list_33_40.append(pointsSort[i][1])

        list_16_22_total, list_16_22_ROG = goThroughGaps(boundary, list_16_22, list_16_22_total, list_16_22_ROG, based_gap)
        for i in range(len(list_16_22_ROG)):
            print(list_16_22_ROG[i], list_16_22_total[i])

        plt.scatter(list_16_22_ROG, list_16_22_total, cmap=plt.cm.Blues, s=0.5)
        plt.title("16_22 ROG-People Total", fontsize=24)

        plt.xlabel("ROG", fontsize=12)
        plt.ylabel("Num", fontsize=12)

        # plt.tick_params(axis='both', labelsize=14)

        # plt.axis([0, 1100, 0, 1100000])

        # plt.savefig('D:\\实验室项目资料\\T.F.E.P.源码\\HelpDrawing\\figure.png', bbox_inches='tight')

        plt.show()

        """
        list_22_27_total, list_22_27_ROG = goThroughGaps(boundary, list_22_27, list_22_27_total, list_22_27_ROG, based_gap)

        list_27_33_total, list_27_33_ROG = goThroughGaps(boundary, list_27_33, list_27_33_total, list_27_33_ROG, based_gap)

        list_33_40_total, list_33_40_ROG = goThroughGaps(boundary, list_33_40, list_33_40_total, list_33_40_ROG, based_gap)
        """


if __name__ == "__main__":

    csv_name = "After_add_ROG.csv"

    based_gap = 8 * 1e-5
    boundary = 0.00001

    readCSV(boundary, csv_name, based_gap)
