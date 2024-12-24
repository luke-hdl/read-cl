import curses

none = {
    curses.KEY_EXIT: curses.KEY_EXIT,
    curses.KEY_BACKSPACE: curses.KEY_BACKSPACE,
    curses.KEY_ENTER: curses.KEY_ENTER
}

windows_x64 = {
    curses.KEY_EXIT: 27,
    curses.KEY_BACKSPACE: 8,
    curses.KEY_ENTER: 10
}