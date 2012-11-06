#!/usr/bin/env python
import curses, argparse, sys

import pygame
from utils import load_banks

parser = argparse.ArgumentParser('Battery - a simple CLI & headless rompler')
parser.add_argument('-b', '--bank-kit', action='store', dest='bank_kit', default='default')
args = parser.parse_args()

VERSION = 0.2
# That's all what MaKeyMaKey has in stock setting, except 'SPC' and 'w'
AVAILABLE_KEYS = 'LEFT RIGHT DOWN UP a s d f g h j'.split()
KEYS = dict(
    [(key, getattr(curses, 'KEY_%s' % key, ord(key[0]))) for key in AVAILABLE_KEYS])

# We need to init mixer before pygame initializations, smaller buffer should avoid lags
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.set_num_channels(8 * len(KEYS)) # Get 8 channels for each key

banks, banks_iter = load_banks(args.bank_kit)
if not banks and not banks_iter:
    sys.exit('Can\'t load bank kit file "%s". Are you sure about this?' % args.bank_kit)
curr_bank, curr_bank_nr, reverse = banks_iter.next(), 1, False

# init curses
screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
LINES, COLS = screen.getmaxyx()

def bank_flash(curr_bank_nr):
    screen.addstr(1, 0, 'Bank: #%s' % (str(curr_bank_nr).zfill(2)), curses.A_REVERSE)
    for line, kv in enumerate(sorted(banks[curr_bank_nr - 1].iteritems()), 4):
        screen.insstr(line, 0, '%s%s' % (' ' * (7 - len(kv[0])), kv[1]['sample'][:-4].ljust(COLS - 1)))
        screen.insstr(line, 0, kv[0], curses.A_REVERSE)


def help_item(key, help, row=0):
    screen.insstr(LINES - 1 - row, 0, ' %s\t' % help)
    screen.insstr(LINES - 1 - row, 0, key, curses.A_REVERSE)


def tray_msg(msg, row=0, style=0):
    screen.addstr(LINES - 2 - row, 0, msg.ljust(COLS - 1), style)

for key, help in reversed((('SPACE', 'change bank'), ('w', 'reverse mode'), ('q', 'exit'))):
    help_item(key, help)

screen.addstr(0, 0, 'Battery v%s - a simple rompler'.center(COLS) % VERSION, curses.A_BOLD)
bank_flash(curr_bank_nr)

while True:
    event = screen.getch()
    if event in (ord('q'), 27): #q or ESC
        break
    elif event == ord(' '):
        curr_bank = banks_iter.next()
        curr_bank_nr += 1 if curr_bank_nr < len(banks) else -(len(banks) - 1)
        bank_flash(curr_bank_nr)
    elif event == ord('w'):
        reverse = not reverse
        tray_msg('reverse mode' if reverse else '', style=curses.A_BOLD)
    for key, code in KEYS.iteritems():
        if event == code:
            try:
                curr_bank[key][int(reverse)].play()
            except KeyError:
                tray_msg('No sample defined for "%s" key\n' % key, row=1, style=curses.A_DIM)

# This should somehow restore terminal back, but it doesn't work all the time.
# Call "reset" in your shell if you need to
curses.endwin()