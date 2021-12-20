import xlwt  # Importing to create excel
import math  # Importing math for calculations


def sheetSetUp(count, frontSheet, xJ, yJ, xR, yR):
    if count == 0:
        # Writing titles in the worksheet
        frontSheet.write(count, count, " ")  # Name title
        frontSheet.write(count, 1, "Xj")  # Coordinate X title
        frontSheet.write(count, 2, "Yj")  # Coordinate Y title
        frontSheet.write(count, 3, "Xr")  # Distance between points title
        frontSheet.write(count, 4, "Yr")  # Distance between points title
        frontSheet.write(count, 5, "Distance between points")  # Distance between points title
        frontSheet.write(count, 6, "Accurate")


def sheetInsert(count, frontSheet, xJ, yJ, xR, yR, range):
    # Measuring the distance between the two points and adding to excel
    if count > 0:
        pointDistance = math.sqrt(((xJ - xR) ** 2) + ((yJ - yR) ** 2) )  # Formula for measuring distance between points
        print(pointDistance)  # Printing distance for debugging
        frontSheet.write(count, 0, "pair" + str(count))  # Image name
        frontSheet.write(count, 1, xJ)  # Image X
        frontSheet.write(count, 2, yJ)  # Image Z
        frontSheet.write(count, 3, xR)
        frontSheet.write(count, 4, yR)
        frontSheet.write(count, 5, pointDistance)  # Point distance
        if pointDistance <= range:
            frontSheet.write(count, 6, "YES")
        if pointDistance > range:
            frontSheet.write(count, 6, "NO")
