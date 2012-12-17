#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os, itertools, json, wave, audioop

from pygame.mixer import Sound

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, 'samples')

def reverse_wav_file(file_path):
    """
        Flips wave file on given path and saves it
    """
    file_path = os.path.sep.join(file_path.split('/'))
    reversed_file =  file_path + '_r.wav'
    if os.path.exists(reversed_file):
        return reversed_file

    with open(reversed_file, 'w') as fr:
        f = wave.open(file_path)
        frames = f.getnframes()
        data = f.readframes(frames)
        reversed = audioop.reverse(data, 2) # '2' is the sample width
        fr = wave.open(fr)
        # Must set params but leave # of frames empty
        fr.setparams((2, 2, 44100, '', 'NONE', 'not compressed'))
        fr.writeframesraw(reversed)
    return reversed_file


def _make_samples(slot):
    """
        Makes Sound instances tuple and sets Sound volumes
    """
    sample_file = os.path.join(SAMPLES_DIR, slot['sample'])
    samples = Sound(sample_file), Sound(reverse_wav_file(sample_file))
    for one in samples:
        one.set_volume(slot.get('volume', 100) / 100.0)
    return samples

def load_banks(bank_kit):
    """
        Loads bank kit definition from file and populates banks
        with Sound instances (both original wave & reversed one)
    """
    fname = os.path.join(BASE_DIR, 'banks', '%s.json' % bank_kit)

    try:
        banks = json.load(open(fname))

        iter_data = []
        for i, bank in enumerate(banks, 1):
            bank_data = {key: _make_samples(slot) for key, slot in bank.iteritems() if slot['sample']}
            iter_data.append((bank, bank_data, i))

        return itertools.cycle(iter_data)
    except IOError, e:
        return None
