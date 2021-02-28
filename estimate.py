import cv2
import numpy as np
from modules import est_transform, segm, tools

class Solution:
    def __init__(self, img1, img2, zip):
        self.img1 = tools.resize(segm.extract_bv(img1), zip)
        self.img2 = tools.resize(segm.extract_bv(img2), zip)
        self.THRESH = 0.9 #

        # total translation
        self.distortion = [0, 0, 0]

    def similarity(self, img1, img2):
        k1 = 0.3; k2 = 0.7

        y,x=img1.shape[:2]

        img1 = img1[int(y*k1):int(y*k2), int(x*k1):int(x*k2)] #cut part of image to avoid edge deformation
        img2 = img2[int(y * k1):int(y * k2), int(x * k1):int(x * k2)]

        intersection = cv2.bitwise_and(img1, img2)
        union = cv2.bitwise_or(img1, img2)

        hits = cv2.countNonZero(intersection)
        hits_max = cv2.countNonZero(union)

        return hits / hits_max

    def iter_compare(self, img1, img2, methods):
        for method in methods:
            if method == 0:
                shift = est_transform.getTranslation(img1, img2)
                img2 = est_transform.affineTrans(img2, shift)

                rot = est_transform.getRot(img1, img2)
                img2 = est_transform.rotAlignment(img2, rot)

            elif method == 1:
                rot = est_transform.getRot(img1, img2)
                img2 = est_transform.rotAlignment(img2, rot)

                shift = est_transform.getTranslation(img1, img2)
                img2 = est_transform.affineTrans(img2, shift)

        self.distortion[0] += rot
        self.distortion[1] += shift[0]
        self.distortion[2] += shift[1]

        return self.similarity(img1, img2) > self.THRESH

    def compare(self):
        step = 1
        angles = [*range(-5, 6, step)] +\
                 [*range(-10, -5, step)] +\
                 [*range(6, 11, step)] +\
                 [*range(-20, -10, step)] +\
                 [*range(11, 21, step)]
        #firstly processes most probable angles, then less
        for angle in angles:
            #if abs(angle) > 10:
            #    continue
            img3 = est_transform.rotAlignment(self.img2, angle)
            shift = est_transform.getTranslation(self.img1, img3)
            img3trans = est_transform.affineTrans(img3, shift)
            rangle = angle - est_transform.getRot(img3trans, self.img1)

            if self.similarity(self.img1, img3trans) > self.THRESH:
                if self.iter_compare(self.img1, img3trans, [1, 0, 1]):
                    self.distortion[0] -= rangle
                    self.distortion[1] -= shift[0]
                    self.distortion[2] -= shift[1]
                    return True
                elif self.iter_compare(self.img1, img3trans, [0, 1, 0]):
                    self.distortion[0] -= rangle
                    self.distortion[1] -= shift[0]
                    self.distortion[2] -= shift[1]
                    return True

        return False
