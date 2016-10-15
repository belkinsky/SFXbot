import timeit
from concurrent.futures import ThreadPoolExecutor
import struct
from sys import argv

import wave
import numpy as np
import pyaudio
import sys
import os
import time
SCRIPT_DIR=os.path.dirname(__file__)
sys.path.append(SCRIPT_DIR + "/../pyAudioAnalysis")
from pyAudioAnalysis import audioTrainTest as aT

SAMPLING_RATE = 16000

SIGNIFICANCE = 0.3     # try different values.
NOISE_THRESHOLD = 200

class AudioInput:
    def __init__(self):
        self.chunk_sz = 1024  # samples
        self.format = pyaudio.paInt16
        self.rate = SAMPLING_RATE
        self.channels = 1
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_sz)

    def read_chunk(self):
        data = self.stream.read(self.chunk_sz)
        return data


class ChunkAccumulator:
    def __init__(self, block_sz):
        self.block = None
        self.block_sz = block_sz  # samples

    def accumulate(self, chunk):
        if self.block is None:
            self.block = chunk
        else:
            self.block += chunk

        if len(self.block) >= self.block_sz * 2: # hardcoded sample size = 2
            ret = self.block
            self.block = None
            return ret
        else:
            return None


class BlockQueue:
    def __init__(self, on_fragment_full, slide_step):
        self.queue = []
        self.slide_step = slide_step
        self.on_fragment_full = on_fragment_full

    def add_block(self, block):
        self.queue.append(block)
        if len(self.queue) > self.slide_step * 3:   # Hardcoded const. Number of fragments
            del self.queue[0]
        for i in range(1, 3+1):
            if len(self.queue) >= self.slide_step * i:
                queue_temp = self.queue[-self.slide_step * i:]
                fragment = bytes().join(queue_temp)
                self.on_fragment_full(fragment)



    
def play(sample):
    chunk = 1024
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLING_RATE,
                    output=True)

    # read data
    # data = wf.readframes(CHUNK)
    sample_conv = bytes()
    for i in sample:
        msb = 0xFF & (i >> 8)
        lsb = 0xFF & i
        sample_conv += bytes([lsb])
        sample_conv += bytes([msb])

        if len(sample_conv) >= chunk:
            stream.write(sample_conv)
            # print(sample_conv)
            sample_conv = bytes()

    # play stream (3)
    # while len(data) > 0:

    print("played")
        # data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()

def convert_to_int_list(bytes_chunk):
    l = list(struct.iter_unpack("<h",bytes_chunk))
    return [item for sublist in l for item in sublist]

def background_recognize(fragment_bytes, model_type):
    model_filename = SCRIPT_DIR + "/../data/"+model_type

    try:
        # print("{} Matching fragment {} samples..".format(datetime.datetime.now().time(), len(fragment)))

        fragment = convert_to_int_list(fragment_bytes)

        max_peak = max(abs(i) for i in fragment)

        if max_peak < NOISE_THRESHOLD:
            print("Silence ", max_peak);
            return

        start_time = time.time()
        Result, P, classNames = aT.fragmentClassification(
            Fs=SAMPLING_RATE,
            x=fragment,
            modelName=model_filename,
            modelType=model_type)

        elapsed_time = time.time() - start_time

        winner = np.argmax(P)

        # print("consumed=", elapsed_time)
        # is the highest value found above the isSignificant threshhold?

        if P[winner] > SIGNIFICANCE:
            print("Event detected: " + classNames[winner] + ", with probability: " + str(P[winner]))
            # x = np.fromstring(fragment, np.short)
            x = np.asarray(fragment)
            print(x.tofile('lastDetected.pcm'))
            play(fragment)

        else:
          # print("Can't classify sound: " + str(P))
          # print("But is the winner: " + classNames[winner] + ", with probability: " + str(P[winner]))
          pass

    except Exception as e:
        print(type(e))    # the exception instance
        print(e.args)     # arguments stored in .args
        print(e)
        raise(e)


def main(argv):
    model_type = argv[1]
    executor = ThreadPoolExecutor(max_workers=3)

    def recognize_in_background(fragment):
        executor.submit(background_recognize, fragment, model_type)

    block_queue = BlockQueue(slide_step=2, on_fragment_full=recognize_in_background)
    audio_input = AudioInput()
    min_frag_sz = 1
    block_size = min_frag_sz * (audio_input.rate / block_queue.slide_step)
    accumulator = ChunkAccumulator(block_size)
    while True:
        chunk = audio_input.read_chunk()
        block = accumulator.accumulate(chunk)
        if block is not None:
            block_queue.add_block(block)




main(argv)

# stream.stop_stream()
# stream.close()
# p.terminate()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()
