#!/usr/bin/python
# -*- coding: latin-1 -*-
# Author: MUJZY
# Date: 2018-01-16
# Function: Resize the JPG File & Calculate the Size of the JPG File


import os
import os.path

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PIL import Image


"""
Description:
    filein: 输入图片
    fileout: 输出图片
    width: 输出图片宽度
    height: 输出图片高度
    type: 输出图片类型（png, gif, jpeg...）（默认为原文件的extension）
"""


def ResizeImage(filein, fileout, width, height):

    image = Image.open(filein)
    out = image.resize((width, height), Image.ANTIALIAS)    # Resize the JPG with High-Quality
    out.save(fileout)

def Calculate_JPGsize(filein):

    img = Image.open(filein)

    return img.size