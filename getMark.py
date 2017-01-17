# coding:UTF-8
# 获取小冰和face++数据

from __future__ import print_function
import json
from poster.encode import multipart_encode
import argparse
import os
from poster.streaminghttp import register_openers
from post_msxiaobing import rating_apperance
import re
import urllib2


def getFaces(fliename):
    datagen, headers = multipart_encode({"api_key": 'YhpFDB15o3-bl66_latt9xKgs8ecrcbt',
                                         "api_secret": 'rI1MWhy17Zrr_Ny_zGwQrCNk-Ek9rE8w',
                                         "image_file": open(fliename, "rb"),
                                         'return_landmark': 1,
                                         'return_attributes': 'gender,age,smiling,glass,headpose,facequality,blur'
                                         })

    request = urllib2.Request("https://api-cn.faceplusplus.com/facepp/v3/detect", datagen, headers)

    r_data = requestsConnect(request)

    count = 0
    while (count < 3):
        if r_data is not None:
            return r_data
        else:
            count += 1
            r_data = requestsConnect(request)


def getFaces2(imgUrl):
    datagen, headers = multipart_encode({"api_key": 'YhpFDB15o3-bl66_latt9xKgs8ecrcbt',
                                         "api_secret": 'rI1MWhy17Zrr_Ny_zGwQrCNk-Ek9rE8w',
                                         "image_url": imgUrl,
                                         'return_landmark': 1,
                                         'return_attributes': 'gender,age,smiling,glass,headpose,facequality,blur'
                                         })

    request = urllib2.Request("https://api-cn.faceplusplus.com/facepp/v3/detect", datagen, headers)

    r_data = requestsConnect(request)

    count = 0
    while (count < 3):
        if r_data is not None:
            return r_data
        else:
            count += 1
            r_data = requestsConnect(request)


def requestsConnect(request):
    try:
        resp = urllib2.urlopen(request, timeout=10)
        token = json.loads(resp.read())["faces"]
        return token
    except Exception as e:
        print(e)
        return None

def getData(f):
    res = f['landmark']

    ssss = ''

    for s in res.keys():
        x = str(res[s]['x'])
        y = str(res[s]['y'])
        ssss = ssss + x + ", "
        ssss = ssss + y + ", "

    attr = f['attributes']
    for a in attr.keys():
        if a == 'gender':
            if attr[a]['value'] == 'Female':
                ssss = ssss + "0" + ", "
            else:
                ssss = ssss + "1" + ", "
        if a == 'age':
            s1 = str(attr[a]['value'])
            ssss = ssss + s1 + ", "
        if a == 'glass':
            if attr[a]['value'] == 'None':
                ssss = ssss + "0" + ", "
            else:
                ssss = ssss + "1" + ", "
        if a == 'headpose':
            s1 = str(attr[a]['yaw_angle'])
            s2 = str(attr[a]['pitch_angle'])
            s3 = str(attr[a]['roll_angle'])
            ssss = ssss + s1 + ", "
            ssss = ssss + s2 + ", "
            ssss = ssss + s3 + ", "
        if a == 'blur':
            gb = attr[a]['gaussianblur']
            s1 = str(gb['threshold'])
            s2 = str(gb['value'])
            ssss = ssss + s1 + ", "
            ssss = ssss + s2 + ", "

            mb = attr[a]['motionblur']
            s1 = str(mb['threshold'])
            s2 = str(mb['value'])
            ssss = ssss + s1 + ", "
            ssss = ssss + s2 + ", "

        if a == 'smile':
            smile = attr[a]
            s1 = str(smile['threshold'])
            s2 = str(smile['value'])
            ssss = ssss + s1 + ", "
            ssss = ssss + s2 + ", "

        if a == 'facequality':
            fq = attr[a]
            s1 = str(fq['threshold'])
            s2 = str(fq['value'])
            ssss = ssss + s1 + ", "
            ssss = ssss + s2 + ", "

    face_rec = f['face_rectangle']
    s1 = str(face_rec['width'])
    s2 = str(face_rec['top'])
    s3 = str(face_rec['height'])
    s4 = str(face_rec['left'])
    ssss = ssss + s1 + ", "
    ssss = ssss + s2 + ", "
    ssss = ssss + s3 + ", "
    ssss = ssss + s4 + ", " + "\n"
    return ssss


def numerical_sort(value):
    numbers = re.compile(r"(\d+)")
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dirPath', type=str, default='../pictures')
    parser.add_argument('--resultPath', type=str,default='./ratings.txt')
    args = parser.parse_args()
    if args.dirPath is not None:
        rootdir = args.dirPath

        register_openers()

        efile = open('error.txt', 'w+')
        lfile = open('landmarks.txt', 'w+')
        f = open(args.resultPath, 'w+')
        imgfile = open('imgname.txt', 'w+')
        i = 1

        file_names = sorted((fn for fn in os.listdir(rootdir) if fn.endswith("jpg")), key=numerical_sort)

        for thefn in file_names:
            thefn = rootdir + '/' + thefn
            print(i)
            i += 1
            print('face begin')
            faces = getFaces(thefn)
            print('face end')
            print('xiaobing begin')
            mark = rating_apperance(thefn)
            print('xiaobing end')
            if faces is not None and mark is not None:
                if len(faces) <= 0:
                    efile.writelines(thefn + " --- face++ 没有识别到脸" + "\n")
                    efile.flush()
                else:
                    if len(faces) == len(mark):
                        for face in faces:
                            sss = getData(face)
                            lfile.writelines(sss)
                            lfile.flush()
                            imgfile.writelines(thefn + '\n')
                            imgfile.flush()
                        for point in mark:
                            point = point[0] + point[2]
                            f.writelines(point + '\n')
                            f.flush()
                    else:
                        efile.writelines(
                            thefn + " --- face++ 和小冰的数据不匹配  face++ : " + str(len(faces)) + "  xiaobing : " + str(
                                len(mark)) + "\n")
                        efile.flush()
            elif faces is None and mark is not None:
                efile.writelines(thefn + " --- face++ 上传图片失败" + "\n")
                efile.flush()
            elif faces is not None and mark is None:
                efile.writelines(thefn + " --- xiaobing 获取评分失败" + "\n")
                efile.flush()
            elif faces is None and mark is None:
                efile.writelines(thefn + " --- face++ 上传图片失败 and xiaobing 获取评分失败" + "\n")
                efile.flush()

        f.close()
        efile.close()
        lfile.close()
        imgfile.close()


if __name__ == '__main__':
    main()
