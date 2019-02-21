import cv2
import numpy as np
from util import *


def detectCircles(image):
    debug = False
    circlesImage = np.zeros(image.shape)
    if debug:
        showImage(image)
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #image, method, dp, minDist, circles=None, param1=None, param2=None, minRadius=None, maxRadius=None
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 30, param1 = 500, param2 = 15, minRadius = 5, maxRadius = 30)
    if (circles is None or len(circles) == 0):
        print("There were no circles")
        return []
    else:
        circles = np.around(circles)
        circles = np.uint16(circles)
        drawCircles(circlesImage, circles)
    if debug:
        showImage(circlesImage)
    return circles

def drawCircles(image, circles):
    for circle in circles[0]:
        cv2.circle(image, (circle[0], circle[1]), circle[2], (255, 255, 255), 1)

def templateInCircle(image, template, location, circleRadius):
    templateRadius = circleRadius * (17.0/150)

    template = cv2.resize(template, (templateRadius*2, templateRadius*2))

    #Instead of the bounding box of the whole circle, let's do half that size. This is an expensive operation
    searchSpace = image[location[0]+.5*circleRadius:location[0]+1.5*circleRadius, location[0]+.5*circleRadius:location[0]+1.5*circleRadius]
    match = cv2.matchTemplate(searchSpace, template, cv2.TM_CCOEFF_NORMED)


    loc = np.where(match >= .6) #todo This should be more automatic.
    return np.any(loc)

    # templateLocations = []
    # for pt in zip(loc[0], loc[1]):
    #     pt = pt[0] + location[0]+.5*circleRadius, location[1]+.5*circleRadius
    #     templateLocations.append((int(pt[0]+width/2),int(pt[1]+height/2)))
    # return templateLocations