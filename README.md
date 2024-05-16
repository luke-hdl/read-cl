# Read-CL

A very simple implementation of single-word speedreading. I wasn't happy with existing Android options, and developing a command-line solution for use with UserLAnd was a practical, quick way for my simple use case. Ad-free and privacy-preserving - like you'd expect from a basic text file reader!

## Usage

```
python3 read-cl.py path/to/your/file.txt wpm
```

where wpm is the words-per-minute you'd like to read at. 250 WPM is the average speed for regular reading, so that may be a good starting point.

For example:
```
python3 read-cl.py samples/lorem.txt 250
```

