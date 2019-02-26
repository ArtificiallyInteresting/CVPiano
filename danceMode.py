

import cv2
from util import *
import vision
import audio
import time

class danceMode:
    def __init__(self, trackname):
        self.startTime = time.time()
        self.bpm = 60 #todo this should come from the track file.
        self.beatsDone = 0
        self.notes = []
        self.score = 0
        with open(trackname + ".txt", 'r') as fp:
            for line in fp:
                #command, time, x, y
                command = line.split()
                for i in range(int(command[1])):
                    if len(command) == 2:
                        self.notes.append([command[0]])
                    else:
                        self.notes.append([command[0], command[2], command[3]])

    def onFrame(self, frame, notes):
        now = time.time()
        if (now - self.startTime) / (60.0/self.bpm) > self.beatsDone + 1:
            #Onto a new beat.
            self.beatsDone += 1
            print("Beat: " + str(self.beatsDone))
            if self.notes[self.beatsDone][0] in notes:
                self.score += 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = 'Score: ' + str(self.score)# + " Play next: " + self.notes[self.beatsDone+1][0]
        #img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]
        cv2.putText(frame, text, (10, 450), font, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        textColor = (0,255,255)
        if (self.notes[self.beatsDone+1][0] == self.notes[self.beatsDone][0]):
            #Next note is the same as this one
            textColor = (0,255,0)
        if (self.notes[self.beatsDone+1][0] != 'wait'):
            x,y = int(self.notes[self.beatsDone+1][1]), int(self.notes[self.beatsDone+1][2])
            cv2.circle(frame, (x,y), 40, textColor, 1)
            cv2.putText(frame, self.notes[self.beatsDone+1][0], (x-15,y+15), font, 1.5, textColor, 2, cv2.LINE_AA)

