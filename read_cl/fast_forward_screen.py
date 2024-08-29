from screen_utils import crop, draw_text_bar
import pause_screen
from book_io import save_bookmarks

class FastForwardScreen:
    def __init__(self, reader, direction):
        self.reader = reader
        self.direction = direction
        self.speed = 5

    def draw(self, stdscr):
        stdscr.addstr(2, 2, "p: pause")
        stdscr.addstr(3, 2, "c: cancel/exit")
        stdscr.addstr(4, 2, "r: go backwards")
        stdscr.addstr(5, 2, "f: go forwards")
        stdscr.addstr(6, 2, "d: slower")
        stdscr.addstr(7, 2, "g: faster")
        stdscr.addstr(8, 2, "Your speed: " + str(10 - self.speed) + "/10")

        dimensions = self.reader.viewpoint.get_dimensions()
        draw_text_bar(dimensions[0], 30, dimensions[1] - 1, stdscr, self.reader.pointer, self.reader.book.words)

    def should_act(self, acting_at, input):
        return acting_at - self.reader.last_acted_on > self.expected_wait_time() or input in [ord('p'), ord('f'), ord('r'), ord('c'), ord('d'), ord('g')]

    def act(self, input):
        if input == ord('p'):
            self.direction = 0
        elif input == ord('f'):
            self.direction = 1
        elif input == ord('r'):
            self.direction = -1
        elif input == ord('c'):
            self.reader.current_screen = pause_screen.PauseScreen(self.reader)
        elif input == ord('d') and int(self.speed) < 10:
            self.speed += 1
        elif input == ord('g') and self.speed > 0:
            self.speed -= 1
        else:
            self.reader.increment_pointer(self.direction)

    def expected_wait_time(self):
        return 60 / 10000 * self.speed