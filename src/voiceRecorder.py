import timeit
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pyaudio
import datetime
import sys
import os
import time
sys.path.append(os.path.dirname(__file__) + "/../pyAudioAnalysis")
from pyAudioAnalysis import audioTrainTest as aT

SAMPLING_RATE = 16000
SIGNIFICANCE = 0.6 #try different values.


class AudioInput:
    def __init__(self):
        self.chunk_sz = 1024
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
        self.block_sz = block_sz

    def accumulate(self, chunk):
        if self.block is None:
            self.block = chunk
        else:
            self.block += chunk

        if len(self.block) >= self.block_sz:
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
                fragment = [item for sublist in queue_temp for item in sublist]
                self.on_fragment_full(fragment)


def background_recognize(fragment):

    try:
        print("{} Matching fragment {} samples..".format(datetime.datetime.now().time(), len(fragment)))

        start_time = time.time()
        Result, P, classNames = aT.fragmentClassification(
            Fs=SAMPLING_RATE,
            x=fragment,
            modelName="..\svmModel",
            modelType="svm")

        elapsed_time = time.time() - start_time

        winner = np.argmax(P)

        print("consumed=", elapsed_time)
        # is the highest value found above the isSignificant threshhold?
        if P[winner] > SIGNIFICANCE :
          print("File:  is in category: " + classNames[winner] + ", with probability: " + str(P[winner]))
        else :
          print("Can't classify sound: " + str(P))
          print("But is the winner: " + classNames[winner] + ", with probability: " + str(P[winner]))
    except Exception as e:
        print(type(e))    # the exception instance
        print(e.args)     # arguments stored in .args
        print(e)


def main():
    executor = ThreadPoolExecutor(max_workers=3)

    def recognize_in_background(fragment):
        executor.submit(background_recognize, fragment)

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

main()

# stream.stop_stream()
# stream.close()
# p.terminate()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()
