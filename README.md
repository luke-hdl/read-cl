# Read-CL

A very simple implementation of single-word speedreading. Supports Windows or Linux. I wasn't happy with existing Android options, and developing a command-line solution for use with UserLAnd was a practical, quick way to set something up for my simple use case. Ad-free and privacy-preserving - like you'd expect from a basic text file reader!

Limited pdf and epub support included. Other file formats will be added as I get annoyed about wanting to read them. Supports fast-forward, rewind, and bookmarking, including a regex auto-bookmark command feature. 

## Usage

The program can be run directly from the command line:
```commandline
read_cl.exe
```
or 
```commandline
python3 read_cl/main.py
```

then, follow the directions to enter a path and WPM, and optionally auto-bookmark.

You can also pass in arguments, as follows: 

Release candidate (via Windows Command Line or PowerShell): 
```
read_cl.exe ./samples/pride2.epub wpm
```

With Python: 
```
python3 read_cl/main.py path/to/your/file.txt wpm
```

where wpm is the words-per-minute you'd like to read at. 250 WPM is the average speed for regular reading, so that may be a good starting point.

For example:
```
python3 read_cl/main.py samples/pride2.epub 300
```

Press p to pause, which will let you set, jump to, delete, and save bookmarks, plus fast-forward and rewind.

You can automatically set bookmarks:
```
read_cl.exe ./samples/pride2.epub -bookmark 'Chapter|CHAPTER' '[A-Z]*/.'
```
or
```
python3 read_cl/main.py samples/pride2.epub -bookmark 'Chapter|CHAPTER' '[A-Z]*/.'
```

Each regex given after the -bookmark and optional -append flag (which adds the bookmarks to your bookmark file instead of overwriting it) matches to a consecutive word that would flash across your screen. If a series of consecutive words matches them consecutively, a bookmark is created. It will be named exactly what was matched in the bookmarks jumper. 


## Dependencies
read-cl depends on Textract. Unfortunately, the library is not maintained. It's not terrible to get it running, but the version available to pip will generally fail to install due to use of a no-longer-supported syntax. You can attempt
```
pip install textract
```

Failing that, 

https://github.com/deanmalmgren/textract/issues/525

has a workaround to set it up; follow the advice given, and remember to also 
```
pip install .
```
in textract's directory at the end. Alternatively, see Releases; these have the textract dependency bundled. 

## Releases
Releases are generated using 
```
pyinstaller read_cl/main.py --onefile --collect-submodules textract
```

For Windows, this is instead:
```
pyinstaller read_cl/main.py --onefile --collect-submodules textract --collect-submodules windows-curses
```

and include all dependencies. 

read_cl.exe, found in /release/, should run on Windows systems. As I'm using Windows Subsystem for Linux for Linux testing, there isn't a functioning release right now. I'll be posting one for Debian 64x systems at a later time, once I find my laptop charger. 
