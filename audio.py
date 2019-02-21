# import pyaudio
import numpy as np
import time
import pygame
import os

class audio:

    def __init__(self):
        pygame.mixer.init()
        folder = os.getcwd() + "\sounds\piano\\"
        self.currentlyPlaying = set()
        self.sounds = {}
        self.keys = ['A', 'As', 'B', 'C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs']
        for key in self.keys:
            filename = key.lower()
            filename = filename[0] + "1"
            if len(key) == 2:
                filename += 's'
            sound = pygame.mixer.Sound(folder + filename + '.wav')
            sound.set_volume(1)
            self.sounds[key] = sound
    def startPlaying(self, note):
        if note in self.currentlyPlaying:
            return
        self.currentlyPlaying.add(note)
        pygame.mixer.find_channel().play(self.sounds[note], -1)
        # print(self.sounds[note].play(1,1))
    def stopPlaying(self, note):
        if note in self.currentlyPlaying:
            self.currentlyPlaying.remove(note)
            self.sounds[note].stop()

myAudio = audio()
time.sleep(1)
myAudio.startPlaying('C')
myAudio.startPlaying('F')
myAudio.startPlaying('A')

time.sleep(4)
myAudio.stopPlaying('C')
myAudio.startPlaying('Ds')
time.sleep(1)
myAudio.stopPlaying('Ds')