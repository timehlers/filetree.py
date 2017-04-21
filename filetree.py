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
        print "<li title=\"Size: " + human_size(os.path.getsize(os.path.join(a, f))) + "\" data-jstree='{\"icon\":\"glyphicon glyphicon-leaf\"}'>" + f + "</li>\n"


print """
<!DOCTYPE html>
<html>
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Filetree</title>
    <!-- Bootstrap -->
    <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css\">
    <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css\">
    <!-- jsTree -->
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.1.1/themes/default/style.min.css\" >
    <style>
      .search:after {
        content: '';
        display: block;
        clear: both;
      }
    </style>
  </head>
  <body>
    <h1> Filetree </h1>
    <span class="label label-info">
    """
print now.strftime("%Y-%m-%d %H:%M")
print """
    </span><div class='clearfix'></div>
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
    <script src=\"https://code.jquery.com/jquery-1.11.3.min.js\"></script>
    <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js\"></script>
    <!-- jsTree -->
    <script src=\"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.1.1/jstree.min.js\"></script>
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
