#Algorithm to sharpen blurry images
#to compare with gamma correction
#Program may take time to run because of image processing

#Libraries
from skimage.exposure import rescale_intensity
import numpy as np 
import cv2

def convolve(image, kernel):
    #get the spatial dimensions of the image along with
    #the spatial dimensions of the kernel
    (iH, iW) = image.shape[:2]
    (kH, kW) = kernel.shape[:2]

    #allocate memory for the output image, making sure to
    #"pad" the borders of the input image so that the spatial
    #size(width and height) are not reduced
    pad = (kW - 1) // 2
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    output = np.zeros((iH, iW), dtype="float32")

    #loop over the input image, "sliding" the kernel across
    #each (x,y) coordinate from left-to-right and
    #top-to-bottom
    for y in np.arange(pad, iH + pad):
        for x in np.arange(pad, iW + pad):
            #extract the ROI of the image by extracting the
            #center region of the current (x,y) coordinate dimensions
            roi = image[y - pad:y + pad + 1, x - pad: x + pad + 1]

            #perform convolution by taking the
            #element-wise multiplicate between the ROI and
            #the kernel, then summing the matrix
            k = (roi * kernel).sum()

            #store the convolved value in the output
            #(x,y) coordinate of the output image
            output[y - pad, x - pad] = k

    #rescale the output image to be in the range [0,255]
    output = rescale_intensity(output, in_range=(0, 255))
    output = (output * 255).astype("uint8")

    return output #return convoled image

#construct sharpen kernel
sharpen = np.array((
                    [0, -1, 0],
                    [-1, 5,-1],
                    [0, -1, 0]), dtype="int")

image = cv2.imread('/home/pi/Desktop/test.jpg') #load image

#apply kernel using the convole function and
#OpenCVs filter2D function
convoleOutput = convolve(image, sharpen)
opencvOutput = cv2.filter2D(image, -1, sharpen)

#show the output images
cv2.imshow("original", image)
cv2.imshow("convole", convoleOutput)
cv2.imshow("opencv", opencvOutput)
cv2.waitKey(0)
cv2.destroyAllWindows()