#Controls the direct relationship to the stdscr and manages clear/refreshes.

class Viewpoint:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def draw(self, screen):
        self.stdscr.erase()
        screen.draw(self.stdscr)
        self.stdscr.refresh()

    def get_dimensions(self):
        return self.stdscr.getmaxyx()

    def getch(self):
        return self.stdscr.getch()