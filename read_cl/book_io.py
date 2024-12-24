import os
import textract
import hashlib
import re
from book import Book

def load_words(filepath):
    words = []
    if filepath.endswith(".epub") or filepath.endswith(".pdf"):
        contents = textract.process(filepath, encoding='utf-8').decode()
    else:
        file_to_read = open(filepath, "r")
        contents = file_to_read.read()
        file_to_read.close()

    save_file_name = ".saves/" + hashlib.md5(contents.encode()).hexdigest() + "_save.txt"
    contents = re.sub("[\s\n]", " ", contents)
    contents = re.sub("[ ]{1,100}", " ", contents)
    raw_words = contents.split(" ")

    for word in raw_words:
        if word != "":
            words.append(word)

    bookmarks = load_bookmarks(save_file_name)

    return Book(words, bookmarks, save_file_name)

def load_bookmarks(save_file_name):
    bookmarks = []
    if os.path.exists(save_file_name  + ".auto"):
        save = open(save_file_name  + ".auto", "r")
        for mark in save.read().split("\n"):
            if len(mark) > 0:
                raw = mark.split("\t")
                if len(raw) == 2:
                    bookmarks.append([raw[0], int(raw[1])])
        save.close()
    if os.path.exists(save_file_name):
        save = open(save_file_name, "r")
        for mark in save.read().split("\n"):
            if len(mark) > 0:
                raw = mark.split("\t")
                if len(raw) == 2:
                    bookmarks.append([raw[0], int(raw[1])])
        save.close()
    return bookmarks

def save_bookmarks(book):
    fl = open(book.save_file_name, "w")
    iter = 0
    if len(book.bookmarks) > 1 and book.bookmarks[0][0] == "Start" and book.bookmarks[1][0] == "Auto":
        iter = 2
    while iter < len(book.bookmarks):
        bookmark = book.bookmarks[iter]
        iter += 1
        fl.write(bookmark[0] + "\t" + str(bookmark[1]) + "\n")
    fl.close()

def save_autosave_bookmark(book, pointer):
    fl = open(book.save_file_name + ".auto", "w")
    fl.write("Start" + "\t" + str(0) + "\n")
    fl.write("Auto" + "\t" + str(pointer) + "\n")
    fl.close()

