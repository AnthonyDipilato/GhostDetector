
# Non blocking wrapper for record audio and video
import datetime as dt
import os
import picamera
import pyaudio
import wave
import subprocess

class Record:
    def __init__(self, mediaDirectory):
        self.cameraStatus = False
        self.audioStatus = False
        self.streamSetup = False
        self.recording = False
        self.mediaDirectory = mediaDirectory
        self.tempDirectory = mediaDirectory + '/Temp'
        
    # initial setup for camera
    def cameraSetup(self):
        self.camera = picamera.PiCamera()
        self.camera.framerate = 25
        self.camera.vflip = True # camera is upside down
        self.camera.hflip = True 
        self.cameraStatus = True
    
    # initial setup for audio
    def audioSetup(self, channels, rate, chunk):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.pa = pyaudio.PyAudio()
        
    def audioStart(self):
        self.audioStatus = True
        self.tempAudio = dt.datetime.now().strftime('%Y-%m-%d-%H%M%S.wav')
        self.wave()
        self.streamSetup = True
        self.audioStream = self.pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.chunk,
                                        stream_callback=self.pa_callback())
        self.audioStream.start_stream()
        
    def audioStop(self):
        self.audioStatus = False
        self.audioStream.stop_stream()
        self.audioStream.close()
        self.wavefile.close()
        
        
    def pa_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback
    
    def wave(self, mode='wb'):
        self.wavefile = wave.open(self.tempDirectory + '/' + self.tempAudio, mode)
        self.wavefile.setnchannels(self.channels)
        self.wavefile.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16))
        self.wavefile.setframerate(self.rate)
    
    # setup preview settings
    def cameraPreview(self, fullscreen, offset_x, offset_y, preview_width, preview_height, annotate_size):
        self.camera.start_preview(fullscreen=False, window = (offset_x, offset_y, preview_width, preview_height))# MENU
        self.camera.annotate_text_size = 20 # default 32
    
    # add/update annotation text
    def cameraAnnotate(self, text):
        self.camera.annotate_text = text
    
    # save current screenshot from preview
    def cameraScreenshot(self):
        filename = dt.datetime.now().strftime('/Screenshots/%Y-%m-%d-%H%M%S.jpg')
        self.camera.capture(self.mediaDirectory + filename, use_video_port=True)
    
    # start recording video
    def cameraRecord(self):
        self.tempFilename = dt.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        self.tempVideo = self.tempDirectory + '/' + self.tempFilename + '.h264'
        self.camera.start_recording(self.tempVideo)
        
    # stop recording video
    def cameraStop(self):
        self.camera.stop_recording()
        
    # encodes and mux audio and video to mp4 in mediadirector
    def encodeVideo(self):
        output = self.mediaDirectory + '/Videos/'+ self.tempFilename + '.mp4'
        audio = self.tempDirectory + '/' + self.tempAudio
        print("Input: {}".format(self.tempVideo))
        print("Output: {}".format(output))
        print("Audio: {}".format(audio))
        # Combining/Merging of Audio/Video File into mkv
        z = "avconv -y -i {}  -r 25 -i {} -c:v copy -c:a aac -strict experimental {}".format(audio, self.tempVideo, output)
        #z = "MP4Box -fps 30 -add {} -add {} {}".format(audio, self.tempVideo, output)
        subprocess.Popen(z,shell=True)
        
    # close down camera
    def cleanup(self):
        self.camera.stop_preview()
        self.camera.close()
        if self.streamSetup:
            self.audioStream.close()
            self.pa.terminate()
            self.wavefile.close()
        
        
        

            

   


