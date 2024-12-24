import re

class Book:
    special_bookmark_names = ["Start", "Auto"]
    def __init__(self, words, bookmarks, save_file_name):
        self.words = words
        self.save_file_name = save_file_name
        self.bookmarks = []
        self.load_bookmarks(bookmarks)

    def bookmark_order(self, mark):
        if mark[0] == "Start":
            return -2
        if mark[0] == "Auto":
            return -1
        return mark[1]

    def load_bookmarks(self, new_bookmarks):
        self.bookmarks = new_bookmarks
        self.bookmarks.sort(key=self.bookmark_order)

    def add_bookmarks(self, new_bookmarks):
        if new_bookmarks[0] in self.special_bookmark_names:
            new_bookmarks[0] = new_bookmarks[0] + "*"
        self.bookmarks += new_bookmarks;
        self.bookmarks.sort(key=self.bookmark_order)

    def auto_bookmark(self, regexes, replace_existing):
        i = 0
        marks = []
        if len(regexes) == 0:
            return
        while i < len(self.words) - len(regexes):
            name = ""
            i2 = i
            match = True
            for regex in regexes:
                if re.search(regex, self.words[i2]) is None:
                    match = False
                    break
                name += self.words[i2] + " "
                i2 += 1
            if match:
                marks.append([name, i])
                i += len(regexes)
            else:
                i += 1
        if replace_existing:
            self.load_bookmarks(marks)
        else:
            self.add_bookmarks(marks)

