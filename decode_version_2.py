#Version 2 of decode script with image processing (gamma correction)
#An attempt to "un-blur" blurry images

#libraries
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

#gamma correction algorithm
def adjust_gamma(image, gamma):
    #build a lookup table and map pixel values(0,255) to their adjusted gamma values
    invGamma = 1.0/gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    
    return cv2.LUT(image, table) #apply gamma correction using the lookup table

def gamma_correction(image): #apply gamma correction and show image
    gamma = 1.7 # set gamma value
    adjusted = adjust_gamma(image, gamma) #call adjust_gamma() 
    cv2.putText(adjusted, "g={}".format(gamma), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3) #show gamma value on image
    cv2.imshow("Images", np.hstack([adjusted])) #display adjusted image
    cv2.imwrite('/home/pi/Desktop/new_img.jpg', np.hstack([adjusted])) #save adjusted image
    cv2.waitKey(0)

def decode(new_img): #new decode algorithm
    #find the barcodes in the image and decode each of the barcodes
    barcodes = pyzbar.decode(new_img)

    #loop over the detected barcodes
    for barcode in barcodes:
        #extract the bounding box location of the barcode and draw the
        #bounding box surrounding the barcode on the image
        (x,y,w,h) = barcode.rect
        cv2.rectangle(new_img, (x,y), (x+w,y+h), (0,0,255), 2)

        #the barcode data is a bytes object so if we want to draw it on
        #out output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        #draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(new_img, text, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        #print the barcode type and data to the terminal
        print("[INFO] FOUND {} barcode: {}".format(barcodeType, barcodeData))

if __name__ == "__main__":
    #read image and call functions
    image = cv2.imread('/home/pi/Desktop/test.jpg') 
    gamma_correction(image)

    new_img = cv2.imread('/home/pi/Desktop/new_img.jpg')
    decode(new_img)