import cv2 #Importing openCV2
import numpy as np #Importing numpy for arrays and more
import matplotlib as plt #Importing for showing images in plot
import copy #Importing to copy images to variables
import glob #Importing to acces files in the computer memory
import math #Importing math for calculations
import xlwt #Importing to create excel 
from xlwt import Workbook
import imutils
import os.path
import imageProcessing
import data

print(cv2.__version__)#Printing open CV version for debugging
#Function for showing images
def showPicture(pic):
    while True:
        cv2.imshow('frame', pic)

        #Cheks if 'ESC' is pressed and exits loop if
        k = cv2.waitKey(30)
        if k == 27:
            break
    
    #Closing window with picture

#Variables

#Variables for upper and lower range in color detection for Joint image
lower_rangeJ = np.array([0, 10,0], np.uint8)
upper_rangeJ = np.array([5,255,255], np.uint8)

#Variables for upper and lower range in color detection for RGB image
lower_rangeR = np.array([0,60,50])
upper_rangeR = np.array([40,255,255])

#percent by which the image is resized
scale_percent = 75

#Creating kernel for OpenCV functions
kernel = np.array([[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]],np.uint8)

#Count variable
count = 0

#Creating workbook with sheet
wb = Workbook() #Creating workbook
frontSheet = wb.add_sheet("Data Sheet")


#Loading an array of pictures
ImageRGB = [] #Creating an array for images from RGB picture
ImageJoint = [] #Creating an array for images with joints
BlobArea = [] #Creating an array for images to measure area of blob
filesRGB = glob.glob ("pictures\\rgb\\*.png") #Adding dirrectory to files from RGB camera
filesJoint = glob.glob ("pictures\\joints\\*.png") #Adding directory to files with joints
filesArea = glob.glob ("pictures\\area\\*.png")

#Array variables
distances = []
accumulated = 0 



#Loop for loading files from RGB directory to the ImageRGB array
for myFile in filesRGB:
    imageR = cv2.imread(myFile) #Reading file as cv2 image
    ImageRGB.append(imageR) #Adding the read image to ImageRGB Array

#Loop for loading files from Joints directory to the ImageJoint array
for myFile in filesJoint:
    imageJ = cv2.imread(myFile) #Reading file as cv2 image
    ImageJoint.append(imageJ) #Adding the read image to ImageJoint Array

#Loop for loading files from area directory to the BlobArea array
for myFile in filesArea:
    imageA = cv2.imread(myFile) #Reading file as cv2 image
    BlobArea.append(imageA) #Adding the read image to the BlobArea Array

#Loop for getting radius and accuracy definition
for imageA in BlobArea:
    areaHsv = imageProcessing.hsvConvert(imageA)
    areaMask = imageProcessing.colorDetection(areaHsv, lower_rangeR, upper_rangeR)
    contourA = imageProcessing.findContours(areaMask)
    distances.append(imageProcessing.findRadius(contourA))

#Accumulating radiuses
for distance in distances:
    i = 0
    accumulated = accumulated + distance
    print(distance) #Print for debugging
    i += 1

#Calculating range
range = accumulated/len(distances)
print(range) #Print for debugging
    
for imageJ in ImageJoint:
    #Resizing both images
    imageJ = imageProcessing.resizeImage(imageJ, scale_percent)
    imageR = imageProcessing.resizeImage(ImageRGB[count], scale_percent)

    #Creating blank canvas for drawing data
    blankCanvas = imageProcessing.backGround(imageJ)

    #Flipping the RGB image
    imageR = imageProcessing.flipImage(imageR)

    #Converting RGB image to HSV
    imageRHSV = imageProcessing.hsvConvert(imageR)
    imageJHSV = imageProcessing.hsvConvert(imageJ)

    #Doing color detection
    imageJMask = imageProcessing.colorDetection(imageJHSV, lower_rangeJ, upper_rangeJ)
    imageRMask = imageProcessing.colorDetection(imageRHSV, lower_rangeR, upper_rangeR)
    
    #Dilate white blobs
    imageJMask = imageProcessing.dilateImage(imageJMask, kernel, 2)
    imageRMask = imageProcessing.dilateImage(imageRMask, kernel, 2)
    
    #Find contours
    contourJ = imageProcessing.findContours(imageJMask)
    contourR = imageProcessing.findContours(imageRMask)

    #Draw contours
    cv2.drawContours(imageJ, contourJ, -1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.drawContours(imageR, contourR, -1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.drawContours(blankCanvas, contourJ, -1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.drawContours(blankCanvas, contourR, -1, (255, 255, 255), 2, cv2.LINE_AA)

    #Contour center Joint
    for c in contourJ:
        M = cv2.moments(c)
        xJ = int(M["m10"] / M["m00"])
        yJ = int(M["m01"] / M["m00"])
        cv2.circle(imageJ, (xJ, yJ), 7, (255, 255, 255), -1)
        cv2.putText(imageJ, "center", (xJ - 20, yJ - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    #Contour center RGB
    for c in contourR:
        M = cv2.moments(c)
        xR = int(M["m10"] / M["m00"])
        yR = int(M["m01"] / M["m00"])
        cv2.circle(imageR, (xR, yR), 7, (255, 255, 255), -1)
        cv2.putText(imageR, "center", (xR - 20, yR - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    canvasData = imageProcessing.drawCanvas(blankCanvas,xJ,yJ,xR,yR)

    data.sheetSetUp(count, frontSheet, xJ, yJ, xR, yR)
    count += 1
    data.sheetInsert(count, frontSheet, xJ, yJ, xR, yR, range)

    
#Saving sheet
wb.save('Distance between points.xls')
    

