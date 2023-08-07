
from fileinput import filename
import sys
import numpy as np
import cv2
import datetime
import os

# get file size of caputured video
def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size

# convert size into bytes
def convert_bytes(size, unit=None):
    filesize="File size: "
    if unit == "KB":
        return print(filesize+ str(round(size / 1024, 3)) + " KB")
    elif unit == "MB":
        return str(round(size / (1024 * 1024), 3))+" MB"
    elif unit == "GB":
        return print(filesize+ str(round(size / (1024 * 1024 * 1024), 3)) + " GB")
    else:
        return print(filesize+ str(size) + " bytes")

def decode_fourcc(fourcc):
    """Decodes the fourcc value to get the four chars identifying it"""
    # Convert to int:
    fourcc_int = int(fourcc)
    # We print the int value of fourcc
    print("int value of fourcc: '{}'".format(fourcc_int))
    fourcc_decode = ""
    for i in range(4):
        int_value = fourcc_int >> 8 * i & 0xFF
        print("int_value: '{}'".format(int_value))
        fourcc_decode += chr(int_value)
    return fourcc_decode
#--------------------------------------------------------------------------------------#
e1 = cv2.getTickCount()# your code execution
cap = cv2.VideoCapture(0)

# set resolution and framerate
fourcc=cv2.VideoWriter_fourcc(*'MJPG')
cap.set(cv2.CAP_PROP_FOURCC,fourcc)

# get resolution and framerate
width =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fps = cap.get(cv2.CAP_PROP_FPS)
fourccwrite=cv2.VideoWriter_fourcc(*'XVID')
duration=int(30)

print('Width:{}'.format(width),'x','Height:{}'.format(height),'_fps:{}'.format(fps))
filename="test.avi"
out = cv2.VideoWriter(filename, fourccwrite, fps, (width,height))

a = datetime.datetime.now()
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # write the frame
        out.write(frame)
        b = datetime.datetime.now()
        print(b-a, end='\r')
        if (b-a) >= datetime.timedelta(0,duration):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
e2 = cv2.getTickCount()
time = (e2 - e1)/ cv2.getTickFrequency()
print('Time frequency',time)

size = get_file_size(filename)
si=str(convert_bytes(size, "MB"))
print("Size: ",si)

