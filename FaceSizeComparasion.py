# encoding = utf-8
# Author: MUJZY
# Date: 2018-01-16
# Function: To choose the Face(s) to Analyse by size comparasion, return a list show which Face having been chosen


def GetSelected(list):

    n = len(list)

    MAX = 0

    for i in range(0, n):

        if list[i] > MAX:
            MAX = list[i]

    for i in range(0, n):

        if MAX / list[i] > 4:   # <Description>: 与最大的那个差距太大，因此定性为噪声
            list[i] = 0 # <Description>: 即最后不是0的那些元素所对应的对象就是被选中的

    return list