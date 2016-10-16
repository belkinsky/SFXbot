import timeit
from concurrent.futures import ThreadPoolExecutor
import struct
from sys import argv
import pygame
import wave
import numpy as np
import pyaudio
import sys
import os
import time
import select
import random
SCRIPT_DIR=os.path.dirname(__file__)
sys.path.append(SCRIPT_DIR + "/../pyAudioAnalysis")
from pyAudioAnalysis import audioTrainTest as aT

SAMPLING_RATE = 16000

SIGNIFICANCE = 0.9     # try different values.
NOISE_THRESHOLD = 200
screen_size = 800, 500
screen = pygame.display.set_mode(screen_size)

black = 0, 0, 0
white = 255, 255, 255
blue = 0, 0, 255
green = 128, 255, 128
red = 255, 0, 0
violet = 255, 0, 255
yellow = 255, 255, 0
pink = 252, 15, 192

response_dict = {"привет": SCRIPT_DIR + "/../data/responses/privet",
                 "будьте здоровы": SCRIPT_DIR + "/../data/responses/spasibo",
                 "доброе утро": SCRIPT_DIR + "/../data/responses/dobroe_utro",
                 "добрый вечер": SCRIPT_DIR + "/../data/responses/dobry_vecher",
                 "спасибо": SCRIPT_DIR + "/../data/responses/spasibo"}


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
        data = convert_to_int_list(data)
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
                fragment = flatten(queue_temp)
                self.on_fragment_full(fragment)


def play_wav(filename):
    # length of data to read.
    chunk = 1024

    # validation. If a wave file hasn't been specified, exit.
    # if len(sys.argv) < 2:
    #     print("Plays a wave file.\n\n" + "Usage: %s filename.wav" % sys.argv[0])
    #     sys.exit(-1)

    #   open the file for reading.

    wf = wave.open(filename, 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while data != b'':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)


def flatten(concat_list):
    return [item for sublist in concat_list for item in sublist]


def convert_to_int_list(bytes_chunk):
    l = list(struct.iter_unpack("<h", bytes_chunk))
    return [item for sublist in l for item in sublist]


def background_recognize(fragment, model_type):
    model_filename = SCRIPT_DIR + "/../data/"+model_type

    try:
        # print("{} Matching fragment {} samples..".format(datetime.datetime.now().time(), len(fragment)))

        max_peak = max(abs(i) for i in fragment)

        if max_peak < NOISE_THRESHOLD:
            print("Silence ", max_peak)
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
            pass
            # print("Event detected: " + classNames[winner] + ", with probability: " + str(P[winner]))
            # x = np.fromstring(fragment, np.short)
            # x = np.asarray(fragment)
            # print(x.tofile('lastDetected.pcm'))
            # play(fragment)

        else:
          # print("Can't classify sound: " + str(P))
          # print("But is the winner: " + classNames[winner] + ", with probability: " + str(P[winner]))
          pass

    except Exception as e:
        print(type(e))    # the exception instance
        print(e.args)     # arguments stored in .args
        print(e)
        raise()


def draw(chunk, i):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    max_chunk = max(chunk)
    min_chunk = min(chunk)
    pygame.draw.rect(screen, black, [i, 0, 10, screen_size[1]])
    pygame.draw.line(screen, green, (0, screen_size[1]/2), (screen_size[0], screen_size[1]/2), 3)
    pygame.draw.line(screen, green, (i, screen_size[1]/2 + max_chunk/50), (i, screen_size[1]/2 + min_chunk/50))
    pygame.display.update()


def get_char(block=True):
    if block or select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)
    raise('NoChar')


def handle_speech(line):
    if response_dict.get(line) is not None:
        to_play = random.choice(os.listdir(response_dict[line]))
        play_wav(response_dict[line]+"/"+to_play)
    else:
        pass


def read_file(file):
    for line in file:
        handle_speech(line.rstrip())
        print(line)


def main(argv):
    pygame.init()
    model_type = argv[1]
    executor = ThreadPoolExecutor(max_workers=3)
    iter = 0
    string_temp = 0
    sphinks_result = open(SCRIPT_DIR + "/../data/sphinx_speech", 'r', encoding='utf-8')

    def recognize_in_background(fragment):
        executor.submit(background_recognize, fragment, model_type)

    block_queue = BlockQueue(slide_step=2, on_fragment_full=recognize_in_background)
    audio_input = AudioInput()
    min_frag_sz = 1
    block_size = min_frag_sz * (audio_input.rate / block_queue.slide_step)
    accumulator = ChunkAccumulator(block_size)
    while True:
        read_file(sphinks_result)
        chunk = audio_input.read_chunk()
        draw(chunk, iter)
        iter += 1
        if iter > screen_size[0]:
            iter = 0
        block = accumulator.accumulate(chunk)
        if block is not None:
            block_queue.add_block(block)


main(argv)
