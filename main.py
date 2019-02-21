print("Hello World")

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
        for circle in circles:
            if vision.templateInCircle(frame, template, (circle[1], circle[2]), circle[0]):#todo double check these circle params
                circlesWithTemplates.append(circle)
        if len(circlesWithTemplates) > 0:
            vision.drawCircles(frame, circlesWithTemplates)

        showFrame(frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    endWebcamFeed()

if __name__ == '__main__':
    main()