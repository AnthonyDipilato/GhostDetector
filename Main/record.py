
# Non blocking wrapper for record audio and video
import datetime as dt
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
        self.streamSetup = False
        self.recording = False
        self.mediaDirectory = mediaDirectory
        
    # initial setup for camera
    def cameraSetup(self):
        self.camera = picamera.PiCamera()
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
        output = self.mediaDirectory + '/Videos/'+ self.tempFilename + '.mkv'
        print("Input: {}".format(self.tempVideo))
        print("Output: {}".format(output))
        audio = self.tempDirectory + '/' + self.tempAudio
        # Combining/Merging of Audio/Video File into mkv
        #z = ['MP4Box', '-fps', '30', '-add', self.tempVideo, '-add', self.tempDirectory + '/' + self.tempAudio, output]
        z = ["avconv", "-y", "-i", audio,  "-r", "30", "-i", self.tempVideo,  "-filter:a", "aresample=async=1", "-c:a", "flac", "-c:v", "copy", output]
        subprocess.Popen(z,shell=True)
    
    # close down camera
    def cleanup(self):
        self.camera.stop_preview()
        self.camera.close()
        if self.streamSetup:
            self.audioStream.close()
            self.wavefile.close()
            self.pa.terminate()
        
        
        
    # returns temp directory, creates it if needed
    def tempDir(self):
        # temp directory
        dirname, filename = os.path.split(os.path.abspath(__file__)) # find current directory
        self.tempDirectory = dirname + '/tmp'
        print("Temp directory: {}".format(self.tempDirectory))
        # check if temp directory exists and create it if not 
        if not os.path.exists(self.tempDirectory):
            os.makedirs(self.tempDirectory)
            

   


