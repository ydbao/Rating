#coding:UTF-8

from __future__ import print_function
from sklearn.externals import joblib
import argparse
from poster.streaminghttp import register_openers
from getMark import getFaces, getData
from getData import getPredictData
import os
import numpy
import matplotlib.pyplot as plt
import numpy as np

# parser = argparse.ArgumentParser()
# parser.add_argument('--picPath', type=str, default='/Users/renjialiang/Downloads/bea/rrr00260.jpg')
# parser.add_argument('--dirPath', type=str, default='/Users/renjialiang/Downloads/dds')
# args = parser.parse_args()

# picPath = args.picPath
#
# register_openers()
#
# f = open('new_landmarks.txt', 'w+')
#
# print 'face begin'
# faces = getFaces(picPath)
# print 'face end'
#
# if faces is not None:
#     if len(faces) <= 0:
#         print (picPath + " --- face++ 没有识别到脸" + "\n")
#     else:
#         for face in faces:
#             sss = getData(face)
#             f.writelines(sss)
#             f.flush()
#         f.close()
#
#         features_p = getPredictData()
#         print features_p.shape
#
#         pca = joblib.load('pcaModel.model')
#         predict_data = pca.transform(features_p)
#
#         regr = joblib.load('trainModel.model')
#
#         size = predict_data.shape
#
#         for x in range(0, size[0]):
#             list = predict_data[x, :]
#             ratings_predict = regr.predict(list)
#             print ratings_predict



# if args.dirPath is not None:
#       rootdir = args.dirPath
#
#       register_openers()
#
#       picList = []
#
#       efile = open('error.txt', 'w')
#       lfile = open('new_landmarks.txt', 'w')
#       i = 1
#       for filenames in os.walk(rootdir):
#         del filenames[2][0]
#         for fn in filenames[2]:
#           print i
#           i+=1
#           thefn = rootdir+"/"+fn
#           print 'face begin'
#           faces = getFaces(thefn)
#           print 'face end'
#
#           if faces is not None:
#               if len(faces) <= 0:
#                   efile.writelines(thefn + " --- face++ 没有识别到脸"+ "\n")
#                   efile.flush()
#               else:
#                     for face in faces:
#                            sss = getData(face)
#                            lfile.writelines(sss)
#                            picList.append(thefn)
#                            lfile.flush()
#           elif faces is None:
#               efile.writelines(thefn + " --- face++ 上传图片失败"+ "\n")
#               efile.flush()
#
#       features_p = getPredictData()
#       print features_p.shape
#
#       pca = joblib.load('pcaModel.model')
#       predict_data = pca.transform(features_p)
#
#       regr = joblib.load('trainModel.model')
#
#       size = predict_data.shape
#
#       for x in range(0, size[0]):
#           list = predict_data[x, :]
#           ratings_predict = regr.predict(list)
#           efile.writelines(picList[x] + " " + str(ratings_predict) + "\n")
#           efile.flush()
#           print ratings_predict
#
#       efile.close()
#       lfile.close()

# #定义求和函数
# def grades_sum(grades):
#     total = 0
#     for grade in grades:
#         total += grade
#     return total
# #定义求平均值函数
# def grades_average(grades):
#     sum_of_grades = grades_sum(grades)
#     average = sum_of_grades / float(len(grades))
#     return average

features_p = getPredictData()


pca = joblib.load('pcaModel.model')
predict_data = pca.transform(features_p)
regr = joblib.load('trainModel.model')

size = predict_data.shape



ratings_test = np.loadtxt('new_ratings.txt', delimiter=',')

l5 = 0
l10 = 0
l15 = 0
l20 = 0
l25 = 0
l30 = 0
l40 = 0


for x in range(0, size[0]):
    list = predict_data[x, :]
    ratings_predict = regr.predict(list)
    m = abs(ratings_predict - ratings_test[x])
    if m <= 5:
        l5 += 1
    if m <= 10:
        l10 += 1
    if m <= 15:
        l15 += 1
    if m <= 20:
        l20 += 1
    if m <= 25:
        l25 += 1
    if m <= 30:
        l30 += 1
    if m > 30:
        l40 += 1



size = predict_data.shape[0]
print(size)
print(l5)
print(l10)
print(l15)
print(l20)
print(l25)
print(l30)
print(l40)

ddlist = []

ddlist.append(l5/size*100)
ddlist.append(l10/size*100)
ddlist.append(l15/size*100)
ddlist.append(l20/size*100)
ddlist.append(l25/size*100)
ddlist.append(l30/size*100)
ddlist.append(l40/size*100)

print(ddlist[0])

truth, = plt.plot(ddlist, 'r')
plt.legend([truth], ["%"])
plt.show()

# predict_data = regr.predict(predict_data)
#
# truth, = plt.plot(ratings_test, 'r')
# prediction, = plt.plot(predict_data, 'b')
# plt.legend([truth, prediction], ["XiaoBing", "Prediction"])
# plt.title("LDA")
#
# plt.show()


