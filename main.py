

import cv2
from util import *
import vision


def main():
    template = getTemplate()
    vc = startWebcamFeed()
    rval, frame = vc.read()
    while rval:
        circles = vision.detectCircles(frame)
        circlesWithTemplates = []
        circlesWithoutTemplates = []

        for circle in circles:
            if vision.templateInCircle(frame, template, (circle[0], circle[1]), circle[2]):#todo double check these circle params
                circlesWithTemplates.append(circle)
            else:
                circlesWithoutTemplates.append(circle)
        if len(circlesWithTemplates) > 0:
            vision.drawCircles(frame, circlesWithTemplates, getColor('green'))
        if len(circlesWithoutTemplates) > 0:
            vision.drawCircles(frame, circlesWithoutTemplates, getColor('red'))

        notes = []
        for circle in circlesWithTemplates:
            notes.append(vision.getNote(frame, (circle[0], circle[1]), circle[2]))
        print("I see these notes in this frame: " + str(notes))
        showFrame(frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    endWebcamFeed()

if __name__ == '__main__':
    main()