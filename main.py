from estimate import Solution
import argparse
import cv2

def main(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    solver = Solution(img1, img2, 3)
    return solver.compare()

def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p1", "--path1", required=True,
                    help="path to first image")
    ap.add_argument("-p2", "--path2", required=True,
                    help="path to second image")
    args = vars(ap.parse_args())
    return args

if __name__ == "__main__":
    try:
        args = {"path1": "C:\MESSIDOR\\1pp.tif",
                "path2": "C:\MESSIDOR\\1pp.tif"}
        #args = parse()
        print(main(args["path1"], args["path2"]))
    except BaseException as err:
        print(err)
