import curses

class TextEntryScreen:
    def __init__(self, reader, enter_text, on_finish, on_cancel):
        self.reader = reader
        self.enter_text = enter_text
        self.entry = ""
        self.on_finish = on_finish
        self.on_cancel = on_cancel
        self.last_entered = None
        self.help_text = "Escape/Exit to exit. Enter/Return to finish."
        n = None

    def draw(self, stdscr):
        dimensions = self.reader.viewpoint.get_dimensions()
        stdscr.addstr(int(dimensions[0] / 2) - 1, int(dimensions[1] / 2 - len(self.enter_text) / 2), self.enter_text)
        stdscr.addstr(int(dimensions[0] / 2), int(dimensions[1] / 2 - len(self.entry) / 2), self.entry)
        stdscr.addstr(int(dimensions[0] / 2 + 1), int(dimensions[1] / 2 - len(self.help_text) / 2), self.help_text)

    def should_act(self, acting_at, input):
        return input != -1

    def act(self, input):
        if input == self.reader.get_override_mapping(curses.KEY_EXIT):
            self.on_cancel()
        elif input == self.reader.get_override_mapping(curses.KEY_ENTER):
            self.on_finish(self.entry)
        elif input == self.reader.get_override_mapping(curses.KEY_BACKSPACE):
            self.entry = self.entry[0:len(self.entry)-1]
        elif 0 <= input < 255:
            self.entry += chr(input)