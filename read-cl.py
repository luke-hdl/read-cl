from curses import wrapper, curs_set
from time import sleep
import os
import textract
import sys
import hashlib
import re

bookmarks = []
words = []
pointer = 0
save_file_name = ""

args_count = len(sys.argv)

if (args_count < 5 or sys.argv[2] != '-bookmark') and (args_count != 3):
    print("To read, include exactly two arguments: the file to read and the WPM.")
    print("To auto-bookmark, begin with the filename, then -bookmark,, e.g. my_file.epub -bookmark CHAPTER|Chapter [A-Z]*\.")
    print("Optionally, after bookmark, you can include -append to append.")
    quit(1)

if not os.path.exists(".saves/"):
    os.mkdir(".saves/")
    
if sys.argv[2].isnumeric():
    sleep_time = 60/int(sys.argv[2])

def load_words():
    global bookmarks
    global words
    global save_file_name
    contents = ""
    if sys.argv[1].endswith(".epub"):
        contents = textract.process(sys.argv[1], encoding='utf-8').decode()

    else:
        file_to_read = open(sys.argv[1], "r")
        contents = file_to_read.read()
        file_to_read.close()

    save_file_name = ".saves/" + hashlib.md5(contents.encode()).hexdigest() + "_save.txt"
    contents = re.sub("[\s\n]", " ", contents)
    contents = re.sub("[ ]{1,100}", " ", contents)
    raw_words = contents.split(" ")
    
    for word in raw_words:
        if word != "":
            words.append(word)
                
    if os.path.exists(save_file_name):
        save = open(save_file_name, "r")
        for mark in save.read().split("\n"):
            if len(mark) > 0:
                raw = mark.split("\t")
                if len(raw) == 2:
                    bookmarks.append([raw[0], int(raw[1])])
        save.close()

def auto_bookmark(regexes):
    global bookmarks
    i = 0
    marks = []
    if len(regexes) == 0:
        return
    while i < len(words) - len(regexes):
        name = ""
        i2 = i
        match = True
        for regex in regexes:
            if re.search(regex, words[i2]) == None:
                match = False
                break
            name += words[i2] + " "
            i2 += 1
        if match == True:
            marks.append([name, i])
            i += len(regexes)
        else:
            i += 1
    bookmarks += marks
    
def iterate_over_words(rows, cols, stdscr):
    global words
    global pointer
    global bookmarks
    while True:
        draw_next_word(rows, cols, stdscr)
        c = stdscr.getch()
        if c == ord('p'):
            while True:
                stdscr.clear()
                stdscr.addstr(2, 2, "Reading paused.")
                stdscr.addstr(3, 3, "q: unpause")
                stdscr.addstr(4, 3, "b: set bookmark")
                stdscr.addstr(5, 3, "f: fast forward")
                stdscr.addstr(6, 3, "r: rewind")
                stdscr.addstr(7, 3, "e: exit")

                if len(bookmarks) > 0:
                    stdscr.addstr(8, 3, "s: save bookmarks file")
                    stdscr.addstr(9, 3, "j: jump to bookmark")
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
                        fl.write(bookmark[0] + "\t" + str(bookmark[1]) + "\n")
                    fl.close()
                if char == ord('f') or char == ord('r'):
                    direction = -1
                    if char == ord('f'):
                        direction = 1
                    speed = 5
                    while True:
                        pointer += direction
                        if pointer >= len(words):
                            pointer = len(words) - 1
                        if pointer < 0:
                            pointer = 0
                        sleep(60/10000*speed)
                        stdscr.erase()
                        draw_word_bar(rows, 30, cols - 1, stdscr)
                        stdscr.addstr(2, 2, "p: pause")
                        stdscr.addstr(3, 2, "c: cancel/exit")
                        stdscr.addstr(4, 2, "r: go backwards")
                        stdscr.addstr(5, 2, "f: go forwards")
                        stdscr.addstr(6, 2, "d: slower")
                        stdscr.addstr(7, 2, "g: faster")
                        stdscr.addstr(8, 2, "Your speed: " + str(10-speed) + "/10")
                        stdscr.refresh()
                        char = stdscr.getch()
                        if char == ord('p'):
                            direction = 0
                        elif char == ord('f'):
                            direction = 1
                        elif char == ord('r'):
                            direction = -1
                        elif char == ord('c'):
                            break
                        elif char == ord('d') and int(speed) < 10:
                            speed += 1
                        elif char == ord('g') and speed > 0:
                            speed -= 1
                if char == ord('b'):
                    bookmarks.append([words[pointer], pointer])
                if char == ord('e'):
                    quit(0)
                if char == ord('j'):
                    if len(bookmarks) == 0:
                        continue
                    stdscr.erase()
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
                                pointer = bookmarks[int(mark)-1][1]
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
        max_ptr = len(words) - 1
    num_cols = col_end - col_start + 1
    stdscr.addstr(center_row, col_start, crop("> " + words[pointer], num_cols))
    current_row = center_row - 1
    while current_row >= 0:
        bar_ptr -= 1
        if bar_ptr < min_ptr:
            break
        stdscr.addstr(current_row, col_start, crop(words[bar_ptr], num_cols))
        current_row -= 1
    current_row = center_row + 1
    bar_ptr = pointer
    while current_row < rows - 1:
        bar_ptr += 1
        if bar_ptr > max_ptr:
            break
        stdscr.addstr(current_row, col_start, crop(words[bar_ptr], num_cols))
        current_row += 1
        
def crop(word, allowed_length):
    if len(word) > allowed_length:
        return word[:allowed_length - 4] + "..."
    return word

def draw_next_word(rows, cols, stdscr):
    global words
    global pointer

    v = words[pointer]
    if len(v) > cols:
        v = crop(v, cols)
    stdscr.clear()
    stdscr.addstr(int(rows/2), int(cols/2-len(v)/2), v)
    stdscr.refresh()
    pointer += 1
    if pointer >= len(words):
        pointer = len(words) - 1
    
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

load_words()
if args_count > 4 and sys.argv[2] == "-bookmark":
    mode = "w"
    regexes = sys.argv[3:]
    if sys.argv[3] == "-append":
        mode = "a"
        regexes = regexes[1:]
    bookmarks = []
    auto_bookmark(regexes)
    print("Found " + str(len(bookmarks)) + " bookmarks.")
    if len(bookmarks) == 0:
        quit(0)
    fl = open(save_file_name, mode)
    for bookmark in bookmarks:
        fl.write(bookmark[0] + "\t" + str(bookmark[1]) + "\n")
    fl.close()
    quit(0)

wrapper(main)
