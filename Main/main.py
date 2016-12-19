#!/usr/bin/env python

import picamera
import datetime as dt
import Tkinter as tk
import time
import sys
import pyaudio
import subprocess
import RPi.GPIO as GPIO
import os
import shutil
import wave
# sensors class
from sensors import Sensors 

# returns temp directory, creates it if needed
def tempDir():
    # temp directory
    dirname, filename = os.path.split(os.path.abspath(__file__)) # find current directory
    tempDirectory = dirname + '/tmp'
    print("Temp directory: {}".format(tempDirectory))
    # check if temp directory exists and create it if not 
    if not os.path.exists(tempDirectory):
        os.makedirs(d)
    return tempDirectory

def annotate():
    date_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.annotate_text = date_time + sensors.output()
    # call again
    root.after(sensor_interval, annotate) 

def sensors_update():
    # update sensor readings
    sensors.update_all()
    # call again
    root.after(sensor_interval, sensors_update)

def screenshot():
    ssFilename = dt.datetime.now().strftime('/Screenshots/%Y-%m-%d-%H%M%S.jpg')
    camera.capture(mediaDirectory + ssFilename, use_video_port=True)

def encodeVideo():
    tempVideo = tempDirectory + tempFilename + '.h264'
    tempAudio = tempDirectory + tempFilename + '.wav'
    outputFile = mediaDirectory + '/Videos'+ tempFilename + '.mp4'
    print("Input: {} {}".format(tempAudio,tempVideo))
    print("Output: {}".format(outputFile))
    
    # Combining/Merging of Audio/Video File into mkv
    z = ['MP4Box', '-fps', '30', '-add', tempVideo, '-add', tempAudio,  outputFile]
    subprocess.Popen(z,shell=False)


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
def toggleRecord(tog=[False]):
    global tempFilename
    global stream #audio stream
    global audio_frames
    tog[0] = not tog[0]
    if tog[0]:
        # record video
        recordButton.config(text="Stop Recording") # update button label
        tempFilename = dt.datetime.now().strftime('/%Y-%m-%d-%H%M%S')
        tempVideo = tempDirectory + tempFilename + '.h264'
        print("Temp: {}".format(tempVideo))
        camera.start_recording(tempVideo)
        # clear_audio frames
        audio_frames = []
        stream = pa.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    output = False,
                    input_device_index = 2,
                    frames_per_buffer = CHUNK)
    else:
        audioFile = tempDirectory + tempFilename + '.wav'
        print("audio file: {}".format(audioFile))
        recordButton.config(text="Record")
        camera.stop_recording()
        stream.stop_stream()  # Pause audio stream
        stream.close()  # Stop audio stream
        # Creation of MIC WAVE FILE
        wf = wave.open(audioFile, 'wb')                              
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_frames))
        wf.close()
        encodeVideo()
        
# quit application
def quit():
    if tog[0]:
        camera.stop_recording()
    camera.stop_preview()
    camera.close()
    root.destroy()


# initialize audio
pa = pyaudio.PyAudio()
# audio settings
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
audio_frames = []
# Settings
# interval to check for sensor updates
sensor_interval = 500 # milliseconds
tog = [False]

RATE = 44100
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
# setup camera
camera = picamera.PiCamera()
camera.vflip = True # camera is upside down
camera.hflip = True 
camera.start_preview(fullscreen=False, window = (offset_x, 0, preview_width, preview_height))# MENU
camera.annotate_text_size = 24 # default 32
try:
    #main loop
    # last check for sensor intervals
    while True:
        
        # annotate
        annotate()
        # recording status, check for errors
        if tog[0]:
            camera.wait_recording()
            # store audio chunk
            data = stream.read(CHUNK)
            print("Chunk")
            audio_frames.append(data)
        # tkinter loop
        root.after(sensor_interval, sensors_update)
        root.after(sensor_interval, annotate) # update every second for clock
        root.mainloop()
        
except KeyboardInterrupt:
    camera.stop_preview()
    camera.close()
    pa.terminate()     
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
except:
    camera.stop_preview()
    camera.close()
    pa.terminate()     
    GPIO.cleanup() # clean up GPIO on normal exit
    print "Unexpected error:", sys.exc_info()[0]
    raise
    


