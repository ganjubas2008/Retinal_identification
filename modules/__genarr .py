import os, tools
from random import uniform
import cv2
from segm import *
import json
import numpy as np

"""This generator produces extra images using augmentation."""
messidor = "/MESSIDOR"

xtr = []
ytr = []
xtest=[]
ytest=[]

def main():
    os.chdir(messidor)
    files = os.listdir(messidor)

    images = [*filter(lambda x: x.endswith('.tif'), files)]

    for i in range(0, 10, 2):
        print(i)
        img = images[i]

        vessels = cv2.resize(cv2.cvtColor(cv2.imread(f"/MESSIDOR/{img}"), cv2.COLOR_BGR2GRAY), (160, 120))
        spam(vessels, i//2, xtr, ytr, k=70)
        spam(vessels, i//2, xtest, ytest, k=10)

    return xtr, ytr, xtest, ytest

def spam(img, key, x, y, k=70):
    dx = dy = 12
    dr = 15
    for i in range(k):
        shift = (uniform(-dx, dx), uniform(-dy, dy))
        rot = (uniform(-dr, dr))
        imgspam = tools.get_img(img, shift, rot)
        # tools.show(imgspam)
        x.append(imgspam)
        y.append(key)

