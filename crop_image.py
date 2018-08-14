import os
import cv2
import glob
import numpy as np


if __name__ == '__main__':
    for fil in glob.glob(os.path.join('.', 'images', '310720180839')):
        print(fil)
        #img = cv2.imread(os.path.join('.', 'images', '310720180839', 'service_100.png'))
        img = cv2.imread(fil)
        rows,cols,depth = img.shape

        current_row = rows - 1
        # ВЫРЕЗАЕМ БЕЛУЮ ОБЛАСТЬ
        while(img[current_row,1][0] == 255 and img[current_row,1][1] == 255 and img[current_row,1][2] == 255):
            current_row -= 1

        # ВЫРЕЗАЕМ ФУТЕР
        while(img[current_row,1][0] == 70 and img[current_row,1][1] == 55 and img[current_row,1][2] == 37):
            current_row -= 1

        # ВЫРЕЗАЕМ ХЕДЕР
        head_row = 1
        while(img[head_row,1][0] == 255 and img[head_row,1][1] == 255 and img[head_row,1][2] == 255):
            head_row += 1


        crop_img = img[head_row:current_row, 0:cols]
        #cv2.imwrite(os.path.join('.', 'images', 'service_100_.png'), crop_img)
        cv2.imwrite(fil, crop_img)
