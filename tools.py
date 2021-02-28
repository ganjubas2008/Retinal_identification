import cv2
import numpy as np
def show(image, wk=0, name="img"):
    cv2.imshow(name, image)
    cv2.waitKey(wk)

def resize(img, k):
    return cv2.resize(img, (img.shape[1]//k, img.shape[0]//k))
