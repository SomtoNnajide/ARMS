from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import os.path
import time

camera = PiCamera()
picpath = '/home/pi/Desktop/test.jpg'

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 261)

camera.start_preview()
sleep(5)
camera.capture(picpath)
camera.stop_preview()

def findPic(path):
    if os.path.exists(path):
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

if __name__ == "__main__":
    findPic(picpath)