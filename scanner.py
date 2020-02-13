import cv2
import numpy as np
import rect
import os
import sys
from scipy import stats
# add image here.
# We can also use laptop's webcam if the resolution is good enough to capture
# readable document content
def main(id):
    #print("in scanner")
    srcdir = "./FromPhone"
    trgdir = "./DST"
    b = np.load("formLogs.npy")
    images = sorted(os.listdir(srcdir))
    cnt=1
    for im in images:
        #image
        # resize image so it can be processed
        # choose optimal dimensions such that important content is not losmx, t
        image = cv2.imread(os.path.join(srcdir,im))
        image = cv2.resize(image, (1500, 880))

        # creating copy of original image
        orig = image.copy()

        # convert to grayscale and blur to smooth
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        #blurred = cv2.medianBlur(gray, 5)

        # apply Canny Edge Detection
        edged = cv2.Canny(blurred, 0, 50)
        orig_edged = edged.copy()

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        derp, contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        #x,y,w,h = cv2.boundingRect(contours[0])
        #cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),0)

        # get approximate contour
        for c in contours:
            p = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * p, True)

            if len(approx) == 4:
                target = approx
                break


        # mapping target points to 800x800 quadrilateral
        approx = rect.rectify(target)
        pts2 = np.float32([[0,0],[800,0],[800,800],[0,800]])

        M = cv2.getPerspectiveTransform(approx,pts2)
        dst = cv2.warpPerspective(orig,M,(800,800))

        cv2.drawContours(image, [target], -1, (0, 255, 0), 2)
        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join("./ForGUI","gui"+str(cnt)+".jpg"), dst)
        dst = dst[50:-5, 200:-5]
        cv2.imwrite(os.path.join(trgdir,"dst"+str(cnt)+".jpg"), dst)
        cnt+=1

if __name__=="__main__":
    main(sys.argv[1])
