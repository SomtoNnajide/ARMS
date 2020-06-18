#A test to autostart ARMS.py program upon pi start-up/reboot
import os
import time
 
time.sleep(10) #10 second delay before program runs

os.system('/usr/bin/python2.7 /home/pi/ARMS_code/ARMS.py') #executable
