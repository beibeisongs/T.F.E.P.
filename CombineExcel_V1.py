# encoding = utf-8
# Date: 2018-05-05
# Function: Export Faces Data to Excels


import os

import json
import xlrd
import xlwt
from  xlutils.copy import copy


def read_record_excel(start_line, excelname_read):

    xlfile = xlrd.open_workbook(excelname_read, 'r')
    sheet1 = xlfile.sheet_by_index(0)

    nrows = sheet1.nrows
    ncols = sheet1.ncols

    old_excel = xlrd.open_workbook(first_excel_name, formatting_info=True)

    # 将操作文件对象拷贝，变成可写的excel对象
    new_excel = copy(old_excel)

    # 获得第一个sheer的对象
    ws = new_excel.get_sheet(0)

    for line in range(0,nrows):

        lng = sheet1.cell(line, 0).value
        lat = sheet1.cell(line, 1).value
        create_at = str(sheet1.cell(line, 2))
        gender = sheet1.cell(line, 3).value
        street_address = sheet1.cell(line, 4).value
        female_score = sheet1.cell(line, 5).value
        male_score = sheet1.cell(line, 6).value
        user_id = sheet1.cell(line, 7).value

        ws.write(start_line + line, 0, lng)
        ws.write(start_line + line, 1, lat)
        ws.write(start_line + line, 2, create_at)
        ws.write(start_line + line, 3, gender)
        ws.write(start_line + line, 4, street_address)
        ws.write(start_line + line, 5, female_score)
        ws.write(start_line + line, 6, male_score)
        ws.write(start_line + line, 7, user_id)

        print("line : ", start_line + line)

    new_excel.save(first_excel_name)

    start_line += nrows

    return start_line


def goThroughExcels(start_line, pre_name, start_nb, end_nb):

    for i in range(start_nb, end_nb + 1):

        excelname_read = pre_name + str(i) + ".xls"

        start_line = read_record_excel(start_line, excelname_read)


def makeFirst(first_excel_name):

    book = xlwt.Workbook()  # 创建一个Excel表对象
    sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)

    book.save(first_excel_name)


if __name__ == "__main__":

    pre_name = "InfoB"

    first_excel_name = "Combine.xls"
    makeFirst(first_excel_name)

    start_line = 0

    start_nb = 1
    end_nb = 16

    goThroughExcels(start_line, pre_name, start_nb, end_nb)