from curses import wrapper, curs_set
from time import sleep
import textract
import sys

bookmarks = []
args_count = len(sys.argv)
if args_count != 3: #Including the program name.
    print("Please include exactly two arguments: the file to read and the WPM.")
    quit(1)

sleep_time = 60/int(sys.argv[2])
line = ""
if sys.argv[1].endswith(".epub"):
    line = textract.process(sys.argv[1], encoding='utf-8').decode()

else:
    file_to_read = open(sys.argv[1], "r")
    line = file_to_read.read()
    
def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    global line
    
    # Clear screen
    stdscr.clear()

    # Hide cursor
    curs_set(0)
    
    # Read sentences
    words = line.split(" ")
    for i in range(0, len(words)):
        v = words[i]
        v = v.replace("\n","; ")
        v = v.replace("\r","; ")
        if len(v) > cols:
            v = v[:cols-4] + "..."
        stdscr.clear()
        stdscr.addstr(int(rows/2), int(cols/2-len(v)/2), v)
        stdscr.refresh()
        sleep(sleep_time)

wrapper(main)
quit(0)
