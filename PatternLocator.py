import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os
import sys

def main(id):
    id = int(id)
    info = np.load("info.npy")
    info = info[id]
    srcdir = "./Cropped"
    trgdir = "./Alphabet"
    B = np.load("formLogs.npy")
    MIN_MATCH_COUNT = int(info[2])
    img1 = cv.imread('BVM-Logo-1.jpg', 0)  # queryImage
    images = sorted(os.listdir(srcdir))
    b = B[id]

    c = 1
    for im in images:
        img2 = cv.imread(os.path.join(srcdir, im), 0)  # trainImage
        img3 = img2[10:-10, 10: -10]
        img2 = img2[10:-10, 10: 220]
        # Initiate SIFT detector
        sift = cv.xfeatures2d.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance <= float(info[1])* n.distance:
                good.append(m)

        if len(good) >= MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv.perspectiveTransform(pts, M)
            intdst = np.int32(dst)
            p1,p2,p3,p4 = intdst
            p1[0][0] = p1[0][0] if p1[0][0] > 0 else 0
            p2[0][0] = p2[0][0] if p2[0][0] > 0 else 0
            p3[0][0] = p3[0][0] if p3[0][0] > 0 else 0
            p4[0][0] = p4[0][0] if p4[0][0] > 0 else 0
            p1[0][1] = p1[0][1] if p1[0][1] > 0 else 0
            p2[0][1] = p2[0][1] if p2[0][1] > 0 else 0
            p3[0][1] = p3[0][1] if p3[0][1] > 0 else 0
            p4[0][1] = p4[0][1] if p4[0][1] > 0 else 0

            p1[0][0] = p1[0][0] if p1[0][0] < img2.shape[0] else img2.shape[0]
            p2[0][0] = p2[0][0] if p2[0][0] < img2.shape[0] else img2.shape[0]
            p3[0][0] = p3[0][0] if p3[0][0] < img2.shape[0] else img2.shape[0]
            p4[0][0] = p4[0][0] if p4[0][0] < img2.shape[0] else img2.shape[0]
            p1[0][1] = p1[0][1] if p1[0][1] < img2.shape[1] else img2.shape[1]
            p2[0][1] = p2[0][1] if p2[0][1] < img2.shape[1] else img2.shape[1]
            p3[0][1] = p3[0][1] if p3[0][1] < img2.shape[1] else img2.shape[1]
            p4[0][1] = p4[0][1] if p4[0][1] < img2.shape[1] else img2.shape[1]


            p1, p2, p3, p4
            temp = (p1[0][0]+p2[0][0])/2
            p1 = [[temp, p1[0][1]]]
            p2 = [[temp, p2[0][1]]]
            temp = (p2[0][1]+p3[0][1])/2
            p2 = [[p2[0][0], temp]]
            p3 = [[p3[0][0], temp]]
            temp = (p3[0][0]+p4[0][0])/2
            p3 = [[temp, p3[0][1]]]
            p4 = [[temp, p4[0][1]]]
            temp = (p4[0][1]+p1[0][1])/2
            p4 = [[p4[0][0], temp]]
            p1 = [[p1[0][0], temp]]
            width = (-(p1[0][1] - p2[0][1]))*10/7
            p3[0][0] = p2[0][0] + width
            p4[0][0] = p1[0][0] + width
            intdst = np.int32([p1,p2,p3,p4])
            

            img3 = cv.polylines(img3, [intdst], True, 255, 3, cv.LINE_AA)
            sx, sy, wid, ht = [min(intdst[:, :, 0])[0], min(intdst[:, :, 1])[0],
                               max(intdst[:, :, 0])[0] - min(intdst[:, :, 0])[0],
                               max(intdst[:, :, 1])[0] - min(intdst[:, :, 1])[0]]  ##startx, starty, width, height

            
            nc = int(b[c - 1][3]) if int(b[c - 1][3])>0 else 0
            nr = int(b[c - 1][4]) if int(b[c - 1][3])>0 else 0
            h = float(b[c - 1][5]) if int(b[c - 1][3])>0 else 0
            w = float(b[c - 1][6]) if int(b[c - 1][3])>0 else 0
            sx = sx if sx > 0 else 0
            sy = sy if sy > 0 else 0
            wid = wid if wid > 0 else 0
            ht = ht if ht > 0 else 0


            ims = []
            foto = []
            for i in range(nr):
                for j in range(0,nc):
                    if not (nc==1 and nr==1):
                        ims.append(img3[int(sy + i * h * ht): int(sy + (i + 1) * h * ht),
                               int(sx + wid +0.6*wid + j * w * wid): int(sx + wid +0.6*wid + (j + 1) * w * wid)])
                    else:
                        foto.append(img3[int(sy + i * h * ht): int(sy + (i + 1) * h * ht),
                                   int(sx + wid + 0.6 * wid + j * w * wid): int(
                                       sx + wid + 0.6 * wid + (j + 1) * w * wid)])
                        
            k = 1
            for x in ims:
                ishan, arya = x.shape
                
                for i in range(ishan):
                    for j in range(arya):
                        if x[i,j]>150:
                            x[i,j]=255
                        else:
                            x[i,j]=0
                cv.imwrite(os.path.join(trgdir, im.split(".")[0] + "_" + str(k) + ".png"), x)
                k += 1
            k = 1
            for x in foto:
                cv.imwrite(os.path.join("Foto", im.split(".")[0] + "_" + str(k) + ".png"), x)
                k += 1

            c = (c+1)
            if c==len(b)+1:
                c=1
        else:
            print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
            matchesMask = None
            c = (c + 1)
            if c == len(b) + 1:
                c = 1

if __name__=="__main__":
    main(sys.argv[1])
