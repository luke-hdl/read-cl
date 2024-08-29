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
    print("To read, include exactly two arguments: the file to read and the WPM. For instance: ")
    print("python3 read_cl.py my_file.epub 300")
    print("To auto-bookmark, begin with the filename, then -bookmark, then regexes for each consecutive word you want to match (these can't match on spaces). For instance, for a chapter book with numbered chapters:")
    print("python3 read_cl.py my_file.epub -bookmark 'CHAPTER|Chapter' '[0-9]*'")
    print("Optionally, after bookmark, you can include -append to append.")
    print("To pause and access bookmarks, fast-forward, etc., press p at any time while reading.")
    quit(1)

if not os.path.exists(".saves/"):
    os.mkdir(".saves/")

if sys.argv[2].isnumeric():
    sleep_time = 60/int(sys.argv[2])

def bookmark_order(mark):
    return mark[1]

def load_words():
    global bookmarks
    global words
    global save_file_name
    contents = ""
    if sys.argv[1].endswith(".epub") or sys.argv[1].endswith(".pdf"):
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

    bookmarks.sort(key=bookmark_order)

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
        c = stdscr.getch()
        if c == ord('p'):
            while True:

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
                        draw_text_bar(rows, 30, cols - 1, stdscr, pointer, words)
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
