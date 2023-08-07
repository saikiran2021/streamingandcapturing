
import sys
import numpy as np
import cv2
import datetime
import os
import xlsxwriter

#--------------------------------------------------------------------------------------#
# get file size of caputured video
def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size

# convert size into bytes
def convert_bytes(size, unit=None):
    if unit == "KB":
        return print('File size: ' + str(round(size / 1024, 3)) + ' KB')
    elif unit == "MB":
        return str(round(size / (1024 * 1024), 3))+" MB"
    elif unit == "GB":
        return print('File size: ' + str(round(size / (1024 * 1024 * 1024), 3)) + ' GB')
    else:
        return print('File size: ' + str(size) + ' bytes')

metrics=[
[1280,720,30,100],
[1280,720,30,200],
[1280,720,30,500], 
[1280,720,20,100],
[1280,720,20,200], 
[1280,720,20,500], 
[1280,720,15,100],
[1280,720,15,200], 
[1280,720,15,500], 
[1280,720,10,100],
[1280,720,10,200], 
[1280,720,10,500], 
[1280,720,5,100],
[1280,720,5,200],
[1280,720,5,500],
[640,480,30,100],
[640,480,30,200],
[640,480,30,500], 
[640,480,20,100],
[640,480,20,200], 
[640,480,20,500], 
[640,480,15,100],
[640,480,15,200], 
[640,480,15,500], 
[640,480,10,100],
[640,480,10,200], 
[640,480,10,500], 
[640,480,5,100],
[640,480,5,200],
[640,480,5,500]

]

workbook = xlsxwriter.Workbook('Runc-Loopback640x480fps30.xlsx')
 
# By default worksheet names in the spreadsheet will be
# Sheet1, Sheet2 etc., but we can also specify a name.
worksheet = workbook.add_worksheet("Runc-Loopback")
title = ['Width.', 'Height', 'Fps','Number of frames', 'Time Frequency','File size']
row = 1
col = 0
j = 0
for headers in title:
    worksheet.write(0, col + j, headers)
    j+=1

for x in metrics:
    e1 = cv2.getTickCount()# your code execution
    cap = cv2.VideoCapture(0,cv2.CAP_V4L)

    # set resolution and framerate
    fourcc=cv2.VideoWriter_fourcc(*'MJPG')
    cap.set(cv2.CAP_PROP_FOURCC,fourcc)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, x[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, x[1])
    cap.set(cv2.CAP_PROP_FPS,  x[2])

    # get resolution and framerate
    width =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)
    fourccwrite=cv2.VideoWriter_fourcc(*'XVID')
    frames= x[3]
    print('Width:{}'.format(width),'x','Height:{}'.format(height),'fps:{}'.format(fps),'frames:{}'.format(frames))
    filename='Runc-Loopback'+str(width)+'x'+str(height)+'fps'+str(fps)+'frames'+str(frames)+'.avi'
    out = cv2.VideoWriter(filename, fourccwrite, fps, (width,height))

    a = datetime.datetime.now()
    iframe=1
    while(iframe<frames):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
        iframe=iframe+1
        b = datetime.datetime.now()
        print(b-a, end='\r')

    # Release everything if job is finished
    cap.release()
    out.release()
    e2 = cv2.getTickCount()
    time = (e2 - e1)/ cv2.getTickFrequency()
    print('Time frequency',time)
    worksheet.write(row, col, x[0])
    worksheet.write(row, col + 1, x[1])
    worksheet.write(row, col + 2, x[2])
    worksheet.write(row, col + 3, x[3])
    worksheet.write(row, col + 4,time)
    size = get_file_size(filename)
    si=str(convert_bytes(size, "MB"))
    print("Size: ",si)
    worksheet.write(row, col + 5,si)
    row +=1

workbook.close()
