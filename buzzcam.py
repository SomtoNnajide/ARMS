#Libraries
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import os.path
import time

camera = PiCamera() #instantiate camera
picpath = '/home/pi/Desktop/test.jpg' #define picture path

#setup pi board and pwm pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 261)

#take picture and save to already defined path
camera.start_preview() #start camera preview
sleep(5)
camera.capture(picpath)
camera.stop_preview() #close camera preview

#a test to check if the path exists 
#buzzer beeps once if true
#and three times if false
#similar to later on system functionality whereby it beeps if barcode is recognised or not
def findPic(path): 
    if os.path.exists(path): #check path
        pwm.start(50)
        time.sleep(1)
        pwm.start(0)
        time.sleep(1)
    else:
        for i in range(3):
            pwm.start(80) 
            time.sleep(0.3)
            pwm.start(0)
            time.sleep(0.3)
            
    GPIO.cleanup()

if __name__ == "__main__": #python main function
    findPic(picpath) #call function with parameter
