# Ghost Detector
![Ghost Detector](http://anthonydipilato.com/wp-content/uploads/2018/03/ghostdetector.jpg)

This project is the code for my DIY ghost detector. It runs on a Raspberry Pi using the NOIR camera to record video and take pictures with overlaid sensor data.

You can see the full build on my blog: <ghost_detector.jpg>

### Features
- BMP180 for barometric pressure and temperature
- HMC5883L magnometer
- Arduino Nano used as an EMF sensor
- RH Electronics Geiger Counter Board

Videos and pictures are saved to a USB flash drive


Raspberry Pi python code is in the Main directory Arduino EMF sensor code in the EMF directory.

UI is built on Tkinter library 

### Required libraries
- [picamera](https://github.com/waveform80/picamera) - Python interface for RasPi camera.
- [Tkinter](https://wiki.python.org/moin/TkInter) - GUI library for python.
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) - Audio I/O Library.
- [MP4Box](https://gpac.wp.imt.fr/mp4box/) - Library for encoding video files.

### Author
Anthony DiPilato, anthony@bumbol.com

### License
All code is available under the MIT license. See LICENSE file for info.
