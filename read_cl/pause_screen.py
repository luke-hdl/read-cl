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

        if len(self.reader.book.bookmarks) > 0:
            stdscr.addstr(8, 3, "s: save bookmarks file")
            stdscr.addstr(9, 3, "j: jump to bookmark")

        dimensions = self.reader.viewpoint.get_dimensions()
        draw_text_bar(dimensions[0], 30, dimensions[1] - 1, stdscr, self.reader.pointer, self.reader.book.words)

    def should_act(self, acting_at, input):
        return input in [ord('q'), ord('s'), ord('b'), ord('e'), ord('f'), ord('r'), ord('j')]

    def act(self, input):
        if input == ord('q'):
            self.reader.current_screen = reading_screen.ReadingScreen(self.reader)
            return
        if input == ord('s'):
            if len(self.reader.book.bookmarks) == 0:
                return
            save_bookmarks(self.reader.book)
        if input == ord('b'):
            self.reader.book.add_bookmarks([[self.reader.book.words[self.reader.pointer] + " (" + str(self.reader.pointer) + ")", self.reader.pointer]])
        if input == ord('e'):
            exit(0)
        if input == ord('f'):
            self.reader.current_screen = fast_forward_screen.FastForwardScreen(self.reader, 1)
        if input == ord('r'):
            self.reader.current_screen = fast_forward_screen.FastForwardScreen(self.reader, -1)
        if input == ord('j'):
            if len(self.reader.book.bookmarks) == 0:
                return
            self.reader.current_screen = jump_screen.JumpScreen(self.reader)