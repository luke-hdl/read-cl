import curses
from time import time

from pause_screen import PauseScreen
from reading_screen import ReadingScreen
from viewpoint import Viewpoint

class Reader:
    def __init__(self, book, target_seconds_between_words):
        self.last_acted_on = time()
        self.book = book
        self.pointer = -1
        self.current_screen = None
        self.target_seconds_between_words = target_seconds_between_words
        self.viewpoint = None
        self.override_mappings = {
            curses.KEY_EXIT: curses.KEY_EXIT,
            curses.KEY_ENTER: curses.KEY_ENTER,
            curses.KEY_BACKSPACE: curses.KEY_BACKSPACE
        }

    def add_override_mapping(self,map_from,map_to):
        self.override_mappings[map_from] = map_to

    def get_override_mapping(self,map_from):
        return self.override_mappings[map_from]

    def set_wpm(self, wpm):
        self.target_seconds_between_words = 60.0/float(wpm)

    def getch(self):
        return self.stdscr.getch()

    def start(self, stdscr):
        self.viewpoint = Viewpoint(stdscr)
        if len(self.book.words) > 0:
            self.current_screen = ReadingScreen(self)
        else:
            self.current_screen = PauseScreen(self)
            self.viewpoint.draw(self.current_screen) #Needed due to some oddities with PauseScreen's implementation.

    def iterate(self):
        c = self.viewpoint.getch()
        if self.current_screen.should_act(time(), c):
            self.current_screen.act(c)
            self.viewpoint.draw(self.current_screen)
            self.last_acted_on = time()

    def get_current_word(self):
        return self.book.words[self.pointer]

    def set_pointer(self, to_number):
        new_pointer = to_number
        if new_pointer < 0:
            new_pointer = 0

        if new_pointer >= len(self.book.words):
            new_pointer = len(self.book.words) - 1

        self.pointer = new_pointer

    def increment_pointer(self, by_number):
        self.set_pointer(self.pointer + by_number)



