from curses import wrapper, curs_set
from time import sleep
import os
import textract
import sys
import hashlib

bookmarks = []
words = []
pointer = 0

args_count = len(sys.argv)
if args_count != 3: #Including the program name.
    print("Please include exactly two arguments: the file to read and the WPM.")
    quit(1)

if not os.path.exists(".saves/"):
    os.mkdir(".saves/")
    
sleep_time = 60/int(sys.argv[2])

#To-do: there's better ways to do this, but they would require some refactoring.
contents = ""
if sys.argv[1].endswith(".epub"):
    contents = textract.process(sys.argv[1], encoding='utf-8').decode()

else:
    file_to_read = open(sys.argv[1], "r")
    contents = file_to_read.read()
    file_to_read.close()

save_file_name = ".saves/" + hashlib.md5(contents.encode()).hexdigest() + "_save.txt"
words = contents.split(" ")

if os.path.exists(save_file_name):
    save = open(save_file_name, "r")
    for mark in save.read().split(" "):
        if len(mark) > 0:
            bookmarks.append(int(mark))
    save.close()

def iterate_over_words(rows, cols, stdscr):
    global words
    global pointer
    global bookmarks
    while pointer < len(words):
        draw_next_word(rows, cols, stdscr)
        c = stdscr.getch()
        if c == ord('p'):
            while True:
                stdscr.clear()
                stdscr.addstr(2, 2, "Reading paused.")
                stdscr.addstr(3, 3, "q: unpause")
                stdscr.addstr(4, 3, "b: set bookmark")
                stdscr.addstr(5, 3, "e: exit")

                if len(bookmarks) > 0:
                    stdscr.addstr(6, 3, "s: save bookmarks file")
                    stdscr.addstr(7, 3, "j: jump to bookmark")
                draw_word_bar(rows, 30, cols - 1, stdscr)
            
                char = stdscr.getch()
                while char == -1:
                    char = stdscr.getch()
                if char == ord('q'):
                    break
                if char == ord('s'):
                    if len(bookmarks) == 0:
                        continue
                    fl = open(save_file_name, "w")
                    for bookmark in bookmarks:
                        fl.write(str(bookmark) + " ")
                    fl.close()
                if char == ord('b'):
                    bookmarks.append(pointer)
                if char == ord('e'):
                    quit(0)
                if char == ord('j'):
                    if len(bookmarks) == 0:
                        continue
                    stdscr.clear()
                    stdscr.addstr(2, 2, "Jumping bookmarks.")
                    stdscr.addstr(3, 2, "Available bookmarks: 1 through " + str(len(bookmarks)))
                    stdscr.addstr(4, 2, "d: done")
                    stdscr.addstr(5, 2, "c: cancel")
                    stdscr.addstr(6, 2, "Your entry:")
                    stdscr.refresh()
                    mark = ""
                    while True:
                        stdscr.addstr(6, 14, mark)
                        entry = stdscr.getch()
                        while entry == -1:
                            entry = stdscr.getch()
                        entry = "" + chr(entry)
                        if entry.isnumeric() and len(mark) < 10:
                            mark += entry
                        if entry == "d":
                            if mark != "" and int(mark) - 1 < len(bookmarks):
                                pointer = bookmarks[int(mark)-1]
                                break
                            elif mark != "":
                                mark = ""
                                stdscr.addstr(6, 14, "           ")
                                stdscr.addstr(8, 2, "Invalid bookmark.")
                                stdscr.refresh()
                        if entry == "c":
                            break
        sleep(sleep_time)

def draw_word_bar(rows, col_start, col_end, stdscr):
    global pointer
    center_row = int(rows/2)
    bar_ptr = pointer
    min_ptr = pointer - center_row
    if min_ptr < 0:
        min_ptr = 0
    max_ptr = pointer + center_row
    if max_ptr >= len(words):
        max_ptr = len(words)
    num_cols = col_end - col_start + 1
    stdscr.addstr(center_row, col_start, crop("> " + clean_word(words[pointer]), num_cols))
    current_row = center_row - 1
    while current_row >= 0:
        bar_ptr -= 1
        if bar_ptr < min_ptr:
            break
        stdscr.addstr(current_row, col_start, crop(clean_word(words[bar_ptr]), num_cols))
        current_row -= 1
    current_row = center_row + 1
    bar_ptr = pointer
    while current_row < rows - 1:
        bar_ptr += 1
        if bar_ptr > max_ptr:
            break
        stdscr.addstr(current_row, col_start, crop(clean_word(words[bar_ptr]), num_cols))
        current_row += 1

def clean_word(word):
    word = word.replace("\n", " ")
    word = word.replace("\r", " ")
    word = word.strip()
    return word
        
def crop(word, allowed_length):
    if len(word) > allowed_length:
        return word[:allowed_length - 4] + "..."
    return word

def draw_next_word(rows, cols, stdscr):
    global words
    global pointer

    v = clean_word(words[pointer])
    if len(v) > cols:
        v = crop(v, cols)
    stdscr.clear()
    stdscr.addstr(int(rows/2), int(cols/2-len(v)/2), v)
    stdscr.refresh()
    pointer += 1
    
def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    if rows < 10 or cols < 40:
        print("Your screen is too small to use read-cl.")
        quit(1)
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
