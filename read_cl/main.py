import sys
import os
import book_io
import reader
from curses import wrapper, curs_set

def process_arguments():
    args_count = len(sys.argv)

    if (args_count < 5 or sys.argv[2] != '-bookmark') and (args_count != 3):
        print("To read, include exactly two arguments: the file to read and the WPM. For instance: ")
        print("python3 read_cl.py my_file.epub 300")
        print(
            "To auto-bookmark, begin with the filename, then -bookmark, then regexes for each consecutive word you want to match (these can't match on spaces). For instance, for a chapter book with numbered chapters:")
        print("python3 read_cl.py my_file.epub -bookmark 'CHAPTER|Chapter' '[0-9]*'")
        print("Optionally, after bookmark, you can include -append to append.")
        print("To pause and access bookmarks, fast-forward, etc., press p at any time while reading.")
        quit(1)

    if not os.path.exists(".saves/"):
        os.mkdir(".saves/")

    sleep_time = 0
    if sys.argv[2].isnumeric():
        target_wpm = int(sys.argv[2])
        if target_wpm > 0:
            sleep_time = 60 / target_wpm

    if sleep_time <= 0:
        print("To read, include exactly two arguments: the file to read and the WPM. For instance: ")
        print("python3 read_cl.py my_file.epub 300")
        print("Your words per minute needs to be a number, like 100, 200, or 300. It can't be negative or 0.")
        quit(1)

    book = book_io.load_words()
    if args_count > 4 and sys.argv[2] == "-bookmark":
        replace_existing = False
        regexes = sys.argv[3:]
        if regexes[0] == "--replace":
            regexes = regexes[1:]
            replace_existing = True

        book.auto_bookmark(regexes, replace_existing)
        print("Your book now has " + len(book.bookmarks) + " bookmarks. Enjoy!")
        if len(book.bookmarks) == 0:
            quit(0)
        book_io.save_bookmarks(book)
        quit(0)

    return reader.Reader(book, sleep_time)


def main(stdscr):
    reader_main = process_arguments()
    rows, cols = stdscr.getmaxyx()
    if rows < 10 or cols < 40:
        print("Your screen is too small to use read_cl. Minimum size: 10x40.")
        quit(1)
    stdscr.nodelay(True)
    curs_set(0)
    reader_main.start(stdscr)
    while True:
        reader_main.iterate()

wrapper(main)