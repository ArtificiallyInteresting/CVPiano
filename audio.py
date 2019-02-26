# import pyaudio
import numpy as np
import time
import pygame
import os

class audio:

    def __init__(self, song=None):
        pygame.init()
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
            sound.set_volume(.3)
            self.sounds[key] = sound
        if song is not None:
            folder = os.getcwd() + "\music\\"
            # sound = pygame.mixer.Sound(folder + song + '.mp3')
            # sound.set_volume(.3)
            pygame.mixer.music.load(folder + song + '.mp3')
            pygame.mixer.music.set_volume(.4)
            pygame.mixer.music.play()


    def setVolume(self, note, volume):
        self.sounds[note].set_volume(volume)

    def startPlaying(self, note):
        print("Playing " + note)
        if note in self.currentlyPlaying:
            return
        self.currentlyPlaying.add(note)
        pygame.mixer.find_channel().play(self.sounds[note], -1)
        # print(self.sounds[note].play(1,1))
    def stopPlaying(self, note):
        if note in self.currentlyPlaying:
            self.sounds[note].stop()
        self.currentlyPlaying.remove(note)
    def stopAll(self):
        for note in self.currentlyPlaying:
            self.sounds[note].stop()
        self.currentlyPlaying = set()
