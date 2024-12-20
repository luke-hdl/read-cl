import curses

class RemapScreen:
    def __init__(self, reader, pause_screen):
        self.reader = reader
        self.entry = ""
        self.pause_screen = pause_screen
        self.last_entered = None
        self.pointer = 0
        self.remapping_text = [
            [curses.KEY_EXIT, "Exit/Escape key"],
            [curses.KEY_ENTER, "Enter/Return key"],
            [curses.KEY_BACKSPACE, "Backspace key"]
        ]

    def draw(self, stdscr):
        dimensions = self.reader.viewpoint.get_dimensions()
        stdscr.addstr(int(dimensions[0] / 2) - 2, int(dimensions[1] / 2 - len("Press the following key:") / 2), "Press the following key:")
        stdscr.addstr(int(dimensions[0] / 2) - 1, int(dimensions[1] / 2 - len(self.remapping_text[self.pointer][1]) / 2), self.remapping_text[self.pointer][1])

    def should_act(self, acting_at, input):
        return input != -1

    def act(self, input):
        self.reader.add_override_mapping(self.remapping_text[self.pointer][0], input)
        self.pointer += 1
        if self.pointer >= len(self.remapping_text):
            self.reader.current_screen = self.pause_screen
