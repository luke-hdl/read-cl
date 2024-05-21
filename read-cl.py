from curses import wrapper, curs_set
from time import sleep
import textract
import sys

bookmarks = []
words = []
pointer = 0

args_count = len(sys.argv)
if args_count != 3: #Including the program name.
    print("Please include exactly two arguments: the file to read and the WPM.")
    quit(1)

sleep_time = 60/int(sys.argv[2])

if sys.argv[1].endswith(".epub"):
    words = textract.process(sys.argv[1], encoding='utf-8').decode().split(" ")

else:
    file_to_read = open(sys.argv[1], "r")
    words = file_to_read.read().split(" ")
    
def iterate_over_words(rows, cols, stdscr):
    global words
    global pointer
    global bookmarks
    while pointer < len(words):
        draw_next_word(rows, cols, stdscr)
        c = stdscr.getch()
        if c == ord('p'):
            while True:
                char = stdscr.getch()
                while char == -1:
                    char = stdscr.getch()
                if char == ord('q'):
                    break
                if char == ord('b'):
                    bookmarks.append(pointer)
                if char == ord('j'):
                    stdscr.clear()
                    stdscr.addstr(2, 2, "Jump to what bookmark? d for done: " + str(len(bookmarks)))
                    stdscr.refresh()
                    mark = ""
                    while True:
                        entry = stdscr.getch()
                        while entry == -1:
                            entry = stdscr.getch()
                        entry = "" + chr(entry)
                        if entry.isnumeric():
                            mark += entry
                        if entry == "d":
                            if int(mark) - 1 < len(bookmarks):
                                pointer = bookmarks[int(mark)-1]
                                break
                            else:
                                mark = ""
                                stdscr.clear()
                                stdscr.addstr(2, 2, "Invalid bookmark (c to cancel)")
                                stdscr.refresh()
                        if entry == "c":
                            break
                    break
        sleep(sleep_time)
    
def draw_next_word(rows, cols, stdscr):
    global words
    global pointer

    v = words[pointer]
    v = v.replace("\n","; ")
    v = v.replace("\r","; ")
    if len(v) > cols:
        v = v[:cols-4] + "..."
    stdscr.clear()
    stdscr.addstr(int(rows/2), int(cols/2-len(v)/2), v)
    stdscr.refresh()
    pointer += 1
    
def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    stdscr.nodelay(True)
    global words
    global pointer
    
    # Clear screen
    stdscr.clear()

    # Hide cursor
    curs_set(0)
    
    # Read sentences
    iterate_over_words(rows, cols, stdscr)

    while True:
        continue #Wait for input to generate an exception

wrapper(main)
