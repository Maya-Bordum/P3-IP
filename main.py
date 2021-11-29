import cv2 #Importing openCV2
import numpy as np #Importing numpy for arrays and more
import matplotlib as plt #Importing for showing images in plot
import copy #Importing to copy images to variables
import glob #Importing to acces files in the computer memory
import math #Importing math for calculations


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

    showPicture(image) #Showing RGB image for debugging
    
    #Converting to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) #Converting normal RGB image to HSV image
    showPicture(hsv) #Showing image for debugging

    #Doing color detection
    mask = cv2.inRange(hsv, lower_range, upper_range) #Making a mask with color detection using our upper and lower range HSV values
    showPicture(mask) #Showing image for debugging

    #Making blobs black
    maskBlack = cv2.bitwise_not(mask) #Inverting the colors of the binarized image
    showPicture(maskBlack) #Showing picture for debugging

    #Eroding image
    erodeImage = cv2.erode(maskBlack, kernel, iterations=2) #Eroding image with the kernel created in variables
    showPicture(erodeImage) #Showing image for debugging

    #Setting parameters of the blob detection
    params = cv2.SimpleBlobDetector_Params() #Creating parameter object for the blob detector
    params.filterByArea = True #Making the parameter of using area true
    params.minArea = 50 #Setting minimum area of blob for not detecting smaller mistakes
 
    #Doing blob detection
    detector = cv2.SimpleBlobDetector_create(params) #Creating the blob detector with our parameters
    keypoints = detector.detect(erodeImage) #Using the detector on the eroded image
    image_keypoints = cv2.drawKeypoints(erodeImage, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) #Drawing the circles around the detected blobs
    showPicture(image_keypoints) #Showing the blob detected picture

    # calculate moments of binary image
    M = cv2.moments(mask) #Calculating moments (Read openCV page) from the picture with white blobs

    #Copying cX and cY from last loop
    if count > 0:
        lastX = cX
        lastY = cY

    # calculate x,y coordinate of center by using moments
    cX = int(M["m10"] / M["m00"]) 
    cY = int(M["m01"] / M["m00"])
    # put text and highlight the center
    imageWithCentroid = erodeImage.copy()
    cv2.circle(imageWithCentroid, (cX, cY), 5, (150, 150, 255), -1) #Inserting the center circle

    #Printing the two points for debugging
    print(cX)
    print(cY)


    if count > 0:
        pointDistance = math.sqrt(((cX-lastX)**2)+((cY-lastY)**2))
        print(pointDistance)

    count += 1


    cv2.putText(imageWithCentroid, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 255), 2) #Inserting text over center circle
    showPicture(imageWithCentroid) #Showing image with center circle and text


    

