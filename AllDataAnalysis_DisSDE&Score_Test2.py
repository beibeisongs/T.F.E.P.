# encoding=utf-8
# Date: 2018-7-30
# Author: MJUZY


import random
import math
import csv
import json
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt


def GetRandom400(dis_40up_50dn_vice, score_40up_50dn_vice, n):
    dis_40up_50dn_vice2 = []
    score_40up_50dn_vice2= []
    for i in range(n):
        dis_40up_50dn_vice2.append(random.choice(dis_40up_50dn_vice))
        score_40up_50dn_vice2.append(random.choice(score_40up_50dn_vice))

    return dis_40up_50dn_vice2, score_40up_50dn_vice2


def combineVices(dis_40up_60dn_vice, score_40up_60dn_vice, dis_60up_70dn_vice, score_60up_70dn_vice, dis_70up_90dn_vice, score_70up_90dn_vice):
    distances_vice = []
    scores_vice = []

    for i in range(len(dis_40up_60dn_vice)):
        distances_vice.append(dis_40up_60dn_vice[i])
        scores_vice.append(score_40up_60dn_vice[i])

    for i in range(len(dis_60up_70dn_vice)):
        distances_vice.append(dis_60up_70dn_vice[i])
        scores_vice.append(score_60up_70dn_vice[i])

    for i in range(len(dis_70up_90dn_vice)):
        distances_vice.append(dis_70up_90dn_vice[i])
        scores_vice.append(score_70up_90dn_vice[i])

    return distances_vice, scores_vice


def DigOutPoints(points_40up_50dn_tuples, points_avg_40up_50dn, errorDigPer):

    dis_40up_50dn_vice = []
    score_40up_50dn_vice = []

    dtype = [('dis', float), ('score', float), ('dis2avg', float)]

    DigRank = int(len(points_40up_50dn_tuples) * errorDigPer)
    print(len(points_40up_50dn_tuples), "--original length")
    print(DigRank, "--DigRank")

    print(points_avg_40up_50dn, "--avg_Dist")

    points_40up_50dn_NewTuples = []
    for i in range(len(points_40up_50dn_tuples)):
        points_40up_50dn_NewTuples.append((points_40up_50dn_tuples[i][0], points_40up_50dn_tuples[i][1], (points_40up_50dn_tuples[i][0] - points_avg_40up_50dn)**2))
    pointsSort = np.array(points_40up_50dn_NewTuples, dtype)
    pointsSort = np.sort(pointsSort, order='dis2avg')
    print(pointsSort, '--pointSort')

    for i in range(len(pointsSort) - DigRank):
        dis_40up_50dn_vice.append(pointsSort[i][0])
        score_40up_50dn_vice.append(pointsSort[i][1])

    for i in range(len(dis_40up_50dn_vice)):
        print(dis_40up_50dn_vice[i])
    print('--after_dist')

    return dis_40up_50dn_vice, score_40up_50dn_vice


def DisScores_KMeans(distances_record, scores_record, errorDigPer, n):

    points_total = 0

    points_40up_60dn_tuples = []
    points_40up_60dn = 0
    points_dissum_40up_60dn = 0

    points_60up_70dn_tuples = []
    points_60up_70dn = 0
    points_dissum_60up_70dn = 0

    points_70up_90dn_tuples = []
    points_70up_90dn = 0
    points_dissum_70up_90dn = 0

    for i in range(len(distances_record)):

        if (distances_record[i] > 0) and scores_record[i] >= 40:

            if (scores_record[i] >= 40) and (scores_record[i] < 60):
                points_40up_60dn += 1
                points_dissum_40up_60dn += distances_record[i]
                points_40up_60dn_tuples.append((distances_record[i], scores_record[i]))

            if (scores_record[i] >= 60) and (scores_record[i] < 70):
                points_60up_70dn += 1
                points_dissum_60up_70dn += distances_record[i]
                points_60up_70dn_tuples.append((distances_record[i], scores_record[i]))

            if (scores_record[i] >= 70) and (scores_record[i] < 90):
                points_70up_90dn += 1
                points_dissum_70up_90dn += distances_record[i]
                points_70up_90dn_tuples.append((distances_record[i], scores_record[i]))

            points_total += 1

    # points_avg_40up_60dn = points_dissum_40up_60dn / points_40up_60dn
    points_avg_40up_60dn = points_dissum_40up_60dn / n
    dis_40up_60dn_vice, score_40up_60dn_vice = DigOutPoints(points_40up_60dn_tuples, points_avg_40up_60dn, errorDigPer)
    dis_40up_60dn_vice, score_40up_60dn_vice = GetRandom400(dis_40up_60dn_vice, score_40up_60dn_vice, n)

    # points_avg_60up_70dn = points_dissum_60up_70dn / points_60up_70dn
    points_avg_60up_70dn = points_dissum_60up_70dn / n
    dis_60up_70dn_vice, score_60up_70dn_vice = DigOutPoints(points_60up_70dn_tuples, points_avg_60up_70dn, errorDigPer)
    dis_60up_70dn_vice, score_60up_70dn_vice = GetRandom400(dis_60up_70dn_vice, score_60up_70dn_vice, n)

    # points_avg_70up_90dn = points_dissum_70up_90dn / points_70up_90dn
    points_avg_70up_90dn = points_dissum_70up_90dn / n
    dis_70up_90dn_vice, score_70up_90dn_vice = DigOutPoints(points_70up_90dn_tuples, points_avg_70up_90dn, errorDigPer)
    dis_70up_90dn_vice, score_70up_90dn_vice = GetRandom400(dis_70up_90dn_vice, score_70up_90dn_vice, n)


    distances_vice, scores_vice = combineVices(dis_40up_60dn_vice, score_40up_60dn_vice, dis_60up_70dn_vice, score_60up_70dn_vice, dis_70up_90dn_vice, score_70up_90dn_vice)
    x1 = np.array(distances_vice)
    x2 = np.array(scores_vice)
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b']
    markers = ['o', 's', 'D', 'v', '^', 'p', '*', '+']

    # tests = [1, 2, 3]
    tests = [1]

    for t in tests:

        kmeans_model = KMeans(n_clusters=t).fit(X)

        for i, l in enumerate(kmeans_model.labels_):
            plt.plot(x1[i], x2[i], color=colors[l], markersize=3, marker=markers[l],alpha=0.5)

        print("Total points : ", points_total)
        print("Total points_70up_80dn : ", n, "Average : ", points_dissum_70up_90dn)
        print("Total points_60up_70dn : ", n, "Average : ", points_dissum_60up_70dn)
        print("Total points_50up_60dn : ", n, "Average : ", points_dissum_40up_60dn)

        plt.show()


def getDate(item_time):

    divided = item_time.split(' ')
    month = divided[1]
    day = divided[2]
    year = divided[5]

    return day, month, year


def getElements(item2):

    userid = item2[0]
    # idstr = item2[1]

    # day, month, year = getDate(item2[2])

    # title = item2[4]

    lon = float(item2[5])
    lat = float(item2[6])

    # gender = item2[7]
    # if gender == "Female": gender = 'f'
    # elif gender == "Male": gender = 'm'

    # text = item2[8]

    # street_address = item2[9]

    # age = item2[10]

    female_score = item2[11]
    male_score = item2[12]
    score = (float(female_score) + float(male_score)) / 2

    return score, lon, lat, userid


def GetDist(lon_temp_ZP, lon_temp_P2_ZP, lon_temp_P3, lat_temp_ZP, lat_temp_P2_ZP, lat_temp_P3, lon_ZP, lon_P2_ZP, lon_P3, lat_ZP, lat_P2_ZP, lat_P3):

    # The Company used below is "KiloMeter"
    dist_P1_lon_sq = ((lon_temp_ZP - lon_ZP) * 111)**2
    dist_P2_lon_sq = ((lon_temp_P2_ZP - lon_P2_ZP) * 1.85)**2
    dist_P3_lon_sq = ((lon_temp_P3 - lon_P3) * 0.0309)**2

    dist_P1_lat_sq = ((lat_temp_ZP - lat_ZP) * 111) ** 2
    dist_P2_lat_sq = ((lat_temp_P2_ZP - lat_P2_ZP) * 1.85) ** 2
    dist_P3_lat_sq = ((lat_temp_P3 - lat_P3) * 0.0309) ** 2

    dis_sum = math.sqrt(dist_P1_lon_sq + dist_P2_lon_sq + dist_P3_lon_sq) * math.sqrt(dist_P1_lat_sq + dist_P2_lat_sq + dist_P3_lat_sq)
    SDE_Sqare = math.pi * dis_sum * 4

    return SDE_Sqare


def Transfer2TimeType(lon_temp, lat_temp):

    # Part1 Used
    lon_temp_ZP = int(lon_temp) # Get The Main Number Part
    lat_temp_ZP = int(lat_temp) # Get The Main Number Part

    lon_temp_minP = (lon_temp - lon_temp_ZP) * 60
    lat_temp_minP = (lat_temp - lat_temp_ZP) * 60

    # Big letter 'P' refers to the Word "Part"
    # Part2 Used
    lon_P2_ZP = int(lon_temp_minP)
    lat_P2_ZP = int(lat_temp_minP)

    lon_P2_minP = lon_temp_minP - lon_P2_ZP
    lat_P2_minP = lat_temp_minP - lat_P2_ZP

    # Part3 Used
    lon_P3 = lon_P2_minP * 60
    lat_P3 = lat_P2_minP * 60

    return lon_temp_ZP, lon_P2_ZP, lon_P3, lat_temp_ZP, lat_P2_ZP, lat_P3


def goThroughCSV(csv_name, errorDigPer, n):

    userid_temp = ""

    SDE_XY_SUM_Records = [] # Use the Sum of the SDEx and the SDEy of the users for one dimendsion
    # distances_record = []
    lon_temp = 0
    lat_temp = 0
    point_num = 0
    sde_x_sum_sq = 0
    sde_y_sum_sq = 0
    sde_Xi_records = []
    sde_Yi_records = []

    scores_record = []

    users_num_passed = 0

    line_i = 0
    with open(csv_name, "r") as csvfile:
        reader2 = csv.reader(csvfile)  # 读取csv文件，返回的是迭代类型
        for item2 in reader2:
            line_i += 1
            # print("现在的行数是：", line_i)

            if (line_i >= start_pt) and (line_i <= end_pt):

                score, lon, lat, userid = getElements(item2)
                if line_i == 1:
                    userid_temp = userid

                    SDE_XY_SUM_Records.append(0)

                    # distances_record.append(0)
                    lon_temp = lon
                    lat_temp = lat
                    users_num_passed += 1
                    point_num += 1
                    sde_Xi_records.append(0)
                    sde_Yi_records.append(0)
                    sde_Xi_records[point_num - 1] = lon
                    sde_Yi_records[point_num - 1] = lat

                    scores_record.append(0)
                    scores_record[users_num_passed - 1] = score

                elif userid == userid_temp:

                    # lon_temp_ZP, lon_temp_P2_ZP, lon_temp_P3, lat_temp_ZP, lat_temp_P2_ZP, lat_temp_P3 = Transfer2TimeType(lon_temp, lat_temp)
                    # lon_ZP, lon_P2_ZP, lon_P3, lat_ZP, lat_P2_ZP, lat_P3 = Transfer2TimeType(lon, lat)

                    # distances_record[users_num_passed - 1] += GetDist(lon_temp_ZP, lon_temp_P2_ZP, lon_temp_P3, lat_temp_ZP, lat_temp_P2_ZP, lat_temp_P3, lon_ZP, lon_P2_ZP, lon_P3, lat_ZP, lat_P2_ZP, lat_P3)

                    point_num += 1
                    sde_Xi_records.append(lon)
                    sde_Yi_records.append(lat)

                elif userid_temp != userid:

                    # distances_record[users_num_passed - 1] /= point_num

                    sde_Xi_sum = 0
                    sde_Yi_sum = 0
                    for i in range(point_num):
                        sde_Xi_sum += sde_Xi_records[i]
                        sde_Yi_sum += sde_Yi_records[i]
                    sde_Xi_av = sde_Xi_sum / point_num
                    sde_Yi_av = sde_Yi_sum / point_num

                    sde_X_dis_sum_sq = 0
                    sde_Y_dis_sum_sq = 0
                    for i in range(point_num):
                        sde_X_dis_sum_sq += (sde_Xi_records[i] - sde_Xi_av)**2
                        sde_Y_dis_sum_sq += (sde_Yi_records[i] - sde_Yi_av)**2

                    sde_X_dis_sum_sq_av = sde_X_dis_sum_sq / point_num
                    sde_Y_dis_sum_sq_av = sde_Y_dis_sum_sq / point_num

                    lon_temp_ZP, lon_temp_P2_ZP, lon_temp_P3, lat_temp_ZP, lat_temp_P2_ZP, lat_temp_P3 = Transfer2TimeType(sde_X_dis_sum_sq_av, sde_Y_dis_sum_sq_av)
                    SDE_X_Y_SUM = GetDist(lon_temp_ZP, lon_temp_P2_ZP, lon_temp_P3, lat_temp_ZP, lat_temp_P2_ZP, lat_temp_P3, 0, 0, 0, 0, 0, 0)
                    SDE_XY_SUM_Records[users_num_passed - 1] = SDE_X_Y_SUM

                    # a = distances_record[users_num_passed - 1]
                    # a = math.sqrt(a)
                    # distances_record[users_num_passed - 1] = a
                    # -------------------------------------------------
                    point_num = 0

                    sde_Xi_records = []
                    sde_Yi_records = []

                    userid_temp = userid
                    # distances_record.append(0)
                    lon_temp = lon
                    lat_temp = lat
                    SDE_XY_SUM_Records.append(0)

                    users_num_passed += 1
                    point_num += 1

                    sde_Xi_records.append(0)
                    sde_Yi_records.append(0)
                    sde_Xi_records[point_num - 1] = lon
                    sde_Yi_records[point_num - 1] = lat

                    scores_record.append(0)
                    scores_record[users_num_passed - 1] = score

            elif (line_i > end_pt):
                break
    """
    print(distances_record)
    print(len(distances_record))
    print(scores_record)
    print(len(scores_record))
    """

    csvfile.close()

    DisScores_KMeans(SDE_XY_SUM_Records, scores_record, errorDigPer, n)


if __name__ == "__main__":

    # b = [12, 22, 27, 33, 40, 50, 63, 88]
    b = [16, 22, 27, 33, 40, 50, 63, 88]

    start_pt = 0
    end_pt = 200000

    n = 500

    errorDigPer = 0

    csv_name = "16_22_CompensateLonLat.csv"
    goThroughCSV(csv_name, errorDigPer, n)
