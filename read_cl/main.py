import sys
from sys import exit
import os
import book_io
import reader
from curses import wrapper, curs_set

from book import Book


def process_arguments():
    args_count = len(sys.argv)

    if not os.path.exists(".saves/"):
        os.mkdir(".saves/")

    if args_count > 1:
        book = book_io.load_words(sys.argv[1])
    else:
        book = Book([],[],None)

    if args_count > 4 and sys.argv[2] == "-bookmark":
        replace_existing = False
        regexes = sys.argv[3:]
        if regexes[0] == "--replace":
            regexes = regexes[1:]
            replace_existing = True

        book.auto_bookmark(regexes, replace_existing)
        print("Your book now has " + str(len(book.bookmarks)) + " bookmarks. Enjoy!")
        if len(book.bookmarks) == 0:
            exit(0)
        book_io.save_bookmarks(book)
        exit(0)

    if args_count > 2:
        sleep_time = 0
        if sys.argv[2].isnumeric():
            target_wpm = int(sys.argv[2])
            if target_wpm > 0:
                sleep_time = 60 / target_wpm
    else:
        sleep_time = None

    return reader.Reader(book, sleep_time)


def main(stdscr):
    reader_main = process_arguments()
    rows, cols = stdscr.getmaxyx()
    if rows < 10 or cols < 40:
        print("Your screen is too small to use read_cl. Minimum size: 10x40.")
        exit(1)
    stdscr.nodelay(True)
    curs_set(0)
    reader_main.start(stdscr)
    while True:
        reader_main.iterate()

wrapper(main)