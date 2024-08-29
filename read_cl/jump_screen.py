from screen_utils import draw_text_bar
import pause_screen
from sys import exit

class JumpScreen:
    def __init__(self, reader):
        self.reader = reader
        self.bookmark_pointer = 0
        self.bookmark_names = []
        for bookmark in reader.book.bookmarks:
            self.bookmark_names.append(bookmark[0])

    def draw(self, stdscr):
        dimensions = self.reader.viewpoint.get_dimensions()
        if len(self.bookmark_names) > 0:
            draw_text_bar(dimensions[0], 30, dimensions[1] - 1, stdscr, self.bookmark_pointer, self.bookmark_names)

        stdscr.addstr(2, 2, "Jumping bookmarks.")
        stdscr.addstr(3, 2, "u: scroll up")
        stdscr.addstr(4, 2, "d: scroll down")
        stdscr.addstr(5, 2, "c: cancel")
        stdscr.addstr(6, 2, "g: go jump")
        stdscr.addstr(7, 2, "l: delete bookmark")


    def should_act(self, acting_at, input):
        return input in [ord('u'), ord('d'), ord('c'), ord('g'), ord('l'), ord('e')]

    def act(self, input):
        if input == ord('u'):
            self.increment_pointer(-1)
        if input == ord('d'):
            self.increment_pointer(1)
        if input == ord('c'):
            self.reader.current_screen = pause_screen.PauseScreen(self.reader)
        if input == ord('g'):
            self.reader.pointer = self.reader.book.bookmarks[self.bookmark_pointer][1]
            self.reader.current_screen = pause_screen.PauseScreen(self.reader)
        if input == ord('l'):
            del self.reader.book.bookmarks[self.bookmark_pointer]
            del self.bookmark_names[self.bookmark_pointer]
            self.increment_pointer(0)
        if input == ord('e'):
            exit(0)

    def increment_pointer(self, by_number):
        new_pointer = self.bookmark_pointer + by_number
        if new_pointer < 0:
            new_pointer = 0

        if new_pointer >= len(self.bookmark_names):
            new_pointer = len(self.bookmark_names) - 1

        self.bookmark_pointer = new_pointer