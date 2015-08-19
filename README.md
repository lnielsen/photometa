# photometa

Dirty script to parse filenames and fix creation date of photos.

Useful prior to importing images into e.g. Lightroom, if you have e.g. a bunch
of scanned images with the correct date in the filename, but not in the XMP
metadata.

## Usage

```console
$ brew install exempi
$ pip install click python-xmp-toolkit
$ python photometa.py
Usage: photometa.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  run  Run command.
```
