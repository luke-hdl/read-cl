import text_entry_screen
import book_io
from screen_utils import draw_text_bar
import reading_screen
import fast_forward_screen
import jump_screen
from book_io import save_bookmarks
from sys import exit

class PauseScreen:
    def __init__(self, reader):
        self.reader = reader

    def draw(self, stdscr):
        stdscr.addstr(2, 2, "Reading paused.")
        stdscr.addstr(3, 3, "q: unpause")
        stdscr.addstr(4, 3, "b: set bookmark")
        stdscr.addstr(5, 3, "f: fast forward")
        stdscr.addstr(6, 3, "r: rewind")
        stdscr.addstr(7, 3, "e: exit")
        stdscr.addstr(8, 3, "w: set wpm")
        stdscr.addstr(9, 3, "a: add autobookmarks")
        stdscr.addstr(10, 3, "o: open book")

        if len(self.reader.book.bookmarks) > 0:
            stdscr.addstr(11, 3, "s: save bookmarks file")
            stdscr.addstr(12, 3, "j: jump to bookmark")

        dimensions = self.reader.viewpoint.get_dimensions()
        if len(self.reader.book.words) > 0:
            draw_text_bar(dimensions[0], 30, dimensions[1] - 1, stdscr, self.reader.pointer, self.reader.book.words)
            if self.reader.target_seconds_between_words is None:
                stdscr.addstr(3, 6, "(You can't unpause, because your WPM isn't set!)")
        else:
            stdscr.addstr(3, 6, "(You can't unpause, because no book is loaded!)")
            stdscr.addstr(4, 6, "(Can't do this either!)")
            stdscr.addstr(5, 6, "(Can't do this either!)")
            stdscr.addstr(6, 6, "(Can't do this either!)")
            stdscr.addstr(9, 6, "(Can't do this either!)")

    def return_to_pause_screen(self):
        self.reader.current_screen = self

    def set_wpm_and_pause(self, wpm):
        self.reader.set_wpm(wpm)
        self.reader.current_screen = self

    def autobookmark_and_pause(self, regex):
        self.reader.book.auto_bookmark(regex.split(" "), False)
        self.reader.current_screen = self

    def load_book_and_pause(self, path):
        #try:
            new_book = book_io.load_words(path)
            self.reader.book = new_book
            self.reader.pointer = 0
            self.reader.current_screen = self
        #except Exception as e:
        #    self.reader.current_screen = text_entry_screen.TextEntryScreen(self.reader,"Couldn't find book. Try again:", self.load_book_and_pause, self.return_to_pause_screen)

    def should_act(self, acting_at, input):
        return input in [ord('q'), ord('s'), ord('b'), ord('e'), ord('f'), ord('r'), ord('j'), ord('w'), ord('a'), ord('o')]

    def act(self, input):
        if input == ord('q') and len(self.reader.book.words) > 0:
            self.reader.current_screen = reading_screen.ReadingScreen(self.reader)
            return
        if input == ord('s'):
            if len(self.reader.book.bookmarks) == 0:
                return
            save_bookmarks(self.reader.book)
        if input == ord('b') and len(self.reader.book.words) > 0:
            self.reader.book.add_bookmarks([[self.reader.book.words[self.reader.pointer] + " (" + str(self.reader.pointer) + ")", self.reader.pointer]])
        if input == ord('e'):
            exit(0)
        if input == ord('f') and len(self.reader.book.words) > 0:
            self.reader.current_screen = fast_forward_screen.FastForwardScreen(self.reader, 1)
        if input == ord('r') and len(self.reader.book.words) > 0:
            self.reader.current_screen = fast_forward_screen.FastForwardScreen(self.reader, -1)
        if input == ord('j') and len(self.reader.book.words) > 0:
            if len(self.reader.book.bookmarks) == 0:
                return
            self.reader.current_screen = jump_screen.JumpScreen(self.reader)
        if input == ord('w'):
            self.reader.current_screen = text_entry_screen.TextEntryScreen(self.reader,"Enter WPM:", self.set_wpm_and_pause, self.return_to_pause_screen)
        if input == ord('a') and len(self.reader.book.words) > 0:
            self.reader.current_screen = text_entry_screen.TextEntryScreen(self.reader,"Enter regexes for autobookmarking (each regex, space-seperated, matches to a consecutive word):", self.autobookmark_and_pause, self.return_to_pause_screen)
        if input == ord('o'):
            self.reader.current_screen = text_entry_screen.TextEntryScreen(self.reader,"Enter path to new book:", self.load_book_and_pause, self.return_to_pause_screen)
