#!/usr/bin/env python

import os
import datetime

now = datetime.datetime.now()

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
    elif extension in ['.mkv','.mp4','.avi','.flv']:
        return 'glyphicon glyphicon-film'
    elif extension in ['.srt']:
        return 'glyphicon glyphicon-subtitles'
    elif extension in ['.nfo']:
        return 'glyphicon glyphicon-tags'
    else:
        return 'glyphicon glyphicon-leaf'

def tracing(a):
    files = []
    dirs = []
    for item in os.listdir(a):
        if os.path.isfile(os.path.join(a, item)):
            files.append(item)
        else:
            dirs.append(item)
    for d in sorted(dirs):
        print "<li title=\"Size: " + human_size(get_size(os.path.join(a, d))) + "\">" + d + "\n<ul>"
        tracing(os.path.join(a, d))
        print "</ul></li>\n"
    for f in sorted(files):
        print "<li title=\"Size: " + human_size(os.path.getsize(os.path.join(a, f))) + "\" data-jstree='{\"icon\":\""+select_icon(f)+"\"}'>" + f + "</li>\n"


print """
<!DOCTYPE html>
<html>
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Filetree</title>
    <!-- Bootstrap -->
    <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">
    <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css\">
    <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css\">
    <!-- jsTree -->
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.4/themes/default/style.min.css\" >
    <style>
      .search:after {
        content: '';
        display: block;
        clear: both;
      }
    </style>
  </head>
  <body>
    <h1>Filetree</h1>
    <h4>Last Update: <span class="label label-info">
    """
print now.strftime("%Y-%m-%d %H:%M")
print """
    </span></h4>
    <div class="search">
      <div class="col-md-3">
        <input type="text" class="form-control" id="treesearch" placeholder="search">
      </div>
    </div>

    <div id=\"tree\">
      <ul>
    """
tracing('.')
print """
      </ul>
    </div>
    <!-- jQuery & Bootstrap -->
    <script src=\"https://code.jquery.com/jquery-1.12.4.min.js\"></script>
    <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script>
    <!-- jsTree -->
    <script src=\"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.4/jstree.min.js\"></script>
    <script>
      $(function () {
        $('#tree').jstree({
          "plugins" : [ "search" ]
        });
        var to = false;
        console.log('buhu');
        $('#tree').jstree(true).settings.search.show_only_matches = true;
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
"""
