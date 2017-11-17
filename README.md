# Ghost Detector

This project is the code for my DIY ghost detector. It runs on a Raspberry Pi using the NOIR camera to record video and take pictures with overlaid sensor data.

You can see the full build on my blog: <http://anthonydipilato.com/2016/12/31/ghost-detector/>

### Features
- BMP180 for barometric pressure and temperature
- HMC5883L magnometer
- Arduino Nano used as an EMF sensor
- RH Electronics Geiger Counter Board

Videos and pictures are saved to a USB flash drive


Raspberry Pi python code is in the Main directory Arduino EMF sensor code in the EMF directory.

UI is built on Tkinter library 

### Required libraries
- picamera
- Tkinter
- PyAudio
- MP4Box

### Author
Anthony DiPilato, anthony@bumbol.com

### License
All code is available under the MIT license. See LICENSE file for info.