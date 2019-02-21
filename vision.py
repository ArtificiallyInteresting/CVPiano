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
    # edges = cv2.Canny(image,300,150,apertureSize = 3)
    # showImage(edges)
    #image, method, dp, minDist, circles=None, param1=None, param2=None, minRadius=None, maxRadius=None
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20, param1 = 300, param2 = 55, minRadius = 15, maxRadius = 300)
    if (circles is None or len(circles) == 0):
        # print("There were no circles")
        return []
    else:
        circles = np.around(circles)
        circles = np.uint16(circles)
        circles = circles[0]
        # correctedCircles = []
        # for circle in circles[0]:
        #     print(circle[0])
        #     correctedCircles.append(circle[0]) #It's a weird format, circles is a list of lists of lists. Fuck logic.
        # circles = correctedCircles
        # print("I found " + str(len(circles)) + " circles")
        drawCircles(circlesImage, circles, getColor('red'))
    if debug:
        showImage(circlesImage)
    return circles

def drawCircles(image, circles, color=(255,255,255)):
    for circle in circles:
        cv2.circle(image, (circle[0], circle[1]), circle[2], color, 1)

def getNote(image, location, circleRadius):
    letterRadius = circleRadius * (6.0/37)
    maxScore = -1
    maxLetter = "Z"
    searchSpace = image[int(location[1] - circleRadius):int(location[1]),
                  int(location[0] - .5 * circleRadius):int(location[0] + .5 * circleRadius)]

    # showImage(searchSpace)
    for letter in getLetters():
        letterImage = load(letter)
        # showImage(letterImage)
        letterImage = cv2.resize(letterImage, (int(letterRadius*2), int(letterRadius*2)))

        #Upper half, near the center
        # searchSpace = image[int(location[0] - circleRadius):int(location[0]),
        #               int(location[0] + .5 * circleRadius):int(location[0] + 1.5 * circleRadius)]
        try:
            # showImage(searchSpace)
            # showImage(letterImage)
            match = cv2.matchTemplate(searchSpace, letterImage, cv2.TM_CCOEFF_NORMED)
        except:  # If it failed, then we were probably just out of bounds or whatever
            # todo better error checking.
            return False
        score = np.max(match)
        print("Letter " + str(letter) + " scored " + str(score))
        if score > maxScore:
            maxLetter = letter
            maxScore = score
    return maxLetter


def templateInCircle(image, template, location, circleRadius):
    #remember that both image and location are row/col
    if circleRadius < 1.0:
        return False #todo figure out why this is happening in the first place. Circles come in as [0,0,0] sometimes.
    templateRadius = circleRadius * (4.2/37)
    # showImage(template)
    template = cv2.resize(template, (int(templateRadius*2), int(templateRadius*2)))
    # showImage(template)

    #Instead of the bounding box of the whole circle, let's do half that size. This is an expensive operation
    # searchSpace = image[int(location[0]+.5*circleRadius):int(location[0]+1.5*circleRadius), int(location[0]+.5*circleRadius):int(location[0]+1.5*circleRadius)]
    searchSpace = image[int(location[1]-.5*circleRadius):int(location[1]+.5*circleRadius), int(location[0]-.5*circleRadius):int(location[0]+.5*circleRadius)]
    # showImage(searchSpace)
    try:
        match = cv2.matchTemplate(searchSpace, template, cv2.TM_CCOEFF_NORMED)
    except: #If it failed, then we were probably just out of bounds or whatever
        #todo better error checking.
        return False
    # print("The best match I saw was " + str(np.max(match)))
    loc = np.where(match >= .4) #todo This should be more automatic.
    return np.any(loc)

    # templateLocations = []
    # for pt in zip(loc[0], loc[1]):
    #     pt = pt[0] + location[0]+.5*circleRadius, location[1]+.5*circleRadius
    #     templateLocations.append((int(pt[0]+width/2),int(pt[1]+height/2)))
    # return templateLocations