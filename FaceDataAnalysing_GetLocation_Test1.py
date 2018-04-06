#encoding=utf-8

import os
import json
import urllib.request
import urllib.parse #quote函数为该方法的实例方法
import re

def composeURL(lng,lat):
    url = "http://restapi.amap.com/v3/geocode/regeo?callback=renderReverse&"
    #详见IE浏览器网页收藏：[Bug反馈] geocoder/v2数据很多有问题
    location = "location="+str(lng)+","+str(lat)+"&"
    output = "output=JSON&"
    ak = "234c60b368623d3fb439e02bb6fbd7dc"
    uri = url + location + output + "key=" + ak
    req = urllib.request.urlopen(uri)
    res = req.read().decode('utf-8')
    return res

def extract_Json(res):
    division1 = res.split("(")
    # print(division1)

    division2 = str(division1[1]).split(")")
    # print(division2)

    get_json = str(division2[0])
    return get_json

def get_Json_FormattedLocation(get_json_str):
    json1 = json.loads(get_json_str)
    # print(json1)
    json2 = json1["regeocode"]["formatted_address"]
    #print(json2)
    province = json1["regeocode"]["addressComponent"]["province"]
    city = json1["regeocode"]["addressComponent"]["city"]
    district = json1["regeocode"]["addressComponent"]["district"]
    township = json1["regeocode"]["addressComponent"]["township"]
    neighborhood_name = json1["regeocode"]["addressComponent"]["neighborhood"]["name"]
    neighborhood_type = json1["regeocode"]["addressComponent"]["neighborhood"]["type"]
    street = json1["regeocode"]["addressComponent"]["streetNumber"]["street"]
    #print(street)
    businessAreas = json1["regeocode"]["addressComponent"]["businessAreas"]
    businessAreas_name = businessAreas[0]["name"]
    #print(businessAreas_name)
    return json2,province,city,district,township,neighborhood_name,neighborhood_type,street,businessAreas_name

def write_Locations_Json(data,locations_records_json_path):
    judgeExisting = os.path.exists(locations_records_json_path)
    if not judgeExisting:
        f1 = open(locations_records_json_path,mode='w')
    else:
        f1 = open(locations_records_json_path,mode='a')
    a = json.dumps(data)
    b = str(a)+'\n'
    f1.write(b)


# print(str(dirpath) + '创建成功！')

def get_LocationDatas(json_source_wholepath,locations_records_json_path,lng,lat):
    data = {}
    f1 = open(json_source_wholepath,encoding='utf-8')
    for line in f1.readlines():
        rline = json.loads(line)
        if lng != rline["geo"]["coordinates"][1]:
            if lat != rline["geo"]["coordinates"][0]:
                lng = rline["geo"]["coordinates"][1]
                lat = rline["geo"]["coordinates"][0]
                response = composeURL(lng,lat)
                get_json_str = extract_Json(response)
                get_formatted_location, province, city, district, township, neighborhood_name, neighborhood_type, street, businessAreas_name = get_Json_FormattedLocation(get_json_str=get_json_str)
                data["get_formatted_location"] = str(get_formatted_location)
                data["province"] = str(province)
                data["city"] = str(city)
                data["district"] = str(district)    #小区
                data["township"] = str(township)    #后湖街街道
                data["neighborhood_name"] = str(neighborhood_name)  #建设新村
                data["neighborhood_type"] = str(neighborhood_type)  #商务住宅;住宅区;住宅小区
                data["street"] = str(street)    #建设新村路
                data["businessAreas_name"] =str(businessAreas_name) #百步亭
                write_Locations_Json(data,locations_records_json_path)


path = "D:\\用户的文件"

#初始化
lng = 0
lat = 0

for dirpath, dirnames, filenames in os.walk(path):
    for filepath in filenames:
        print(os.path.join(dirpath, filepath))
        str1 = "json"
        str2 = "results"
        if str1 in filepath:
            if str2 in filepath :
                pass
            else:
                json_source_wholepath = dirpath+"\\"+filepath
                locations_records_json_path = dirpath+"\\"+"locations.json"
                get_LocationDatas(json_source_wholepath,locations_records_json_path,lng,lat)