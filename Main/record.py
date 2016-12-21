
# Non blocking wrapper for record audio and video

import os
import picamera
import pyaudio
import wave
import subprocess

class Record:
    def __init__(self, mediaDirectory):
        self.tempDir()
        self.cameraStatus = False
        self.audioStatus = False
        self.recording = False
        self.mediaDirectory = mediaDirectory
        
    def cameraSetup(self):
        self.camera = picamera.PiCamera()
        self.camera.vflip = True # camera is upside down
        self.camera.hflip = True 
        self.cameraStatus = True
    
    def cameraPreview(self, fullscreen, offset_x, offset_y, preview_width, preview_height, annotate_size):
        self.camera.start_preview(fullscreen=False, window = (offset_x, offset_y, preview_width, preview_height))# MENU
        self.camera.annotate_text_size = 20 # default 32
    
    def cameraAnnotate(self, text):
        self.camera.annotate_text = text
    
    def cameraScreenshot(self):
        filename = dt.datetime.now().strftime('/Screenshots/%Y-%m-%d-%H%M%S.jpg')
        self.camera.capture(self.mediaDirectory + filename, use_video_port=True)
    
    def cameraRecord(self):
        self.tempFilename = dt.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        self.tempVideo = self.tempDirectory + '/' + self.tempFilename + '.h264'
        self.camera.start_recording(self.tempVideo)
        
    def cameraStop(self):
        self.camera.stop_recording()
        
    def encodeVideo(self):
        output = self.mediaDirectory + '/Videos/'+ self.tempFilename + '.mp4'
        print("Input: {}".format(self.tempVideo))
        print("Output: {}".format(outputFile))
        # Combining/Merging of Audio/Video File into mkv
        z = ['MP4Box', '-fps', '30', '-add', self.tempVideo, output]
        subprocess.Popen(z,shell=False)
        
        
    # returns temp directory, creates it if needed
    def tempDir(self):
        # temp directory
        dirname, filename = os.path.split(os.path.abspath(__file__)) # find current directory
        self.tempDirectory = dirname + '/tmp'
        print("Temp directory: {}".format(self.tempDirectory))
        # check if temp directory exists and create it if not 
        if not os.path.exists(self.tempDirectory):
            os.makedirs(self.tempDirectory)
            

   


