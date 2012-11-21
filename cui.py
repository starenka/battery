import curses

class CUI(object):
    def __init__(self, version):
        screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        screen.keypad(1)
        self.LINES, self.COLS = screen.getmaxyx()
        self.screen = screen

        self.version = version

        self._init_cui()


    def _init_cui(self):
        self.screen.addstr(0, 0, 'Battery v%s - a simple rompler'.center(self.COLS) % self.version, curses.A_BOLD)
        for key, text in (('r', 'loop record/play'), ('p', 'delete last loop'),
            ('w', 'reverse mode'), ('q', 'exit'), ('SPACE', 'change bank')):
            self.screen.insstr(self.LINES - 1, 0, ' %s\t' % text)
            self.screen.insstr(self.LINES - 1, 0, key, curses.A_REVERSE)

    def show_bank(self, bank, bank_nr):
        self.screen.addstr(1, 0, 'Bank: #%s' % (str(bank_nr).zfill(2)), curses.A_REVERSE)
        for line, kv in enumerate(sorted(bank.iteritems()), 4):
            self.screen.insstr(line, 0, '%s%s' % (' ' * (7 - len(kv[0])), kv[1]['sample'][:-4].ljust(self.COLS - 1)))
            self.screen.insstr(line, 0, kv[0], curses.A_REVERSE)


    def tray_msg(self, msg, row=0, style=0):
        self.screen.addstr(self.LINES - 2 - row, 0, msg.ljust(self.COLS - 1), style)



