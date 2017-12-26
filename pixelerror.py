import cv2
import numpy as np
import moviepy.editor as mpy
import os
import sys
import math


#COMPARESIZE: checks if two np arrays are of same dimensions
#RETURNS: True (if same dimensions)
#         False (if different dimensions)
def comparesize(img, img2):
    return img.shape == img2.shape
            

def pixel_error_fn(imgx, imgy):
    print(imgx.shape)
    (w, h, z) = imgx.shape
    inf = 1000000000
    if (comparesize(imgx, imgy) == False):
        print("Inconsistent dimensions. Please check your images.")
        return inf
    totalerror = 0
    r = 5
    for i in range(0, w, max(1, w/33)):
        for j in range(0, h, max(1, h/33)):
            pixelval = imgx[i,j]
            minerror = inf
            for k in range(i - r, i + r):
                for l in range(j - r, j + r):
                    #check if out of range
                    if (0 > k or w <= k):
                        pass
                    elif (0 > l or h <= l):
                        pass
                    else:
                        curerror = 0
                        for m in range(3):
                            curerror = curerror + (pixelval[m] - imgy[k,l][m])**2
                            #print(pixelval[m] - imgy[k,l][m])
                        #print(curerror)
                        minerror = min(curerror, minerror)
            totalerror = totalerror + minerror
    return totalerror/((w/max(1, w/33))*(h/max(1,h/33)))


"""
filename = "0.45 - 0.56Despacito.mp4"
clip = mpy.VideoFileClip(filename)


tt = 3.0
tt2 = 3.1

imgxx = clip.get_frame(tt)
imgyy = clip.get_frame(tt2)
print(comparesize(imgxx, imgyy))
#print(imgxx)
#print(imgyy)
print(pixel_error_fn(imgxx, imgyy))
"""

