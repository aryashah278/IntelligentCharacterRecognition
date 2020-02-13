import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import cv2 as cv

def main(id):
    id = int(id)
    srcdir = "./DST"
    trgdir = "./Cropped"
    b = np.load("formLogs.npy")
    files = sorted(os.listdir(srcdir))
    c = 1
    b = b[id]
    for file in files:
        img = cv.imread(os.path.join(srcdir,file))
        cc=1
        for row in b:
            im = img[int(row[1]):int(row[2])][:]
            cv.imwrite(os.path.join(trgdir, "dst"+str(c)+"_"+str(cc)+".jpg"),im)
            cc += 1
        c+=1

if __name__ == "__main__":
    main(sys.argv[1])
