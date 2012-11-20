#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os, itertools, json, wave, audioop

from pygame.mixer import Sound

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, 'samples')

# proof of concept - reversed samples
#def reverse_wav_file(file_path):
#    """
#        Flips wave file on given path and saves it
#    """
#    reversed_file = file_path + '_r.wav'
#    if os.path.exists(reversed_file):
#        return reversed_file
#
#    with open(file_path, 'r') as f, open(reversed_file, 'w') as fr:
#        f = wave.open(f)
#        frames = f.getnframes()
#        data = f.readframes(frames)
#        reversed = audioop.reverse(data, 2) # '2' is the sample width
#        fr = wave.open(fr)
#        # Must set params but leave # of frames empty
#        fr.setparams((2, 2, 44100, '', 'NONE', 'not compressed'))
#        fr.writeframesraw(reversed)
#    return reversed_file


def SoundBank(object):
    def __init__(self):
        pass


def _make_sample(slot):
    """
        Makes Sound instances tuple and sets Sound volumes
    """
    global SAMPLES_DIR
    sample_file = os.path.join(SAMPLES_DIR, slot['sample'])
    sample = Sound(sample_file)
    sample.set_volume(slot.get('volume', 100) / 100.0)
    return sample

def load_banks(bank_kit):
    """
        Loads bank kit definition from file and populates banks
        with Sound instances (both original wave & reversed one)
    """
    global BASE_DIR
    fname = os.path.join(BASE_DIR, 'banks', '%s.json' % bank_kit)

    try:
        banks = json.load(open(fname))

        iter_data = []
        i = 0
        for bank in banks:
            i += 1
            bank_data = {}
            for key, slot in bank.iteritems():
                if slot['sample']:
                    bank_data[key] = _make_sample(slot)
            iter_data.append((bank, bank_data, i))

        iterator = itertools.cycle(iter_data)

        return iterator
    except IOError, e:
        return None
