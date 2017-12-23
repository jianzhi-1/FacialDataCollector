import Tkinter as tk
import tkFileDialog
import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
import imageio
import threading
import subprocess
import ffprobe
import time

from numpy import arange, sin, pi
from PIL import Image, ImageTk

#BACKEND
import datacollector


#def getLength(filename):
#    result = subprocess.Popen(["ffprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
#    return [x for x in result.stdout.readlines() if "Duration" in x]

#ARGUMENTS: PATH OF VIDEO FILE
#RETURNS: DURATION OF VIDEO FILE IN MILISECONDS
def getLength(filename):
    return int(float(ffprobe.FFProbe(filename).video[0].duration)*1000)

class Application(tk.Frame):
    def __init__(self, master = None):
        self.master = master
        master.title = "MovieEmotions"
        self.label = tk.Label(root, text = "Red Sun", bg = "red", fg = "white")
        self.label.pack(fill = tk.X)

        self.greet_button = tk.Button(master, text = "Greet", command = self.greet)
        self.greet_button.pack(fill = tk.X)

        self.close_button = tk.Button(master, text = "Close", command = master.quit)
        self.close_button.pack()

        #VID_NAME: Name of the video file
        #FULL_VID_NAME: Full path of the video file
        #VIDEO: Video object
        #VID_LABEL: Label showing the name of video
        #SELECT_VID: Button for selecting video
        
        self.vid_name = "No video file attached"
        self.full_vid_name = "temp/tempvid.mp4"
        self.video = imageio.get_reader(self.full_vid_name)
        #temporary video

        self.vid_label = tk.Label(root, text = self.vid_name)
        self.vid_label.pack()
        
        self.select_vid = tk.Button(master, text = "Browse Video", command = self.browse_vid)
        self.select_vid.pack()

        self.aud_name = "No audio file attached"
        self.full_aud_name = ""

        self.aud_label = tk.Label(root, text = self.aud_name)
        self.aud_label.pack()
        
        self.select_aud = tk.Button(master, text = "Browse Audio", command = self.browse_aud)
        self.select_aud.pack()

        self.process_button = tk.Button(master, text = "Process Video", command = self.process)
        self.process_button.pack()

        self.imagestr = "images/smiley.png"
        photo = ImageTk.PhotoImage(Image.open(self.imagestr))
        self.show_vid_label = tk.Label(root, image = photo)
        #Image.fromarray(self.video).show() this part is ok, shows the image in quicktime
        self.show_vid_label.image = photo
        self.show_vid_label.pack()
        #self.show_vid_label.grid(row = 10, column = 10, rowspan = 10, columnspan = 10)

        #vid = tkFileDialog.askopenfile(parent = root, mode = 'rb', title = 'Choose a file')
        

    
    def greet(self):
        print("Greetings!")

    def browse_vid(self):
        vidx = tkFileDialog.askopenfile()
        self.vid_name = os.path.split(vidx.name)[1]
        self.full_vid_name = vidx.name
        self.vid_label.config(text = self.vid_name)
        self.set_up_video()

    def browse_aud(self):
        audx = tkFileDialog.askopenfile()
        self.aud_name = os.path.split(audx.name)[1]
        self.full_aud_name = audx.name
        self.aud_label.config(text = self.aud_name)


    def stream(self, label, dura):
        noframes = 0
        for image in self.video.iter_data():
            noframes += 1
        delta = float(dura)/(float(1000)*float(noframes))
        for image in self.video.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            label.config(image = frame_image)
            label.image = frame_image
            time.sleep(delta*0.75)

    def set_up_video(self):
        self.video = imageio.get_reader(self.full_vid_name)
        print("DURATION OF THE VIDEO IS: " + str(getLength(self.full_vid_name)) + " MILISECONDS")
        thread = threading.Thread(target = self.stream, args = (self.show_vid_label, getLength(self.full_vid_name),))
        #thread.daemon = 1
        thread.setDaemon(True)
        thread.start()

    def process(self):
        #EPSILON usually set to 25000
        datacollector.process_video(self.full_vid_name, 25000)

root = tk.Tk()
app = Application(root)
root.mainloop()

#y = tk.Label(root, text = "Red Sun", bg = "red", fg = "white")
#b1 = tk.Button(root, text = "One")
#b2 = tk.Button(root, text = "Two")
#b1.pack(side=LEFT,padx=10)
#y.pack(fill = tk.X)
#b1.pack(fill = tk.X)
#b2.pack(fill = tk.X)
