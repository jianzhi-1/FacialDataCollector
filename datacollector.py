import cv2
import numpy as np
import moviepy.editor as mpy
import os
import sys
import pixelerror

#LOADING THE CLASSIFIERS
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

#DO_NOTHING: This function acts as a placeholder
def do_nothing():
    return

#MAKR_FACE: This function marks out faces in image
#Use this function to mark out in red the face rectangles
def mark_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y: y + h, x: x + w]
        roi_color = img[y: y + h, x: x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    return img

#ERROR_FN: This function calculates the error value between adjacent frames
#PARAMETERS: TUP1, TUP2 tuples of length 4, defining rectangle of faces
#returns the error function, sum of squares
def face_error_fn(tup1, tup2):
    total = 0
    total += (tup1[0] - tup2[0])**2
    total += (tup1[1] - tup2[1])**2
    total += (tup1[0] + tup1[2] - tup2[0] - tup2[2])**2
    total += (tup1[1] + tup1[3] - tup2[1] - tup2[3])**2
    return total


#PROCESS_VIDEO: This function is called by gui.py to process video
#PARAMETERS: FILENAME - filename of file
#            EPSILON - error margin, typically set to 25000
def process_video(filename, epsilon):

    clip = mpy.VideoFileClip(filename)
    newfilename = os.path.split(filename)[1]

    continuous = False
    #prev = (-1, -1, -1, -1)
    
    #PREV stores all tuples of previous faces
    prev = []

    prevti = -1
    ti = 0
    while (ti < clip.duration):
        
        img = clip.get_frame(ti)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if (len(faces) == 0):
            #empties prev
            prev = []
            if (continuous == True):
                #end continuous streak, export subclip
                continuous = False
                newclip = clip.subclip(prevti, ti)
                newclip.write_videofile("exported/" + str(prevti) + "-" + str(ti) + newfilename)
            else:
                do_nothing()
        else:
            if (continuous == False):
                prev = faces
                prevti = ti
                continuous = True
            else:
                
                #check for continuity
                isit = False
                for (x, y, w, h) in faces:
                    if (isit == True):
                        break
                    for (x1, y1, w1, h1) in prev:
                        if (face_error_fn((x1, y1, w1, h1), (x, y, w, h)) > epsilon):
                            do_nothing()
                        else:
                            isit = True
                            break

                if (isit == True):
                    do_nothing()
                else:
                    continuous = True #still True because have new face
                    newclip = clip.subclip(prevti, ti)
                    newclip.write_videofile("exported/" + str(prevti) + "-" + str(ti) + newfilename)
                    prev = faces
                    prevti = ti
        ti += 0.1

    if continuous == True:
        newclip = clip.subclip(prevti, clip.duration)
        newclip.write_videofile("exported/" + str(prevti) + "-" + str(ti) + newfilename)

"""
filename = "0.45 - 0.56Despacito.mp4"
clip = mpy.VideoFileClip(filename)


tt = 3.0
tt2 = 3.1

imgxx = clip.get_frame(tt)
grayx = cv2.cvtColor(imgxx, cv2.COLOR_BGR2GRAY)
facesx = face_cascade.detectMultiScale(grayx, 1.3, 5)
imgyy = clip.get_frame(tt2)
print(pixelerror.comparesize(imgxx, imgyy))
grayy = cv2.cvtColor(imgyy, cv2.COLOR_BGR2GRAY)
facesy = face_cascade.detectMultiScale(grayy, 1.3, 5)
print(len(facesx))
print(len(facesy))
for (x, y, w, h) in facesx:
    for (x1, y1, w1, h1) in facesy:
        print("Face error is " + str(face_error_fn((x1, y1, w1, h1), (x, y, w, h))/4))
#print(imgxx)
#print(imgyy)
"""
