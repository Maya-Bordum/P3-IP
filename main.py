import cv2 #Importing openCV2
import numpy as np #Importing numpy for arrays and more
import matplotlib as plt #Importing for showing images in plot
import copy #Importing to copy images to variables
import glob #Importing to acces files in the computer memory
import math #Importing math for calculations
import xlwt #Importing to create excel 
from xlwt import Workbook
import imutils


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

#Variables for upper and lower range in color detection Hue, Saturation and Value
lower_range = np.array([15,80,80])
upper_range = np.array([40,255,255])

#percent by which the image is resized
scale_percent = 25

#Creating kernel for OpenCV functions
kernel = np.array([[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]],np.uint8)

#Count variable
count = 0

#Creating workbook with sheet
wb = Workbook() #Creating workbook
frontSheet = wb.add_sheet("Data Sheet")


#Loading an array of pictures
Pictures = [] #Creating an array
files = glob.glob ("pictures\\*.jpg") #Adding dirrectory to files

#Loop for loading files from directory to the Pictures array
for myFile in files:
    image = cv2.imread(myFile) #Reading file as cv2 image
    Pictures.append(image) #Adding the read image to Pictures Array

    
for image in Pictures:
    #Resizing image
    width = int(image.shape[1] * scale_percent / 100) #calculate the 50 percent of original dimension widht
    height = int(image.shape[0] * scale_percent / 100) #calculate the 50 percent of original dimension height
    dsize = (width, height) #Width and height together
    image = cv2.resize(image, dsize)#Resize image
    #showPicture(image) #Showing RGB image for debugging
    
    #Converting to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #Converting normal RGB image to HSV image
    #showPicture(hsv) #Showing image for debugging

    #Doing color detection
    mask = cv2.inRange(hsv, lower_range, upper_range) #Making a mask with color detection using our upper and lower range HSV values
    #showPicture(mask) #Showing image for debugging

    #Dilate white blobs
    dilateImage = cv2.dilate(mask,kernel,iterations=2)
    #showPicture(dilateImage)

    # calculate moments of binary image
    M = cv2.moments(dilateImage) #Calculating moments (Read openCV page) from the picture with white blobs

    #Copying cX and cY from last loop
    if count > 0:
        lastX = cX
        lastY = cY

    # calculate x,y coordinate of center by using moments
    cX = int(M["m10"] / M["m00"]) 
    cY = int(M["m01"] / M["m00"])

    # put text, highlight the center and calculate distance between two points
    imageWithCentroid = image.copy()
    cv2.circle(imageWithCentroid, (cX, cY), 5, (0, 0, 0), -1) #Inserting the center circle

    #Printing the two points for debugging
    print(cX)
    print(cY)

    #Setting up excel
    if count == 0:
        #Writing titles in the worksheet
        frontSheet.write(count,count, 'Image Name') #Name title
        frontSheet.write(count,1,'X') #Coordinate X title
        frontSheet.write(count,2,'Y') #Coordinate Y title
        frontSheet.write(count,3,'Distance point last image') #Distance between points title
        frontSheet.write(count+1,0, 'pic' + str(count)) #First image name
        frontSheet.write(count+1,1, cX) #First image X
        frontSheet.write(count+1,2, cY) #First image Y
        frontSheet.write(count+1,3, 'NoDistance') #No distance from first picture

    #Measuring the distance between the two points and adding to excel
    if count > 0:
        pointDistance = math.sqrt(((cX-lastX)**2)+((cY-lastY)**2)) #Formula for measuring distance between points
        print(pointDistance) #Printing distance for debugging
        frontSheet.write(count+1,0, 'pic' + str(count)) #Image name
        frontSheet.write(count+1,1, cX) #Image X
        frontSheet.write(count+1,2, cY) #Image Z
        frontSheet.write(count+1,3, pointDistance) #Point distance

    cnts = cv2.findContours(dilateImage.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # loop over the contours
    for c in cnts:
	    # compute the center of the contour
	    Q = cv2.moments(c)
	    cAX = int(Q["m10"] / Q["m00"])
	    cAY = int(Q["m01"] / Q["m00"])
	    # draw the contour and center of the shape on the image
	    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	    cv2.circle(image, (cAX, cAY), 7, (255, 255, 255), -1)
	    cv2.putText(image, "center", (cAX - 20, cAY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    showPicture(image)

    #Increaing count to know which loop we are in 
    count += 1

    cv2.putText(imageWithCentroid, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2) #Inserting text over center circle
    showPicture(imageWithCentroid) #Showing image with center circle and text

wb.save('Distance between points.xls')


    

