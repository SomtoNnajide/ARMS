#3rd buzzer test
#the aim is to make buzzer beep every second at 261 frequency

#Libraries
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #pinmode
GPIO.setup(18,GPIO.OUT) #pin output
pwm = GPIO.PWM(18,261) #set pwm pin and frequency

for i in range(5):
    pwm.start(70) #beep algorithm
    time.sleep(1)
    pwm.start(0)
    time.sleep(1)

GPIO.cleanup() #resets pin

