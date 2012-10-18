#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, itertools, json, wave

import audioop
from pygame.mixer import Sound

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, 'samples')

def reverse_wav_file(file_path):
    """
        Flips wave file on given path and saves it
    """
    reversed_file = file_path + '_r.wav'
    if os.path.exists(reversed_file):
        return reversed_file

    with open(file_path, 'r') as f:
        f = wave.open(f)
        frames = f.getnframes()
        data = f.readframes(frames)
        reversed = audioop.reverse(data, 2) # '2' is the sample width
        with open(reversed_file, 'w') as fr:
            fr = wave.open(fr)
            # Must set params but leave # of frames empty
            fr.setparams((2, 2, 44100, '', 'NONE', 'not compressed'))
            fr.writeframesraw(reversed)
    return reversed_file


def load_banks(bank_kit):
    """
        Loads bank kit definition from file and populates banks
        with Sound instances (both original wave & reversed one)
    """
    file = os.path.join(BASE_DIR, 'banks', '%s.json' % bank_kit)
    try:
        with open(file) as f:
            banks = json.load(f)
            iter = itertools.cycle([{k: (Sound(os.path.join(SAMPLES_DIR, v)),
                                         Sound(reverse_wav_file(os.path.join(SAMPLES_DIR, v))))
                                     for k, v in bank.iteritems() if v} for bank in banks])
            return banks, iter
    except IOError:
        return None, None