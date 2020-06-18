#Completed version of ARMS real-time barcode decoder
#Program is good enough of the scale of this assignment
#but the project can be improved and extended to practical systems

#Libraries needed
from imutils.video import VideoStream    #capture threaded video streams                                                                                        .
from time import sleep                   #time delays
import RPi.GPIO as GPIO                  #to access the Pi board
import pyzbar.pyzbar as pyzbar           #decoding library
import cv2                               #assists in the decode process
import imutils                           #video stream
import datetime                          #timezone and date
import os                                #for system config

def beep():
    GPIO.setmode(GPIO.BCM)               #setmode to BCM refering to gpio pin number
    GPIO.setup(18, GPIO.OUT)             #setup the pin (gpio18) as output
    pwm = GPIO.PWM(18, 261)              #initialise the pwm (pulse width modulation) with given frequency

    pwm.start(50)                        #start duty cycle
    sleep(1)                             #delay
    pwm.start(0)                         #stop duty cycle
    sleep(1)                             #delay
                                         #hence creating a beep effect
    GPIO.cleanup()                       #reset pin
                                                                                                                                                                                                                                          
def scanCode():
    #initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...") 
    vs = VideoStream(usePiCamera=True).start()
    sleep(2)

    #open the output csv file for writing and initialize a list of barcodes found so far
    csv = open("barcodes.csv", "w+")          #clear previous content in csv file
    csv.close()
    csv = open("barcodes.csv", "a")           #open csv for new content
    csv.write("ID,Time\n")                   
    found = []

    #loop over the frames from the video stream
    while True:
        #grab the frame from the threaded video stream and resize it to
        #have a maximum width of 600px
        frame = vs.read()
        frame = imutils.resize(frame, width=600)

        #find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        #loop over the detected barcodes
        for barcode in barcodes:
            #extract the bounding box location of the barcode and draw the
            #bounding box surrounding the barcode on the image
            (x,y,w,h) = barcode.rect
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

            #the barcode data is a bytes object so if we want to draw it on
            #out output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            #draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

            #if the barcode text is currently not in our csv file, write
            #the timestamp and barcode to file and update list
            #and call beep() 
            if barcodeData not in found:
                csv.write("{},{}\n".format(barcodeData, datetime.datetime.now()))
                beep()
                csv.flush()
                found.extend([barcodeData, 100])

        #extension of content check however
        #this permits multiple scans after 10 seconds
        #and deletes duplicates        
        for i in range(0, len(found)):
            if i % 2 == 1:
                found[i] = found[i] - 1
                if found[i] == 0:
                    del found[i]
                    del found[i - 1]

        #show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        #if the 'q' key is pressed, break loop
        if key == ord("q"):
            break

    #close output csv field and do some cleanup
    print("[INFO] cleaning up...")
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()

if __name__ == '__main__':
    #uncomment line 101 if timezone incorrect
    #os.system('sudo date -s "$(wget -qSO- -max-redirect=0 google.com 2>&1 | grep Date: | cut -d\'\'-f5-8)Z"') 
    scanCode()                                                                                                  
