import curses

# That's all what MaKeyMaKey has in stock setting, except 'SPC' and 'w'
AVAILABLE_KEYS = 'LEFT RIGHT DOWN UP a s d f g h j'.split()


class CUI(object):
    BANNER = ''
    HELP_ITEMS = tuple()

    def __init__(self):
        screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        screen.keypad(1)
        self.LINES, self.COLS = screen.getmaxyx()
        self.screen = screen

        self._init_cui(self.BANNER, self.HELP_ITEMS)


    def _init_cui(self, banner, help_items):
        self.screen.addstr(0, 0, banner.center(self.COLS), curses.A_BOLD)
        for key, text in help_items:
            self.screen.insstr(self.LINES - 1, 0, ' %s\t' % text)
            self.screen.insstr(self.LINES - 1, 0, key, curses.A_REVERSE)

    def show_bank(self, bank, bank_nr):
        self.screen.addstr(1, 0, 'Bank: #%s' % (str(bank_nr).zfill(2)), curses.A_REVERSE)
        for line, kv in enumerate(sorted(bank.iteritems()), 4):
            self.screen.insstr(line, 0, '%s%s' % (' ' * (7 - len(kv[0])), kv[1]['sample'][:-4].ljust(self.COLS - 1)))
            self.screen.insstr(line, 0, kv[0], curses.A_REVERSE)


    def tray_msg(self, msg, row=0, style=0):
        self.screen.addstr(self.LINES - 2 - row, 0, msg.ljust(self.COLS - 1), style)


class BatteryCUI(CUI):
    VERSION = 0.3
    HELP_ITEMS = (('r', 'loop record/play'),
                  ('p', 'delete last loop'),
                  ('w', 'reverse mode'),
                  ('q', 'exit'),
                  ('SPACE', 'change bank')
        )
    BANNER = 'Battery v%s - a simple rompler' % VERSION


class BrowserCUI(CUI):
    VERSION = 0.1
    HELP_ITEMS = (('w', 'reverse mode'),
                  ('m', 'prev sample'),
                  ('n', 'next sample'),
                  ('p', 'play'),
                  ('q', 'exit'),
        )
    BANNER = 'Sample browser v%s' % VERSION