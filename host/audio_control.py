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
import sounddevice as sd
import soundfile as sf
# import numpy as np

filename = "kickflip_eyepopping.wav"
device_num = 4

parser = argparse.ArgumentParser(add_help=False)

event = threading.Event()

try:
    data, fs = sf.read(filename)

    current_frame = 0

    def callback(outdata, frames, time, status):
        global current_frame
        if status:
            print(status)
        chunksize = min(len(data) - current_frame, frames)
        outdata[:chunksize] = data[current_frame:current_frame + chunksize]
        if chunksize < frames:
            outdata[chunksize:] = 0
            raise sd.CallbackStop
        current_frame += chunksize

    stream = sd.OutputStream(
        samplerate=fs, device=device_num, channels=data.shape[1],  
        callback=callback, finished_callback=event.set)
    
    # plays the audio
    with stream:
        event.wait()

except KeyboardInterrupt:
    print("Interrupted by user")
    parser.exit(1, "Interrupted by user")
except Exception as e:
    print("Crashed")
    parser.exit(1, type(e).__name__ + ': ' + str(e))
