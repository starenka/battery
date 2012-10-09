#!/usr/bin/env python
import curses
import pygame
from utils import load_banks

AVAILABLE_KEYS = 'LEFT RIGHT DOWN UP a s d f g h j'.split() #it's all MaKeyMaKey has, except SPC and w
KEYS = dict(
    [(key, getattr(curses, 'KEY_%s' % key, ord(key[0]))) for key in AVAILABLE_KEYS])

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.set_num_channels(4 * len(KEYS) + 1)

bank_kit = 'default'
banks, banks_iter = load_banks(bank_kit)
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