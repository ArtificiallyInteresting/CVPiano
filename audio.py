import pyaudio
import numpy as np
import time
import pygame

class audio:

    def __init__(self):
        self.currentlyPlaying = set()
        self.sounds = {}
        self.keys = ['A', 'As', 'B', 'C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs']
        for key in self.keys:
            filename = key.toLower()
            filename = filename[0] + "1"
            if len(key) == 2:
                filename += s
            sound = pygame.mixer.Sound('sounds/piano/' + filename + '.wav')
            self.sounds[key] = sound
    def startPlaying(self, note):
        if note in self.currentlyPlaying:
            return
        self.currentlyPlaying.add(note)
        self.sounds[key].play(-1)
    def stopPlaying(self, note):
        if note in self.currentlyPlaying:
            self.currentlyPlaying.remove(note)
            self.sounds[key].stop()

myAudio = audio()
audio.startPlaying('C')
time.sleep(1)
audio.stopPlaying('C')
audio.startPlaying('Ds')
time.sleep(1)
audio.stopPlaying('Ds')



#
#
# p = pyaudio.PyAudio()
# # define callback (2)
# def callback(in_data, frame_count, time_info, status):
#     print("data: " + str(in_data))
#     print("frame count: " + str(frame_count))
#     print("time: " + str(time_info))
#     print("status: " + str(status))
#     volume = 0.5     # range [0.0, 1.0]
#     fs = 44100       # sampling rate, Hz, must be integer
#     duration = .05 #time_info['output_buffer_dac_time'] - time_info['current_time']   # in seconds, may be float
#     f = 440.0        # sine frequency, Hz, may be float
#
#     # generate samples, note conversion to float32 array
#     samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
#     return (samples, pyaudio.paContinue)
#
# # # open stream using calalback (3)
# # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
# #                 channels=wf.getnchannels(),
# #                 rate=wf.getframerate(),
# #                 output=True,
# #                 stream_callback=callback)
# #
# # # start the stream (4)
# # stream.start_stream()
# #
# # # wait for stream to finish (5)
# # while stream.is_active():
# #     time.sleep(0.1)
# #
# # # stop stream (6)
# # stream.stop_stream()
# # stream.close()
# # wf.close()
# #
# # # close PyAudio (7)
# # p.terminate()
#
#
#
#
#
# ###OLD
# volume = 0.5     # range [0.0, 1.0]
# fs = 44100       # sampling rate, Hz, must be integer
# duration = 10.0   # in seconds, may be float
# f = 440.0        # sine frequency, Hz, may be float
#
# # generate samples, note conversion to float32 array
# samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
#
# # for paFloat32 sample values must be in range [-1.0, 1.0]
# stream = p.open(format=pyaudio.paFloat32,
#                 channels=1,
#                 rate=fs,
#                 output=True,
#                 stream_callback=callback,
#                 frames_per_buffer=4096)
#
# # play. May repeat with different volume values (if done interactively)
# # stream.write(volume*samples)
# time.sleep(1)
# stream.stop_stream()
# stream.close()
#
# p.terminate()