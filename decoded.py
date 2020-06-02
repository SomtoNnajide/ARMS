from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np 
import cv2

def decode(img):
  #Find QR code
  decodedObj = pyzbar.decode(img)

  for obj in decodedObj:
    print('Type : ', obj.type)
    print('Data : ', obj.data)

  return decodedObj

def display(img, decodedObj):
  for decodedObj in decodedObj:
    points = decodedObj.polygon

    if len(points) > 4:
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else:
      hull = points

    n = len(hull)

    for j in range(0,n):
      cv2.line(img, hull[j], hull[ (j+1) % n], (255,0,0), 3)
  
  cv2.imshow("Results", img)
  cv2.waitKey(0)

if __name__ == "__main__":
  img = cv2.imread('/home/pi/Pictures/qr_test.jpg')
  decodedObj = decode(img)
  display(img, decodedObj)