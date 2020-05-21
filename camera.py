#camera test

#libraries
from picamera import PiCamera
from time import sleep

camera = PiCamera() #camera object

camera.start_preview() #start a 5 second preview
sleep(5)
camera.capture('/home/pi/Desktop/img2.jpg') #capture and save to location
camera.stop_preview() #stop preview


