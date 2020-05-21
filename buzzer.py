#2nd buzzer test 
#the aim is to produce a constant tone at single frequency

#Libraries
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #set pin mode
GPIO.setup(18,GPIO.OUT) #set pin output
pwm = GPIO.PWM(18,250) #assign pwm pin with 1000 frequency

while True:
    pwm.start(50) #start duty cycle
    time.sleep(100) #play for 100 secs
