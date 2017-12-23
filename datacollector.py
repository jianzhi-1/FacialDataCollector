import cv2
import numpy as np
import moviepy.editor as mpy
import os

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
def error_fn(tup1, tup2):
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

    continuous = False
    prev = (-1, -1, -1, -1)
    prevti = -1
    ti = 0
    while (ti < clip.duration):
        
        img = clip.get_frame(ti)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if (len(faces) == 0):
            if (continuous == True):
                #end continuous streak, export subclip
                continuous = False
                newclip = clip.subclip(prevti, ti)
                newclip.write_videofile("test4\\" + str(prevti) + " - " + str(ti) + filename + ".mp4")
            else:
                do_nothing()
        else:
            if (continuous == False):
                prev = faces[0]
                prevti = ti
                continuous = True
            else:
                
                #check for continuity
                isit = False
                for (x, y, w, h) in faces:
                    if error_fn(prev, (x, y, w, h)) > epsilon:
                        do_nothing()
                    else:
                        isit = True
                        break
                if (isit == True):
                    do_nothing()
                else:
                    continuous = True #still True because have new face
                    newclip = clip.subclip(prevti, ti)
                    newclip.write_videofile("test4\\" + str(prevti) + " - " + str(ti) + filename + ".mp4")
                    prev = faces[0]
                    prevti = ti
        ti += 0.1

    if continuous == True:
        newclip = clip.subclip(prevti, clip.duration)
        newclip.write_videofile("test4\\" + str(prevti) + " - " + str(clip.duration) + filename + ".mp4")


