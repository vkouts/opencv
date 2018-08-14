import os
import sys
import cv2
import numpy as np
import imutils
from skimage.measure import compare_ssim


IMAGE1 = os.path.join('.', 'images','030820180653','base','site__about_company_.png')
IMAGE2 = os.path.join('.', 'images','140820180838','base','site__about_company_.png')


if __name__ == '__main__':
    if not os.path.exists(IMAGE1):
         print('File {} not found'.format(IMAGE1))
         sys.exit(1)

    if not os.path.exists(IMAGE2):
         print('File {} not found'.format(IMAGE2))
         sys.exit(1)


    image1 = cv2.imread(IMAGE1)
    rows1,cols1,depth1 = np.array(image1).shape

    print(rows1,cols1,depth1)

    image2 = cv2.imread(IMAGE2)
    rows2,cols2,depth2 = np.array(image2).shape

    print(rows2,cols2,depth2)

    my_rows = min([rows1, rows2])
    my_cols = min([cols1, cols2])

    crop_img1 = image1[0:my_rows, 0:my_cols]
    crop_img2 = image2[0:my_rows, 0:my_cols]

    
    crop_img1BW = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)
    crop_img2BW = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(crop_img1BW, crop_img2BW, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))


    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(crop_img1BW, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(crop_img2BW, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
        cv2.imshow("Original", crop_img1BW)
        cv2.imshow("Modified", crop_img2BW)
        cv2.imshow("Diff", diff)
        cv2.imshow("Thresh", thresh)
        cv2.waitKey(0)

    #difference = cv2.subtract(crop_img1, crop_img2)
    #result = not np.any(difference)

    #res_img = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    #ret, mask = cv2.threshold(res_img, 10, 255, cv2.THRESH_BINARY)
    #mask_inv = cv2.bitwise_not(mask)

    #color_img = cv2.cvtColor(res_img, cv2.COLOR_GRAY2RGB)

    # for x in color_img:
    #     for y in color_img:

    # color_img[:, :, 0] = 0
    # color_img[:, :, 1] = 0

    #res = cv2.bitwise_and(crop_img1, crop_img1, mask=mask_inv)
    #res = cv2.bitwise_and(crop_img1, crop_img1, mask=mask)


    #if result is True:
    #    print('Images are the same')
    #else:
    #    cv2.imwrite('result.png', res)