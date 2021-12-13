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

def resizeImage(image, scale_percent):
    #Resizing image
    width = int(image.shape[1] * scale_percent / 100) #calculate the 50 percent of original dimension widht
    height = int(image.shape[0] * scale_percent / 100) #calculate the 50 percent of original dimension height
    dsize = (width, height) #Width and height together
    image = cv2.resize(image, dsize)#Resize image
    return image

def flipImage(image):
    image = cv2.flip(image, 0)
    return image
    

def hsvConvert(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #Converting normal RGB image to HSV image
    return image

def colorDetection(image, lower, upper):
    image = cv2.inRange(image, lower, upper) #Making a mask with color detection using our upper and lower range HSV values
    return image

def dilateImage(image, kernel, iteration):
    image = cv2.dilate(image,kernel,iterations=iteration)
    return image

def findContours(image):
    contours = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
    return cnts

def backGround(image):
    blank = np.zeros((image.shape[0], image.shape[1], 1), dtype = "uint8")
    return blank

def drawCanvas(canvas, xJ, yJ, xR, yR):
    cv2.circle(canvas, (xR, yR), 7, (255, 255, 255), -1)
    cv2.putText(canvas, "RGB", (xR - 20, yR - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.circle(canvas, (xJ, yJ), 7, (255, 255, 255), -1)
    cv2.putText(canvas, "Kinectr", (xJ - 20, yJ - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return canvas

#Find radius of circle with area of specific contour
def findRadius(contour):
    area = cv2.contourArea(contour[0]) #Finding area of contour with OpenCV2 function
    radius = math.sqrt(area/math.pi)
    return radius
    
    
    
    

    
    



    
    