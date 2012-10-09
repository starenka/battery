#!/usr/bin/env python
import curses, argparse

import pygame
from utils import load_banks

parser = argparse.ArgumentParser('Battery - a simple CLI & headless rompler')
parser.add_argument('-b', '--bank-kit', action='store', dest='bank_kit', default='default')
args = parser.parse_args()


AVAILABLE_KEYS = 'LEFT RIGHT DOWN UP a s d f g h j'.split() #it's all MaKeyMaKey has, except SPC and w
KEYS = dict(
    [(key, getattr(curses, 'KEY_%s' % key, ord(key[0]))) for key in AVAILABLE_KEYS])

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)

#we need to init mixer before pygame initializations, smaller buffer should avoid lags
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
#get 4 channels for each key
pygame.mixer.set_num_channels(4 * len(KEYS) + 1)

banks, banks_iter = load_banks(args.bank_kit)
curr_bank, bank_changes, reverse = banks_iter.next(), 0, False

def bank_flash():
    screen.addstr(0, 0, 'Bank: #%s' % (str(bank_changes % len(banks) + 1).zfill(2)), curses.A_REVERSE)


def tray_msg(msg, row=0):
    BOTTOM = 25 #unhordcode
    screen.addstr(BOTTOM - row, 0, msg)


bank_flash(), tray_msg('Use %s keys to play. "SPACE" to change bank, "w" to reverse, "ESC" or "q" to exit.' % ', '.join(
    map(lambda x: '"%s"' % x, AVAILABLE_KEYS)))

while True:
    event = screen.getch()
    if event in (ord('q'), 27): #q or ESC
        break
    elif event == ord(' '):
        curr_bank = banks_iter.next()
        bank_changes += 1
        bank_flash()
    elif event == ord('w'):
        reverse = not reverse
        tray_msg('reversed' if reverse else ' ' * 8, row=1)
    for key, code in KEYS.iteritems():
        if event == code:
            try:
                curr_bank[key][int(reverse)].play()
            except KeyError:
                tray_msg('No sample defined for "%s" key\n' % key, row=1)

curses.endwin()