# Read-CL

A very simple implementation of single-word speedreading. I wasn't happy with existing Android options, and developing a command-line solution for use with UserLAnd was a practical, quick way for my simple use case. Ad-free and privacy-preserving - like you'd expect from a basic text file reader!

Limited pdf and epub support included. Other file formats will be added as I get annoyed about wanting to read them. Supports fast-forward, rewind, and bookmarking, including a regex auto-bookmark command feature. 

## Dependencies
```
pip install textract
```

## Usage

```
python3 read-cl.py path/to/your/file.txt wpm
```

where wpm is the words-per-minute you'd like to read at. 250 WPM is the average speed for regular reading, so that may be a good starting point.

For example:
```
python3 read-cl.py samples/lorem.txt 300
```

Press p to pause, which will let you set, jump to, delete, and save bookmarks, plus fast-forward and rewind.

You can automatically set bookmarks:
```
python3 read-cl.py samples/pride2.epub -bookmark 'Chapter|CHAPTER' '[A-Z]*\.'
```

Each regex given after the -bookmark and optional -append flag (which adds the bookmarks to your bookmark file instead of overwriting it) matches to a consecutive word that would flash across your screen. If a series of consecutive words matches them consecutively, a bookmark is created. It will be named exactly what was matched in the bookmarks jumper. 
