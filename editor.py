#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, curses, itertools

from cui import BrowserCUI, AVAILABLE_KEYS
from utils import discover_samples, make_sample_tuples, init_mixer


init_mixer(8)
i, samples = 0, discover_samples()
reverse, curr = False, samples[i]
sample = make_sample_tuples(dict(sample=curr))

ui = BrowserCUI()
ui.tray_msg(curr, row=1)

while True:
    event = ui.screen.getch()
    if event in (ord('q'), 27): #q or ESC
        break
    elif event == ord('p'):
        if sample:
            sample[int(reverse)].play()
        else:
            ui.tray_msg('%s - FAILED' % curr, row=2)
        ui.tray_msg(curr, row=1)

    elif event in (ord('n'), ord('m')):
        if event == ord('n'):
            i += 1
        else:
            i -= 1

        curr = samples[i]
        sample = make_sample_tuples(dict(sample=curr))
        ui.tray_msg(curr, row=1)

    elif event == ord('w'):
        reverse = not reverse
        ui.tray_msg('reverse mode' if reverse else '', style=curses.A_BOLD)

curses.endwin()
sys.exit(0)
