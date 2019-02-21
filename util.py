import cv2
import os
import numpy as np

sharps = {
    "A": "As",
    "As": "B",
    "B": "C",
    "C": "Cs",
    "Cs": "D",
    "D": "Ds",
    "Ds": "E",
    "E": "F",
    "F": "Fs",
    "Fs": "G",
    "G": "Gs",
    "Gs": "A"
}

flats = {v: k for k, v in sharps.items()}



def load(filename):
    image = cv2.imread(os.getcwd() + '/inputImages/' + filename + '.jpg', cv2.IMREAD_UNCHANGED)
    # showImage(image)
    return image

def showImage(img_in, img_name='image'):
    cv2.imshow(img_name, img_in)
    cv2.waitKey(0)
    cv2.destroyWindow(img_name)
    return

def showFrame(frame, name='preview'):
    cv2.imshow(name, frame)

def startWebcamFeed(name='preview'):
    cv2.namedWindow(name)
    vc = cv2.VideoCapture(0)

    if not vc.isOpened():
        raise RuntimeError("No webcam found or webcam is busy.")

    return vc


def endWebcamFeed(name='preview'):
    cv2.destroyWindow(name)

def getTemplate():
    return load("centerMarkingSquare")

def getColor(name):
    if name == 'red':
        return (0,0,255)
    if name == 'green':
        return (0,255,0)
    if name == 'blue':
        return (255,0,0)
    if name == 'black':
        return (255,255,255)

def getLetters():
    return ["A","B","C","D","E","F","G"]

def makeSharp(note):
    return sharps[note]

def makeFlat(note):
    return flats[note]