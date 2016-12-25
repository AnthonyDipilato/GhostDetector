from datetime import datetime
from time import time
# sensor libraries
import Adafruit_BMP.BMP085 as BMP085
from compass import hmc5883l
from arduinoEMF import EMF
# we will need the gpio pin for the geiger counter
import RPi.GPIO as GPIO


class Sensors:
    def __init__(self):
        #initialize pin for geiger counter
        GPIO.setmode(GPIO.BOARD) # board pin numbering 
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # we are using pin 12 for int
        #initialize sensors
        self.barometer = BMP085.BMP085() # this is altimeter, barometer, and thermometer
        self.compass = hmc5883l(gauss = 4.7, declination = (-6,42))
        self.emf = EMF()
        self.pressure = 0.00
        self.temperature = 0.00
        self.altitude = 0.00 
        self.direction = "N  "
        self.geigerCpm = 0
        self.emfL = 0
        self.emfR = 0
        self.counter = 0
        self.counterSeconds = 0
        self.counterMinute = 0
        self.counterReset = 20 # interval to reset timer
        self.counterResetTime = time()
        # GPIO callback for geiger counter int. 
        GPIO.add_event_detect(12, GPIO.FALLING, callback=self.tube_impulse_callback) 
        
    def tube_impulse_callback(self, channel): # threaded callback -- falling edge detected   
        self.counter+=1
        self.counterSeconds = datetime.now().second
        if self.counterSeconds != 0:
            self.geigerCpm = (self.counter / self.counterSeconds) * 60 # estimated clicks per minute
        
        
    def update_all(self):
        # Counter reset
        if datetime.now().minute != self.counterMinute:
            self.counterMinute = datetime.now().minute
            self.counterSeconds = 0
            self.counter = 0
        self.update_pressure()
        self.update_altitude()
        self.update_temperature()
        self.update_compass()
        self.update_emf()
        
    def update_emf(self):
        #print(self.emf.update())
        self.emfL, self.emfR = self.emf.update()
        
        
    def update_pressure(self):
        # read pressure and conver to millibars
        self.pressure = float(self.barometer.read_pressure()) / 100
        
    def update_altitude(self):
        # read altitude and convert to feet
        self.altitude = int(float(self.barometer.read_altitude()) / 0.3048)
        
    def update_temperature(self):
        # update temperate and conver to F
        self.temperature = (float(self.barometer.read_temperature()) * (9.0/5)) + 32
        
    def update_compass(self):
        self.direction = self.compass.direction()
        
    def output(self):
        return " Compass: %s \n Temperature: %0.2fF Pressure: %0.2fmb \n  Geiger: %dcpm EMF Left: %d%% EMF Right: %d%%" % (self.direction, self.temperature, self.pressure, self.geigerCpm, self.emfL, self.emfR)
        # picamera doesn't allow placement for annotations so we have to resort to formatting with spaces and newlines
               
