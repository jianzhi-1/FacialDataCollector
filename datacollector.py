import cv2
import numpy as np
import moviepy.editor as mpy
import os
import sys
import pixelerror

#LOADING THE CLASSIFIERS
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

#MARK_FACE: This function marks out faces in image
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
    previmg = clip.get_frame(0.0)
    while (ti < clip.duration):
        
        img = clip.get_frame(ti)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if (len(faces) == 0):
            if (continuous == True):
                #check continuity
                if (ti + 0.1 < clip.duration and ti + 0.2 < clip.duration and ti + 0.3 < clip.duration):
                    img22 = clip.get_frame(ti + 0.1)
                    gray22 = cv2.cvtColor(img22, cv2.COLOR_BGR2GRAY)
                    faces22 = face_cascade.detectMultiScale(gray22, 1.3, 5)
                    img33 = clip.get_frame(ti + 0.2)
                    gray33 = cv2.cvtColor(img33, cv2.COLOR_BGR2GRAY)
                    faces33 = face_cascade.detectMultiScale(gray33, 1.3, 5)
                    img44 = clip.get_frame(ti + 0.3)
                    gray44 = cv2.cvtColor(img44, cv2.COLOR_BGR2GRAY)
                    faces44 = face_cascade.detectMultiScale(gray44, 1.3, 5)
                    if (len(faces22) == 0 and len(faces33) == 0 and len(faces44) == 0):
                        #empties prev
                        prev = []
                        previmg = img
                        continuous = False
                        newclip = clip.subclip(prevti, ti)
                        newclip.write_videofile("exported/" + str(prevti) + "-" + str(ti) + newfilename)
                    else:
                        #Put on hold first
                        previmg = img
                        pass
                else:
                    #end continuous streak, export subclip
                    #empties prev
                    prev = []
                    previmg = img
                    continuous = False
                    newclip = clip.subclip(prevti, ti)
                    newclip.write_videofile("exported/" + str(prevti) + "-" + str(ti) + newfilename)
            else:
                pass
        else:
            if (continuous == False):
                prev = faces
                prevti = ti
                previmg = img
                continuous = True
            else:
                
                #check for continuity
                inf = 1000000000
                minfaceerror = inf
                for (x, y, w, h) in faces:
                    for (x1, y1, w1, h1) in prev:
                        minfaceerror = min(minfaceerror, face_error_fn((x1, y1, w1, h1), (x, y, w, h)))

                if (minfaceerror < inf and minfaceerror + pixelerror.pixel_error_fn(previmg, img) < epsilon):
                    prev = faces
                    previmg = img
                    pass
                else:
                    continuous = True #still True because have new face
                    newclip = clip.subclip(prevti, ti)
                    newclip.write_videofile("exported/" + str(prevti) + "-" + str(ti) + newfilename)
                    prev = faces
                    previmg = img
                    prevti = ti
        ti += 0.1

    if continuous == True:
        newclip = clip.subclip(prevti, clip.duration)
        newclip.write_videofile("exported/" + str(prevti) + "-" + str(ti) + newfilename)
    print("Done processing file")

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
