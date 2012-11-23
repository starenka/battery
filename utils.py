#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os, itertools, json, wave, audioop

import pygame
from pygame.mixer import Sound

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, 'samples')
BANKS_DIR = os.path.join(BASE_DIR, 'banks')

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
        rev = audioop.reverse(data, 2) # '2' is the sample width
        fr = wave.open(fr)
        # Must set params but leave # of frames empty
        fr.setparams((2, 2, 44100, '', 'NONE', 'not compressed'))
        fr.writeframesraw(rev)
    return reversed_file


def make_sample_tuples(slot, prepend=SAMPLES_DIR):
    """
        Makes Sound instances tuple and sets Sound volumes
    """
    sample_file = os.path.join(prepend, slot['sample'])
    try:
        samples = Sound(sample_file), Sound(reverse_wav_file(sample_file))
    except (wave.Error, audioop.error):
        return None

    for one in samples:
        one.set_volume(slot.get('volume', 100) / 100.0)
    return samples

def discover_samples(dir=SAMPLES_DIR):
    """
        Walks SAMPLES dir and gets all available samples
    """
    samples = []
    for path, dirs, files in os.walk(dir, followlinks=True):
        for one in filter(lambda x: not x.endswith('_r.wav') and x.endswith('.wav'), files):
            rel_path = os.path.join(path, one).replace(SAMPLES_DIR,'')[1:]
            samples.append(rel_path)
    return samples


def load_banks(bank_kit, bank_dir=BANKS_DIR):
    """
        Loads bank kit definition from file and populates banks
        with Sound instances (both original wave & reversed one)
    """
    fname = os.path.join(bank_dir, '%s.json' % bank_kit)

    try:
        banks = json.load(open(fname))
    except IOError:
        return None

    iter_data = []
    for i, bank in enumerate(banks, 1):
        bank_data = {}
        for key, slot in bank.iteritems():
            if slot['sample']:
                samples = make_sample_tuples(slot)
                if samples:
                    bank_data[key] = samples
        iter_data.append((bank, bank_data, i))

    return itertools.cycle(iter_data)

def init_mixer(channels):
    """
        Init's pygame's mixes & pygame itself
        We need to init mixer before pygame initializations, smaller buffer should avoid lags
    """
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.mixer.set_num_channels(channels)