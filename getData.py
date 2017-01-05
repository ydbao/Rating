#coding:UTF-8
#获取features

import numpy
import numpy as np

def facialDist(x1, x2, w):
    x0 = x1 - x2
    r = 200 / w
    d = x0 * r
    return d

def generateFeatures(landmarks):
    size = landmarks.shape
    if size[0] == 184:
        allFeatures = numpy.zeros((1, 164))
        for x in range(0, 1):
            list = landmarks
            w = list[-4]
            dists = []
            for i in range(0, 83):
                x1 = list[2 * i]
                y1 = list[2 * i + 1]
                x2 = list[2 * 65]  # nose-tip
                y2 = list[2 * 65 + 1]
                if i != 65:
                    dists.append(facialDist(x1, x2, w))
                    dists.append(facialDist(y1, y2, w))
            allFeatures[x, :] = numpy.asarray(dists)
    else:
        allFeatures = numpy.zeros((size[0], 164))
        for x in range(0, size[0]):
            list = landmarks[x, :]
            w = list[-4]
            dists = []
            for i in range(0, 83):
                x1 = list[2 * i]
                y1 = list[2 * i + 1]
                x2 = list[2 * 65]  # nose-tip
                y2 = list[2 * 65 + 1]
                if i != 65:
                    dists.append(facialDist(x1, x2, w))
                    dists.append(facialDist(y1, y2, w))
            allFeatures[x, :] = numpy.asarray(dists)
    return allFeatures

def getTrainData():
    landmarks = numpy.loadtxt('landmarks.txt', delimiter=',', usecols=range(184))
    featuresAll = generateFeatures(landmarks)
    numpy.savetxt('features_All.txt', featuresAll, delimiter=',', fmt='%.04f')
    return np.loadtxt('features_All.txt', delimiter=',')

def getPredictData():
    landmarks = numpy.loadtxt('new_landmarks.txt', delimiter=',', usecols=range(184))
    featuresAll = generateFeatures(landmarks)
    numpy.savetxt('new_features.txt', featuresAll, delimiter=',', fmt='%.04f')
    return np.loadtxt('new_features.txt', delimiter=',')

if __name__ == '__main__':
    getTrainData()