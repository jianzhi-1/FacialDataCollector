# FacialDataCollector
This application focuses on extracting segments of video with facial recognition and cutting them to form a database of videos.



This application consists of:
GUI : sdf
Error Algorithms: for calculating continuous frames


### Dependencies:
To use the application, install Python 2.7
This project depends on a few python libraries:
- numpy
- matplotlib
- imageio
- ffprobe
- moviepy
- PIL (installed together with moviepy)
- cv2

To install the first five libraries, run the following:
```
pip install numpy matplotlib imageio ffprobe moviepy
```

To install cv2, please follow the instructions [here](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html).

### Using FacialDataCollector
Using Python 2.7, run gui.py.

Click 'Browse Video' to select a video (.mp4). The GUI also allows you to preview the video you have chosen.

Click 'Process Video' to start processing the video. The resulting clips will be exported to the 'export' folder.

![Image of GUI](interface.png)

### Performance of FacialDataCollector
FacialDataCollector depends on the library MoviePy, so the speed of exporting clips is mainly limited by MoviePy.

It takes around 1 day (24 hours) to process 2 hours of video.


### Error Function for Continuous Frames:
FacialDataCollector uses two error values to judge continuity
- Face Error
The sum of squares of differences of rectangles marking out faces in adjacent frames.
- Pixel Error
The sum of the difference in pixels of adjacent frames.
See Report_FINAL.pdf for more information.

Epsilon (error threshold) is determined based on the following graph, where the number of clips obtained is minimum.

![Image of Error Threshold Graph](error_graph.png)

For effective data collection, epsilon is set to be 60000.
To set it to other value, change the datacollector.process_video() function.


### Common Bugs and Fixes
When running gui.py on Windows, the following Python error may occur:
```
Error handling:
  File "C:\Python27_64\lib\site-packages\imageio\plugins\ffmpeg.py", line 444, in _terminate
    self._proc.kill()
  File "C:\Python27_64\lib\subprocess.py", line 1019, in terminate
    _subprocess.TerminateProcess(self._handle, 1)
WindowsError: [Error 5] Access is denied
```
To correct this error, in the ffmpeg.py line 444, change
```python
self._proc.kill()
```
to 
```python
try:
    self._proc.kill()
except WindowsError:
    pass
```