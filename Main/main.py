#!/usr/bin/env python

import datetime as dt
import Tkinter as tk
import time
import sys
import RPi.GPIO as GPIO
import os
import shutil

# sensors class
from sensors import Sensors 

# add annotations to video
def annotate():
    date_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record.cameraAnnotate(date_time + sensors.output())
    # call again
    root.after(sensor_interval, annotate) 

def sensors_update():
    # update sensor readings
    sensors.update_all()
    # call again
    root.after(sensor_interval, sensors_update)

   
def screenshot():
    record.cameraScreenshot()


def deleteTempFiles(tempDirectory):
    for file in os.listdir(tempDirectory):
        file_path = os.path.join(tempDirectory, file)
        try:
            if os.path.isfile(file_path):
                print("delete: ")
                print(file_path)
                os.unlink(file_path)
        except Exception as e:
            print(e)

# toggle record video
def toggleRecord():
    global tog
    tog[0] = not tog[0]
    # recording
    if tog[0]:
        record.cameraRecord()
        # update button label
        recordButton.config(text="Stop Recording")
        
    # stop recording
    else:
        #stop camera recording
        record.cameraStop()
        # encode and mux video
        record.encodeVideo()
        # update button label
        recordButton.config(text="Record")

# quit application
def quit():
    if tog[0]:
        camera.stop_recording()
    camera.stop_preview()
    camera.close()
    audio_stream.close()
    p.terminate()     
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
    root.destroy()


def record_loop():
    global audio_frames
    # recording status, check for errors
    # tog = 0 recording
    print("record loop: {}".format(tog[0]))
    if tog[0]:
        # store audio chunk
        data = audio_stream.read(CHUNK)
        audio_frames.append(data)
    root.after(record_interval, record_loop)

# Settings
# interval to check for sensor updates
sensor_interval = 500 # milliseconds
tog = [0]

# initialize tkinter
root = tk.Tk()
root.configure(bg="#000")
# set window to full screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set() # <-- move focus to this widget

# used for final encoded output
# location of the Flash Drive 
mediaDirectory = '/media/pi/Media'

tempDirectory = tempDir()
# Delete temp files
deleteTempFiles(tempDirectory)
# widgets
# preview area
preview_height = h - 45
preview_width = int(w * (float(preview_height) / h ) ) # get ratio to scale width
# preview offsets
offset_y = int( float(h - preview_height) / 2 )
offset_x = int( float(w - preview_width) / 2 )
# Build GUI
tk.Frame(width=w, height=preview_height, bg="#000").grid(row=0, columnspan=3)
tk.Button(root, text="Quit", command=quit).grid(row=1, column=0, pady=10)
# assign record button to variable so we can edit the label with recording status
recordButton = tk.Button(root, text="Record", command=toggleRecord)
recordButton.grid(row=1, column=1, pady=10)
tk.Button(root, text="Snapshot", command=screenshot).grid(row=1, column=2, pady=10)
# Sensor Class
sensors = Sensors()
# Record class
record = Record(mediaDirectory)
# Setup Camera
record.cameraSetup()
# (fullscreen, offset_x, offset_y, preview_width, preview_height, annotate_size)
record.cameraPreview(False, offset_x, 0, preview_width, preview_height, 20)
# initial record state
tog[0] = False

try:
    #main loop
    # last check for sensor intervals
    while True:
        if tog[0]:
            camera.wait_recording()
        # annotate
        annotate()
        # tkinter loop
        # tikinter handles loops a little different we will call functions on an interval
        # that calls themselves again on the interval
        root.after(record_interval, record_loop)
        root.after(sensor_interval, sensors_update)
        root.after(sensor_interval, annotate) # update every second for clock
        root.mainloop()
        
except KeyboardInterrupt:
    camera.stop_preview()
    camera.close()
    audio_stream.close()
    p.terminate()     
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
    root.destroy()
except:
    camera.stop_preview()
    camera.close()
    audio_stream.close()
    p.terminate()     
    GPIO.cleanup() # clean up GPIO on normal exit
    print "Unexpected error:", sys.exc_info()[0]
    raise
    root.destroy()
    


