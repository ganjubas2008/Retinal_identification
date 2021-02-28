from solution import Solution
import cv2
import numpy as np
import tools
import segm
from math import sqrt, atan, pi
import matplotlib.pyplot as plt

"""This file is not needed for solution.
   Here are stored few functions that were used for estimating correctness of solution. 
   Estimator builds dependence of tp, tn, fp, fn on deformation of image"""


def main(mode="random", iter_num=20, k=5):
    """average time to 1 pair = (2 / k^2) sec"""


    if mode == "random":
        from random import uniform
        from time import time

        img1 = cv2.imread("comp1.tif")
        img1 = tools.resize(img1, k)
        cont = []
        for i in range(iter_num):

            dx = dy = 0
            dr = 0

            shift=(uniform(-dx, dx), uniform(-dy, dy))
            rot = (uniform(-dr, dr))
            img2 = tools.get_img(img1, shift, rot)

            solver = Solution(img1, img2, 100)

            print("RIGHT", rot, shift)

            start = time()
            solver.estimate()
            shift1 = [0, 0]
            rot1, shift1[0], shift1[1] = solver.rotXY
            if rot1 != False:
                print("EST", rot1, shift1)
                print("rotXY", solver.rotXY)
                delta = [abs(rot - rot1), abs(shift[0] - shift1[0]), abs(shift[1] - shift1[1])]
                print(f"FALLIBILITY = {delta}")
            else:
                print("NOT")

            cont.append(time() - start)
            print("___")
        print(f"MAX = {max(cont)}, MIN = {min(cont)}, AVERAGE = {sum(cont) / iter_num} SECONDS")

    elif mode == "compare":
        name1, name2 = f"/MESSIDOR/1pp.tif", f"/MESSIDOR/20051216_43913_0200_PP.tif"
        img1 = (cv2.imread(name1))
        img2 = (cv2.imread(name2))
        #img2 = tools.rotAlignment(img2, 0)


        #tools.show(img1)
        #tools.show(img2)
        img1 = segm.extract_bv(tools.resize(img1, k))
        img2 = segm.extract_bv(tools.resize(img2, k))
        solver = Solution(img1, img2)
        print(solver.estimate())
        return 0

from tools import *
def getans(mode, pshift, drot, iter_num=10, zip=3):
    from random import uniform, randint

    names = ["comp1.tif", "comp2.tif", "comp3.tif", "comp4.tif", "comp5.tif"]

    imgs = [cv2.imread(name) for name in names]

    TTFF = {"tn":0, "tp":0, "fn":0, "fp":0}

    k = 0
    dx = dy = imgs[0].shape[0] * pshift

    for i in range(iter_num):

        shift1 = (uniform(-dx, dx), uniform(-dy, dy))
        rot1 = (randint(-drot, drot))
        shift2 = (uniform(-dx, dx), uniform(-dy, dy))
        rot2 = (randint(-drot, drot))

        if mode=="sim":
            ind1 = randint(0, 1)
            ind2 = randint(0, 1)
        elif mode=="any":
            ind1 = randint(0, 4)
            ind2 = randint(0, 4)
        img1 = tools.get_img(imgs[ind1], shift1, rot1)
        img2 = tools.get_img(imgs[ind2], shift2, rot2)
        solver = Solution(img1, img2, zip)

        #show(segm.extract_bv(img1), name="_____")

        SIM = solver.estimate()
        shift1 = [0, 0]
        rot1, shift1[0], shift1[1] = solver.rotXY
        print("->", ind1, ind2, "->", SIM)
        if SIM: #ОДИНАКОВЫЕ
            if ind1 == ind2:
                TTFF["tp"] += 1
            else:
                TTFF["fp"] += 1
                print("!!!")
        else: #РАЗНЫЕ
            if ind1 != ind2:
                TTFF["tn"] += 1
            elif ind1==ind2:
                TTFF["fn"] += 1
                print("&&")

    return TTFF

def estimator(picnum=15, k=6):
    y=[]
    tp, tn, fp, fn=[], [], [], []
    iter_num = 15
    for pshift in range(0, 61, 3):
        pshift=pshift/160
        drot = int(pshift*2)
        y.append(round(((pshift**2 + drot**2)**(1/2)), 4))
        metrics = getans(
            mode="sim", pshift=pshift/1.2, drot=drot, iter_num=iter_num, zip=k)
        print(metrics, pshift)
        tp.append(metrics["tp"]* 100/iter_num)
        tn.append(metrics["tn"]* 100/iter_num)
        fp.append(metrics["fp"]* 100/iter_num)
        fn.append(metrics["fn"]* 100/iter_num)
        if pshift == 52: tn.append(1* 100/iter_num)


    plt.plot(y, tp, label="tp")
    plt.plot(y, fn, label="fn")
    plt.plot(y, tn, label="tn")
    plt.plot(y, fp, label="fp")

    plt.ylabel("число метрик, % от общего числа", fontsize=12)
    plt.xlabel("деформация", fontsize=12)

    plt.legend()
    plt.savefig(f"accuracy{picnum}.png")
    plt.show()

    print(sum(tn), sum(tp), sum(fn), sum(fp))






