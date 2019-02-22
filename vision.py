import cv2
import numpy as np
from util import *


def detectCircles(image):
    debug = False
    if debug:
        circlesImage = np.zeros(image.shape)
        showImage(image)
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    #image, method, dp, minDist, circles=None, param1=None, param2=None, minRadius=None, maxRadius=None
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 50, param1 = 300, param2 = 45, minRadius = 15, maxRadius = 300)
    if (circles is None or len(circles) == 0):
        return []
    else:
        circles = np.around(circles)
        circles = np.uint16(circles)
        circles = circles[0]
        if debug:
            print("I found " + str(len(circles)) + " circles")
    if debug:
        drawCircles(circlesImage, circles, getColor('red'))
        showImage(circlesImage)
    return circles

def drawCircles(image, circles, color=(255,255,255)):
    for circle in circles:
        cv2.circle(image, (circle[0], circle[1]), circle[2], color, 1)


#todo Quite a bit of overlap between this and template matching. We should make it more generic.
def getNote(image, location, circleRadius, font="boldFont"):
    fontRadius = 1
    if font == "boldFont":
        fontRadius = 17.0
    if font == "curlyFont":
        fontRadius = 13.0
    if font == "originalFont":
        fontRadius = 5.5
    letterRadius = circleRadius * (fontRadius/37)
    maxScore = -1
    maxLetter = "Z"
    searchSpace = image[int(location[1] - circleRadius):int(location[1]),
                  int(location[0] - .8 * circleRadius):int(location[0] + .8 * circleRadius)]
    # showImage(searchSpace)
    for letter in getLetters():
        letterImage = load(letter, font)
        newShape = int(letterRadius*2), int(letterRadius*2 * (letterImage.shape[0]/letterImage.shape[1]))
        letterImage = cv2.resize(letterImage, newShape)
        # showImage(letterImage)
        try:
            match = cv2.matchTemplate(searchSpace, letterImage, cv2.TM_CCOEFF_NORMED)
        except:  # If it failed, then we were probably just out of bounds or whatever
            # todo better error checking.
            return None
        score = np.max(match)
        # print("Letter " + letter + " scored " + str(score))
        if score > maxScore:
            if letter == 'C':
                letter = 'Cs'
            if letter == 'D':
                letter = 'Ds'
            maxLetter = letter
            maxScore = score
    return maxLetter


def templateInCircle(image, template, location, circleRadius):
    #remember that both image and location are row/col
    if circleRadius < 1.0:
        return False #todo figure out why this is happening in the first place. Circles come in as [0,0,0] sometimes.
    templateRadius = circleRadius * (4.2/37)
    template = cv2.resize(template, (int(templateRadius*2), int(templateRadius*2)))

    #Instead of the bounding box of the whole circle, let's do half that size. This is an expensive operation
    searchSpace = image[int(location[1]-.5*circleRadius):int(location[1]+.5*circleRadius), int(location[0]-.5*circleRadius):int(location[0]+.5*circleRadius)]
    try:
        match = cv2.matchTemplate(searchSpace, template, cv2.TM_CCOEFF_NORMED)
    except: #If it failed, then we were probably just out of bounds or whatever
        #todo better error checking.
        return False
    loc = np.where(match >= .7) #todo This should be more automatic.
    return np.any(loc)
