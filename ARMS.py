from __future__ import print_function
from imutils.video import VideoStream
#from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import pyzbar.pyzbar as pyzbar
import numpy as np
import argparse
import cv2
import imutils
import datetime

#initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...") 
vs = VideoStream(usePiCamera=True).start()
sleep(2)

#open the output csv file for writing and initialize the set of
#barcodes found so far
csv = open("barcodes.csv", "a")
found = []

#loop over the frames from the video stream
while True:
    #grab the frame from the threaded video stream and resize it to
    #have a maximum width of 400px
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
        #the timestamp and barcode to file and update set
        if barcodeData not in found:
            csv.write("{},{}\n".format(barcodeData, datetime.datetime.now()))
            csv.flush()
            found.extend([barcodeData, 100])
            
    for i in found:
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

#close output csv fiel and do some cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()
