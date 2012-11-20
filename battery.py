#!/usr/bin/env python
import curses, argparse, sys

import pygame
from utils import load_banks

import cui


VERSION = 0.2
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


if __name__ == "__main__":
    # That's all what MaKeyMaKey has in stock setting, except 'SPC' and 'w'
    init_mixer()
    args = parse_args()

    banks_iter = load_banks(args.bank_kit)
    if not banks_iter:
        sys.exit('Can\'t load bank kit file "%s"' % args.bank_kit)

    bank_desc, bank_samples, bank_nr = banks_iter.next()

    cui = cui.CUI(VERSION)
    cui.show_bank(bank_desc, bank_nr)

    while True:
        event = cui.screen.getch()

        if event in (ord('q'), 27): #q or ESC
            break

        elif event == ord(' '): # switch bank
            bank_desc, bank_samples, bank_nr = banks_iter.next()
            cui.show_bank(bank_desc, bank_nr)
            continue

        try:
            key = KEYS[event]
            try:
                bank_samples[key].play()
            except KeyError:
                cui.tray_msg('No sample defined for "%s" key\n' % key, row=1, style=curses.A_DIM)
        except KeyError:
            pass

    # This should somehow restore terminal back, but it doesn't work all the time.
    # Call "reset" in your shell if you need to
    curses.endwin()
