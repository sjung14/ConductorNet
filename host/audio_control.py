'''
1. Find audio file with filename in directory
2. Make numpy array from audio file
3. Get packets over wifi
3. Call back function
    a. Modify Numpy array with info over wifi (from wand)
    b. Play short interval of audio
        (smaller than hardware frames, ideally IMU sample rate)
    c. when song ends, stop call back
'''

import argparse
import threading    # will act like a flag
# import sounddevice as sd
# import soundfile as sf
# import numpy as np
import math
import sys
import pyaudio
import audiotsm
from audiotsm.io.wav import WavReader
from audiotsm.io.stream import StreamWriter
from audiotsm import phasevocoder


class AudioControl:
    def __init__(self):
        self.filename = "kickflip_eyepopping.wav"
        self.speed = 1.0
        self.tsm = None
        self.thread = None
        self.ready = threading.Event()

    def change_speed(self, val):
        if not self.ready.is_set():
            return
        self.tsm.set_speed(val)

    def stream_audio(self):
        with WavReader(self.filename) as reader:
            with StreamWriter(reader.channels, reader.samplerate) as writer:

                self.tsm = phasevocoder(reader.channels, speed=1.0)

                self.ready.set()

                self.tsm.run(reader, writer)

    def start(self):
        self.thread = threading.Thread(target=self.stream_audio, daemon=True)
        self.thread.start()
    
    

    
