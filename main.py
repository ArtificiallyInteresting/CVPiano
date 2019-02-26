

import cv2
from util import *
import vision
import audio
from danceMode import *


def main(trackName = None):
    template = getTemplate()
    vc = startWebcamFeed()
    myAudio = audio.audio("bensound-jazzyfrenchy")
    if trackName is not None:
        dance = danceMode(trackName)

    rval, frame = vc.read()
    while rval:
        circles = vision.detectCircles(frame)
        circlesWithTemplates = []
        circlesWithoutTemplates = []
        cv2.line(frame, (0, int(.25*frame.shape[0])), (frame.shape[1]-1,int(.25*frame.shape[0])), (255,0,0))
        cv2.line(frame, (0, int(.75*frame.shape[0])), (frame.shape[1]-1,int(.75*frame.shape[0])), (255,0,0))

        for circle in circles:
            if vision.templateInCircle(frame, template, (circle[0], circle[1]), circle[2]):
                circlesWithTemplates.append(circle)
            else:
                circlesWithoutTemplates.append(circle)
        if len(circlesWithTemplates) > 0:
            vision.drawCircles(frame, circlesWithTemplates, getColor('green'))
        if len(circlesWithoutTemplates) > 0:
            vision.drawCircles(frame, circlesWithoutTemplates, getColor('red'))

        notes = []
        notesDictionary = {}
        for circle in circlesWithTemplates:
            note = vision.getNote(frame, (circle[0], circle[1]), circle[2], "boldFont")
            if note is None:
                continue
            #todo These circles are x,y but the frame is row,col! Fuck!
            # print(circle)
            if (circle[1] < .25*frame.shape[0]):
                note = makeSharp(note)
            elif (circle[1] > .75*frame.shape[0]):
                note = makeFlat(note)
            notes.append(note)
            notesDictionary[note] = (circle[0], circle[1])
            myAudio.setVolume(note, (circle[2] - 25)/(80-25))
        if (len(notes) >= 1):
            print("I see these notes in this frame: " + str(notes))

        myAudio.stopAll()
        for note in notes:
            myAudio.startPlaying(note)
        if trackName is not None:
            dance.onFrame(frame, notesDictionary)
        showFrame(frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    endWebcamFeed()

if __name__ == '__main__':
    # main()
    main("jazz")
    # main("track1")