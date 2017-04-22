#!/usr/bin/env python3

import os
import datetime
import shlex
import argparse

now = datetime.datetime.now()

parser = argparse.ArgumentParser(description='Recurse directory into jsTree HTML.')
parser.add_argument('-b', '--base', default='.',
                   help='directory that is the base for the tree')
parser.add_argument('-a', '--assets', default=None,
                   help='path to assets directory relative to html file for loading js and css locally')
parser.add_argument('-p', '--prefix', default='',
                   help='absolute path prefix to add in paths')
args = parser.parse_args()

def human_size(number):
    supportedunits = ['B', 'KB', 'MB', 'GB', 'TB']
    if number == 0: return '0 B'
    i = 0
    while number >= 1024 and i < len(supportedunits)-1:
        number /= 1024.
        i += 1
    dezimal = ('%.2f' % number).rstrip('0').rstrip('.')
    return '%s %s' % (dezimal, supportedunits[i])

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def select_icon(filename):
    extension = os.path.splitext(filename)[1].lower()
    if extension in ['.txt']:
        return 'fa fa-file-text-o'
    elif extension in ['.pdf']:
        return 'fa fa-file-pdf-o'
    elif extension in ['.zip','.tar','.gzip','.tgz']:
        return 'fa fa-file-archive-o'
    elif extension in ['.doc','.docx','.odt','.rtf']:
        return 'fa fa-file-word-o'
    elif extension in ['.xls','.xlsx','.ods','.gnumeric']:
        return 'fa fa-file-excel-o'
    elif extension in ['.ppt','.pptx','.odp']:
        return 'fa fa-file-powerpoint-o'
    elif extension in ['.jpg','.jpeg','.png','.tiff','.psd','.xcf']:
        return 'glyphicon glyphicon-picture'
    elif extension in ['.mp3','.ogg','.flac','m4a','.wav']:
        return 'glyphicon glyphicon-music'
    elif extension in ['.mkv','.mp4','.avi','.flv','.mpg','.m2ts','.iso','.ISO','.wmv']:
        return 'glyphicon glyphicon-film'
    elif extension in ['.srt']:
        return 'glyphicon glyphicon-subtitles'
    elif extension in ['.nfo']:
        return 'glyphicon glyphicon-tags'
    else:
        return 'glyphicon glyphicon-leaf'

def get_filepathlink(a,f):
    return shlex.quote(os.path.normpath(os.path.join(args.prefix, a, f)))

def tracing(a):
    files = []
    dirs = []
    for item in os.listdir(a):
        if os.path.isfile(os.path.join(a, item)):
            files.append(item)
        else:
            dirs.append(item)
    for d in sorted(dirs):
        print ("<li data-path=\"", get_filepathlink(a, d), "\" title=\"Size: ", human_size(get_size(os.path.join(a, d))), "\">", d, "\n<ul>",sep="")
        tracing(os.path.join(a, d))
        print ("</ul></li>\n")
    for f in sorted(files):
        print ("<li data-path=\"", get_filepathlink(a, f), "\" title=\"Size: ", human_size(os.path.getsize(os.path.join(a, f))), "\" data-jstree='{\"icon\":\"", select_icon(f), "\"}'>", f, "</li>\n",sep="")

def print_head():
    print ("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>Filetree</title>
        """)
    if args.assets != None:
        print ("<link rel=\"stylesheet\" href=\"",args.assets,"bootstrap.min.css\">",sep="")
        print ("<link rel=\"stylesheet\" href=\"",args.assets,"bootstrap-theme.min.css\">",sep="")
        print ("<link rel=\"stylesheet\" href=\"",args.assets,"font-awesome.min.css\">",sep="")
        print ("<link rel=\"stylesheet\" href=\"",args.assets,"style.min.css\" >",sep="")
    else:
        print ("""
            <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">
            <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css\">
            <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css\">
            <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.4/themes/default/style.min.css\" >
            """)
    print ("""
        <style>
        .formarea:after {
            content: '';
            display: block;
            clear: both;
        }
        .filetree-grey {
            color: grey;
        }
        </style>
    </head>
    <body>
        <h1>Filetree</h1>
        <h4>Last Update: <span class="label label-info">
        """)
    print (now.strftime("%Y-%m-%d %H:%M"))
    print ("""
        </span></h4>
        <div class="formarea">
        <div class="col-md-3">
            <input type="text" class="form-control" id="treesearch" placeholder="search">
        </div>
        <div class="col-md-3">
            <div class="input-group">
            <span class="input-group-addon" id="sizing-addon2">Path</span>
            <input type="text" class="form-control" id="selectedpath" placeholder="/" aria-describedby="sizing-addon2">
            </div>
        </div>
        </div>
        <div id=\"tree\">
        <ul>
        """)

def print_bottom():
    print ("""
        </ul>
        </div>
        """)
    if args.assets != None:
        print ("<script src=\"",args.assets,"jquery-1.12.4.min.js\"></script>",sep="")
        print ("<script src=\"",args.assets,"bootstrap.min.js\"></script>",sep="")
        print ("<script src=\"",args.assets,"jstree.min.js\"></script>",sep="")
    else:
        print ("""
            <script src=\"https://code.jquery.com/jquery-1.12.4.min.js\"></script>
            <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script>
            <script src=\"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.4/jstree.min.js\"></script>
            """)

    print ("""
        <script>
        $(function () {
          $('#tree').jstree({
            "plugins" : [ "search" ]
          });
          var to = false;
          $('#tree').jstree(true).settings.search.show_only_matches = true;
          $('#tree').on('changed.jstree', function (e, data) {
            if(data && data.selected && data.selected.length) {
              $('#selectedpath').val(data.node.data.path);
            }
          });
          $('#treesearch').keyup(function () {
            if(to) { clearTimeout(to); }
            to = setTimeout(function () {
              var v = $('#treesearch').val();
              $('#tree').jstree(true).search(v);
            }, 250);
          });
        });
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    # execute only if run as a script
    print_head()
    tracing(args.base)
    print_bottom()
