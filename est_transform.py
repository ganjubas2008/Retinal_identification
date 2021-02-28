import cv2
import numpy as np

def affineTrans(src, shift):

    x, y = shift
    rows, cols = src.shape[0], src.shape[1]
    srcTri = np.array([[0, 0], [cols - 1, 0], [0, rows-1]]).astype(np.float32)
    dstTri = np.array([[x, y],
                       [cols - 1 + x, y],
                       [x, rows - 1 + y]
                       ]).astype(np.float32)

    warp_mat = cv2.getAffineTransform(srcTri, dstTri)
    warp_rotate_dst = cv2.warpAffine(src, warp_mat, (cols, rows))
    #show(warp_rotate_dst, name=f"{shift[0]}, {shift[1]}")
    return warp_rotate_dst

def getTranslation(img1, img2):
    shift = cv2.phaseCorrelate(np.float64(img1), np.float64(img2))
    shift = -shift[0][0], -shift[0][1]
    return shift



def getRot(img1, img2, toshow=False):
    center = (img1.shape[1]//2, img1.shape[0]//2)
    size = min(center)
    const = 0

    polar1 = cv2.linearPolar(img1, center, size, const)
    polar2 = cv2.linearPolar(img2, center, size, const)

    y = img1.shape[0]

    shift = getTranslation(polar1, polar2)
    return -shift[1] * (360/y)

def rotAlignment(img, rotation):
    rows, cols = img.shape[:2]

    center = (cols // 2, rows // 2)
    rotMap = cv2.getRotationMatrix2D(center, rotation, 1)
    img = cv2.warpAffine(img, rotMap, (cols, rows))

    return img


def get_deformed_img(img, shift, rot):
    #img = cv2.copyMakeBorder(img, 100, 100, 100, 100, 1)
    img = affineTrans(img, shift)
    img = rotAlignment(img, rot)
    return img