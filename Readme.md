# filetree.py

This Python script recursively parses the directory it is run from and outputs a single HTML file containing the directory tree with [jsTress](https://www.jstree.com/).

## Usage

The script can be called from the command line

```
usage: filetree.py [-h] [-b BASE] [-a ASSETS] [-p PREFIX]

Recurse directory into jsTree HTML.

optional arguments:
  -h, --help            show this help message and exit
  -b BASE, --base BASE  directory that is the base for the tree
  -a ASSETS, --assets ASSETS
                        path to assets directory relative to html file for
                        loading js and css locally
  -p PREFIX, --prefix PREFIX
                        prefix to add in paths
  -s, --sortfiles       create alphabetical sorting for files
```


