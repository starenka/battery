#!/usr/bin/env python
import curses
import argparse
import sys
import time
import threading
import itertools
import Queue

import pygame

from utils import load_banks
import cui


VERSION = 0.2
# That's all what MaKeyMaKey has in stock setting, except 'SPC' and 'w'
AVAILABLE_KEYS = 'LEFT RIGHT DOWN UP a s d f g h j'.split()
KEYS = dict(
    [(getattr(curses, 'KEY_%s' % key, ord(key[0])), key) for key in AVAILABLE_KEYS])


def parse_args():
    parser = argparse.ArgumentParser('Battery - a simple CLI & headless rompler')
    parser.add_argument('-b', '--bank-kit', action='store', dest='bank_kit', default='default')
    return parser.parse_args()

def init_mixer():
    # We need to init mixer before pygame initializations, smaller buffer should avoid lags
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.mixer.set_num_channels(8 * len(KEYS)) # Get 8 channels for each key

class MusicThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.q = Queue.Queue()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.q.get().play()

    def stop(self):
        self.running = False

class LoopThread(threading.Thread):
    def __init__(self, music_thread):
        threading.Thread.__init__(self)
        self.mt = music_thread
        self.loop = []
        self.running = False

    def run(self):
        self.mt.q.put(self.loop.next()[1])
#        try:
#            self.mt.q.put(self.loop.next()[1])
#        except StopIteration:
#            return

        self.running = True
        while self.running:
            sleep_time, sample = self.loop.next()
            time.sleep(sleep_time)
            self.mt.q.put(sample)

    def stop(self):
        self.running = False



if __name__ == "__main__":
    init_mixer()
    args = parse_args()

    banks_iter = load_banks(args.bank_kit)
    if not banks_iter:
        sys.exit('Can\'t load bank kit file "%s"' % args.bank_kit)

    bank_desc, bank_samples, bank_nr = banks_iter.next()

    cui = cui.CUI(VERSION)
    cui.show_bank(bank_desc, bank_nr)

    m_thread = MusicThread()
    m_thread.daemon = True
    m_thread.start()


    LOOP_recording = False
    LOOPS = []

    while True:
        event = cui.screen.getch()

        if event in (ord('q'), 27): #q or ESC
            break

        elif event == ord(' '): # switch bank on SPACE
            bank_desc, bank_samples, bank_nr = banks_iter.next()
            cui.show_bank(bank_desc, bank_nr)
            continue

        elif event == ord('r'): # start/stop recording new loop
            t = time.time()
            if LOOP_recording is False: #start new loop
                lt = LoopThread(m_thread)
                lt.daemon = True
                LOOPS.append(lt)
            else:
                try:
                    end_time = LOOPS[-1].loop[-1][0]
                except IndexError:
                    del(LOOPS[-1])
                    LOOP_recording = not LOOP_recording
                    continue

                #re-count the times to relative differences
                for i in range(len(LOOPS[-1].loop)-1, 0 , -1):
                    LOOPS[-1].loop[i][0] -= LOOPS[-1].loop[i-1][0]

                LOOPS[-1].loop[0][0] = t - end_time
                f = open("out.dat", "w")
                f.write(str(LOOPS[-1].loop))
                f.close()
                LOOPS[-1].loop = itertools.cycle(LOOPS[-1].loop)
                LOOPS[-1].start()
            LOOP_recording = not LOOP_recording

        elif event == ord('p'): # purge all loops
            for loop in LOOPS:
                loop.stop()

            LOOPS = []

        try:
            t = time.time()
            key = KEYS[event]
            try:
                sample = bank_samples[key]
                if LOOP_recording:
                    LOOPS[-1].loop.append([time.time(), sample])
                m_thread.q.put(sample)
            except KeyError:
                cui.tray_msg('No sample defined for "%s" key\n' % key, row=1, style=curses.A_DIM)
        except KeyError:
            pass

    # This should somehow restore terminal back, but it doesn't work all the time.
    # Call "reset" in your shell if you need to
    curses.endwin()
    sys.exit(0)
