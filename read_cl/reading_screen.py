from screen_utils import crop
import pause_screen

class ReadingScreen:
    def __init__(self, reader):
        self.reader = reader

    def draw(self, stdscr):
        word = self.reader.get_current_word()
        dimensions = self.reader.viewpoint.get_dimensions()
        if len(word) > dimensions[1]:
            word = crop(word, dimensions[1])
        stdscr.addstr(int(dimensions[0] / 2), int(dimensions[1] / 2 - len(word) / 2), word)

    def should_act(self, acting_at, input):
        return input in [ord('p')] or acting_at - self.reader.last_acted_on > self.reader.target_seconds_between_words

    def act(self, input):
        if input == ord('p'):
            self.reader.current_screen = pause_screen.PauseScreen(self.reader)
        else:
            self.reader.increment_pointer(1)