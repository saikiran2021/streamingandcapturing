# import module
import cv2
import datetime
import xlsxwriter

 
# create video capture object
videolist=[
"RUNSC_ACTUALCAMERA1280x720fps15.0duration30.avi",
"RUNSC_ACTUALCAMERA1280x720fps20.0duration30.avi",
"RUNSC_ACTUALCAMERA1280x720fps30.0duration30.avi",
"RUNSC_ACTUALCAMERA1280x720fps5.0duration30.avi"
]
workbook = xlsxwriter.Workbook('Runc-Loopback640x480fps30.xlsx')
 
# By default worksheet names in the spreadsheet will be
# Sheet1, Sheet2 etc., but we can also specify a name.
worksheet = workbook.add_worksheet("Runc-Loopback")
title = ['Filename.', 'duration']
row = 1
col = 0
j = 0
for headers in title:
    worksheet.write(0, col + j, headers)
    j+=1
worksheet.set_column('A:A', 50)

for i in videolist:
    print(i)
    data = cv2.VideoCapture(i)
    
    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)
    # calculate duration of the video
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)
    # print(f"duration in seconds: {seconds}")
    print(f"video time(playback time): {video_time}")
    worksheet.write(row, col, i)
    worksheet.write(row, col + 1,str(video_time))
    row +=1

workbook.close()
